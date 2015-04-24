

Tool Wrapper Scripts and Parameter Files
========================================

${toc}

In addition to a runtime environment, which has been defined by Docker, a tool needs some form of wrapper script and parameter file so that other people will know how to interface with it.  These configuration files should contain all the command line parameters and parallelization directives necessary to run the tool in a production environment. The wrapper is an XML file defined by the Galaxy Tool Syntax, and it will usually be accompanied by runner scripts that do small amount of run time preparation, like creating configuration files or running data preparation commands.

The example for the DPC code would be the:

Wrapper XML File:
https://github.com/Sage-Bionetworks/SMC-Het-Challenge


Each tool wrapper configuration includes
1. The tool name, id and version number
2. Environmental requirements, ie the name of the Docker container
3. Inputs file and parameters
4. Output files
5. A templated command line to be execute in the container for the given inputs and outputs

Optional Sections of the Tool Configuration include
1. Configuration file creation
2. Unit tests
3. Documentation and help


Tutorials
---------
A quick introduction to the [Galaxy Tool Wrapper](http://www.slideshare.net/pjacock/galaxy-tools)

A video introduction to [Galaxy Tool Integration](http://screencast.g2.bx.psu.edu/toolIntegration/). The introduction of this video doesn't apply to the Planemo SDK VM. Information related to tool development starts at around minute 4.

Tool Wrapper Stanzas
--------------------
Every wrapper has required stanzas needed to fully describe how to interface with the tool.

1. The Header: tool name, tool ID and tool version
2. Requirements: declaration of the software requirements needed to run the tool. In the case of the SMC-Het challenge, this must be a declaration of a Docker container
3. Command line: a template for the command line that will be filled out by a templating engine at run time to container the correct parameter values and file paths.
4. Input declaration: All of the input parameters and files that will be passed to the program
5. Output declaration: All of the files that will be output by the program


Example Wrapper
--------------
```
<tool id="dpc" name="VCF DPC" version="1.0.0">
  <description>VCF clustering</description>
  <requirements>
    <container type="docker">r-base</container>
  </requirements>
  <command interpreter="Rscript">
dpc.R ${input_vcf}
  </command>

  <inputs>
    <param format="vcf" name="input_vcf" type="data" label="VCF file" help="" />
  </inputs>

  <outputs>
    <data format="png" name="output_png" label="DirichletProcessplotBinomial PNG" from_work_dir="DirichletProcessplotBinomial.png"/>
    <data format="txt" name="output_density" label="DirichletProcessplotBinomial Density" from_work_dir="DirichletProcessplotBinomialdensity.txt"/>
    <data format="txt" name="output_polygon" label="DirichletProcessplotBinomial Polygon" from_work_dir="DirichletProcessplotBinomialpolygonData.txt"/>
  </outputs>

  <help>
You should totally explain how to use your tool here
  </help>

</tool>
```

In this wrapper the tool identification is on the line
```
<tool id="dpc" name="VCF DPC" version="1.0.0">
```

The requirements found in the section
```
  <requirements>
    <container type="docker">r-base</container>
  </requirements>
```

There is a single VCF input file to this tool
```
  <inputs>
    <param format="vcf" name="input_vcf" type="data" label="VCF file" help="" />
  </inputs>
```

There are three output files
```
  <outputs>
    <data format="png" name="output_png" label="DirichletProcessplotBinomial PNG" from_work_dir="DirichletProcessplotBinomial.png"/>
    <data format="txt" name="output_density" label="DirichletProcessplotBinomial Density" from_work_dir="DirichletProcessplotBinomialdensity.txt"/>
    <data format="txt" name="output_polygon" label="DirichletProcessplotBinomial Polygon" from_work_dir="DirichletProcessplotBinomialpolygonData.txt"/>
  </outputs>
```


Declaring Input Parameters
--------------------

Lets take a few of the parameters from the help command and build Galaxy `param` blocks to stick in the tool's `inputs` block.

```
-V        shift quality by '(-Q) - 33'
```

In the previous section we saw `param` block of type `data` for input files, but there are many different kinds of parameters one can use. Flag parameters such as the above `-V` parameter are frequently represented by `boolean` parameters in Galaxy tool XML.
```
<param name="shift_quality" type="boolean" label="Shift quality"
truevalue="-V" falsevalue=""
help="shift quality by '(-Q) - 33' (-V)" />
```
We can then stick `$shift_quality` in our `command` block and if the user has selected this option it will be expanded as `-V` (since we have defined this as the `truevalue`). If the user hasn't selected this option `$shift_quality` will just expand as an empty string and not affect the generated command line.

Now consider the following `seqtk seq` parameters:

  ```
  -q INT    mask bases with quality lower than INT [0]
  -X INT    mask bases with quality higher than INT [255]
  ```

These can be translated into Galaxy parameters as:
  ```
  <param name="quality_min" type="integer" label="Mask bases with quality lower than"
  value="0" min="0" max="255" help="(-q)" />
  <param name="quality_max" type="integer" label="Mask bases with quality higher than"
  value="255" min="0" max="255" help="(-X)" />
  ```
These can be add to the command tag as
  ```
  -q $quality_min -X $quality_max.
  ```

Conditional Parameters
----------------------
The previous parameters were simple because they always appeared, now consider.
```
  -M FILE   mask regions in BED or name list FILE [null]
```

We can mark this `data` type `param` as optional by adding the attribute `optional="true"`.
```
  <param name="mask_regions" type="data" label="Mask regions in BED"
  format="bed" help="(-M)" optional="true" />
```
Then instead of just using `$mask_regions` directly in the `command` block, one can wrap it in an `if` [statement](http://www.cheetahtemplate.org/docs/users_guide_html/users_guide.html#SECTION0001040000000000000000).

```
  #if $mask_regions
  -M $mask_regions
  #end if
```

Next consider the parameters:
```
  -s INT    random seed (effective with -f) [11]
  -f FLOAT  sample FLOAT fraction of sequences [1]
```

In this case, the `-s` random seed parameter should only be seen or used if the sample parameter is set. We can express this using a `conditional` block.
```
  <conditional>
    <param name="sample" type="boolean" label="Sample fraction of sequences" />
    <when value="true">
      <param name="fraction" label="Fraction" type="float" value="1.0" help="(-f)" />
      <param name="seed" label="Random seed" type="integer" value="11" help="(-s)" />
    </when>
    <when value="false">
    </when>
  </conditional>
```

In our command block, we can again use an `if` statement to include these parameters.

```
  #if $sample
  -f $sample.faction -s $sample.seed
  #end if
```

Notice we must reference the parameters using the `sample.` prefix since they are defined within the `sample` conditional block.

For tools like this where there are many options but in most uses the defaults are preferred - a common idiom is to break the parameters into simple and advanced sections using a `conditional`.


Writing Command line templates
------------------------------
For the command line, the templating language is Cheetah. The return characters are removed and blank file paths set to empty strings. There should be one command line to run the entire analysis. Variable inputs should be demarcated in the style:
```
${variable_name}
```

You can find documentation at:

http://www.cheetahtemplate.org/
http://www.devshed.com/c/a/Python/Templating-with-Cheetah/
http://www.onlamp.com/pub/a/python/2005/01/13/cheetah.html

A wrapper can provide a simple set of command lines to be executed. Or it can provide a more complex wrapper for which there is both a defined command line as well as a runner script which does additional task such file and config setup as well as simple SMP parallelization (as allowed by the GALAXY_SLOTS environment variable).  In the case of the MuTect wrapper, the runner script 'chunks' the genome into intervals to be run under MuTect independently and concatenates the result VCF files at the end of the run.


Work environment
----------------
The command line will be executed in a temporary working directory where you can write temporary files and it will be cleaned out at the end of run. The input and output paths will be set to locations in different directories.

An important thing to note about Galaxy's parallelization control is the setting/checking of the GALAXY_SLOTS environmental variable in the script above at the line:
```
-nct \${GALAXY_SLOTS:-4}
```
in the Simple Wrapper section.  This allows the number of threads used by the program to be configured by the system, with a default of 4 if it is not defined. Note that the '\$', as the dollar sign character is passed on as a literal to the script (and not evaluated by the template system), this is because
```
$GALAXY_SLOTS
```
is actually an environmental variable defined at runtime, and not a variable that is filled in by the templating engine. For more notes on parallel process settings see http://galacticengineer.blogspot.co.uk/2015/04/using-galaxyslots-for-multithreaded_22.html

Catching Errors
---------------
See https://wiki.galaxyproject.org/Admin/Tools/ToolConfigSyntax#A.3Cstdio.3E.2C_.3Cregex.3E.2C_and_.3Cexit_code.3E_tag_sets for details on how to configure the error state checking. The standard method is to look for error exit code. Note, if you are using a BASH script, use the 'set -e' so that any command error will result in the script failing. You can set up a regex to search stderr for failure messages, but this method should not be used by itself, as it may not catch all errors.
