*** Settings ***
Documentation    API 测试套件（使用 Robot Framework）
...              演示如何用 Robot Framework 编写 API 测试用例
...              包括：GET/POST 请求、请求头、查询参数、错误处理等

Library    Collections
Library    RequestsLibrary

Suite Setup    Initialize Session
Suite Teardown    Delete All Sessions

*** Variables ***
${API_BASE_URL}    https://httpbin.org
${TIMEOUT}    10


*** Test Cases ***

API 基础测试 - GET 请求获取 IP
    [Documentation]    演示简单的 GET 请求和响应验证
    [Tags]    api    get    smoke
    
    ${response}=    GET    ${API_BASE_URL}/ip
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.json()}    origin


API 基础测试 - POST 请求提交数据
    [Documentation]    演示 POST 请求和 JSON 数据提交
    [Tags]    api    post
    
    ${payload}=    Create Dictionary    name=Test User    email=test@example.com
    ${response}=    POST    ${API_BASE_URL}/post    json=${payload}
    
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Be Equal    ${response.json()}[json][name]    Test User
    Should Be Equal    ${response.json()}[json][email]    test@example.com


API 基础测试 - PUT 请求更新数据
    [Documentation]    演示 PUT 请求
    [Tags]    api    put
    
    ${payload}=    Create Dictionary    id=1    title=Updated Title    completed=${True}
    ${response}=    PUT    ${API_BASE_URL}/put    json=${payload}
    
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Be Equal    ${response.json()}[json][title]    Updated Title


API 基础测试 - DELETE 请求
    [Documentation]    演示 DELETE 请求
    [Tags]    api    delete
    
    ${response}=    DELETE    ${API_BASE_URL}/delete
    Should Be Equal As Numbers    ${response.status_code}    200


API 请求头测试 - 自定义请求头
    [Documentation]    测试带自定义请求头的请求
    [Tags]    api    headers
    
    ${headers}=    Create Dictionary    
    ...    User-Agent=Custom API Client/1.0
    ...    Authorization=Bearer test-token
    
    ${response}=    GET On Session    api_session    /headers    headers=${headers}
    
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.json()}[headers]    Authorization
    Should Be Equal    ${response.json()}[headers][Authorization]    Bearer test-token


API 查询参数测试
    [Documentation]    测试带查询参数的 GET 请求
    [Tags]    api    query_params
    
    ${params}=    Create Dictionary    page=1    limit=10    sort=name
    ${response}=    GET    ${API_BASE_URL}/get    params=${params}
    
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Be Equal    ${response.json()}[args][page]    1
    Should Be Equal    ${response.json()}[args][limit]    10


API 表单数据测试
    [Documentation]    测试 Form 数据提交
    [Tags]    api    form
    
    ${data}=    Create Dictionary    username=testuser    password=testpass123    remember=on
    ${response}=    POST    ${API_BASE_URL}/post    data=${data}
    
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.json()}    form


API 响应格式测试
    [Documentation]    验证响应格式和内容类型
    [Tags]    api    format
    
    ${response}=    GET    ${API_BASE_URL}/json
    
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Contain    ${response.headers}    Content-Type


API 错误处理 - 404 错误
    [Documentation]    测试 404 错误响应
    [Tags]    api    error     404
    
    ${response}=    GET On Session    api_session    /status/404    expected_status=404
    Should Be Equal As Numbers    ${response.status_code}    404


API 错误处理 - 500 错误
    [Documentation]    测试 500 错误响应
    [Tags]    api    error    500
    ${result}=    Run Keyword And Ignore Error    GET On Session    api_session    /status/500
    Should Be Equal    ${result[0]}    FAIL
    Should Contain    ${result[1]}    500


API 错误处理 - 无效请求
    [Documentation]    测试无效请求处理
    [Tags]    api    error
    
    ${response}=    GET On Session    api_session    /status/400    expected_status=400
    Should Be Equal As Numbers    ${response.status_code}    400


API 响应头验证
    [Documentation]    验证响应头信息
    [Tags]    api    headers
    
    ${response}=    GET    ${API_BASE_URL}/get
    
    # 验证常见的响应头
    Should Contain    ${response.headers}    Content-Type
    Should Contain    ${response.headers}    Content-Length


API 重定向测试
    [Documentation]    测试重定向处理
    [Tags]    api    redirect    load    performance
    
    ${response}=    GET On Session    api_session    /redirect/3
    Should Be Equal As Numbers    ${response.status_code}    200
    
    # 创建包含大量数据的 payload
    ${large_payload}=    Create Dictionary
    FOR    ${i}    IN RANGE    100
        ${key}=    Catenate    key_    ${i}
        ${value}=    Catenate    value_    ${i}
        Set To Dictionary    ${large_payload}    ${key}    ${value}
    END
    
    ${response}=    POST    ${API_BASE_URL}/post    json=${large_payload}
    Should Be Equal As Numbers    ${response.status_code}    200


API 连续请求测试
    [Documentation]    测试连续发送多个请求
    [Tags]    api    sequential
    
    FOR    ${i}    IN RANGE    5
        ${response}=    GET    ${API_BASE_URL}/get    params={'index': ${i}}
        Should Be Equal As Numbers    ${response.status_code}    200
    END


API 响应验证 - 必需字段检查
    [Documentation]    验证响应中的必需字段
    [Tags]    api    validation
    
    ${response}=    GET    ${API_BASE_URL}/get
    ${data}=    Set Variable    ${response.json()}
    
    # 验证必需字段存在
    Should Contain    ${data}    headers
    Should Contain    ${data}    args
    Should Contain    ${data}    url


API 响应验证 - 数据类型检查
    [Documentation]    验证响应数据的数据类型
    [Tags]    api    validation
    
    ${response}=    GET    ${API_BASE_URL}/get
    ${data}=    Set Variable    ${response.json()}
    
    # 验证字段类型
    ${is_headers_dict}=    Evaluate    isinstance($data['headers'], dict)
    ${is_args_dict}=    Evaluate    isinstance($data['args'], dict)
    ${is_url_str}=    Evaluate    isinstance($data['url'], str)
    Should Be True    ${is_headers_dict}
    Should Be True    ${is_args_dict}
    Should Be True    ${is_url_str}


API 认证测试
    [Documentation]    测试带认证信息的请求
    [Tags]    api    auth
    ${auth_headers}=    Create Dictionary    Authorization=Bearer test-token
    ${response}=    GET On Session    api_session    /bearer    headers=${auth_headers}
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Be True    ${response.json()}[authenticated]
    Should Be Equal    ${response.json()}[token]    test-token


API Cookie 测试
    [Documentation]    测试 Cookie 处理
    [Tags]    api    cookie
    
    ${response}=    GET    ${API_BASE_URL}/cookies/set    params={'test': 'value'}
    Should Be Equal As Numbers    ${response.status_code}    200


*** Keywords ***

Initialize Session
    [Documentation]    初始化 HTTP 会话
    Create Session    api_session    ${API_BASE_URL}    timeout=${TIMEOUT}


GET
    [Arguments]    ${url}    ${params}=${EMPTY}    ${expected_status}=200    ${allow_redirects}=${True}
    [Documentation]    发送 GET 请求的便捷关键字
    
    ${response}=    GET On Session    api_session    ${url}    params=${params}
    Should Be Equal As Numbers    ${response.status_code}    ${expected_status}
    [Return]    ${response}


POST
    [Arguments]    ${url}    ${json}=${EMPTY}    ${data}=${EMPTY}    ${expected_status}=200
    [Documentation]    发送 POST 请求的便捷关键字
    
    ${response}=    POST On Session    api_session    ${url}    json=${json}    data=${data}
    Should Be Equal As Numbers    ${response.status_code}    ${expected_status}
    [Return]    ${response}


PUT
    [Arguments]    ${url}    ${json}=${EMPTY}    ${expected_status}=200
    [Documentation]    发送 PUT 请求的便捷关键字
    
    ${response}=    PUT On Session    api_session    ${url}    json=${json}
    Should Be Equal As Numbers    ${response.status_code}    ${expected_status}
    [Return]    ${response}


DELETE
    [Arguments]    ${url}    ${expected_status}=200
    [Documentation]    发送 DELETE 请求的便捷关键字
    
    ${response}=    DELETE On Session    api_session    ${url}
    Should Be Equal As Numbers    ${response.status_code}    ${expected_status}
    [Return]    ${response}
