*** Settings ***
Documentation   Measure the event exported time
Library         ../lib/EdgeX.py
Library         ../lib/EventExportedTime.py

*** Test Cases ***
Measure the event exported time
    [Setup]  EdgeX is deployed with compose file  docker-compose-export-service.yml
    Given mark pushed config is enable
    And export registration is added
    When query event
    Then fetch the exported time
    And show the summary table  EXPORT-CLIENT
    [Teardown]  Shutdown EdgeX with compose file  docker-compose-export-service.yml

Measure the event exported time using app-service
    [Setup]  EdgeX is deployed with compose file    docker-compose-app-service.yml
    When query event
    Then fetch the exported time
    And show the summary table  APP-SERVICE-MQTT-EXPORT
    [Teardown]  Shutdown EdgeX with compose file    docker-compose-app-service.yml
