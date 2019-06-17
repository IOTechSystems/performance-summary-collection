*** Settings ***
Documentation   Measure the response time
...             Measure the response time of ping API for each edgex service
...             Measure the execution time from creating event by device-virtual until export-distro send event to a MQTT broker
Library         Process
Suite Teardown  Shutdown EdgeX


*** Test Cases ***
Get footprint and CPU, memory usage
    Given EdgeX deployed
    When fetch footprint and CPU, memory usage
    Then show the summary table


*** Keywords ***
EdgeX deployed
    ${result} =   Run Process     docker-compose      up    -d   
    Log    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}	0

Shutdown EdgeX
    ${result}  Run Process   docker-compose  down 
    Log    ${result.stderr}
    Should Be Equal As Integers	     ${result.rc}	0

Fetch footprint and CPU, memory usage
    Log    "Fetch footprint and CPU, memory usage"

Show the summary table
    Log    "show the summary"