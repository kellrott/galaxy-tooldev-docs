

Google Cloud Engine based Deployment
====================================

For GCE Based SDK first Install [Google Cloud SDK](https://developers.google.com/cloud/sdk/) on your local machine.

This section will help you set up a compute instance and a persistent disk containing challenge data. For most steps, you can choose to use either the Developers Console web interface or the Google Cloud SDK command line tools ("gcutil" and "gsutil"). If
you need help getting started with using the Google Cloud, [the user documentation ](https://developers.google.com/compute/docs/console) provides a good intro/summary of how to use the console:

The main steps in this procedure are:
1. create a persistent disk big enough to hold the data
2. create an instance and attach the disk
3. mount and format the disk
4. copy data to the disk

First go to https://console.developers.google.com to view your projects, and obtain
your project id. If you do not already have a project use the 'Create Project' button.

>For GCE, a Project is a area to organize members, cloud resource instances and billing. Every GCE project has a name and an ID. You can assign the name yourself, but the ID will be assigned automatically by GCE. You can find your project name at the [GCE Console](https://console.developers.google.com/project)

To start up the Planemo Machine under GCE:
------------------------------------------
If you haven't already done it, run the Google Cloud SDK login
```
gcloud auth login
```

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

Load the image into your account, replace YOUR-PROJECT-ID with the Google cloud project
that you want to run the VM inside of
```
gcloud compute images create planemo-machine-image --source-uri http://storage.googleapis.com/galaxyproject_images/planemo_machine.image.tar.gz
```

This will return a read out like
```
Created [https://www.googleapis.com/compute/v1/projects/level-elevator-666/global/images/planemo-machine-image].
NAME                  PROJECT            ALIAS DEPRECATED STATUS
planemo-machine-image level-elevator-666                  READY
```

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
    --zone us-central1-f --tags http-server
```

This will return a read out like
```
Created [https://www.googleapis.com/compute/v1/projects/level-elevator-666/zones/us-central1-f/instances/planemo].
NAME    ZONE          MACHINE_TYPE  INTERNAL_IP    EXTERNAL_IP    STATUS
planemo us-central1-f n1-standard-2 10.240.143.115 162.222.182.19 RUNNING

```

Now if you navigate to the listed EXTERNAL_IP, you will find the running Planemo-Machine

>If you go to the web page and you see an error that 'an internal server error' has occured, and the message doesn't go away, you can restart the server by sshing into the server and issuing the command `sudo supervisorctl restart galaxy:`

To SSH into the machine use (where planemo is the name of the instance you provided earlier and
the instance was started in us-central1-f)
```
gcloud compute ssh --zone us-central1-f ubuntu@planemo
```

>Remember when you are done using your VM, turn it off. You are changed for every hour it is on, and if you forget about it, it will rack up costs quickly.

To deploy via the web interface
-------------------------------
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

To Attach Additional Storage to you GCE VM
------------------------------------------
You can create a volume to attach to your machine with the command
```
gcloud compute disks create --size 30GB --zone us-central1-f planemo-data
```

Then attach the disk to your instance
```
gcloud compute instances attach-disk --zone us-central1-f --disk planemo-data planemo
```
After the disk is attached to the instance, it will be available to be mounted.

Updating Planemo Image
----------------------

If there is a need to update the SDK image, usually because bug fixes or new features, you will need to create a new VM based on a fresh image download.

> Please Note: if you upgrade your VM, please make sure that your work is stored at an external location. If you've followed the instructions to attach additional storage to your machine, make sure that your work is storage on the external volume. If you create a new VM without transferring your work, you may lose it.

When updating the image, you may want to get delete the older version. There is no need to keep an image if there is an instance running based on that image. Deleting the image isn't required if you are willing to pay for the extra storage space, and can manage the names of multiple images. In the previous instructions, we referred to the disk image as `planemo-machine-image`, but you could easily create a second image named `planemo-machine-image-v2`.

To delete the image
```
gcloud compute images delete planemo-machine-image
```

Then follow the instructions starting a new image. If you are keeping an older instance of the VM running, you will need to find a name. So you can replace `planemo` with `planemo-v2` in the instructions.
