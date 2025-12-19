*** Settings ***
Documentation    通用资源文件
Library           SeleniumLibrary
Library           Browser
Library           ../../utils/robot_custom_library.py    WITH NAME    PlayLib

*** Keywords ***
打开浏览器
    [Arguments]    ${url}    ${browser}=chrome
    Open Browser    ${url}    ${browser}
    Maximize Browser Window

关闭浏览器
    Close Browser

输入搜索关键词
    [Arguments]    ${keyword}
    # 默认使用 SeleniumLibrary 的关键字
    Input Text    id=kw    ${keyword}
    Click Button    id=su

等待搜索结果加载
    Wait Until Element Is Visible    id=content_left    timeout=10s

验证搜索结果
    [Arguments]    ${expected_text}
    ${title}=    Get Title
    Should Contain    ${title}    ${expected_text}

*** Keywords ***
打开 Playwright 浏览器
    [Arguments]    ${url}    ${headless}=True
    Open Playwright Browser    headless=${headless}
    Go To    ${url}

关闭 Playwright 浏览器
    Close Playwright Browser

Playwright 输入并搜索
    [Arguments]    ${selector}    ${text}
    Wait For Selector    ${selector}    timeout=15
    Input Text    ${selector}    ${text}
    Click    css=button#su

