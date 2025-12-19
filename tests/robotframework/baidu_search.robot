*** Settings ***
Documentation    百度搜索示例测试用例
Library           SeleniumLibrary
Library           Browser
Resource          ../resources/common.robot

*** Variables ***
${BASE_URL}       https://www.baidu.com
${SEARCH_KEYWORD}    Robot Framework

*** Test Cases ***
百度搜索测试 - Selenium
    [Documentation]    使用 Selenium 进行百度搜索测试
    [Tags]    selenium    smoke
    Open Browser    ${BASE_URL}    chrome
    Maximize Browser Window
    Input Text      id=kw    ${SEARCH_KEYWORD}
    Click Button    id=su
    Wait Until Element Is Visible    id=content_left    timeout=10s
    ${title}=    Get Title
    Should Contain    ${title}    百度
    Close Browser

百度搜索测试 - Playwright
    [Documentation]    使用 Playwright 进行百度搜索测试
    [Tags]    playwright    smoke
    New Page    ${BASE_URL}
    Fill Text    id=kw    ${SEARCH_KEYWORD}
    Click    id=su
    Wait For Elements State    id=content_left    visible    timeout=10s
    ${title}=    Get Title
    Should Contain    ${title}    百度
    Close Browser

页面标题验证
    [Documentation]    验证页面标题
    [Tags]    selenium
    Open Browser    ${BASE_URL}    chrome
    ${title}=    Get Title
    Should Not Be Empty    ${title}
    Close Browser

