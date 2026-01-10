*** Settings ***
Library    SeleniumLibrary

*** Keywords ***
Open Login Page
    [Documentation]    函数层关键字：打开浏览器并导航到登录页面
    [Arguments]    ${base_url}
    Open Browser    ${base_url}    ${BROWSER}
    Maximize Browser Window

Input Login Credentials
    [Documentation]    函数层关键字：输入登录凭证（用户名和密码）
    [Arguments]    ${username}    ${password}
    SeleniumLibrary.Input Text    id=user-name    ${username}
    SeleniumLibrary.Input Text    id=password     ${password}

Click Login Button
    [Documentation]    函数层关键字：点击登录按钮
    SeleniumLibrary.Click Button    id=login-button


