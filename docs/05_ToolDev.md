
Galaxy Tool Development
=======================

There are many available resources to help with developing tools for galaxy. Technical questions can be directed to the [BioStars](https://biostar.usegalaxy.org/) group or the [Galaxy Dev mailing list](http://dev.list.galaxyproject.org/). Because of the cloud nature of the SMC-Het challenge, there are a few caveats that apply to submitted SMC-Het Galaxy tools.

1. Every submitted tool MUST define a docker container requirement. Other requirements mechanisms [documented in galaxy](https://wiki.galaxyproject.org/Admin/Tools/ToolConfigSyntax?action=show&redirect=Admin%2FTools%2FTool+Config+Syntax#A.3Crequirements.3E_tag_set), for example the 'package' system, are not supported for the challenge.
2. The docker requirement must point to a valid image on the [Docker Registry](https://registry.hub.docker.com/) or the user must provide a Dockerfile as part of the tool package.
3. ToolData inputs, ie reference file paths specified by the `from_file` or `from_data_table` flags in [the options tag](https://wiki.galaxyproject.org/Admin/Tools/ToolConfigSyntax?action=show&redirect=Admin%2FTools%2FTool+Config+Syntax#A.3Coptions.3E_tag_set), are not allowed.

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
Rather then start from a blank page, you can use Planemo to populate a stub file you can start filling in.

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

More examples of how to use the `tool_init` method can be found at in the [Planemo Docs](http://planemo.readthedocs.org/en/latest/writing_standalone.html#the-basics)


Web Based IDE
-------------

Included in the Planemo VM is an installation of [Codebox](https://www.codebox.io/). You can find it by going to `http://<ip address>`/ide/

It automatically loads the the /opt/galaxy/tools directory, which is the same directory Galaxy scans to look for installed tools.

${image?fileName=codebox_ide.png}
