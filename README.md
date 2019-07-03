# performance-summary-collection
Use Robot framework to collect performance summary

## Prerequisites

* Install docker
* Clone repo
    ```
    $ git clone git@github.com:IOTechSystems/performance-summary-collection.git
    ```
    
## Run Robot Test suites

### Run Robot Test suites on x86_64 machine 

```
$ cd /path/to/performance-summary-collection
$ docker run --rm --network host -v $PWD:$PWD -w $PWD -v /var/run/docker.sock:/var/run/docker.sock  \
    iotech-services.jfrog.io/robotframework_x86_64:1.0.0 -d report .

```

### Run Robot Test suites on arm64 machine 
```
$ cd /path/to/performance-summary-collection
$ docker run --rm --network host -v $PWD:$PWD -w $PWD -v /var/run/docker.sock:/var/run/docker.sock  \
    iotech-services.jfrog.io/robotframework_arm64:1.0.0 -d report .
```

Note:
On RasPi, please enable cgroup memory with following instruction, otherwise memory usage cann't found in `docker stats` command.
1. Add cgroup_enable=memory cgroup_memory=1 in /boot/cmdline.txt
2. Reboot
Refer to https://www.raspberrypi.org/forums/viewtopic.php?t=203128#p1262431

Similar issue: https://github.com/moby/moby/issues/18420


## For Development

* sudo apt install python3-pip
* python3 -m pip install robotframework

* python lib
  * pip3 install docker
  * pip3 install -U python-dotenv
  * pip3 install -U RESTinstance


### Run Robot

```
robot -d report .
```

### Run docker-compose in container

```
docker run --rm --env-file x86_64.env -v $PWD:$PWD -w $PWD -v /var/run/docker.sock:/var/run/docker.sock   \
    docker/compose:1.24.0 up -d
    
docker run --rm --env-file arm64.env -v $PWD:$PWD -w $PWD -v /var/run/docker.sock:/var/run/docker.sock   \
    edgexfoundry/compose_arm64:1.24.0 up -d
```


## Build robotframework docker image
```
docker build -t edgexfoundry/robotframework:1.0.0 .
```
