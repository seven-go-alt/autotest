*** Settings ***
Library    SeleniumLibrary

*** Keywords ***
Open Login Page
    [Arguments]    ${base_url}
    Open Browser    ${base_url}/    ${BROWSER}
    Maximize Browser Window

Input Login Credentials
    [Arguments]    ${username}    ${password}
    Input Text    id=user-name    ${username}
    Input Text    id=password     ${password}

Click Login Button
    Click Button    id=login-button


