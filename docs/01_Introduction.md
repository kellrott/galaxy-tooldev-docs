
Getting Started
===============

Planemo-Machine is a Galaxy Tool Standard Development Kit (SDK) designed to
make developing Docker based Galaxy tools easy. It has an installed copy of Galaxy,
an up to date version of Docker, a web based IDE and the Planemo tools.

With this system, which can be deployed on a variety of virtual machine services,
you can quickly develop and test new tools and see how they behave in the Galaxy environment.
To develop a Galaxy wrapped tool, the steps are:

1) Create a Docker container capable of running your tool

2) Write a Wrapper that describes your tools inputs, outputs and parameters.

3) Test the tool inside a Galaxy environment to debug issues


Before any development can happen, you must first deploy a Planemo-Machine in your VM
system of choice. The current deployment options are: Google Cloud Engine,
Virtual Box and Docker.


Vagrant Based Development
====================


The latest version of the planemo appliance can be found
at https://images.galaxyproject.org/planemo/latest.box. Once you have
installed Vagrant (download now at http://www.vagrantup.com/downloads),
the appliance can be enabled by first creating a `Vagrantfile` in your tool
directory - the following demonstrates an example of such file.

```
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "planemo"
  config.vm.box_url = "https://images.galaxyproject.org/planemo/latest.box"

  # Forward nginx.
  config.vm.network "forwarded_port", guest: 80, host: 8010

  # Disable default mount and mount pwd to /opt/galaxy/tools instead.
  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.vm.synced_folder ".", "/opt/galaxy/tools", owner: "vagrant"

end
```

This file must literally be named `Vagrantfile`. Next you will need to
startup the appliance. This is as easy as

```
vagrant up
```

From this point, you can point your webbrowser to http://localhost:8010/ to log into the
Galaxy server


To access the command line inside the virtual machine
```
vagrant ssh
```

You can get change to the tool directory with
```
cd /opt/galaxy/tools
```

Google Cloud Engine based Deployment
====================================

For GCE Based SDK first Install [Google Cloud SDK](https://developers.google.com/cloud/sdk/) on your local machine.

This section will help you set up a compute instance and a persistent disk containing challenge data. For most steps, you can choose to use either the Developers Console web interface or the Google Cloud SDK command line tools ("gcutil" and "gsutil"). [This page](https://developers.google.com/compute/docs/console) is a good short intro/summary of how to use the console:

The main steps in this procedure are:

1) create a persistent disk big enough to hold the data
2) create an instance and attach the disk
3) mount and format the disk
4) copy data to the disk

To start up the Planemo Machine under GCE:

If you haven't already done it, run the Google Cloud SDK login
```
gcloud auth login
```

Load the image into your account, replace YOUR-PROJECT-NAME with the Google cloud project
that you want to run the VM inside of
```
gcutil --project="YOUR-PROJECT-NAME" addimage planemo-machine-image http://storage.googleapis.com/galaxyproject_images/planemo_machine.image.tar.gz
```

To deploy via the web interface
-------------------------------
1) Go to your console at https://console.developers.google.com
2) Select the project you want to deploy under
3) Under the left hand menu, select Compute -> Compute Engine -> VM Instances
4) If a dialog pops up asking what you want to do, select 'Create Instance', otherwise click the
'New Instance' button
5) Fill out the instance creation dialog, this will include
5.1) Set the name
5.2) Allow HTTP and HTTPS traffic
5.3) Select the Zone you want to deploy in
5.4) Select the machine type of choice, a system with at least 6GB of RAM is expected
5.5) For the Boot Disk, Select 'New Disk From Image'
5.6) For the image, Select 'planemo-machine-image'
6) Hit Create
7) To see your instance list, navigate back to Compute -> Compute Engine -> VM Instances
8) If you click the IP address for the instance you should be directed the the home page of you newly
create Galaxy SDK instance


To deploy via command line interface
------------------------------------
From there start up a server
```
gcutil launch image <- please fix this
```

Docker based Development
========================

Please note: Docker based deployment requires the user to install and run docker
well as setup 'Docker-By-Docker' deployment, so it is considered an option only for
'advanced users'

Download the most update SDK docker image
```
docker pull planemo/box
```

Deploy SDK
```
docker run -v `pwd`:/opt/galaxy/tools -v /var/run/docker.sock:/var/run/docker.sock -p 8010:80 -e GALAXY_DOCKER_ENABLED=true -e GALAXY_DOCKER_SUDO=true -e GALAXY_DOCKER_VOLUMES_FROM=planemo --name planemo planemo/box
```

Note: If you get the error message
```
FATA[0000] Error response from daemon: Conflict, The name planemo is already assigned to 0109fd956412. You have to delete (or rename) that container to be able to assign planemo to a container again.

```

You can either restart the server with
```
docker start -a planemo
```

Or delete the server before starting again
```
docker rm -v planemo
```

Obtain a command line inside the
```
docker exec -i -t planemo /bin/bash
```
