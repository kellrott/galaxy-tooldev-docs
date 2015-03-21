
Developing a Docker Container
=============================

To run a collaborator's tool (e.g. variant caller) on a compute cluster, there needs to be a "Dockerfile" which describes all dependencies and environmental setup required to run the tool.  This includes any and all software packages, symlinks, and environmental variables that are needed by the tool itself or needed by its dependencies.  

Dockerfiles use a 'fork and commit' strategy similar to github. You can start from a predefined system, and make small alterations on top of it. Available images can be found at https://registry.hub.docker.com/.

The Mutect Build starts with the 'java' image, which contains java pre-installed.

```
FROM java

RUN apt-get update
RUN apt-get install -y zip wget
#
# Install samtools and the python vcf libraries for wrapper code
#
RUN apt-get install -y samtools python-pip
RUN pip install PyVCF

# We'll be working in /opt from now on
WORKDIR /opt

#
# Download and unpack Mutect
#
RUN wget https://github.com/broadinstitute/mutect/releases/download/1.1.5/muTect-1.1.5-bin.zip
RUN wget https://github.com/broadinstitute/picard/releases/download/1.122/picard-tools-1.122.zip

RUN unzip muTect-1.1.5-bin.zip
RUN unzip picard-tools-1.122.zip

# Link the picard tools to /opt/picard
RUN ln -s picard-tools-1.122 picard
```
From there, the system issues 'apt-get' commands (the Debian package management system) to install zip, wget, samtools and pip. Pip is then used to install PyVCF. Zip files for MuTect and Picard are downloaded and unzipped (in /opt, which was defined as the 'WORKDIR').

Once a docker file is built it should be tested on the collaborator's local host system using a pre-installed Docker service before submission to the target host system.  The following links should help in understanding how to install/configure the docker service, create a docker container, and run it on the docker instance.

Docker's own basic interactive tutorial:
https://www.docker.com/tryit/

A written step-by-step guide to creating docker files and running them is here:
https://www.digitalocean.com/community/tutorials/docker-explained-using-dockerfiles-to-automate-building-of-images

The Dockerfile reference manual
https://docs.docker.com/reference/builder/

A simple example of docker files produced for UCSC projects is the Broad MuTect variant caller tool:
https://github.com/ucscCancer/pcawg_tools/blob/master/tools/mutect/Dockerfile


Using Planemo to Develop Docker Containers
==========================================

${PLANEMO_DOCKER}
