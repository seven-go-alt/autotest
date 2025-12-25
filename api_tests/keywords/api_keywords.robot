*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${USERS_ENDPOINT}    /users

*** Keywords ***
Create API Session
    [Arguments]    ${alias}    ${base_url}    ${headers}=${None}    ${auth_token}=${None}
    # 如果提供了 auth_token，则把 Authorization 添加到 headers 中
    Run Keyword If    '${auth_token}' != 'None' and '${headers}' == 'None'    ${headers}=    Create Dictionary    Authorization=Bearer ${auth_token}
    Run Keyword If    '${auth_token}' != 'None' and '${headers}' != 'None'    Set To Dictionary    ${headers}    Authorization=Bearer ${auth_token}
    Run Keyword If    '${headers}' != 'None'    Create Session    ${alias}    ${base_url}    headers=${headers}
    ...    ELSE    Create Session    ${alias}    ${base_url}

Get Users List
    [Arguments]    ${base_url}    ${params}=${None}    ${expected_status}=200    ${headers}=${None}    ${retries}=1    ${delay}=1    ${auth_token}=${None}
    Run Keyword If    '${headers}' != 'None' or '${auth_token}' != 'None'    Create API Session    api    ${base_url}    ${headers}=${headers}    ${auth_token}=${auth_token}
    ...    ELSE    Create API Session    api    ${base_url}
    Log    Base URL: ${base_url}
    ${max}=    Evaluate    int(${retries}) + 1
    FOR    ${i}    IN RANGE    1    ${max}
        ${resp}=    Run Keyword If    '${headers}' != 'None'    GET On Session    api    ${USERS_ENDPOINT}    params=${params}    headers=${headers}
        ...    ELSE    GET On Session    api    ${USERS_ENDPOINT}    params=${params}
        Log    Request URL: ${resp.url}
        Log    Response status: ${resp.status_code}
        Run Keyword If    ${resp.status_code} == ${expected_status}    Return From Keyword    ${resp.json()}
        Sleep    ${delay}
    END
    Fail    Expected status ${expected_status} but got ${resp.status_code}

Get User By Id
    [Arguments]    ${base_url}    ${user_id}    ${expected_status}=200    ${headers}=${None}    ${retries}=1    ${delay}=1    ${auth_token}=${None}
    Run Keyword If    '${headers}' != 'None' or '${auth_token}' != 'None'    Create API Session    api    ${base_url}    ${headers}=${headers}    ${auth_token}=${auth_token}
    ...    ELSE    Create API Session    api    ${base_url}
    ${endpoint}=    Catenate    SEPARATOR=    ${USERS_ENDPOINT}/    ${user_id}
    ${max}=    Evaluate    int(${retries}) + 1
    FOR    ${i}    IN RANGE    1    ${max}
        ${resp}=    Run Keyword If    '${headers}' != 'None'    GET On Session    api    ${endpoint}    headers=${headers}
        ...    ELSE    GET On Session    api    ${endpoint}
        Log    Request URL: ${resp.url}
        Log    Response status: ${resp.status_code}
        Run Keyword If    ${resp.status_code} == ${expected_status}    Return From Keyword    ${resp.json()}
        Sleep    ${delay}
    END
    Fail    Expected status ${expected_status} but got ${resp.status_code}

Create User
    [Arguments]    ${base_url}    ${payload}    ${expected_status}=201    ${headers}=${None}    ${retries}=1    ${delay}=1    ${auth_token}=${None}
    Run Keyword If    '${headers}' != 'None' or '${auth_token}' != 'None'    Create API Session    api    ${base_url}    ${headers}=${headers}    ${auth_token}=${auth_token}
    ...    ELSE    Create API Session    api    ${base_url}
    ${max}=    Evaluate    int(${retries}) + 1
    FOR    ${i}    IN RANGE    1    ${max}
        ${resp}=    Run Keyword If    '${headers}' != 'None'    POST On Session    api    ${USERS_ENDPOINT}    json=${payload}    headers=${headers}
        ...    ELSE    POST On Session    api    ${USERS_ENDPOINT}    json=${payload}
        Log    Request URL: ${resp.url}
        Log    Response status: ${resp.status_code}
        Run Keyword If    ${resp.status_code} == ${expected_status}    Return From Keyword    ${resp.json()}
        Sleep    ${delay}
    END
    Fail    Expected status ${expected_status} but got ${resp.status_code}

Update User
    [Arguments]    ${base_url}    ${user_id}    ${payload}    ${expected_status}=200    ${headers}=${None}    ${retries}=1    ${delay}=1    ${auth_token}=${None}
    Run Keyword If    '${headers}' != 'None' or '${auth_token}' != 'None'    Create API Session    api    ${base_url}    ${headers}=${headers}    ${auth_token}=${auth_token}
    ...    ELSE    Create API Session    api    ${base_url}
    ${endpoint}=    Catenate    SEPARATOR=    ${USERS_ENDPOINT}/    ${user_id}
    ${max}=    Evaluate    int(${retries}) + 1
    FOR    ${i}    IN RANGE    1    ${max}
        ${resp}=    Run Keyword If    '${headers}' != 'None'    PUT On Session    api    ${endpoint}    json=${payload}    headers=${headers}
        ...    ELSE    PUT On Session    api    ${endpoint}    json=${payload}
        Log    Request URL: ${resp.url}
        Log    Response status: ${resp.status_code}
        Run Keyword If    ${resp.status_code} == ${expected_status}    Return From Keyword    ${resp.json()}
        Sleep    ${delay}
    END
    Fail    Expected status ${expected_status} but got ${resp.status_code}

Delete User
    [Arguments]    ${base_url}    ${user_id}    ${expected_status}=204    ${headers}=${None}    ${retries}=1    ${delay}=1    ${auth_token}=${None}
    Run Keyword If    '${headers}' != 'None' or '${auth_token}' != 'None'    Create API Session    api    ${base_url}    ${headers}=${headers}    ${auth_token}=${auth_token}
    ...    ELSE    Create API Session    api    ${base_url}
    ${endpoint}=    Catenate    SEPARATOR=    ${USERS_ENDPOINT}/    ${user_id}
    ${max}=    Evaluate    int(${retries}) + 1
    FOR    ${i}    IN RANGE    1    ${max}
        ${resp}=    Run Keyword If    '${headers}' != 'None'    DELETE On Session    api    ${endpoint}    headers=${headers}
        ...    ELSE    DELETE On Session    api    ${endpoint}
        Log    Request URL: ${resp.url}
        Log    Response status: ${resp.status_code}
        Run Keyword If    ${resp.status_code} == ${expected_status}    Return From Keyword
        Sleep    ${delay}
    END
    Fail    Expected status ${expected_status} but got ${resp.status_code}

Response Should Contain Keys
    [Arguments]    ${json_obj}    @{keys}
    @{missing}=    Create List
    FOR    ${key}    IN    @{keys}
        ${current}=    Set Variable    ${json_obj}
        @{parts}=    Split String    ${key}    .
        ${found}=    Set Variable    ${True}
        FOR    ${seg}    IN    @{parts}
            Run Keyword If    '${seg}'.isdigit()    ${res}=    Run Keyword And Ignore Error    Get From List    ${current}    ${seg}
            ...    ELSE    ${res}=    Run Keyword And Ignore Error    Get From Dictionary    ${current}    ${seg}
            ${status}=    Set Variable    ${res[0]}
            ${value}=    Set Variable    ${res[1]}
            Run Keyword If    '${status}' == 'PASS'    ${current}=    Set Variable    ${value}
            ...    ELSE    Set Variable    ${found}    ${False}
            Run Keyword If    '${found}' == 'False'    Exit For Loop
        END
        Run Keyword If    '${found}' == 'False'    Append To List    ${missing}    ${key}
    END
    Run Keyword If    ${len(${missing})} > 0    Log    Missing keys: ${missing}
    Length Should Be    ${missing}    0    msg=Missing keys: ${missing}


