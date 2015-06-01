

Galaxy Tool Development
=======================

The software dependencies are managed by Docker (http://docker.io). A Docker build script is the set of instructions used to create the environment needed to run a specific software package (e.g. Samtools).  This build script can then be executed on any system running the Docker service.  The produced container image can be viewed as a 'light-weight VM', which should cover all software dependencies regardless of programming language or SDK. The software container provides an easy way to package up all dependencies and move them to a target machine where the program will actually be run.

In order to actually run the program, the correct interface to the tool must be described. It is assumed that all tools can be invoked from a command line. The tool wrapper provides a template command line that will be filled out at run time. After a template command line is filled out using the input files and parameters, it will run inside the packaged Docker containers. Specifically the tool configuration is written using the Galaxy Tool Wrapping specification ( https://wiki.galaxyproject.org/Admin/Tools/ToolConfigSyntax )

Getting Started
===============

Planemo-Machine is a Galaxy Tool Standard Development Kit (SDK) designed to
make developing Docker based Galaxy tools easy. It has an installed copy of Galaxy,
an up to date version of Docker, a web based IDE and the Planemo tools.

With this system, which can be deployed on a variety of virtual machine services,
you can quickly develop and test new tools and see how they behave in the Galaxy environment.
To develop a Galaxy wrapped tool, the steps are:

1. Create a Docker container capable of running your tool
2. Write a Wrapper that describes your tools inputs, outputs and parameters.
3. Test the tool inside a Galaxy environment to debug issues


Before any development can happen, you must first deploy a Planemo-Machine in your VM
system of choice. The current deployment options are: [Google Cloud Engine](https://www.synapse.org/#!Synapse:syn2786217/wiki/209793) or
[Virtual Box](https://www.synapse.org/#!Synapse:syn2786217/wiki/209795).
