*** Settings ***
Documentation     ReqRes API 测试套件
...               演示如何测试 RESTful API
...               包括：用户管理、登录、CRUD 操作

Library    Collections
Library    RequestsLibrary
Library    ../data/user_data.py
Library    ../data/post_data.py
Library    ../config/api_config.py
Library    ../config/testcase_config.py

Suite Setup       创建 API 会话
Suite Teardown    关闭所有会话

*** Variables ***
${REQRES_BASE_URL}    https://reqres.in
${TIMEOUT}            10


*** Keywords ***
创建 API 会话
    [Documentation]    创建 ReqRes API 的会话
    Create Session    reqres    ${REQRES_BASE_URL}    timeout=${TIMEOUT}


关闭所有会话
    [Documentation]    关闭所有 API 会话
    Delete All Sessions


*** Test Cases ***

获取用户列表
    [Documentation]    测试获取用户列表 API
    [Tags]    api    get    smoke
    
    ${response}=    GET On Session    reqres    /api/users    params={'page': 1}
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.json()}    data
    Should Contain    ${response.json()}    page


获取单个用户
    [Documentation]    测试获取单个用户 API
    [Tags]    api    get
    
    ${response}=    GET On Session    reqres    /api/users/1
    Should Be Equal As Numbers    ${response.status_code}    200
    ${user}=    Set Variable    ${response.json()}[data]
    Should Not Be Empty    ${user}[email]
    Should Not Be Empty    ${user}[first_name]


创建用户
    [Documentation]    测试创建用户 API
    [Tags]    api    post
    
    ${payload}=    Create Dictionary    name=John Doe    job=Engineer
    ${response}=    POST On Session    reqres    /api/users    json=${payload}
    Should Be Equal As Numbers    ${response.status_code}    201
    Should Contain    ${response.json()}    id
    Should Contain    ${response.json()}    createdAt


更新用户
    [Documentation]    测试更新用户 API
    [Tags]    api    put
    
    ${payload}=    Create Dictionary    name=Jane Doe    job=Senior Engineer
    ${response}=    PUT On Session    reqres    /api/users/1    json=${payload}
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.json()}    updatedAt


删除用户
    [Documentation]    测试删除用户 API
    [Tags]    api    delete
    
    ${response}=    DELETE On Session    reqres    /api/users/1
    Should Be Equal As Numbers    ${response.status_code}    204


登录成功
    [Documentation]    测试成功登录
    [Tags]    api    login    smoke
    
    ${payload}=    Create Dictionary    email=eve.holt@reqres.in    password=cityslicka
    ${response}=    POST On Session    reqres    /api/login    json=${payload}
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.json()}    token


登录失败 - 缺少密码
    [Documentation]    测试缺少密码的登录请求
    [Tags]    api    login    negative
    
    ${payload}=    Create Dictionary    email=eve.holt@reqres.in
    ${response}=    POST On Session    reqres    /api/login    json=${payload}    expected_status=400
    Should Be Equal As Numbers    ${response.status_code}    400
    Should Contain    ${response.json()}    error


用户不存在
    [Documentation]    测试获取不存在的用户
    [Tags]    api    negative
    
    ${response}=    GET On Session    reqres    /api/users/999    expected_status=404
    Should Be Equal As Numbers    ${response.status_code}    404
