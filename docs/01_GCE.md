

Google Compute Engine based Deployment
======================================

${toc}

This section will help you set up a compute instance and a persistent disk containing challenge code and data. You can choose to use either the Developers Console web interface (covered in the quick-start) or the Google Cloud SDK command line tool (covered in the FAQ). If you need more help getting started with using Google Compute Engine, [the user documentation](https://cloud.google.com/compute/docs/quickstart-developer-console) provides a good intro/summary of how to use the console.

The main steps in this procedure are:
1. import the planemo image
2. create a persistent disk big enough to hold your code and the data
3. create an instance and attach the disk
4. mount and format the disk
5. run the provided sample workflow via Galaxy!

${image?fileName=DREAM_Comic_GCE.png}

Google Cloud Platform Quick Start
---------------------------------

(1) First go to https://console.developers.google.com to view your projects. If you do not already have a project use the 'Create Project' button.

    TODO: screenshot here of a project home screen

    > For Google Cloud Platform, a Project is an area to organize members, cloud resources such as GCE instances, and billing.  Every GCP project has an ID and number. You can choose your own ID, but the number will be assigned automatically by GCP.

(2) Load the planemo image into your project.

    * Name: planemo-machine-image
    * Source type: Cloud storage object
    * Cloud storage object path: galaxyproject_images/planemo_machine.image.tar.gz

    TODO screenshot here of Compute -> Compute Engine -> Images -> New Image with dialog filled in

(3) Create your data disk.

    * Name: planemo-data
    * Zone: choose your preferred zone but be sure to make note of it and use the same zone when creating your VM
    * Source type: None (blank disk)
    * Size: we recommend at least ??GB (TODO: add recommended # of GB)

    TODO screenshot here of Compute -> Compute Engine -> Disks -> New Disk with dialog filled in

(4) Create your VM.

    1. Compute -> Compute Engine -> VM Instances
      If a dialog pops up asking what you want to do, select 'Create Instance', otherwise click the 'New Instance' button.
    2. Fill out the instance creation dialog, this will include:
        1. Set the name (in these examples, we name the machines 'planemo')
        2. Select the Zone you want to deploy in (should be the same as for the disk created in the prior step)
        3. Select the machine type of choice, a system with at least 6GB of RAM is expected
        4. For the Boot Disk -> Change -> Your Image
        5. For the image, Select 'planemo-machine-image'
        6. Allow HTTP and HTTPS traffic
    3. Click on the 'Management, disk, networking, access & security options' to expand the drop-down.
    4. Click on Disks -> Add Item and select the disk you created in the prior step.
    5. Hit Create

    TODO: screenshot of instance creation dialog all filled in.

(5) SSH to the newly created VM.

    To see your instance list, navigate back to Compute -> Compute Engine -> VM Instances

    TODO: screenshot of list of one instance and the ssh button

(6) Format and mount your data disk.

    We do all of the commands that follow as user `ubuntu` on the VM.  Change to this user.
```
sudo su ubuntu
```

    Run the following command to find the disk (look for the one with the name you chose when creating the disk).
```
ubuntu@planemo:~$ ls -l /dev/disk/by-id/google-*
lrwxrwxrwx 1 root root  9 May  8 23:02 /dev/disk/by-id/google-persistent-disk-0 -> ../../sda
lrwxrwxrwx 1 root root 10 May  8 23:02 /dev/disk/by-id/google-persistent-disk-0-part1 -> ../../sda1
lrwxrwxrwx 1 root root  9 May  8 23:03 /dev/disk/by-id/google-persistent-disk-1 -> ../../sdb
```
TODO: update the above output to match the disk name we used in the above screenshot

    Make sure the `/opt/galaxy/tools` directory is empty.
```
ubuntu@planemo:~$ ls -l /opt/galaxy/tools
total 0
```
    Mount and format the disk.
```
$ sudo /usr/share/google/safe_format_and_mount -m "mkfs.ext4 -F" /dev/sdb /opt/galaxy/tools
```

    Set ownership of the disk to user `ubuntu`.
```
ubuntu@planemo:~$ sudo chown -R ubuntu /opt/galaxy/tools
```

    Now your external disk should be mounted by the VM.
```
ubuntu@planemo:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       9.9G  3.1G  6.3G  33% /
none            4.0K     0  4.0K   0% /sys/fs/cgroup
udev            3.7G   12K  3.7G   1% /dev
tmpfs           749M  412K  748M   1% /run
none            5.0M     0  5.0M   0% /run/lock
none            3.7G     0  3.7G   0% /run/shm
none            100M     0  100M   0% /run/user
/dev/sdb         30G   44M   28G   1% /opt/galaxy/tools
```

(6) Install the SMC-Het example on the VM.
```
cd /opt/galaxy/tools
git clone https://github.com/Sage-Bionetworks/SMC-Het-Challenge.git
cd SMC-Het-Challenge
```

(7) Restart Galaxy and Docker.
```
sudo service docker restart
sudo supervisorctl restart galaxy:
```

(8) Go back to the Developers Console and click the little pop-out arrow to the right of theexternal IP address for the instance.  Your browser will be redirected the the home page for Galaxy on your VM.

    TODO: screenshot of Galaxy home page

(9) Upload data.

    You can upload test data to your instance by hitting the upload button and then selecting 'Paste/Fetch Data' and telling galaxy to download the file `https://raw.githubusercontent.com/Sage-Bionetworks/SMC-Het-Challenge/master/data/mutect_filtered_IS3_chr21.vcf`
    TODO: screenshot of upload small sample file

(10) Run the workflow.

    1. Select the DPC tool in the left hand tool panel
    2. Find the downloaded VCF file in the 'VCF file' selection in the center panel
    3. Click the Execute button at the bottom of the form
    4. The output data files should appear in the data history panel on the right hand side of the screen
    
    TODO: screenshot of completed run of the workflow.

Ta da!  You have set up your Google Compute engine virtual machine running Galaxy and executed the sample workflow.

Frequently Asked Questions
==========================

How can I save my work?
-----------------------
Create [snapshots](https://cloud.google.com/compute/docs/disks/persistent-disks#snapshots) of your persistent disks.

How can I make the most of my credits?
--------------------------------------
[Stop](https://cloud.google.com/compute/docs/instances/#stopping_an_instance) your virtual machine instances when not in use and [restart](https://cloud.google.com/compute/docs/instances/#restarting_a_stopped_instance) them when you are ready to work again.

How can I see how much I have spent?
------------------------------------
View your [cost and payment history](https://support.google.com/cloudbilling/answer/3540823?hl=en&ref_topic=2991962).

How do I get support for Google Compute Engine
----------------------------------------------
For any questions about Google Compute Engine, please post to the forum on [Stack Overflow](http://stackoverflow.com/questions/tagged/google-compute-engine)

For assistance from a Google Support Engineer, please see https://cloud.google.com/support/.

How do I install and configure the gcloud command line tool?
-------------------------------------------------------------

(1) First go to https://console.developers.google.com to view your projects, and obtain your project ID. If you do not already have a project use the 'Create Project' button.

(2) Follow the instructions [here](https://developers.google.com/cloud/sdk/) to install the Google Cloud SDK on your local machine.

(3) Authenticate to gcloud.
```
gcloud auth login
```

(4) Configure the default project ID.
```
gcloud config set project YOUR-PROJECT-ID
```
>  You can find your project ID at the [Google Developers Console](https://console.developers.google.com/project).

    If you don't set the current project, for later steps you make get an error message like:
    
    ```
    ERROR: (gcloud.compute.instances.create) The required property [project] is not currently set.
    You may set it for your current workspace by running:

    $ gcloud config set project VALUE

    or it can be set temporarily by the environment variable [CLOUDSDK_CORE_PROJECT]
    ```

(5) Configure the default zone (replace us-central1-f with your preference).
```
gcloud config set compute/zone us-central1-f
```

(6) If you've never used GCE before, you may need to enable the Compute Engine API.  You can [click here](https://console.developers.google.com/start/api?id=compute_component) to enable the API or enable it manually via:
    1. go to the webpage "Google Developers Console" at https://console.developers.google.com/project
    2. choose the project
    3. Under APIs, choose Compute Engine API and "Enable"


    If you don't enable the API, for later steps you make get an error message like:
    ```
    NAME PROJECT ALIAS DEPRECATED STATUS
    ERROR: (gcloud.compute.images.create) Some requests did not succeed:

    Access Not Configured. The API (Compute Engine API) is not enabled for your project. Please
    use the Google Developers Console to update your configuration.
    ```

How can I update the Planemo Image?
----------------------------------
If there is a need to update the SDK image, usually because bug fixes or new features, you will need to create a new VM based on a fresh image download.

When updating the image, you may want to get delete the older version. There is no need to keep an image if there is an instance running based on that image. Deleting the image isn't required if you are willing to pay for the extra storage space, and can manage the names of multiple images. In the previous instructions, we referred to the disk image as `planemo-machine-image`, but you could easily create a second image named `planemo-machine-image-v2`.

>Deleting an image is different then deleting an instance. The image is simply the start source, and once an instance as been started it is no longer dependent on the image. You work is stored in the instance. Do not delete that until you've copied it somewhere else.

If you want to stop a VM, but not delete it:
```
gcloud compute instances stop planemo
```

To delete the old image
```
gcloud compute images delete planemo-machine-image
Do you want to continue (Y/n)?  Y
Deleted [https://www.googleapis.com/compute/v1/projects/level-elevator-666/global/images/planemo-machine-image].
```

To get the updated image, follow the instructions starting a new image. The URL mentioned in the command line points to the current image. If you are keeping an older instance of the VM running, you will need to find a name. So you can replace `planemo` with `planemo-v2` in the instructions.

How can I transfer data between instances?
------------------------------------------
The easiest way to move data between two VMs is to use your personal machine as a transfer point. So we will be transferring data from the old VM to your local machine and then to the new VM.

To transfer data from the old instance to the new one, have both instances running at the same time. First list running instances
```
gcloud compute instances list
```
Which should return a list:
```
NAME       ZONE          MACHINE_TYPE  INTERNAL_IP   EXTERNAL_IP     STATUS
planemo-v2 us-central1-f n1-standard-2 10.240.229.40 162.222.179.9   RUNNING
planemo    us-central1-f n1-standard-2 10.240.49.28  130.211.131.162 RUNNING
```

Copy the files from the original machine to your local machine:
```
gcloud compute copy-files ubuntu@planemo:/opt/galaxy/tools ./
```

Copy the files from your local machine to the new VM:
```
gcloud compute copy-files tools ubuntu@planemo-v2:/opt/galaxy/
```

How can I set up my VM using the command line tools?
---------------------------------------------------

### Load the Planemo Image

> This only needs to be done once.  If you already did this using the Developers Console, skip this step.

Load the image into your project:
```
gcloud compute images create planemo-machine-image --source-uri http://storage.googleapis.com/galaxyproject_images/planemo_machine.image.tar.gz
```
This will return a read out like:
```
Created [https://www.googleapis.com/compute/v1/projects/level-elevator-666/global/images/planemo-machine-image].
NAME                  PROJECT            ALIAS DEPRECATED STATUS
planemo-machine-image level-elevator-666                  READY
```
### Start the VM instance

At this point you may need to add a firewall rule set to allow traffic to the HTTP port (80). Instructions about this can be found in the GCE [quick start](https://cloud.google.com/compute/docs/quickstart#addfirewall) manual.

The command to add a HTTP ruleset is (note that we are assigning the tagset name 'http-server', this will be reference later when we create an VM instance that uses these firewall rules):
```
gcloud compute firewall-rules create allow-http \
    --target-tag http-server \
    --description "Incoming http allowed." --allow tcp:80
```
To create and start running the planemo instance via command line interface
```
gcloud compute instances create planemo \
    --machine-type n1-standard-2 --image planemo-machine-image \
    --tags http-server
```
This will return a read out like
```
Created [https://www.googleapis.com/compute/v1/projects/level-elevator-666/zones/us-central1-f/instances/planemo].
NAME    ZONE          MACHINE_TYPE  INTERNAL_IP    EXTERNAL_IP    STATUS
planemo us-central1-f n1-standard-2 10.240.143.115 162.222.182.19 RUNNING
```
Now if you navigate to the listed EXTERNAL_IP, you will find the running Planemo-Machine

> If you go to the web page and you see an error that 'an internal server error' has occured, and the message doesn't go away, you can restart the server by sshing into the server and issuing the command `sudo supervisorctl restart galaxy:`

To SSH into the machine use (where planemo is the name of the instance you provided earlier)
```
gcloud compute ssh ubuntu@planemo
```
> Remember when you are done using your VM, turn it off. You are charged for every hour it is on, and if you forget about it, it will rack up costs quickly.

### Attach additional storage to the VM

1. You can create a volume to attach to your machine with the command
```
gcloud compute disks create --size 30GB planemo-data
```

2. Then attach the disk to your instance
```
gcloud compute instances attach-disk --disk planemo-data planemo
```
  After the disk is attached to the instance, it will be available to be mounted.  Follow the rest of the instructions in the above quick-start to proceed from here.
