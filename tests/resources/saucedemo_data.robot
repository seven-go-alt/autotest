*** Settings ***
Documentation    SauceDemo 测试数据资源文件
Library          Collections

*** Variables ***
# ========== SauceDemo 登录用户数据 ==========
# 所有用户密码均为：secret_sauce

# 标准用户（正常用户）
${SAUCEDEMO_STANDARD_USER}        standard_user
${SAUCEDEMO_STANDARD_PASSWORD}    secret_sauce

# 被锁定的用户
${SAUCEDEMO_LOCKED_USER}          locked_out_user
${SAUCEDEMO_LOCKED_PASSWORD}      secret_sauce

# 问题用户（渲染问题）
${SAUCEDEMO_PROBLEM_USER}         problem_user
${SAUCEDEMO_PROBLEM_PASSWORD}     secret_sauce

# 性能问题用户（加载缓慢）
${SAUCEDEMO_PERFORMANCE_USER}     performance_glitch_user
${SAUCEDEMO_PERFORMANCE_PASSWORD}     secret_sauce

# 错误用户（500 错误）
${SAUCEDEMO_ERROR_USER}           error_user
${SAUCEDEMO_ERROR_PASSWORD}       secret_sauce

# 可视问题用户（界面差异）
${SAUCEDEMO_VISUAL_USER}          visual_user
${SAUCEDEMO_VISUAL_PASSWORD}      secret_sauce

# ========== SauceDemo 通用数据 ==========
${SAUCEDEMO_BASE_URL}             https://www.saucedemo.com/
${SAUCEDEMO_COMMON_PASSWORD}      secret_sauce

# ========== 结账表单数据 ==========
# 标准结账信息
${CHECKOUT_FIRST_NAME}            Auto
${CHECKOUT_LAST_NAME}             Tester
${CHECKOUT_POSTAL_CODE}           12345

# ========== 所有用户列表 ==========
@{SAUCEDEMO_ALL_USERS}
...    standard_user
...    locked_out_user
...    problem_user
...    performance_glitch_user
...    error_user
...    visual_user

*** Keywords ***
获取用户凭证
    [Documentation]    根据用户类型返回用户名和密码
    [Arguments]    ${user_type}=standard
    [Tags]    utility
    ${credentials}=    Create Dictionary
    ...    username=${SAUCEDEMO_STANDARD_USER}
    ...    password=${SAUCEDEMO_STANDARD_PASSWORD}
    Run Keyword If    '${user_type}' == 'locked'    Set To Dictionary    ${credentials}    username=${SAUCEDEMO_LOCKED_USER}    password=${SAUCEDEMO_LOCKED_PASSWORD}
    Run Keyword If    '${user_type}' == 'problem'    Set To Dictionary    ${credentials}    username=${SAUCEDEMO_PROBLEM_USER}    password=${SAUCEDEMO_PROBLEM_PASSWORD}
    Run Keyword If    '${user_type}' == 'performance'    Set To Dictionary    ${credentials}    username=${SAUCEDEMO_PERFORMANCE_USER}    password=${SAUCEDEMO_PERFORMANCE_PASSWORD}
    Run Keyword If    '${user_type}' == 'error'    Set To Dictionary    ${credentials}    username=${SAUCEDEMO_ERROR_USER}    password=${SAUCEDEMO_ERROR_PASSWORD}
    Run Keyword If    '${user_type}' == 'visual'    Set To Dictionary    ${credentials}    username=${SAUCEDEMO_VISUAL_USER}    password=${SAUCEDEMO_VISUAL_PASSWORD}
    [Return]    ${credentials}
