Install [Google Cloud SDK](https://developers.google.com/cloud/sdk/) on your local machine.

#Starting up Galaxy Development Server

${youtube?videoId=jnarp%2Dj12lw}

We need better screen casts

#Composing a Dockerfile
${youtube?videoId=S%2DEOr9a5lr8}


#Galaxy Tool Wrappers

${youtube?videoId=kphYnONMOP8}
We need better screen casts

#Running the DREAM submission script



Summary
Every tool deployed in the UCSC NCI-Cluster environment requires two components; a ‘container image’ that describes the software dependencies required for running an analysis and a tool wrapper description the describes the command line used to invoke that tool and the different inputs and parameters used when invoking a tool.

The software dependencies are managed by Docker (http://docker.io). A Docker build script is the set of instructions used to create the environment needed to run a specific software package (e.g. Samtools).  This build script can then be executed on any system running the Docker service.  The produced container image can be viewed as a ‘light-weight VM’, which should cover all software dependencies regardless of programming language or SDK. The software container provides an easy way to package up all dependencies and move them to a target machine where the program will actually be run.

In order to actually run the program, the correct interface to the tool must be described. It is assumed that all tools can be invoked from a command line. The tool wrapper provides a template command line that will be filled out at run time. After a template command line is filled out using the input files and parameters, it will run inside the packaged Docker containers. Specifically the tool configuration is written using the Galaxy Tool Wrapping specification ( https://wiki.galaxyproject.org/Admin/Tools/ToolConfigSyntax )

This gives us a working copy of the collorabor’s tool and a way to call it, with no install requirements. Having tools described this way makes them workflow system independent. For example, containerized tools could be deployed under OICR’s SeqWare system, for ICGC PanCan analysis, if needed.

Pindel and Varscan are already working inside of Docker containers.  Broad’s MuTect and ContEst have been converted into containers and wrapped for Galaxy. The key ingredient to progress is working with collaborators to have them share their entire workflows and all of the necessary dependencies.  The work the collaborators need to do involves creating portable tool descriptions and workflow specifications.  This is described in detail below.
