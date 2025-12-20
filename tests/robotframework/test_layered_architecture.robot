*** Settings ***
Documentation    Python.org 搜索功能综合测试
...              使用分层 Robot 库：定位器层 -> 操作层 -> 功能层
...              演示功能测试、操作测试、定位器测试的统一写法

Library    Collections
Library    ../utils/robot_functional.py    AS    Functional
Library    ../utils/robot_steps.py    AS    Steps
Library    ../utils/robot_locators.py    AS    Locators
Library    ../utils/playwright_helper.py    AS    Playwright

Suite Setup    Initialize Browser
Suite Teardown    Cleanup Browser

*** Variables ***
${BASE_URL}    https://www.python.org
${SEARCH_KEYWORD}    pytest
${HEADLESS}    True


*** Test Cases ***

功能层测试 - 完整搜索流程
    [Documentation]    使用功能层关键字执行完整搜索流程
    [Tags]    functional    smoke    robot
    
    Functional.Complete Search Flow    ${SEARCH_KEYWORD}


功能层测试 - 验证搜索结果
    [Documentation]    验证搜索结果是否正确
    [Tags]    functional    robot
    
    Functional.Setup Browser And Navigate    ${BASE_URL}
    Functional.Verify Search Result    ${SEARCH_KEYWORD}
    Functional.Cleanup Browser


功能层测试 - 获取和验证页面标题
    [Documentation]    获取页面标题并验证内容
    [Tags]    functional    robot
    
    Functional.Setup Browser And Navigate    ${BASE_URL}
    ${title}=    Functional.Get And Verify Page Title
    Should Contain    ${title}    Python    msg=页面标题应包含 "Python"


操作层测试 - 导航到主页
    [Documentation]    使用操作层关键字进行基本导航
    [Tags]    steps    smoke    robot
    
    Steps.Init Browser    ${HEADLESS}
    Steps.Navigate To    ${BASE_URL}
    ${title}=    Steps.Get Page Title
    Should Not Be Empty    ${title}
    Steps.Close Browser


操作层测试 - 搜索框交互
    [Documentation]    测试搜索框的填充和点击
    [Tags]    steps    robot
    
    Steps.Init Browser    ${HEADLESS}
    Steps.Navigate To    ${BASE_URL}
    Steps.Wait For Element By Name    search_input    timeout=10
    Steps.Fill Input By Name    search_input    ${SEARCH_KEYWORD}
    Steps.Click Element By Name    search_button
    ${title}=    Steps.Get Page Title
    Should Not Be Empty    ${title}
    Steps.Close Browser


操作层测试 - 等待元素可见
    [Documentation]    测试元素等待和可见性验证
    [Tags]    steps    robot
    
    Steps.Init Browser    ${HEADLESS}
    Steps.Navigate To    ${BASE_URL}
    Steps.Wait For Element By Name    page_content    timeout=15
    ${content}=    Steps.Get Element Text By Name    page_content
    Should Not Be Empty    ${content}
    Steps.Close Browser


操作层测试 - 截图功能
    [Documentation]    测试截图功能和截图保存
    [Tags]    steps    robot
    
    Steps.Init Browser    ${HEADLESS}
    Steps.Navigate To    ${BASE_URL}
    ${screenshot_path}=    Steps.Take Screenshot    main_page.png
    File Should Exist    ${screenshot_path}
    Steps.Close Browser


定位器层测试 - 获取定位器
    [Documentation]    测试获取各种元素的定位器
    [Tags]    locators    robot
    
    ${search_input_locator}=    Locators.Get Locator    search_input
    Should Not Be Empty    ${search_input_locator}
    
    ${search_button_locator}=    Locators.Get Locator    search_button
    Should Not Be Empty    ${search_button_locator}
    
    ${page_content_locator}=    Locators.Get Locator    page_content
    Should Not Be Empty    ${page_content_locator}


定位器层测试 - 页面特定定位器
    [Documentation]    测试特定页面的定位器
    [Tags]    locators    robot
    
    ${python_logo_locator}=    Locators.Get Locator    python_logo
    Should Not Be Empty    ${python_logo_locator}
    
    ${nav_menu_locator}=    Locators.Get Locator    navigation_menu
    Should Not Be Empty    ${nav_menu_locator}


多层混合测试 - 完整搜索和验证
    [Documentation]    混合使用多层关键字进行复杂操作
    [Tags]    integration    robot
    
    # 使用功能层初始化
    Functional.Setup Browser And Navigate    ${BASE_URL}
    
    # 使用操作层进行详细操作
    Steps.Wait For Element By Name    search_input    timeout=10
    Steps.Fill Input By Name    search_input    robotframework
    Steps.Click Element By Name    search_button
    
    # 使用定位器层验证
    ${button_locator}=    Locators.Get Locator    search_button
    Should Not Be Empty    ${button_locator}
    
    # 使用操作层等待结果
    Steps.Wait For Element By Name    search_results    timeout=15
    
    # 获取结果并验证
    ${title}=    Steps.Get Page Title
    Should Not Be Empty    ${title}
    
    # 清理
    Functional.Cleanup Browser


异常处理测试 - 超时重试
    [Documentation]    测试超时和重试机制
    [Tags]    error_handling    robot
    
    ${result}=    Run Keyword And Ignore Error    
    ...    Steps.Wait For Element By Name    nonexistent_element    timeout=2
    Should Be Equal    ${result[0]}    FAIL


性能测试 - 页面加载时间
    [Documentation]    测试页面加载性能
    [Tags]    performance    robot
    
    Steps.Init Browser    ${HEADLESS}
    
    ${start_time}=    Get Time    epoch
    Steps.Navigate To    ${BASE_URL}
    ${end_time}=    Get Time    epoch
    
    ${load_time}=    Evaluate    ${end_time} - ${start_time}
    Log    页面加载时间: ${load_time} 秒
    
    Should Be True    ${load_time} < 30    msg=页面加载时间过长
    
    Steps.Close Browser


跨浏览器测试标记
    [Documentation]    标记此测试用于跨浏览器运行
    [Tags]    cross_browser    robot
    
    Functional.Setup Browser And Navigate    ${BASE_URL}
    ${title}=    Steps.Get Page Title
    Should Contain    ${title}    Python
    Functional.Cleanup Browser


本地化测试标记
    [Documentation]    标记此测试用于本地化测试
    [Tags]    localization    robot
    
    Functional.Setup Browser And Navigate    ${BASE_URL}
    ${title}=    Steps.Get Page Title
    Should Not Be Empty    ${title}
    Functional.Cleanup Browser


*** Keywords ***

Initialize Browser
    [Documentation]    测试套件初始化：初始化浏览器
    Log    初始化测试环境
    # 可在此添加其他初始化逻辑


Cleanup Browser
    [Documentation]    测试套件清理：关闭浏览器
    Log    清理测试环境
    # 确保所有浏览器实例都已关闭
    Functional.Cleanup Browser    No Operation    Ignore Error
