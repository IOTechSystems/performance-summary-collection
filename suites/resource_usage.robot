*** Settings ***
Documentation   Get footprint and CPU, memory usage
...             Image Footprint:            Get docker image footprint of each edgex services
...             Executable Footprint:	    Copy service executable file from container to host and get the executable footprint of each edgex services
...             CPU used on start up:	    Start all services at once and get CPU usage of each edgex services on startup using "docker stats"
...             Memory used on start up: 	Start all services at once and get memory usage of each edgex services on startup using "docker stats"
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