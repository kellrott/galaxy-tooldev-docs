

Google Compute Engine based Deployment
====================================

For a GCE-based deployment, first Install [Google Compute SDK](https://developers.google.com/cloud/sdk/) on your local machine.

This section will help you set up a compute instance and a persistent disk containing challenge data. For most steps, you can choose to use either the Developers Console web interface or the Google Compute SDK command line tools. If you need help getting started with using the Google Compute, [the user documentation ](https://developers.google.com/compute/docs/console) provides a good intro/summary of how to use the console.

The main steps in this procedure are:
1. create a persistent disk big enough to hold the data
2. create an instance and attach the disk
3. mount and format the disk
4. copy data to the disk


To start up the Planemo Machine under GCE
-----------------------------------------

> Parts of this documentation will cover it, but the very first thing you will want to do is make sure you have the `gcloud` command installed and are properly logged in. Follow the instruction found at https://cloud.google.com/compute/docs/gcloud-compute/

First go to https://console.developers.google.com to view your projects, and obtain your project id. If you do not already have a project use the 'Create Project' button.

>For Google Cloud Platform, a Project is an area to organize members, cloud resources such as GCE instances, and billing.  Every GCP project has a name and an ID. You can assign the name yourself, but the ID will be assigned automatically by GCP. You can find your project name at the [Google Developers Console](https://console.developers.google.com/project)


Before you can can start, make sure you have done the following (again, following the instructions found at https://cloud.google.com/compute/docs/gcloud-compute/)
1. Authenticated your command line tools
2. Set the default project
3. Set the default zone

To authenticate
```
gcloud auth login
```
You can manage your projects on the [command line](https://cloud.google.com/compute/docs/projects) or via the [web](https://developers.google.com/console/help/new/?&_ga=1.38552803.1582672075.1425679810#managingprojects)

You can set the current project with the command
```
gcloud config set project YOUR-PROJECT-ID
```
If you don't set the current project, for later steps you make get an error message like:
```
ERROR: (gcloud.compute.instances.create) The required property [project] is not currently set.
You may set it for your current workspace by running:

$ gcloud config set project VALUE

or it can be set temporarily by the environment variable [CLOUDSDK_CORE_PROJECT]
```
Set your default zone (replace us-central1-f with your preference)
```
gcloud config set compute/zone us-central1-f
```

Loading the Planemo Image
-------------------------
Before you can launch the VM instance you will need install the


Load the image into your account
```
gcloud compute images create planemo-machine-image --source-uri http://storage.googleapis.com/galaxyproject_images/planemo_machine.image.tar.gz
```
This will return a read out like
```
Created [https://www.googleapis.com/compute/v1/projects/level-elevator-666/global/images/planemo-machine-image].
NAME                  PROJECT            ALIAS DEPRECATED STATUS
planemo-machine-image level-elevator-666                  READY
```

Starting VM instance via command line
-------------------------------------
At this point you may need to add a firewall rule set to allow traffic to the HTTP port (80). Instructions about this can be found in the GCE [quick start](https://cloud.google.com/compute/docs/quickstart#addfirewall) manual.

The command to add a HTTP ruleset is (note that we are assigning the tagset name 'http-server', this will be reference later when we create an VM instance that uses these firewall rules):
```
gcloud compute firewall-rules create allow-http \
    --target-tag http-server \
    --description "Incoming http allowed." --allow tcp:80
```
To deply via command line interface
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

>If you go to the web page and you see an error that 'an internal server error' has occured, and the message doesn't go away, you can restart the server by sshing into the server and issuing the command `sudo supervisorctl restart galaxy:`

To SSH into the machine use (where planemo is the name of the instance you provided earlier)
```
gcloud compute ssh ubuntu@planemo
```
>Remember when you are done using your VM, turn it off. You are charged for every hour it is on, and if you forget about it, it will rack up costs quickly.

Starting VM instance via the web interface
-------------------------------

> There is no way to add a custom VM image to a GCE project via the web interface, so you will still need to follow the instructions related to `Loading the Planemo Image` before you can start an instance based on that image

1. Go to your console at https://console.developers.google.com
2. Select the project you want to deploy under
3. Under the left hand menu, select Compute -> Compute Engine -> VM Instances
4. If a dialog pops up asking what you want to do, select 'Create Instance', otherwise click the
'New Instance' button
5. Fill out the instance creation dialog, this will include:
    1. Set the name (in these examples, we name the machines 'planemo')
    2. Allow HTTP and HTTPS traffic
    3. Select the Zone you want to deploy in
    4. Select the machine type of choice, a system with at least 6GB of RAM is expected
    5. For the Boot Disk, Select 'New Disk From Image'
    6. For the image, Select 'planemo-machine-image'
6. Hit Create
7. To see your instance list, navigate back to Compute -> Compute Engine -> VM Instances
8. If you click the IP address for the instance you should be directed the the home page of you newly
create Galaxy SDK instance


Updating Planemo Image
----------------------
If there is a need to update the SDK image, usually because bug fixes or new features, you will need to create a new VM based on a fresh image download.

When updating the image, you may want to get delete the older version. There is no need to keep an image if there is an instance running based on that image. Deleting the image isn't required if you are willing to pay for the extra storage space, and can manage the names of multiple images. In the previous instructions, we referred to the disk image as `planemo-machine-image`, but you could easily create a second image named `planemo-machine-image-v2`.

>Deleting an image is different then deleting an instance. The image is simply the start source, and once an instance as been started it is no longer dependent on the image. You work is stored in the instance. Do not delete that until you've copied it somewhere else.

To delete the old image
```
> gcloud compute images delete planemo-machine-image
Do you want to continue (Y/n)?  Y
Deleted [https://www.googleapis.com/compute/v1/projects/level-elevator-666/global/images/planemo-machine-image].
```

To get the updated image, follow the instructions starting a new image. The URL mentioned in the command line points to the current image. If you are keeping an older instance of the VM running, you will need to find a name. So you can replace `planemo` with `planemo-v2` in the instructions.

Transferring data between instances
-----------------------------------
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

To Attach Additional Storage to you GCE VM
==========================================

You can create a volume to attach to your machine with the command
```
gcloud compute disks create --size 30GB planemo-data
```

Then attach the disk to your instance
```
gcloud compute instances attach-disk --disk planemo-data planemo
```
After the disk is attached to the instance, it will be available to be mounted.

Mount and format the disk.
--------------------------

1. From the Google Compute instance, run the following command to find the disk (look for the one with the name you chose when creating the disk):

```
$ ls -l /dev/disk/by-id/google-*
lrwxrwxrwx 1 root root  9 Dec 13 00:34 /dev/disk/by-id/google-dream-challenge-simulated-data1 -> ../../sdb
lrwxrwxrwx 1 root root  9 Dec 13 00:34 /dev/disk/by-id/google-smc-testing-highmem -> ../../sda
lrwxrwxrwx 1 root root 10 Dec 13 00:35 /dev/disk/by-id/google-smc-testing-highmem-part1 -> ../../sda1
```

2. identify and create if necessary the directory to which you want to mount the disk:
```
$ sudo mkdir /mnt/simdata1
```

3. mount and format:
```
$ sudo /usr/share/google/safe_format_and_mount -m "mkfs.ext4 -F" /dev/sdb /mnt/simdata1/
You may need to chmod and/or chown to allow users other than root to write to this directory.
```

Note: If you created your instance first and now need to attach the disk, you can do this using the Developers Console (select your instance, then use the "Attach" option under the "Disks" section) or using gcutil attachdisk command. Then follow the mount and format instructions above.


GCE Support
===========

For any questions about Google Compute Engine, please post to the forum on [Stack Overflow](http://stackoverflow.com/questions/tagged/google-compute-engine)

For assistance from a Google Support Engineer, please see https://cloud.google.com/support/
