

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
