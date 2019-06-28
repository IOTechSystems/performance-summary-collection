*** Settings ***
Documentation   Measure the startup time for starting all services(exclude ruleengine) at once
...             Get service start up time ,total time with creating containers
...             Get service start up time ,total time without creating containers
Library         Process
Library         ../lib/EdgeX.py
Library         ../lib/AllServicesStartupAtOnce.py
Suite Teardown  Shutdown EdgeX

*** Test Cases ***
Get service start up time ,total time with creating containers
    Given Start time is recorded
    When EdgeX is deployed exclude ruleengine
    Then fetch services start up time and total time exclude ruleengine
    [Teardown]  Stop EdgeX

Get service start up time ,total time without creating containers
    Given Start time is recorded
    When EdgeX is deployed exclude ruleengine
    Then fetch services start up time and total time without creating containers exclude ruleengine
    [Teardown]  Stop EdgeX

Show comparison tables for start up time with/without creating containers
    show the comparison table for exclude ruleengine case
