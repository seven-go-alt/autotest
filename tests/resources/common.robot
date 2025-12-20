*** Settings ***
Documentation    通用资源文件
Library           SeleniumLibrary
Library           ../../utils/robot_custom_library.py    WITH NAME    PlayLib

*** Keywords ***
使用 Selenium 登录
    [Arguments]    ${base_url}    ${username}    ${password}
    Open Browser    ${base_url}    chrome
    Maximize Browser Window
    Wait Until Element Is Visible    id=user-name    timeout=10s
    Input Text    id=user-name    ${username}
    Input Text    id=password     ${password}
    Click Button    id=login-button

*** Keywords ***
打开 Playwright 浏览器
    [Arguments]    ${url}    ${headless}=True
    PlayLib.Open Playwright Browser    headless=${headless}
    PlayLib.Go To    ${url}

关闭 Playwright 浏览器
    PlayLib.Close Playwright Browser

Playwright 登录
    [Arguments]    ${base_url}    ${username}    ${password}
    PlayLib.Open Playwright Browser    headless=True
    PlayLib.Go To    ${base_url}
    PlayLib.Wait For Selector    css=input#user-name    timeout=15
    PlayLib.Input Text    css=input#user-name    ${username}
    PlayLib.Input Text    css=input#password    ${password}
    PlayLib.Click    css=button#login-button

