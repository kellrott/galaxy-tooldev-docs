

Working on Examples
===================

These examples are based on being able to access a terminal on the planemo machine and work in the ``/opt/galaxy/tools` directory. If you don't know how to do this, fix the instructions on how to SSH into your system. You will want to execute these commands as the `ubuntu` user.

Download example code
---------------------

1. Obtain the example tool set
```
git clone https://github.com/Sage-Bionetworks/SMC-Het-Challenge.git
cd SMC-Het-Challenge
```

2. Navigate to the web server to view the Galaxy UI. On GCE based machines it will
be `http://IP_ADDRESS/` (where IP_ADDRESS is given as the `external address` for the VM in the system console), while on VirtualBox system it will likely be `http://localhost:8010`

3. The general Galaxy layout is to have a tool panel on the left hand side of the screen, with a data history panel on the right hand side. The Planemo Machine has been set up to automatically scan the `/opt/galaxy/tools` directory for valid tools. Because of this, the "VCF DPC clustering" program from the smc\_het\_example package should appear in the left hand side of the window.

> If the DPC example does not display in the tool selection panel on the left hand side of the window, try running `sudo supervisorctl restart galaxy:` to restart the Galaxy server



Using the DPC code
==================

You can upload test data to you instance by hitting the upload button, selecting 'Paste/Fetch Data' and telling galaxy to download the file
```
https://raw.githubusercontent.com/Sage-Bionetworks/SMC-Het-Challenge/master/data/mutect_filtered_IS3_chr21.vcf
```

1. Select the DPC tool in the left hand tool panel
2. Find the downloaded VCF file in the 'VCF file' selection in the center panel
3. Click the `Execute` button at the bottom of the form
4. The output data files should appear in the data history panel on the right hand side of the screen
