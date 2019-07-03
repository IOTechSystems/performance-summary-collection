*** Settings ***
Documentation   Measure the startup time for starting all services at once
...             Get service start up time ,total time with creating containers
...             Get service start up time ,total time without creating containers
Library         ../lib/EdgeX.py
Library         ../lib/AllServicesStartupAtOnce.py
Suite Teardown  Shutdown EdgeX

*** Test Cases ***
Get service startup time ,total time with creating containers
    Given Start time is recorded
    When EdgeX is deployed
    Then fetch services start up time and total time
    [Teardown]  Stop EdgeX

Get service startup time ,total time without creating containers
    Given Start time is recorded
    When EdgeX is deployed
    Then fetch services start up time and total time without creating containers
    [Teardown]  Stop EdgeX

Show comparison tables for startup time with/without recreate containers
    show the comparison table
