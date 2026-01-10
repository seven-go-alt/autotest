*** Settings ***
Library    SeleniumLibrary
Resource   ../function_layer/web_functions.robot

*** Keywords ***
打开登录页面
    [Documentation]    页面层关键字：打开登录页面
    [Arguments]    ${base_url}
    Open Login Page    ${base_url}

登录页面输入用户名和密码
    [Documentation]    页面层关键字：在登录页面输入用户名和密码
    [Arguments]    ${username}    ${password}
    Input Login Credentials    ${username}    ${password}

登录页面点击登录按钮
    [Documentation]    页面层关键字：点击登录按钮
    Click Login Button


