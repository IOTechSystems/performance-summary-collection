*** Settings ***
Documentation   Measure the event exported time
Library         ../lib/EdgeX.py
Library         ../lib/EventExportedTime.py
Suite Setup  EdgeX is deployed with compose file    docker-compose-mqtt.yml
Suite Teardown  Shutdown EdgeX with compose file    docker-compose-mqtt.yml

*** Test Cases ***
Measure the event exported time
    Given mark pushed config is enable
    And export registration is added
    When query event
    Then fetch the exported time
    And show the summary table