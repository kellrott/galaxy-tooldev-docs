

Tool Wrapper Scripts and Parameter Files
========================================


In addition to a runtime environment, which has been defined by Docker, a tool needs some form of wrapper script and parameter file so that other people will know how to interface with it.  These configuration files should contain all the command line parameters and parallelization directives necessary to run the tool in a production environment. The wrapper is an XML file defined by the Galaxy Tool Syntax, and it will usually be accompanied by runner scripts that do small amount of run time preperation, like creating configuration files or running data preparation commands.

The example for the DPC code would be the::

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
is actually an environmental variable defined at runtime, and not a variable that is filled in by the templating engine.

Catching Errors
---------------
See https://wiki.galaxyproject.org/Admin/Tools/ToolConfigSyntax#A.3Cstdio.3E.2C_.3Cregex.3E.2C_and_.3Cexit_code.3E_tag_sets for details on how to configure the error state checking. The standard method is to look for error exit code. Note, if you are using a BASH script, use the 'set -e' so that any command error will result in the script failing. You can set up a regex to search stderr for failure messages, but this method should not be used by itself, as it may not catch all errors.

Testing and debugging
Tools for project creation, building and wrapper format checking can be found at https://planemo.readthedocs.org
VMs for debugging and interactive development will be provided in Q1 2015.
