*** Settings ***
Resource    ../pages_layer/login_page.robot

*** Keywords ***
User Login With Username And Password
    [Arguments]    ${base_url}    ${username}    ${password}
    Open Login Page                 ${base_url}
    Login Page Input Credentials    ${username}    ${password}
    Login Page Submit


