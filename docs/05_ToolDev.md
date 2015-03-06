
Tool Development
================

Galaxy tool files are just simple XML files, so at this point one could just
open a text editor and start implementing the tool. Planemo has a command
``tool_init`` to quickly generate some of the boilerplate XML, so lets
start by doing that.

::

    % planemo tool_init --id 'seqtk_seq' --name 'Convert to FASTA (seqtk)'

The ``tool_init`` command can take various complex arguments - but the two
most basic ones are shown above ``--id`` and ``--name``. Every Galaxy tool
needs an ``id`` (this a short identifier used by Galaxy itself to identify the
tool) and a ``name`` (this is display to the Galaxy user and should be a short
description of the tool). A tool's ``name`` can have whitespace but its ``id``
should not.

The above command will generate the file ``seqtk_seq.xml`` - which should look
like this.

.. literalinclude:: writing/seqtk_seq_v1.xml
   :language: xml

This tool file has the common sections required for Galaxy tool but you will
still need to open up the editor and fill out the command template, describe
input parameters, tool outputs, writeup a help section, etc....

The ``tool_init`` command can do a little bit better than this as well. We can
use the test command we generated above ``seqtk seq -a 2.fastq > 2.fasta`` as
an example to generate a command block by specifing the inputs and the outputs
as follows.

::

    % planemo tool_init --force \
                        --id 'seqtk_seq' \
                        --name 'Convert to FASTA (seqtk)' \
                        --requirement seqtk@1.0-r68 \
                        --example_command 'seqtk seq -a 2.fastq > 2.fasta' \
                        --example_input 2.fastq \
                        --example_output 2.fasta

This will generate the following tool XML file - which now has correct
definitions for the input and output as well as an actual command template.

.. literalinclude:: writing/seqtk_seq_v2.xml
   :language: xml

As shown above the command ``seqtk seq`` generates a help message for this the
``seq`` command. ``tool_init`` can take that help message and stick it right
in the generated tool file using the ``help_from_command`` option. Generally
command help messages aren't exactly appropriate for Galaxy tool wrappers
since they mention argument names and simillar details that are abstracted
away by the tool - but they can be a good place to start.

::

    % planemo tool_init --force \
                        --id 'seqtk_seq' \
                        --name 'Convert to FASTA (seqtk)' \
                        --requirement seqtk@1.0-r68 \
                        --example_command 'seqtk seq -a 2.fastq > 2.fasta' \
                        --example_input 2.fastq \
                        --example_output 2.fasta \
                        --test_case \
                        --help_from_command 'seqtk seq'

.. literalinclude:: writing/seqtk_seq_v3.xml
   :language: xml

At this point we have a fairly a functional tool with test and help. This was
a pretty simple example - usually you will need to put more work into the tool
XML to get to this point - ``tool_init`` is really just designed to get you
started.

Now lets lint and test the tool we have developed. The planemo ``lint`` (or
just ``l``) command will reviews tools for obvious mistakes and compliance
with best practices.

::

    % planemo l
    Linting tool /home/john/test/seqtk_seq.xml
    Applying linter lint_top_level... CHECK
    .. CHECK: Tool defines a version.
    .. CHECK: Tool defines a name.
    .. CHECK: Tool defines an id name.
    Applying linter lint_tests... CHECK
    .. CHECK: 1 test(s) found.
    Applying linter lint_output... CHECK
    .. INFO: 1 output datasets found.
    Applying linter lint_inputs... CHECK
    .. INFO: Found 1 input parameters.
    Applying linter lint_help... CHECK
    .. CHECK: Tool contains help section.
    .. CHECK: Help contains valid reStructuredText.
    Applying linter lint_command... CHECK
    .. INFO: Tool contains a command.
    Applying linter lint_citations... WARNING
    .. WARNING: No citations found, consider adding citations to your tool.

By default ``lint`` will find all the tools in your current working directory,
but we could have specified a particular tool with ``planemo lint
seqtk_seq.xml``. The only warning we received here is telling us the tool
lacks citations. Seqtk_ is unpublished, but if there were a paper to cite we
could have done so by passing in the DOI_ (e.g. ``--doi '10.1101/010538'``).

Next we can run our tool's functional test with the ``test`` (or just ``t``)
command. This will print a lot of output but should ultimately reveal our one
test passed.

::

    % planemo --galaxy_root=/path/to/galaxy t
    ...
    All 1 test(s) executed passed.
    seqtk_seq[0]: passed


More information:

 * `Galaxy's Tool XML Syntax <https://wiki.galaxyproject.org/Admin/Tools/ToolConfigSyntax>`_
 * `Big List of Tool Development Resources <https://wiki.galaxyproject.org/Develop/ResourcesTools>`_

.. _DOI: http://www.doi.org/
.. _Seqtk: https://github.com/lh3/seqtk
