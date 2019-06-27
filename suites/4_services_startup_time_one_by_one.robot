*** Settings ***
Documentation   Measure the startup time for starting services one by one
...             Get service start up time with creating containers
...             Get service start up time without creating containers
#Library         ../lib/EdgeX.py
#Library         ../lib/ServiceStartupTime.py

#*** Test Cases ***
#Get core-data start up with creating containers
#    Given dependecy services are deployed     mongo     logging
#    And start time is recorded
#    When deploy service      data
#    Then fetch statup time from service     edgex-core-data
#    [Teardown]  Stop EdgeX
#
#Get core-data start up without creating containers
#    Given dependecy services are deployed     mongo     logging
#    And start time is recorded
#    When deploy service      data
#    Then fetch statup time from service     edgex-core-data
#    [Teardown]  Shutdown EdgeX