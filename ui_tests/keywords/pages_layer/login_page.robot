*** Settings ***
Library    SeleniumLibrary
Resource   ../function_layer/web_functions.robot

*** Keywords ***
Open Login Page
    [Arguments]    ${base_url}
    Open Login Page    ${base_url}

Login Page Input Credentials
    [Arguments]    ${username}    ${password}
    Input Login Credentials    ${username}    ${password}

Login Page Submit
    Click Login Button


