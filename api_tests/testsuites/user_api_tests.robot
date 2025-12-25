*** Settings ***
Resource    ../keywords/api_keywords.robot

*** Test Cases ***
P1 获取用户列表成功
    [Tags]    P1    user    api    pc
    ${data}=    Get Users List    ${API_BASE_URL}
    Should Not Be Empty    ${data}


