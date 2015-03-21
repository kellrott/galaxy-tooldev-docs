
Submitting a workflow to the SMC-Het Challenge
==============================================

A submission to the challenge is a Workflow. The workflow will connect to several different tools. This script will scan a Galaxy workflow, download all of the relavant tools and then upload them to your Synapse Project Folder

The first step is to create a workflow that takes the challenge input files, runs the analysis and produces the outputs. There are a few additional things that need to be added to the workflow so that it can be run in the framework.

The code for submitting code to the challenge can be found at https://github.com/Sage-Bionetworks/SMC-Het-Challenge to install:
```
git clone https://github.com/Sage-Bionetworks/SMC-Het-Challenge.git
```

Extracting a Workflow
-------------------
You will need to edit the workflow in the Galaxy Editor but if you have already done all the operations by hand, you can select the 'History Options' drop down menu on the right hand of the Analysis panel above the history, which looks like a gear. There will be a selection called 'Extract Workflow', which will give you the option of creating a workflow based on your previous actions in the history.

Creating a Workflow
-------------------
Go to the workflow menu, once on the Workflow page, select 'Create new Workflow', you can then name it and hit the 'Create' button. Once in the workflow editor, find the tools required in the panel on the lefthand side and click them to create an instance in the central editor panel. You can connect the tools by dragging a 'connection noodle' from the outputs on the right hand side or the first tool to the inputs on the left hand side of the next tool. The panel on the right hand side will allow you to edit parameters.

You will also need to create inputs to the workflow. That selection is at the bottom of the tool panel on the left hand side of the screen. Under 'Inputs' you can click 'Input Dataset' to create an instance in the editor. You will need to drag the connection noodles from that input dataset to the tools that require it.

Annotating the Workflow
-----------------------

Once your workflow has been created you will need to do some minor edits to make sure the leaderboard system can correctly assign inputs to the workflow and collect the right file for evaluation. In the workflow editor, you will click the different elements of the workflow to bring up their info in the 'Details' panel on the right hand side of the screen. When requested to add annotations to a element in the workflow, look for the `Edit Step Attributes` subsection in the tool and use the `Annotation / Notes:` section to add annotation text to the step.

To create a workflow that can be used by the evaluation system you will:
1. Use the 'Annotation' field to name one of the dataset inputs `VCF_INPUT`
2. For reference files, upload the required file to your project in Synapse, then put the Synapse ID (ie syn12345) into the Annotation fields of the workflow data inputs
3. For the output file, use the 'Post Job Rename' option in the tool option menu to rename the submission file to 'OUTPUT'


Test the workflow
-----------------

Submit the workflow
-------------------
