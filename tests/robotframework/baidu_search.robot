*** Settings ***
Documentation    SauceDemo 登录与购物流程示例
Library           SeleniumLibrary
Library           ../../utils/robot_custom_library.py    WITH NAME    PlayLib
Resource          ../resources/common.robot

*** Variables ***
${BASE_URL}       https://www.saucedemo.com/
${STANDARD_USER}    standard_user
${LOCKED_USER}      locked_out_user
${PASSWORD}         secret_sauce
${FIRST_NAME}       Auto
${LAST_NAME}        Tester
${POSTAL_CODE}      12345

*** Test Cases ***
SauceDemo 登录并查看商品 - Selenium
    [Documentation]    使用 Selenium 登录并验证商品列表
    [Tags]    selenium    smoke
    Open Browser    ${BASE_URL}    chrome
    Maximize Browser Window
    Wait Until Element Is Visible    id=user-name    timeout=10s
    Input Text      id=user-name    ${STANDARD_USER}
    Input Text      id=password     ${PASSWORD}
    Click Button    id=login-button
    Wait Until Page Contains Element    css:.inventory_list    timeout=10s
    Page Should Contain Element    css:button[data-test="add-to-cart-sauce-labs-backpack"]
    Close Browser

SauceDemo 登录并下单 - Playwright
    [Documentation]    使用 Playwright（自定义关键字）登录并执行结账流程
    [Tags]    playwright    smoke
    Open Playwright Browser    headless=True    browser_name=chromium
    Go To    ${BASE_URL}
    Wait For Selector    css=input#user-name    timeout=15
    Input Text    css=input#user-name    ${STANDARD_USER}
    Input Text    css=input#password     ${PASSWORD}
    Click    css=button#login-button
    Wait For Selector    css=.inventory_list    timeout=15
    Click    css=button[data-test="add-to-cart-sauce-labs-backpack"]
    Click    css=a.shopping_cart_link
    Wait For Selector    css=.cart_list    timeout=10
    Click    css=button#checkout
    Wait For Selector    css=input#first-name    timeout=10
    Input Text    css=input#first-name    ${FIRST_NAME}
    Input Text    css=input#last-name     ${LAST_NAME}
    Input Text    css=input#postal-code   ${POSTAL_CODE}
    Click    css=button#continue
    Wait For Selector    css=.summary_info    timeout=10
    ${title}=    Get Title
    Should Contain    ${title}    Swag Labs
    Close Playwright Browser

锁定用户登录失败提示
    [Documentation]    验证锁定用户的错误提示
    [Tags]    selenium    regression
    Open Browser    ${BASE_URL}    chrome
    Input Text      id=user-name    ${LOCKED_USER}
    Input Text      id=password     ${PASSWORD}
    Click Button    id=login-button
    Wait Until Page Contains Element    css:[data-test="error"]    timeout=10s
    ${err}=    Get Text    css:[data-test="error"]
    Should Contain    ${err.lower()}    locked out
    Close Browser

