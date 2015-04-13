

Working on Examples
===================

These examples are based on being able to access a terminal on the
planemo machine and work in the /opt/galaxy/tools directory. If you don't know
how to do this, fix the instructions on how to SSH into your system. You will
want to execute these commands as the `ubuntu` user.

Download example code
---------------------

1. Obtain the example tool set
```
git clone https://github.com/ucscCancer/smc_het_example
cd smc_het_example
```

2. Navigate to the web server to view the Galaxy UI. On GCE based machines it will
be `http://IP_ADDRESS/` (where IP_ADDRESS is given as the `external address` for the VM in the system console), while on VirtualBox system it will likely be `http://localhost:8010`

3. The general Galaxy layout is to have a tool panel on the left had side of the screen, with a data history panel on the right hand side. The Planemo Machine has been set up to automatically scan the `/opt/galaxy/tools` directory for valid tools. Because of this, the "DPC" program from the smc_het_example package should appear in the left hand side of the window.

> If the DPC example does not display in the tool selection panel on the left hand side of the window, try running `sudo supervisorctl restart galaxy:` to restart the Galaxy server


Wrapper
=======
```
<tool id="${TOOL_ID}" name="${TOOL_NAME}" version="1.0.0">
    <description>Put Description Here</description>
    <requirements>
        <container type="docker">r-base</container>
    </requirements>
    <command interpreter="Rscript">
dpc.R ${input_vcf}
    </command>

    <inputs>
        <param format="vcf" name="input_vcf" type="data" label="VCF file" help="" />
    </inputs>

    <outputs>
        <data format="png" name="output_png" label="DirichletProcessplotBinomial PNG" from_work_dir="DirichletProcessplotBinomial.png"/>
        <data format="txt" name="output_density" label="DirichletProcessplotBinomial Density" from_work_dir="DirichletProcessplotBinomialdensity.txt"/>
        <data format="txt" name="output_polygon" label="DirichletProcessplotBinomial Polygon" from_work_dir="DirichletProcessplotBinomialpolygonData.txt"/>
    </outputs>

    <help>
You should totally explain how to use your tool here
    </help>

    <tests>
        <test>
        </test>
    </tests>

</tool>
```
