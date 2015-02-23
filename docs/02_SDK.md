

For GCE Based SDK

Install [Google Cloud SDK](https://developers.google.com/cloud/sdk/) on your local machine.



For Virtual Box Based SDK
=========================


The latest version`Vagrant`_ version of the planemo appliance can be found
`here <https://images.galaxyproject.org/planemo/latest.box>`_. Once you have
installed `Vagrant`_ (`download now <http://www.vagrantup.com/downloads>`_),
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

  # config.vm.provider "virtualbox" do |vb|
  #   # Don't boot with headless mode
  #   vb.gui = true
  #
  #   # Use VBoxManage to customize the VM. For example to change memory:
  #   vb.customize ["modifyvm", :id, "--memory", "1024"]
  # end
end
```

This file must literally be named ``Vagrantfile``. Next you will need to
startup the appliance. This is as easy as

::

    vagrant up
