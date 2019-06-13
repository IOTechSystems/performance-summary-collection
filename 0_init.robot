*** Settings ***
Library         Process
Documentation   This suite used for pulling all required docker image,
...             Only execute at initialization.


*** Test Cases ***
Pull all required docker image
    # @{output}   Run And Return Rc And Output   docker-compose up
    
    ${result}   Run Process   docker-compose    pull
    Log    ${result.stderr}
    Log    ${result.rc}
    Should Be Equal As Integers     ${result.rc}	0