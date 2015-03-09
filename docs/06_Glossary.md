
Container
---------
An encapsulated runtime environment that contains all of the dependencies needed to run a particular piece of software. Unlike a traditional VM, it shares the kernel and filesystem of the parent OS. Special APIs in the linux kernel keep the container sandboxed in its own environment.

Docker
------
made up of both a service which runs on the host system and a set of instructions which are used to build a docker container image and then run it. Docker provides a simple interface to complex container environment APIs that have been added into the Linux Kernel.

Docker container build file (Dockerfile)
----------------------------------------
a text file which contains the set of instructions which define all the dependencies (including OS) and environmental settings a piece of software needs to run.  Containers can also include commands to execute either during the build ("RUN" instructions) or during the execution of the software ("CMD" instructions).

Docker Image
------------
The compiled result of a 'Dockerfile'. This is the actual file system of the container as an archive. When a container is initialized, a copy of the image is used as start point.

Host system
-----------
is the actual underlying machine and OS used to run a Docker container.  Host systems can be virtual or "bare metal", either way they must have the Docker service installed ahead of time.

Runner
------
Python or shell script used to actually execute a piece of software within a running Docker container, takes a Wrapper as input.  Used primarily to manage file organization and setting up configuration files for more complex software invocations.

Stanza
------
Block of configuration in an XML file

Wrapper
-------
script or description of a way to execute another piece of software with all parameters defined within a running Docker container.  This differs from a Dockerfile as it primarily defines the actual invocation of the specific piece of software, not the complete set of dependencies and/or environmental settings (though it might include environmental settings as well).
