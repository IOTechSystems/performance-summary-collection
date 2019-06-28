*** Settings ***
Documentation   Measure the startup time for starting services one by one
...             Get service startup time with creating containers
...             Get service startup time without creating containers
Library         ../lib/EdgeX.py
Library         ../lib/AllServicesStartupOneByOne.py


*** Test Cases ***
Get core-data start up with creating containers
    Given dependecy services are deployed       support-logging
    And start time is recorded
    When deploy service      core-data
    Then fetch startup time from service     core-data
    [Teardown]  Stop EdgeX

Get core-data start up without creating containers
    Given dependecy services are deployed     support-logging
    And start time is recorded
    When deploy service      core-data
    Then fetch startup time from service without recreate     core-data
    [Teardown]  Shutdown EdgeX

Get core-metadata start up with creating containers
    Given dependecy services are deployed       support-logging
    And start time is recorded
    When deploy service      core-metadata
    Then fetch startup time from service     core-metadata
    [Teardown]  Stop EdgeX

Get core-metadata start up without creating containers
    Given dependecy services are deployed     support-logging
    And start time is recorded
    When deploy service      core-metadata
    Then fetch startup time from service without recreate     core-metadata
    [Teardown]  Shutdown EdgeX

Get core-command start up with creating containers
    Given dependecy services are deployed       support-logging     core-metadata
    And start time is recorded
    When deploy service      core-command
    Then fetch startup time from service     core-command
    [Teardown]  Stop EdgeX

Get core-command start up without creating containers
    Given dependecy services are deployed     support-logging       core-metadata
    And start time is recorded
    When deploy service      core-command
    Then fetch startup time from service without recreate     core-command
    [Teardown]  Shutdown EdgeX

Get support-logging start up with creating containers
    Given dependecy services are deployed
    And start time is recorded
    When deploy service      support-logging
    Then fetch startup time from service     support-logging
    [Teardown]  Stop EdgeX

Get support-logging start up without creating containers
    Given dependecy services are deployed
    And start time is recorded
    When deploy service      support-logging
    Then fetch startup time from service without recreate     support-logging
    [Teardown]  Shutdown EdgeX

Get support-notifications start up with creating containers
    Given dependecy services are deployed       support-logging
    And start time is recorded
    When deploy service      support-notifications
    Then fetch startup time from service     support-notifications
    [Teardown]  Stop EdgeX

Get support-notifications start up without creating containers
    Given dependecy services are deployed       support-logging
    And start time is recorded
    When deploy service      support-notifications
    Then fetch startup time from service without recreate     support-notifications
    [Teardown]  Shutdown EdgeX

Get support-scheduler start up with creating containers
    Given dependecy services are deployed       support-logging
    And start time is recorded
    When deploy service      support-scheduler
    Then fetch startup time from service     support-scheduler
    [Teardown]  Stop EdgeX

Get support-scheduler start up without creating containers
    Given dependecy services are deployed       support-logging
    And start time is recorded
    When deploy service      support-scheduler
    Then fetch startup time from service without recreate     support-scheduler
    [Teardown]  Shutdown EdgeX

Get support-rulesengine start up with creating containers
    Given dependecy services are deployed       support-logging     core-data       export-client
    And start time is recorded
    When deploy service      support-rulesengine
    Then fetch startup time from service     support-rulesengine
    [Teardown]  Stop EdgeX

Get support-rulesengine start up without creating containers
    Given dependecy services are deployed       support-logging     core-data       export-client
    And start time is recorded
    When deploy service      support-rulesengine
    Then fetch startup time from service without recreate     support-rulesengine
    [Teardown]  Shutdown EdgeX

Get export-client start up with creating containers
    Given dependecy services are deployed       support-logging     core-data
    And start time is recorded
    When deploy service      export-client
    Then fetch startup time from service     export-client
    [Teardown]  Stop EdgeX

Get export-client start up without creating containers
    Given dependecy services are deployed       support-logging     core-data
    And start time is recorded
    When deploy service      export-client
    Then fetch startup time from service without recreate     export-client
    [Teardown]  Shutdown EdgeX

Get export-distro start up with creating containers
    Given dependecy services are deployed       support-logging     core-data       export-client
    And start time is recorded
    When deploy service      export-distro
    Then fetch startup time from service     export-distro
    [Teardown]  Stop EdgeX

Get export-distro start up without creating containers
    Given dependecy services are deployed       support-logging     core-data       export-client
    And start time is recorded
    When deploy service      export-distro
    Then fetch startup time from service without recreate     export-distro
    [Teardown]  Shutdown EdgeX

Get device-virtual start up with creating containers
    Given dependecy services are deployed       support-logging     core-data       core-metadata       core-command
    And start time is recorded
    When deploy service      device-virtual
    Then fetch startup time from service     device-virtual
    [Teardown]  Stop EdgeX

Get device-virtual start up without creating containers
    Given dependecy services are deployed       support-logging     core-data       core-metadata       core-command
    And start time is recorded
    When deploy service      device-virtual
    Then fetch startup time from service without recreate     device-virtual
    [Teardown]  Shutdown EdgeX

Show comparison tables for startup time with/without recreate containers
    show the comparison table