*** Settings ***
Resource    ../../keywords/process_layer/user_flows.robot
Resource    ../../../tests/resources/common.robot

*** Test Cases ***
P0 用户使用正确账号密码登录成功
    [Tags]    P0    user    login    pc
    User Login With Username And Password    ${BASE_URL}    ${STANDARD_USER}    ${STANDARD_PASSWORD}
    Page Should Contain    Products

P1 用户使用错误密码登录失败
    [Tags]    P1    user    login    pc
    User Login With Username And Password    ${BASE_URL}    ${STANDARD_USER}    wrong_password
    Page Should Contain    Epic sadface


