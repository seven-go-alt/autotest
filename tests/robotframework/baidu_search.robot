*** Settings ***
Documentation    SauceDemo 登录与购物流程示例
Library           SeleniumLibrary
Library           ../../utils/robot_custom_library.py    WITH NAME    PlayLib
Resource          ../resources/common.robot
Resource          ../resources/saucedemo_data.robot
Resource          ./locators/all_locators.robot

*** Variables ***
# 使用来自 saucedemo_data.robot 的变量
# ${BASE_URL}       已在 saucedemo_data.robot 中定义为 ${SAUCEDEMO_BASE_URL}
# 本文件为向后兼容保留别名
${BASE_URL}                   ${SAUCEDEMO_BASE_URL}
${STANDARD_USER}              ${SAUCEDEMO_STANDARD_USER}
${LOCKED_USER}                ${SAUCEDEMO_LOCKED_USER}
${PASSWORD}                   ${SAUCEDEMO_COMMON_PASSWORD}
${PROBLEM_USER}               ${SAUCEDEMO_PROBLEM_USER}
${PERFORMANCE_USER}           ${SAUCEDEMO_PERFORMANCE_USER}
${ERROR_USER}                 ${SAUCEDEMO_ERROR_USER}
${VISUAL_USER}                ${SAUCEDEMO_VISUAL_USER}
${FIRST_NAME}                 ${CHECKOUT_FIRST_NAME}
${LAST_NAME}                  ${CHECKOUT_LAST_NAME}
${POSTAL_CODE}                ${CHECKOUT_POSTAL_CODE}

*** Test Cases ***
SauceDemo 登录并查看商品 - Selenium
    [Documentation]    使用 Selenium 登录并验证商品列表
    [Tags]    selenium    smoke
    Open Browser    ${BASE_URL}    chrome
    Maximize Browser Window
    Wait Until Element Is Visible    ${LOGIN_USERNAME_INPUT}    timeout=10s
    SeleniumLibrary.Input Text      ${LOGIN_USERNAME_INPUT}    ${STANDARD_USER}
    SeleniumLibrary.Input Text      ${LOGIN_PASSWORD_INPUT}    ${PASSWORD}
    Click Button    ${LOGIN_BUTTON}
    Wait Until Page Contains Element    ${INVENTORY_LIST}    timeout=10s
    Page Should Contain Element    ${ADD_TO_CART_BACKPACK}
    Close Browser

SauceDemo 登录并下单 - Playwright
    [Documentation]    使用 Playwright（自定义关键字）登录并执行结账流程
    [Tags]    playwright    smoke
    PlayLib.Open Playwright Browser    headless=True    browser_name=chromium
    PlayLib.Go To    ${BASE_URL}
    PlayLib.Wait For Selector    ${LOGIN_USERNAME_INPUT}    timeout=15
    PlayLib.Input Text    ${LOGIN_USERNAME_INPUT}    ${STANDARD_USER}
    PlayLib.Input Text    ${LOGIN_PASSWORD_INPUT}    ${PASSWORD}
    PlayLib.Click    ${LOGIN_BUTTON}
    PlayLib.Wait For Selector    ${INVENTORY_LIST}    timeout=15
    PlayLib.Click    ${ADD_TO_CART_BACKPACK}
    PlayLib.Click    ${SHOPPING_CART_LINK}
    PlayLib.Wait For Selector    ${CART_LIST}    timeout=10
    PlayLib.Click    ${CHECKOUT_BUTTON}
    PlayLib.Wait For Selector    ${CHECKOUT_FIRST_NAME_INPUT}    timeout=10
    PlayLib.Input Text    ${CHECKOUT_FIRST_NAME_INPUT}    ${FIRST_NAME}
    PlayLib.Input Text    ${CHECKOUT_LAST_NAME_INPUT}    ${LAST_NAME}
    PlayLib.Input Text    ${CHECKOUT_POSTAL_CODE_INPUT}    ${POSTAL_CODE}
    PlayLib.Click    ${CONTINUE_BUTTON}
    PlayLib.Wait For Selector    ${CHECKOUT_SUMMARY_CONTAINER}    timeout=10
    ${title}=    PlayLib.Get Title
    Should Contain    ${title}    Swag Labs
    PlayLib.Close Playwright Browser

锁定用户登录失败提示
    [Documentation]    验证锁定用户的错误提示
    [Tags]    selenium    regression
    Open Browser    ${BASE_URL}    chrome
    SeleniumLibrary.Input Text      ${LOGIN_USERNAME_INPUT}    ${LOCKED_USER}
    SeleniumLibrary.Input Text      ${LOGIN_PASSWORD_INPUT}    ${PASSWORD}
    Click Button    ${LOGIN_BUTTON}
    Wait Until Page Contains Element    ${LOGIN_ERROR_MESSAGE}    timeout=10s
    ${err}=    Get Text    ${LOGIN_ERROR_MESSAGE}
    Should Contain    ${err.lower()}    locked out
    Close Browser

