*** Settings ***
Documentation   Measure the startup time for starting all services at once
...             Get service start up time ,total time with creating containers
...             Get service start up time ,total time without creating containers
Library         ../lib/EdgeX.py
Library         ../lib/ServiceStartupTime.py
Suite Teardown  Shutdown EdgeX

*** Test Cases ***
Get service start up time ,total time with creating containers
    Given Start time is recorded
    When EdgeX is deployed
    Then fetch services start up time and total time
    [Teardown]  Stop EdgeX

Get service start up time ,total time without creating containers
    Given Start time is recorded
    When EdgeX is deployed
    Then fetch services start up time and total time without creating containers
    [Teardown]  Stop EdgeX

Show comparison tables for start up time with/without recreate containers
    show the comparison table
