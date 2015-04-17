
Galaxy Tool Development
=======================

Tool Development Cycle
----------------------

1. In '/opt/galaxy/tools' run
```
planemo tool_init
```
2. Reload the Galaxy panel. You tool should now appear in the list of tools

3. Build Dockerfile to describe how your container is built

4. Run docker build to construct a working container
```
planemo docker_build
```
5. Edit wrapper. Check the file syntax with
```
planemo lint my_cool_tool.xml
```
6. Test your tool

Note: If you think that Galaxy is failing dynamically to reload your tool. Use
the command
```
supervisorctl restart galaxy:
```

Base XML config file
--------------------

```
> planemo project_init mytool
Creating empty project, this function doesn't do much yet.
> cd mytool
> planemo tool_init
Name: MyTool
Id: mytool
Tool written to mytool.xml
```

Which will produce the file
```
<tool id="mytool" name="MyTool" version="0.1.0">
<requirements>
</requirements>
<stdio>
<exit_code range="1:" />
</stdio>
<command><![CDATA[
TODO: Fill in command template.
]]></command>
<inputs>
</inputs>
<outputs>
</outputs>
<help><![CDATA[
TODO: Fill in help.
]]></help>
</tool>
```

More examples of how to use the `tool_init` method can be found at http://planemo.readthedocs.org/en/latest/writing_standalone.html#the-basics
