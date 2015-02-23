
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

5) Edit wrapper. Check the file synax with
```
planemo lint my_cool_tool.xml
```

6) Test your tool

Note: If you think that Galaxy is failing dynamically to reload your tool. Use
the command
```
supervisorctl restart galaxy:
```
