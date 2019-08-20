*** Settings ***
Documentation   Get footprint and CPU, memory usage
...             Image Footprint:            Get docker image footprint of each edgex services
...             Executable Footprint:	    Copy service executable file from container to host and get the executable footprint of each edgex services
...             CPU used at startup:	    Start all services at once and get CPU usage of each edgex services on startup using "docker stats"
...             Memory used at startup: 	Start all services at once and get memory usage of each edgex services on startup using "docker stats"
Library         Process
Library         ../lib/EdgeX.py
Library         ../lib/ResourceUsage.py


*** Test Cases ***
Get footprint and CPU, memory usage
    Given EdgeX is deployed
    When fetch footprint cpu memory
    Then show the summary table
    And Shutdown EdgeX

Get footprint and CPU, memory usage (redis, no security)
    Given EdgeX with redis is deployed no secty
    When fetch footprint cpu memory with redis
    Then show the summary table with redis
    And Shutdown EdgeX Redis
