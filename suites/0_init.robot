*** Settings ***
Documentation   This suite used for pulling all required docker image,
...             Only execute at initialization.
Library         ../lib/EdgeX.py

*** Test Cases ***
Should pull all required docker image
   Pull the EdgeX docker images
