
Developing a Docker Container
=============================
${image?fileName=docker_logo.png}
To run an analysis tool in a cloud compute environment, all of the dependencies and environmental configurations that are need for running the code need to be packaged so that they can be transported. For this reason we use [Docker](https://www.docker.com/) to describe the tool environment.

Introduction To Docker
----------------------
${youtube?videoId=YiZkHUbE6N0}


Building a Dockerfile
---------------------
${youtube?videoId=gG_x28rDxus}

${youtube?videoId=L6bjTlVdc6U}

There is an [interactive tutorial](https://www.docker.com/tryit/) to learn how to work with the Docker command line. There is a large collection of pre-defined Docker environments that can be found at the [Docker Registry](https://registry.hub.docker.com/). These include full installations of [R](https://registry.hub.docker.com/_/r-base/) and [Python's SciKit-Learn](https://registry.hub.docker.com/u/buildo/docker-python2.7-scikit-learn/). If what you need is missing, you can also join and add your own projects to the registry.

If the environment you need is not available on the registry you can provide a build description as part of your Galaxy tool. For this to work there needs to be a "Dockerfile" which describes all dependencies and environmental setup required to run the tool.  This includes any and all software packages, symlinks, and environmental variables that are needed by the tool itself or needed by its dependencies.  

Dockerfiles use a 'fork and commit' strategy similar to github. You can start from a predefined system, and make small alterations on top of it. Any of the images found at the [Registry](https://registry.hub.docker.com/) and be can used as a basis of builds.

A written step-by-step guide to creating docker files and running them is here:
https://www.digitalocean.com/community/tutorials/docker-explained-using-dockerfiles-to-automate-building-of-images

The Dockerfile reference manual
https://docs.docker.com/reference/builder/


The PhyloWGS Build starts with the 'ubuntu' image.

```
FROM ubuntu

RUN apt-get update && apt-get install -y gfortran build-essential make gcc build-essential python python-dev wget libgsl0ldbl gsl-bin libgsl0-dev python-pip git

# blas
ADD blas.sh /tmp/blas.sh
RUN chmod 755 /tmp/blas.sh
RUN /tmp/blas.sh
ENV BLAS /usr/local/lib/libfblas.a

# lapack
ADD lapack.sh /tmp/lapack.sh
RUN chmod 755 /tmp/lapack.sh
RUN /tmp/lapack.sh
ENV LAPACK /usr/local/lib/liblapack.a

RUN pip install numpy scipy
RUN easy_install -U ete2

WORKDIR /opt

RUN git clone https://github.com/morrislab/phylowgs.git

RUN cd phylowgs && g++ -o mh.o  mh.cpp  util.cpp `gsl-config --cflags --libs`
```

The first part of the docker file uses 'apt-get' commands (the Debian package management system) to install zip, wget, samtools and pip. Pip is then used to install numpy and scipy. Finally the source code for the tool is 'git cloned' and build (in /opt, which was defined as the 'WORKDIR').
