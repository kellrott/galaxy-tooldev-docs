Tool Wrapper Scripts and Parameter Files
========================================
${toc}

In addition to a runtime environment, which has been defined by Docker, a tool needs some form of wrapper script and parameter file so that other people will know how to interface with it.  These configuration files should contain all the command line parameters and parallelization directives necessary to run the tool in a production environment. The wrapper is an XML file defined by the Galaxy Tool Syntax, and it will usually be accompanied by runner scripts that do small amount of run time preparation, like creating configuration files or running data preparation commands.

Each tool wrapper configuration includes
1. The tool name, id and version number
2. Environmental requirements, ie the name of the Docker container
3. Input files and parameters
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
5. Output declaration: All of the files that will be outputted by the program

Example Wrapper
--------------
You can find two example tool wrappers that are part of the [SMC-Het-Challenge package](https://github.com/Sage-Bionetworks/SMC-Het-Challenge).
The first, the [DPC example](https://github.com/Sage-Bionetworks/SMC-Het-Challenge/blob/master/dpc/dpc.xml), is a simple tool wrapper that is a simple wrapper that defines the input and outputs and how to call the dpc.R script.
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
