*** Settings ***
Documentation     HTTPBin API 测试套件
...               演示各种 HTTP 方法和请求类型
...               包括：GET、POST、PUT、DELETE、请求头、状态码

Library    Collections
Library    RequestsLibrary

Suite Setup       创建 HTTPBin 会话
Suite Teardown    关闭所有会话

*** Variables ***
${HTTPBIN_BASE_URL}    https://httpbin.org
${TIMEOUT}             10


*** Keywords ***
创建 HTTPBin 会话
    [Documentation]    创建 HTTPBin API 的会话
    Create Session    httpbin    ${HTTPBIN_BASE_URL}    timeout=${TIMEOUT}


关闭所有会话
    [Documentation]    关闭所有 API 会话
    Delete All Sessions


*** Test Cases ***

HTTPBin GET 请求
    [Documentation]    测试 GET 请求
    [Tags]    api    httpbin    get
    
    ${response}=    GET On Session    httpbin    /get
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.json()}    url
    Should Contain    ${response.json()}    headers


HTTPBin POST 请求
    [Documentation]    测试 POST 请求
    [Tags]    api    httpbin    post
    
    ${payload}=    Create Dictionary    name=Test User    email=test@example.com
    ${response}=    POST On Session    httpbin    /post    json=${payload}
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.json()}    json


HTTPBin PUT 请求
    [Documentation]    测试 PUT 请求
    [Tags]    api    httpbin    put
    
    ${payload}=    Create Dictionary    id=1    updated=true
    ${response}=    PUT On Session    httpbin    /put    json=${payload}
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.json()}    json


HTTPBin DELETE 请求
    [Documentation]    测试 DELETE 请求
    [Tags]    api    httpbin    delete
    
    ${response}=    DELETE On Session    httpbin    /delete
    Should Be Equal As Numbers    ${response.status_code}    200


HTTPBin 查询参数
    [Documentation]    测试带查询参数的请求
    [Tags]    api    httpbin    params
    
    ${params}=    Create Dictionary    key1=value1    key2=value2
    ${response}=    GET On Session    httpbin    /get    params=${params}
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.json()}[args]    key1


HTTPBin 请求头
    [Documentation]    测试自定义请求头
    [Tags]    api    httpbin    headers
    
    ${headers}=    Create Dictionary    X-Custom-Header=custom-value    X-Another=another-value
    ${response}=    GET On Session    httpbin    /headers    headers=${headers}
    Should Be Equal As Numbers    ${response.status_code}    200


HTTPBin 状态码 200
    [Documentation]    测试 200 状态码
    [Tags]    api    httpbin    status
    
    ${response}=    GET On Session    httpbin    /status/200
    Should Be Equal As Numbers    ${response.status_code}    200


HTTPBin 状态码 404
    [Documentation]    测试 404 状态码
    [Tags]    api    httpbin    status    negative
    
    ${response}=    GET On Session    httpbin    /status/404    expected_status=404
    Should Be Equal As Numbers    ${response.status_code}    404


HTTPBin 获取 IP
    [Documentation]    测试获取 IP 的端点
    [Tags]    api    httpbin    get
    
    ${response}=    GET On Session    httpbin    /ip
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.json()}    origin
