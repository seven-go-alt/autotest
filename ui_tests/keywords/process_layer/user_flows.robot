*** Settings ***
Resource    ../pages_layer/login_page.robot

*** Keywords ***
用户使用账号密码登录
    [Documentation]    流程层关键字：完整的用户登录流程
    [Arguments]    ${base_url}    ${username}    ${password}
    打开登录页面                 ${base_url}
    登录页面输入用户名和密码    ${username}    ${password}
    登录页面点击登录按钮


