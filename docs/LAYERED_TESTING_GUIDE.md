# 分层测试架构使用指南

## 概述

本自动化框架采用**分层测试架构**设计，旨在实现代码复用、易于维护、扩展性强的测试框架。

### 架构组成

```
┌─────────────────────────────────────────┐
│   测试用例层（Test Cases）              │
│  Robot Framework / pytest / Manual       │
├─────────────────────────────────────────┤
│   功能层（Functional Layer）             │
│  完整业务流程关键字                      │
│  (robot_functional.py)                  │
├─────────────────────────────────────────┤
│   操作层（Steps/Operations Layer）       │
│  原子 UI 操作关键字                      │
│  (robot_steps.py)                       │
├─────────────────────────────────────────┤
│   定位器层（Locators Layer）             │
│  元素定位器定义                          │
│  (robot_locators.py)                    │
├─────────────────────────────────────────┤
│   辅助层（Helper Layer）                 │
│  低级驱动程序封装                        │
│  (playwright_helper.py, selenium_helper.py)│
├─────────────────────────────────────────┤
│   基础设施（Infrastructure）             │
│  WebDriver、Browser 实例                 │
└─────────────────────────────────────────┘
```

## 各层详解

### 1. 定位器层 (Locators Layer)

**文件**: `utils/robot_locators.py`

**职责**: 
- 集中管理所有 UI 元素的定位器
- 提供元素的逻辑名称到选择器的映射
- 支持多种定位方式（CSS、XPath 等）

**用途**:
```python
# 在代码中定义所有定位器
SEARCH_INPUT = "css=input#search-box"
SEARCH_BUTTON = "xpath=//button[text()='Search']"
RESULTS_CONTAINER = "id=results"

# 通过逻辑名称获取定位器
get_locator("search_input")  # 返回 CSS 选择器
```

**优势**:
- ✅ 定位器修改无需改动测试用例
- ✅ 支持多页面管理
- ✅ 统一维护管理

### 2. 操作层 (Steps/Operations Layer)

**文件**: `utils/robot_steps.py`

**职责**:
- 提供原子级别的 UI 操作
- 每个关键字表示一个完整的操作
- 内部使用 PlaywrightHelper 驱动

**提供的关键字**:
```
Init Browser                    初始化浏览器
Navigate To                     导航到 URL
Click Element By Name           通过名称点击元素
Fill Input By Name              通过名称填充输入框
Wait For Element By Name        等待元素出现
Get Page Title                  获取页面标题
Get Element Text By Name        获取元素文本
Take Screenshot                 截图
Close Browser                   关闭浏览器
```

**用法示例**:
```robot
Steps.Navigate To    ${BASE_URL}
Steps.Fill Input By Name    search_input    pytest
Steps.Click Element By Name    search_button
Steps.Wait For Element By Name    search_results
${title}=    Steps.Get Page Title
```

**优势**:
- ✅ 操作细粒度可控
- ✅ 复用性高
- ✅ 错误处理集中

### 3. 功能层 (Functional Layer)

**文件**: `utils/robot_functional.py`

**职责**:
- 组织操作层关键字成完整的业务流程
- 高级别的业务逻辑表达
- 通常由多个操作层关键字组成

**提供的关键字**:
```
Complete Search Flow            完整搜索流程
Verify Search Result            验证搜索结果
Setup Browser And Navigate      初始化并导航
Get And Verify Page Title       获取并验证标题
Cleanup Browser                 清理浏览器
```

**用法示例**:
```robot
# 高级业务流程，一个关键字表示完整的用户故事
Functional.Complete Search Flow    ${SEARCH_KEYWORD}

# 或者组合多个功能关键字
Functional.Setup Browser And Navigate    ${BASE_URL}
Functional.Verify Search Result    ${KEYWORD}
Functional.Cleanup Browser
```

**优势**:
- ✅ 业务语言清晰
- ✅ 测试用例简洁
- ✅ 维护工作量少

## 测试编写指南

### 方式 1: 使用功能层（推荐用于高级测试）

```robot
*** Test Cases ***

搜索功能完整测试
    [Documentation]    使用功能层编写的完整测试
    [Tags]    functional    smoke
    
    Functional.Complete Search Flow    pytest
```

**适用场景**:
- 完整的用户流程测试
- 业务接收标准测试
- 烟雾测试

### 方式 2: 使用操作层（推荐用于中等粒度测试）

```robot
*** Test Cases ***

搜索框交互测试
    [Documentation]    使用操作层编写的详细测试
    [Tags]    steps    interaction
    
    Steps.Init Browser    ${HEADLESS}
    Steps.Navigate To    ${BASE_URL}
    Steps.Wait For Element By Name    search_input    timeout=10
    Steps.Fill Input By Name    search_input    ${KEYWORD}
    Steps.Click Element By Name    search_button
    ${title}=    Steps.Get Page Title
    Should Contain    ${title}    ${KEYWORD}
    Steps.Close Browser
```

**适用场景**:
- 详细的用户交互测试
- 需要精细控制的场景
- 中间层测试

### 方式 3: 直接使用定位器层（用于验证定位器）

```robot
*** Test Cases ***

元素定位器验证
    [Documentation]    验证定位器层的有效性
    [Tags]    locators
    
    ${search_input}=    Locators.Get Locator    search_input
    Should Not Be Empty    ${search_input}
    Should Contain    ${search_input}    css=
```

**适用场景**:
- 定位器维护和验证
- 页面更新后的快速验证
- 自动化框架本身的测试

### 方式 4: 混合使用多层（复杂场景）

```robot
*** Test Cases ***

复杂业务流程测试
    [Documentation]    混合使用多层关键字
    [Tags]    integration
    
    # 使用功能层初始化
    Functional.Setup Browser And Navigate    ${BASE_URL}
    
    # 使用操作层进行控制
    Steps.Wait For Element By Name    search_input
    Steps.Fill Input By Name    search_input    robotframework
    Steps.Click Element By Name    search_button
    
    # 使用定位器验证
    ${button_loc}=    Locators.Get Locator    search_button
    Should Not Be Empty    ${button_loc}
    
    # 继续业务流程
    Steps.Wait For Element By Name    search_results
    
    # 清理
    Functional.Cleanup Browser
```

**适用场景**:
- 复杂的用户交互
- 需要多个独立步骤的场景
- 跨多个功能模块的流程

## 添加新的定位器和关键字

### 添加新定位器

编辑 `utils/robot_locators.py`:

```python
class Locators:
    # 现有定位器...
    
    # 添加新页面的定位器
    ADVANCED_SEARCH_LINK = "xpath=//a[contains(text(), 'Advanced Search')]"
    FILTER_CHECKBOX = "css=input.filter-checkbox"
    
    @keyword("Get Locator")
    def get_locator(self, element_name: str) -> str:
        locators_map = {
            # 现有映射...
            "advanced_search": self.ADVANCED_SEARCH_LINK,
            "filter": self.FILTER_CHECKBOX,
        }
        return locators_map.get(element_name.lower())
```

### 添加新操作关键字

编辑 `utils/robot_steps.py`:

```python
class StepsLibrary:
    # 现有代码...
    
    @keyword("Advanced Search With Filters")
    def advanced_search_with_filters(self, query: str, filters: list):
        """执行带过滤条件的高级搜索"""
        # 使用操作层关键字组合
        self.click_element_by_name("advanced_search_link")
        self.fill_input_by_name("search_box", query)
        
        for filter_name in filters:
            # 点击过滤器复选框
            locator = self.locators.get_locator(filter_name)
            self.helper.click(locator)
        
        self.click_element_by_name("search_button")
```

### 添加新功能关键字

编辑 `utils/robot_functional.py`:

```python
class FunctionalLibrary:
    # 现有代码...
    
    @keyword("Advanced Product Search")
    def advanced_product_search(self, category: str, price_range: str):
        """高级产品搜索业务流程"""
        self.steps.navigate_to_advanced_search()
        self.steps.select_category(category)
        self.steps.set_price_range(price_range)
        self.steps.execute_search()
        self.steps.verify_results_displayed()
```

## 运行测试

### 运行所有 Robot 测试

```bash
# 使用 Python 模块运行
python -m robot tests/robotframework/

# 或指定特定文件
python -m robot tests/robotframework/test_layered_architecture.robot

# 带标签过滤
python -m robot -i smoke tests/robotframework/

# 指定输出目录
python -m robot --outputdir reports/robotframework tests/robotframework/
```

### 运行 pytest 测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定类别
python -m pytest tests/ -m api
python -m pytest tests/ -m selenium
python -m pytest tests/ -m playwright

# 运行特定文件
python -m pytest tests/test_api_example.py
python -m pytest tests/test_playwright_advanced.py

# 带详细输出
python -m pytest tests/ -v --tb=short
```

### 使用 run_test.py 菜单

```bash
python run_test.py
```

菜单选项：
- 选项 1: 运行 pytest 测试
- 选项 2: 运行 Robot Framework 测试  
- 选项 3: 运行所有测试
- 选项 4: 退出

## 失败截图机制

当 Selenium 测试失败时，自动保存失败时的页面截图。

**位置**: `reports/selenium_screenshots/`

**文件名格式**: `failure_<test_name>.png`

### 自动捕获原理

在 `conftest.py` 中，pytest 钩子在测试失败时自动调用截图：

```python
@pytest.fixture(scope="function", autouse=True)
def selenium_failure_screenshot(request, selenium_driver):
    """自动为 Selenium 测试失败的情况生成截图"""
    yield
    
    if request.node.rep_call.failed:
        # 自动保存截图
        selenium_driver.driver.save_screenshot(...)
```

### 手动截图

```python
# 在测试中手动调用
def test_manual_screenshot(selenium_driver):
    selenium_driver.navigate_to("https://example.com")
    selenium_driver.take_screenshot("custom_screenshot.png")
```

## API 测试

### 使用 Robot Framework 运行 API 测试

```bash
python -m robot tests/robotframework/test_api.robot
```

### 使用 pytest 运行 API 测试

```bash
python -m pytest tests/test_api_example.py -m api
```

### API 测试特点

- 使用 `RequestsLibrary` 进行 HTTP 请求
- 支持 GET、POST、PUT、DELETE 等多种方法
- 集成请求头、查询参数、请求体等处理
- 包含错误处理和超时重试机制

## 性能测试

框架包含性能测试示例，测试：
- 页面加载时间
- API 响应时间
- 并发请求处理

```bash
# 运行性能测试
python -m pytest tests/test_playwright_advanced.py::TestPlaywrightPerformance -v
```

## 最佳实践

### 1. 定位器管理

✅ **DO**:
```python
# 集中定义定位器
SEARCH_INPUT = "css=input#search"

# 通过逻辑名称访问
get_locator("search_input")
```

❌ **DON'T**:
```python
# 分散定义定位器
css=input#search  # 在多个地方

# 硬编码定位器
self.helper.click("css=input#search")
```

### 2. 关键字编写

✅ **DO**:
```python
@keyword("Fill Login Credentials")
def fill_login_credentials(self, username: str, password: str):
    """填充登录信息的完整过程"""
    self.fill_input_by_name("username", username)
    self.fill_input_by_name("password", password)
```

❌ **DON'T**:
```python
# 过度细化
@keyword("Type Username")
def type_username(self, text):
    # 单个字段输入...
```

### 3. 测试用例组织

✅ **DO**:
```robot
*** Test Cases ***

完整搜索功能
    [Tags]    functional    smoke
    Functional.Complete Search Flow    ${KEYWORD}

搜索框交互
    [Tags]    steps    interaction
    Steps.Fill Input By Name    search_input    test
```

❌ **DON'T**:
```robot
*** Test Cases ***

测试 1
    # 混乱的操作序列

测试 2
    # 重复代码
```

### 4. 错误处理

✅ **DO**:
```python
def click_element_by_name(self, element_name):
    """点击元素，包含错误处理"""
    try:
        locator = self.locators.get_locator(element_name)
        self.helper.click(locator)
    except TimeoutException:
        logger.error(f"元素 {element_name} 未找到")
        raise
```

❌ **DON'T**:
```python
def click_element(self, locator):
    """无错误处理的点击操作"""
    self.helper.click(locator)
```

## 故障排除

### 问题 1: 定位器找不到元素

**原因**: 元素选择器不正确或元素加载延迟

**解决方案**:
```python
# 增加等待时间
self.steps.wait_for_element_by_name("element_name", timeout=30)

# 或检查定位器定义
locator = self.locators.get_locator("element_name")
print(f"使用的定位器: {locator}")
```

### 问题 2: 测试间歇性失败

**原因**: 网络延迟或资源加载时间不稳定

**解决方案**:
```python
# 增加隐式等待时间
self.steps.wait_for_element_by_name("element", timeout=15)

# 使用显式等待
self.helper.wait_for_selector(locator, timeout=20000)
```

### 问题 3: 截图路径错误

**原因**: 报告目录不存在

**解决方案**:
```bash
# 确保 reports 目录存在
mkdir -p reports/selenium_screenshots

# 检查 config/settings.py 中的 REPORTS_DIR 配置
```

## 报告和分析

### pytest 报告

```bash
# 生成详细的 HTML 报告
python -m pytest tests/ --html=reports/pytest_report.html

# 生成覆盖率报告
python -m pytest tests/ --cov=utils --cov-report=html
```

### Robot Framework 报告

```bash
# 报告自动保存在 --outputdir 指定的目录
python -m robot --outputdir reports/robotframework tests/robotframework/

# 查看报告
open reports/robotframework/report.html
```

### 失败截图查看

失败时的截图自动保存在：
```
reports/selenium_screenshots/failure_<test_name>.png
```

## 总结

这个分层测试架构提供了：

1. **清晰的关注点分离** - 定位器、操作、功能层分离
2. **高度的代码复用** - 关键字可复用于多个测试
3. **易于维护** - 页面修改只需更新定位器
4. **良好的可扩展性** - 添加新功能无需修改现有代码
5. **完善的错误追踪** - 自动失败截图和报告
6. **多种测试方法** - 支持 Robot、pytest、API 测试

按照这个架构编写测试用例，可以显著提高自动化效率和代码质量。
