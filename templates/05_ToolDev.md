
Tool Development
================

Once logged into the SDK
------------------------

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


$WRITING_PARAMS
