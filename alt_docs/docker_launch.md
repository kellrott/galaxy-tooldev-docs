

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
