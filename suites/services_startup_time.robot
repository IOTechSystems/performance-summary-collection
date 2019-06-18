*** Settings ***
Documentation   Measure the startup time for starting all services at once
...             Get service start up time ,total time with creating containers
...             Get service start up time ,total time without creating containers
Library         Process
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

*** Keywords ***
Deploy EdgeX
    ${result} =   Run Process     docker-compose      up    -d   
    Log    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}	0

EdgeX is deployed
    Deploy EdgeX

EdgeX is started
    Deploy EdgeX

Shutdown EdgeX
    ${result}      Run Process   docker-compose  down 
    Log    ${result.stdout}
    Log    ${result.stderr}
    Should Be Equal As Integers	     ${result.rc}	0

Stop EdgeX
    ${result}       Run Process   docker-compose  stop 
    Log    ${result.stderr}
    Should Be Equal As Integers	     ${result.rc}	0
