*** Settings ***
Library         Process
Documentation   This suite used for pulling all required docker image,
...             Only execute at initialization.


*** Test Cases ***
Should pull all required docker image
    Given we need to pull the EdgeX docker images
    When pull the docker images
    Then return the success code 0


*** Keywords ***
We need to pull the EdgeX docker images
    Log    "Start to pull image ..."

Pull the docker images
    ${result}  Run Process   docker-compose  pull 
    Log    ${result.stderr}
    Set Test Variable  ${RESULT_CODE}    ${result.rc}

Then return the success code ${code}
    Should Be Equal As Integers    ${RESULT_CODE}    ${code}
