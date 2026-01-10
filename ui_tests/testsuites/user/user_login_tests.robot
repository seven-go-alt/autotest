*** Settings ***
Resource    ../../keywords/process_layer/user_flows.robot
Resource    ../../../tests/resources/common.robot
Resource    ../../../tests/resources/saucedemo_data.robot

*** Variables ***
${BASE_URL}          ${SAUCEDEMO_BASE_URL}
${STANDARD_USER}     ${SAUCEDEMO_STANDARD_USER}
${STANDARD_PASSWORD}    ${SAUCEDEMO_STANDARD_PASSWORD}

*** Test Cases ***
P0 用户使用正确账号密码登录成功
    [Documentation]    P0 级别：验证标准用户使用正确密码登录成功
    [Tags]    P0    user    login    pc
    用户使用账号密码登录    ${BASE_URL}    ${STANDARD_USER}    ${STANDARD_PASSWORD}
    Wait Until Page Contains    Products    timeout=10s
    Page Should Contain    Products
    [Teardown]    Close Browser

P1 用户使用错误密码登录失败
    [Documentation]    P1 级别：验证使用错误密码登录失败并显示错误提示
    [Tags]    P1    user    login    pc
    用户使用账号密码登录    ${BASE_URL}    ${STANDARD_USER}    wrong_password
    Wait Until Page Contains    Epic sadface    timeout=10s
    Page Should Contain    Epic sadface
    [Teardown]    Close Browser


