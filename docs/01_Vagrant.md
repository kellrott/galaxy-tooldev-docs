

Vagrant Based Development
========================

As an alternative to the Google Cloud based development kit, it is possible to run the Planemo SDK on your personal machine. For the purposes of the SMC-Het challenge, we provide this as an alternative but encourage contestants to use Google Cloud VMs and take advantage of the free compute credits provided.

> For this to work you'll need to install both [VirtualBox](https://www.virtualbox.org/) and [Vagrant](https://www.vagrantup.com/). And note, building a new VM may take some time.

The latest version of the planemo appliance can be found at https://images.galaxyproject.org/planemo/latest.box. Once you have installed Vagrant (download now at http://www.vagrantup.com/downloads), the appliance can be enabled by first creating a `Vagrantfile` in your tool directory - the following demonstrates an example of such file.

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

This file must literally be named `Vagrantfile`. Next you will need to startup the appliance. This is as easy as

```
vagrant up
```

From this point, you can point your webbrowser to http://localhost:8010/ to log into the Galaxy server


To access the command line inside the virtual machine
```
vagrant ssh
```

You can get change to the tool directory with
```
cd /opt/galaxy/tools
```
