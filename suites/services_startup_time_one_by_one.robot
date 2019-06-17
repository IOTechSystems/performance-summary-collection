*** Settings ***
Documentation   Measure the startup time for starting each service one by one
...             Get service start up time with creating containers
...             Get service start up time without creating containers
Library         Process
Suite Teardown  Shutdown EdgeX

*** Test Cases ***
Get coreData service start up time with creating containers
    Given EdgeX is deployed
    When fetch services start up time and total time
    Then show the summary table
    [Teardown]  Stop EdgeX

Get coreData service start up time without creating containers
    Given EdgeX is deployed
    When fetch services start up time and total time
    Then show the summary table
    [Teardown]  Stop EdgeX

Get service start up time without creating containers
    Given EdgeX is started
    When fetch services start up time and total time
    Then show the summary table
    [Teardown]  Stop EdgeX

Show services startup summary
    Given EdgeX is started
    When fetch services start up time and total time
    Then show the summary table
    [Teardown]  Stop EdgeX

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
    ${result}  Run Process   docker-compose  down 
    Log    ${result.stderr}
    Should Be Equal As Integers	     ${result.rc}	0

Stop EdgeX
    ${result}  Run Process   docker-compose  stop 
    Log    ${result.stderr}
    Should Be Equal As Integers	     ${result.rc}	0



Fetch services start up time and total time
    Log    "Fetch services start up time and total time"

Show the summary table
    Log    "show the summary"