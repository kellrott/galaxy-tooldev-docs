Work environment
The command line will be executed in a temporary working directory where you can write temporary files and it will be cleaned out at the end of run. The input and output paths will be set to locations in different directories.

An important thing to note about Galaxy’s parallelization control is the setting/checking of the GALAXY_SLOTS environmental variable in the script above at the line:
```
-nct \${GALAXY_SLOTS:-4}
```
in the Simple Wrapper section.  This allows the number of threads used by the program to be configured by the system, with a default of 4 if it is not defined. Note that the ‘\$’, as the dollar sign character is passed on as a literal to the script (and not evaluated by the template system), this is because
```
$GALAXY_SLOTS
```
is actually an environmental variable defined at runtime, and not a variable that is filled in by the templating engine.

Catching Errors
See https://wiki.galaxyproject.org/Admin/Tools/ToolConfigSyntax#A.3Cstdio.3E.2C_.3Cregex.3E.2C_and_.3Cexit_code.3E_tag_sets for details on how to configure the error state checking. The standard method is to look for error exit code. Note, if you are using a BASH script, use the ‘set -e’ so that any command error will result in the script failing. You can set up a regex to search stderr for failure messages, but this method should not be used by itself, as it may not catch all errors.

Testing and debugging
Tools for project creation, building and wrapper format checking can be found at https://planemo.readthedocs.org
VMs for debugging and interactive development will be provided in Q1 2015.
