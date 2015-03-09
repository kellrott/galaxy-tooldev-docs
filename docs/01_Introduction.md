
Getting Started
===============





Development Life Cycle
======================

To develop a Galaxy wrapped tool, the steps are:

1) Create a Docker container capable of running your tool

2) Write a Wrapper that describes your tools inputs, outputs and parameters.

3) Test the tool inside a Galaxy environment to debug issues


The Galaxy Tool Standard Development Kit (SDK) is named Planemo. Part of Planemo
is a Virtual Machine Image


VM Based Development
====================

Once logged into the SDK

1) In '/opt/galaxy/tools' run
```
planemo tool_init
```

2) Reload the Galaxy panel. You tool should now appear in the list of tools


3) Build Dockerfile to describe how your container is built

4) Run docker build to construct a working container
```
planemo docker_build
```

5) Edit wrapper. Check the file syntax with
```
planemo lint my_cool_tool.xml
```

6) Test your tool

Note: If you think that Galaxy is failing dynamically to reload your tool. Use
the command
```
supervisorctl restart galaxy:
```

Docker based Development
========================

Please note: Docker based deployment requires the user to install and run docker
well as setup 'Docker-By-Docker' deployment, so it is considered an option only for
'advanced users'

Download the most update SDK docker image
```
docker pull planemo/box
```

Deploy SDK
```
docker run -v `pwd`:/opt/galaxy/tools -v /var/run/docker.sock:/var/run/docker.sock -p 8080:80 --name planemo planemo/box
```

Note: If you get the error message
```
FATA[0000] Error response from daemon: Conflict, The name planemo is already assigned to 0109fd956412. You have to delete (or rename) that container to be able to assign planemo to a container again.

```

You can either restart the server with
```
docker start -a planemo
```

Or delete the server before starting again
```
docker rm -v planemo
```


Obtain a command line inside the
```
docker exec -i -t planemo /bin/bash
```

Working on Examples
===================

1) Obtain the example tool set
```
git clone https://github.com/ucscCancer/smc_het_example
cd smc_het_example
```

2) Launch the development server

3) The example program "DPC", should appear in the window
