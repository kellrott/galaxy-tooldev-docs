
Developing a Docker Container
=============================

`docker_build` command
======================

This section is auto-generated from the help text for the planemo
command `docker_build`. This help message can be generated with
`planemo docker_build --help`.

**Usage**:

    planemo docker_build [OPTIONS] TOOL_PATH

**Help**

Builds (and optionally caches Docker images) for tool Dockerfiles.

Loads the tool or tools referenced by `TOOL_PATH` (by default all tools
in current directory), and ensures they all reference the same Docker
image and then attempts to find a Dockerfile for these tools (can be
explicitly specified with `--dockerfile` but by default it will check
the tool's directory and the current directory as well).

This command will then build and tag the image so it is ready to be
tested and published. The docker\_shell command be used to test out the
built image.:

    % planemo docker_build bowtie2.xml # asssumes Dockerfile in same dir
    % planemo docker_shell --from_tag bowtie2.xml

**Options**:

    --dockerfile TEXT
    --docker_image_cache TEXT
    --docker_cmd TEXT          Command used to launch docker (defaults to
                               docker).
    --docker_sudo              Flag to use sudo when running docker.
    --docker_sudo_cmd TEXT     sudo command to use when --docker_sudo is enabled
                               (defaults to sudo).
    --docker_host TEXT         Docker host to target when executing docker
                               commands (defaults to localhost).
    --help                     Show this message and exit.




Producing Tool Containers with Docker
=====================================

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
