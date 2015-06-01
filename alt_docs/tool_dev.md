

Simple Wrapper
--------------
Create a shell script with your variables in it and execute that shell script. The pattern to note is how the 'configfiles' stanza is used to create a shell script, which is executed with no arguments using the 'command' stanza.

The GATK's BQSR program exemplifies this type of wrapper:
https://github.com/ucscCancer/pcawg_tools/blob/master/tools/gatk_bqsr/gatk_bqsr.xml

What follows is an annotated version of the GATK BQSR wrapper XML file:

Basic tool information first:
```
<tool id="gatk_bqsr" name="GATK BQSR" version="1.0.0">
```
Then a simple description of the tool:
```
<description>base quality score recalibration</description>
```
One docker container image file needs to be specified; put all dependencies + environmental setup in it:
```
<requirements>
<container type="docker">gatk</container>
</requirements>
```

Images can be provided in one of two ways:
Use an image that has been uploaded to the Docker Registry https://registry.hub.docker.com/

For Example, the stanza
```
<requirements>
<container type="docker">sjackman/bwa</container>
</requirements>
```
Would download the container image avalible from https://registry.hub.docker.com/u/sjackman/bwa/ and use it to run the tool.


Provide a 'Dockerfile' in the same directory as the tool wrapper.  This file will be built and the created image will be stored using the tag name provided in the requirements stanza.


Next is the directive to run the wrapper shell script:
```
<command interpreter="bash">$runscript</command>
```
Next, define the necessary inputs:
```
<inputs>
<param format="bam"   type="data" name="input_bam"      label="Input BAM" help="" />
<param format="vcf"   type="data" name="known_sites"    label="Known SNP sites VCF" />
<param format="fasta" type="data" name="reference"      label="Reference Genome" />
</inputs>
```

Then define the necessary outputs. Note the optional `from_work_dir` parameter, which defines the output filename. This allows the tool author to hard code an output file name, like 'output.vcf' in their command line. The alternate method is to use the 'name' of the output data parameter in the script, ie
```
-o ${output_report}
```
rather than
```
-o recal_data.table
```

The with this feature, the output stanza becomes:
```
<outputs>
<data format="txt" name="output_report" label="BQSR Report" from_work_dir="recal_data.table"/>
<data format="bam" name="output_bam" label="BQSR BAM" from_work_dir="output.bam"/>
</outputs>
```

Then the actual shell script which runs the command (this leverages the "configfile" directive though technically not a configuration file):

```
<configfiles>
<configfile name="runscript">#!/bin/bash
ln -s ${input_bam} input.bam
ln -s ${input_bam.metadata.bam_index} input.bam.bai
ln -s ${reference} reference.fasta
ln -s ${known_sites} known_sites.vcf

samtools faidx reference.fasta
java -jar /opt/picard/CreateSequenceDictionary.jar R=reference.fasta O=reference.dict

java -jar /opt/GenomeAnalysisTK.jar \
-T BaseRecalibrator \
-R reference.fasta \
-I input.bam \
-knownSites known_sites.vcf \
-nct \${GALAXY_SLOTS:-4}
-o recal_data.table

java -jar /opt/GenomeAnalysisTK.jar \
-T PrintReads \
-R reference.fasta \
--emit_original_quals \
-I input.bam \
-BQSR recal_data.table \
-o output.bam
</configfile>
</configfiles>
```
Finally describe the error handling:
```
<stdio>
<exit_code range="1:" level="fatal" />
<regex match="ERROR"
source="both"
level="fatal"
description="Error running BQSR" />
</stdio>
```
You can include help text as a form of documentation about how to use the program
```
<help>
You can put notes on how to run your program here.
</help>
```



Wrapper with a Runner Script
----------------------------

This creates a command line which is then passed into a runner script which is also part of the deliverable package.

Broad's MuTect variation caller demonstrates this type of wrapper with the runner script.

An example of the wrapper XML for MuTect:
https://github.com/ucscCancer/pcawg_tools/blob/master/tools/mutect/muTect.xml

The runner script is here:
https://github.com/ucscCancer/pcawg_tools/blob/master/tools/mutect/muTect.py

Galaxy Parameters Types
https://wiki.galaxyproject.org/Admin/Tools/ToolConfigSyntax#type_Attribute_Values_and_Dependent_Attributes
Galaxy Data Types
https://wiki.galaxyproject.org/Learn/Datatypes
Note on Bam files
Currently BAM file indices are not stored in the expected manner, ie the file_name + ".bai" (work is being done to fix this issue)
The easiest way to fix this issue it to symlink files into the working directory with the correct names. As seen in https://github.com/ucscCancer/pcawg_tools/blob/master/tools/gatk_bqsr/gatk_bqsr.xml

For an input `input_bam`
Run the commands
```
ln -s ${input_bam} input.bam
ln -s ${input_bam.metadata.bam_index} input.bam.bai
```
And then pass in input.bam as an input to the program.




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





A wrapper can provide a simple set of command lines to be executed. Or it can provide a more complex wrapper for which there is both a defined command line as well as a runner script which does additional task such file and config setup as well as simple SMP parallelization (as allowed by the GALAXY_SLOTS environment variable).  In the case of the MuTect wrapper, the runner script 'chunks' the genome into intervals to be run under MuTect independently and concatenates the result VCF files at the end of the run.
