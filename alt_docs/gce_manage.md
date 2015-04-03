

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






> Please Note: if you upgrade your VM, please make sure that your work is stored at an external location. If you've followed the instructions to attach additional storage to your machine, make sure that your work is storage on the external volume. If you create a new VM without transferring your work, you may lose it.
