

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



When updating the image, you may want to get delete the older version. There is no need to keep an image if there is an instance running based on that image. Deleting the image isn't required if you are willing to pay for the extra storage space, and can manage the names of multiple images. In the previous instructions, we referred to the disk image as `planemo-machine-image`, but you could easily create a second image named `planemo-machine-image-v2`.

To delete the image
```
gcloud compute images delete planemo-machine-image
```



> Please Note: if you upgrade your VM, please make sure that your work is stored at an external location. If you've followed the instructions to attach additional storage to your machine, make sure that your work is storage on the external volume. If you create a new VM without transferring your work, you may lose it.
