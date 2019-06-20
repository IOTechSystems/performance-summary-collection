# performance-summary-collection
Use Robot framework to collect performance summary

Report
https://docs.google.com/spreadsheets/d/1ZBQvbFf-XwXcSfcFe7g5coys9hNsWMG7d1ja-UbdB2A/edit#gid=0
Test case
https://docs.google.com/spreadsheets/d/1ScN7urohtlbwL9ns-5rSxjRy5hIL3j3Jr4eyLeD000w/edit#gid=0


## Install

* docker, docker-compose
* Robot framework https://github.com/robotframework/robotframework/blob/master/INSTALL.rst

* python lib
  * pip install docker
  * pip install pytz


## Run Robot

```
git clone git@github.com:IOTechSystems/performance-summary-collection.git

cd /path/to/performance-summary-collection
robot -d report .
```