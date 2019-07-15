*** Settings ***
Documentation   Measure the ping response time
...             Measure the ping response time of ping API for each edgex service
...             Measure the ping execution time from creating event by device-virtual until export-distro send event to a MQTT broker
Library         REST
Library         ../lib/EdgeX.py
Library         ../lib/PingResponse.py
Suite Setup  EdgeX is deployed
Suite Teardown  Shutdown EdgeX

*** Test Cases ***
Measure the ping response time of ping API for each edgex service
    ${res} =    GET   http://localhost:48080/api/v1/ping        headers={ "Accept": "text/plain" }
    Record response   edgex-core-data        ${res}

    ${res} =    GET   http://localhost:48081/api/v1/ping        headers={ "Accept": "text/plain" }
    Record response   edgex-core-metadata        ${res}

    ${res} =    GET   http://localhost:48082/api/v1/ping        headers={ "Accept": "text/plain" }
    Record response   edgex-core-command        ${res}

    ${res} =    GET   http://localhost:48085/api/v1/ping        headers={ "Accept": "text/plain" }
    Record response   edgex-support-scheduler        ${res}

    ${res} =    GET   http://localhost:48061/api/v1/ping        headers={ "Accept": "text/plain" }
    Record response   edgex-support-logging        ${res}

    ${res} =    GET   http://localhost:48060/api/v1/ping        headers={ "Accept": "text/plain" }
    Record response   edgex-support-notifications        ${res}

    ${res} =    GET   http://localhost:48071/api/v1/ping        headers={ "Accept": "text/plain" }
    Record response   edgex-export-client        ${res}

    ${res} =    GET   http://localhost:48070/api/v1/ping        headers={ "Accept": "text/plain" }
    Record response   edgex-export-distro        ${res}

    ${res} =    GET   http://localhost:49990/api/v1/ping        headers={ "Accept": "text/plain" }
    Record response   edgex-device-virtual        ${res}

    Then show the summary table