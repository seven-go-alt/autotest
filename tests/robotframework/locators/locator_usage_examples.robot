*** Settings ***
Documentation    定位器层使用说明和示例
Library          Collections

*** Keywords ***
示例：使用定位器进行登录
    [Documentation]    演示如何使用定位器层进行页面操作
    [Arguments]    ${username}    ${password}
    [Tags]    example
    Input Text      ${LOGIN_USERNAME_INPUT}    ${username}
    Input Text      ${LOGIN_PASSWORD_INPUT}    ${password}
    Click Button    ${LOGIN_BUTTON}
    Wait Until Page Contains Element    ${INVENTORY_LIST}    timeout=10s

示例：使用定位器添加商品到购物车
    [Documentation]    演示如何使用定位器层添加商品
    [Arguments]    ${product_locator}
    [Tags]    example
    Click Element    ${product_locator}

示例：使用定位器完成结账
    [Documentation]    演示如何使用定位器层完成结账流程
    [Arguments]    ${first_name}    ${last_name}    ${postal_code}
    [Tags]    example
    Input Text    ${CHECKOUT_FIRST_NAME_INPUT}    ${first_name}
    Input Text    ${CHECKOUT_LAST_NAME_INPUT}    ${last_name}
    Input Text    ${CHECKOUT_POSTAL_CODE_INPUT}    ${postal_code}
    Click Button    ${CONTINUE_BUTTON}
    Wait Until Page Contains Element    ${CHECKOUT_SUMMARY_CONTAINER}    timeout=10s
    Click Button    ${FINISH_BUTTON}
