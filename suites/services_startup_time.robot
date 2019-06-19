*** Settings ***
Documentation   Measure the startup time for starting all services at once
...             Get service start up time ,total time with creating containers
...             Get service start up time ,total time without creating containers
Library         Process
Library         ../lib/EdgeX.py
Library         ../lib/ServiceStartupTime.py
Suite Teardown  Shutdown EdgeX

*** Test Cases ***
Get service start up time ,total time with creating containers
    Given Start time is recorded
    And EdgeX is deployed
    When fetch services start up time and total time
    Then show the summary table
    [Teardown]  Stop EdgeX

Get service start up time ,total time without creating containers
    Given Start time is recorded
    And EdgeX is deployed
    When fetch services start up time and total time without creating containers
    Then show the summary table2
    [Teardown]  Stop EdgeX

Show comparison tables for start up time with/without creating containers
    show the comparison table
