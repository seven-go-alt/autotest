*** Settings ***
Documentation    通用资源文件
Library           SeleniumLibrary
Library           Browser

*** Keywords ***
打开浏览器
    [Arguments]    ${url}    ${browser}=chrome
    Open Browser    ${url}    ${browser}
    Maximize Browser Window

关闭浏览器
    Close Browser

输入搜索关键词
    [Arguments]    ${keyword}
    Input Text    id=kw    ${keyword}
    Click Button    id=su

等待搜索结果加载
    Wait Until Element Is Visible    id=content_left    timeout=10s

验证搜索结果
    [Arguments]    ${expected_text}
    ${title}=    Get Title
    Should Contain    ${title}    ${expected_text}

