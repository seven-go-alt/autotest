*** Settings ***
Documentation     百度搜索功能测试
...               演示百度搜索功能
...               包括：搜索、结果验证

Library    ../keywords/baidu_keywords.py

Suite Setup       打开浏览器    https://www.baidu.com
Suite Teardown    关闭浏览器

*** Test Cases ***

搜索 Robot Framework
    [Documentation]    搜索 Robot Framework 相关内容
    [Tags]    ui    baidu    search
    
    搜索    Robot Framework
    验证搜索结果存在
    验证搜索结果包含关键词    Robot Framework


搜索 Python
    [Documentation]    搜索 Python 相关内容
    [Tags]    ui    baidu    search
    
    搜索    Python
    验证搜索结果存在
    ${count}=    获取搜索结果数
    Should Be True    ${count} > 0


搜索多个关键词
    [Documentation]    依次搜索多个关键词
    [Tags]    ui    baidu    search
    
    搜索    自动化测试
    验证搜索结果存在
    刷新页面
    搜索    Web 测试
    验证搜索结果存在
