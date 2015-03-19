

Google Cloud Engine based Deployment
====================================

For GCE Based SDK first Install [Google Cloud SDK](https://developers.google.com/cloud/sdk/) on your local machine.

This section will help you set up a compute instance and a persistent disk containing challenge data. For most steps, you can choose to use either the Developers Console web interface or the Google Cloud SDK command line tools ("gcutil" and "gsutil"). [This page](https://developers.google.com/compute/docs/console) is a good short intro/summary of how to use the console:

The main steps in this procedure are:

1. create a persistent disk big enough to hold the data
2. create an instance and attach the disk
3. mount and format the disk
4. copy data to the disk

First go to https://console.developers.google.com to view your projects, and obtain
your project id.

> Every GCE project has a name and an ID. You can assign the name yourself,
> but the ID will be assigned automatically by GCE.


To start up the Planemo Machine under GCE:
------------------------------------------

If you haven't already done it, run the Google Cloud SDK login
```
gcloud auth login
```

Load the image into your account, replace YOUR-PROJECT-ID with the Google cloud project
that you want to run the VM inside of
```
gcutil --project="YOUR-PROJECT-ID" addimage planemo-machine-image http://storage.googleapis.com/galaxyproject_images/planemo_machine.image.tar.gz
```

To deply via command line interface
```
user@ubuntu:~$ gcloud compute instances create planemo --machine-type n1-standard-2 --image planemo-machine-image --zone us-central1-f --tags http-server
Created [https://www.googleapis.com/compute/v1/projects/level-elevator-666/zones/us-central1-f/instances/planemo].
NAME    ZONE          MACHINE_TYPE  INTERNAL_IP    EXTERNAL_IP    STATUS
planemo us-central1-f n1-standard-2 10.240.143.115 162.222.182.19 RUNNING

```


Now if you navigate to the listed EXTERNAL_IP, you will find the running Planemo-Machine
If you go to the web page and you see an error that 'an internal server error' has occured, and the
message doesn't go away, you can restart the server by sshing into the server and issuing the command
```
sudo supervisorctl restart galaxy:
```

To SSH into the machine use (where planemo is the name of the instance you provided earlier and
the instance was started in us-central1-f)
```
gcloud compute ssh --zone us-central1-f ubuntu@planemo
```

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


> And remember when you are done using your VM, turn it off. You are changed for every
> hour it is on, and if you forget about it, it will rack up costs quickly.
