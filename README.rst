###############################
performance-summary-collection
###############################

The project purpose is collect EdgeX performance data.

* Footprint, CPU, memory usage
* EdgeX startup time
* API latency

===========================
Test Environment Structure
===========================
This project has following execution steps:

* Put this project into the target test machine
* Run the automation script executor by docker.
* The automation script executor will deploy required services and collect the data or execute test.

    .. image:: doc/env-structure.png
        :scale: 50%
        :alt: env-structure

==========================
Automation script executor
==========================
After comparing different test framework, we choose the Robotframwork https://robotframework.org/ as our automation script executor.

* readable test case
* great test report
* community support

==============
Prerequisites
==============

* Install docker on the test machine
* Clone repo

.. code-block::

    $ git clone git@github.com:IOTechSystems/performance-summary-collection.git



======================
Project Folder Content
======================
.. code-block::

    performance-summary-collection
    ├── Dockerfile
    ├── robot-entrypoint.sh
    ├── Jenkinsfile
    ├── README.md
    ├── x86_64.env
    ├── arm64.env
    ├── arm.env
    ├── docker-compose.yml
    ├── docker-compose-exclude-ruleengine.yml
    ├── lib
    │   ├── AllServicesStartupAtOnce.py
    │   ├── AllServicesStartupOneByOne.py
    │   ├── EdgeX.py
    │   ├── ...
    ├── suites
    │   ├── 0_init.robot
    │   ├── 1_resource_usage.robot
    │   ├── 2_services_startup_time.robot
    │   ├── ...

* **x86_64.env, arm64.env, arm.env:** project settings for different system architecture.
* **docker-compose.yml** used to deploy EdgeX by docker-compose command
* **docker-compose-exclude-ruleengine.yml** used to deploy EdgeX without rulesengines by docker-compose command
* **lib:** python scripts
* **suites:** test suites
* **Dockerfile, robot-entrypoint.sh:** these two files are used for building robotframework docker image.

========
Settings
========
.. code-block::

    waitTime=5
    retryFetchStartupTimes=20

    compose=docker/compose:1.24.0

    volume=nexus3.edgexfoundry.org:10004/docker-edgex-volume:1.0.0
    consul=consul:1.3.1
    configSeed=nexus3.edgexfoundry.org:10004/docker-core-config-seed-go:1.0.0
    mongo=nexus3.edgexfoundry.org:10004/docker-edgex-mongo:1.0.0

    coreData=nexus3.edgexfoundry.org:10004/docker-core-data-go:1.0.0
    coreMetadata=nexus3.edgexfoundry.org:10004/docker-core-metadata-go:1.0.0
    coreCommand=nexus3.edgexfoundry.org:10004/docker-core-command-go:1.0.0

    supportLogging=nexus3.edgexfoundry.org:10004/docker-support-logging-go:1.0.0
    supportNotifications=nexus3.edgexfoundry.org:10004/docker-support-notifications-go:1.0.0
    supportScheduler=nexus3.edgexfoundry.org:10004/docker-support-scheduler-go:1.0.0
    supportRulesengine=nexus3.edgexfoundry.org:10004/docker-support-rulesengine:1.0.0

    exportClient=nexus3.edgexfoundry.org:10004/docker-export-client-go:1.0.0
    exportDistro=nexus3.edgexfoundry.org:10004/docker-export-distro-go:1.0.0
    deviceVirtual=nexus3.edgexfoundry.org:10004/docker-device-virtual-go:1.0.0

After deploying the required service, these service still take some time to initialize, so we try to ping the services to make sure they are all startup.

* waitTime: if fail to ping the service and then take some time to wait the service startup and ping again
* retryFetchStartupTimes: the maximum number of times we try to ping the services

compose, volume, consul, ...: docker image name


Why use compose tool in docker container?
=========================================
Because compose didn't release for any kind of system architecture, see https://github.com/docker/compose/releases

So we build the compose docker image with https://github.com/docker/compose/blob/master/Dockerfile for running on any kind of os.


======================
Run with Test Suites
======================


Run on x86_64 machine
======================
.. code-block::

    $ cd /path/to/performance-summary-collection
    $ docker run --rm --network host -v $PWD:$PWD -w $PWD -v /var/run/docker.sock:/var/run/docker.sock  \
        iotech-releases.jfrog.io/robotframework-x86_64:1.0.0 -d report .

Run on arm64 machine
======================
.. code-block::

    $ cd /path/to/performance-summary-collection
    $ docker run --rm --network host -v $PWD:$PWD -w $PWD -v /var/run/docker.sock:/var/run/docker.sock  \
        iotech-releases.jfrog.io/robotframework-arm64:1.0.0 -d report .

After finishing the test, you can see the generated report under the **/path/to/performance-summary-collection/report**

Please open report/log.html to see the summary report, We create a "summary" test suite to gather all test result.

    .. image:: doc/report-log.png
        :scale: 50%
        :alt: report-log


Memory usage issue
------------------
We collect the CPU, memory usage by docker client sdk, the result just same as docker stats command. But in some environment, the memory usage is zero.

In RasPi case, please enable cgroup memory with following instruction.

* Add cgroup_enable=memory cgroup_memory=1 in /boot/cmdline.txt
* Reboot

This solution is refer to https://www.raspberrypi.org/forums/viewtopic.php?t=203128#p1262431

Similar issue: https://github.com/moby/moby/issues/18420

================
For Development
================

Install robotframework and dependency lib:

* sudo apt install python3-pip
* python3 -m pip install robotframework
* python lib
    * pip3 install docker
    * pip3 install -U python-dotenv
    * pip3 install -U RESTinstance

Run Robot
==========
.. code-block::

    robot -d report .


Run docker-compose in container
===============================
.. code-block::

    docker run --rm --env-file x86_64.env -v $PWD:$PWD -w $PWD -v /var/run/docker.sock:/var/run/docker.sock   \
        docker/compose:1.24.0 up -d



Build robotframework docker image
=================================
.. code-block::

    docker build -t edgexfoundry/robotframework:1.0.0 .
