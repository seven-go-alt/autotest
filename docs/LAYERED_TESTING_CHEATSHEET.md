# 分层测试架构快速参考

## 核心概念速览

| 层级 | 文件 | 职责 | 示例 |
|------|------|------|------|
| **定位器层** | `robot_locators.py` | 定义元素定位器 | `SEARCH_INPUT = "css=input#q"` |
| **操作层** | `robot_steps.py` | 原子 UI 操作 | `Fill Input By Name "search_input"` |
| **功能层** | `robot_functional.py` | 业务流程 | `Complete Search Flow "pytest"` |
| **辅助层** | `*_helper.py` | 驱动程序包装 | `PlaywrightHelper`, `SeleniumHelper` |

## 常用关键字速查

### 初始化和导航

```robot
# 初始化浏览器
Steps.Init Browser    headless=True

# 导航到 URL
Steps.Navigate To    https://www.python.org

# 关闭浏览器
Steps.Close Browser
```

### 元素操作

```robot
# 点击元素
Steps.Click Element By Name    search_button

# 填充输入框
Steps.Fill Input By Name    search_input    pytest

# 等待元素出现
Steps.Wait For Element By Name    search_results    timeout=15

# 获取元素文本
${text}=    Steps.Get Element Text By Name    result_title
```

### 页面信息

```robot
# 获取页面标题
${title}=    Steps.Get Page Title

# 获取页面 URL
${url}=    Steps.Get Page URL

# 截图
${path}=    Steps.Take Screenshot    page.png
```

### 定位器操作

```robot
# 获取定位器
${locator}=    Locators.Get Locator    search_input

# 验证定位器
Should Not Be Empty    ${locator}
Should Contain    ${locator}    css=
```

### 功能流程

```robot
# 完整搜索流程
Functional.Complete Search Flow    robotframework

# 设置浏览器并导航
Functional.Setup Browser And Navigate    ${BASE_URL}

# 验证搜索结果
Functional.Verify Search Result    pytest

# 清理浏览器
Functional.Cleanup Browser
```

## 快速测试编写模板

### 模板 1：简单功能测试

```robot
*** Test Cases ***

简单功能测试
    [Tags]    smoke
    Functional.Complete Search Flow    ${KEYWORD}
```

### 模板 2：详细交互测试

```robot
*** Test Cases ***

详细交互测试
    [Tags]    interaction
    Steps.Init Browser
    Steps.Navigate To    ${BASE_URL}
    Steps.Fill Input By Name    search_input    pytest
    Steps.Click Element By Name    search_button
    Steps.Wait For Element By Name    results
    ${title}=    Steps.Get Page Title
    Should Contain    ${title}    Python
    Steps.Close Browser
```

### 模板 3：混合多层测试

```robot
*** Test Cases ***

混合多层测试
    [Tags]    integration
    
    # 功能层初始化
    Functional.Setup Browser And Navigate    ${BASE_URL}
    
    # 操作层细节控制
    Steps.Fill Input By Name    search_input    robotframework
    Steps.Click Element By Name    search_button
    
    # 定位器验证
    ${locator}=    Locators.Get Locator    search_button
    Should Contain    ${locator}    css=
    
    # 继续操作
    Steps.Wait For Element By Name    results
    
    # 功能层清理
    Functional.Cleanup Browser
```

## pytest 快速参考

### 运行命令

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定标记
python -m pytest tests/ -m api        # API 测试
python -m pytest tests/ -m selenium   # Selenium 测试
python -m pytest tests/ -m playwright # Playwright 测试

# 运行特定文件
python -m pytest tests/test_api_example.py

# 详细输出
python -m pytest tests/ -v

# 显示打印输出
python -m pytest tests/ -s

# 快速失败（第一个失败即停止）
python -m pytest tests/ -x

# 仅运行失败的测试
python -m pytest tests/ --lf
```

### pytest 测试示例

```python
@pytest.mark.api
@pytest.mark.smoke
def test_api_get_request():
    """API GET 请求测试"""
    response = requests.get("https://httpbin.org/ip")
    assert response.status_code == 200

@pytest.mark.selenium
def test_selenium_navigation(selenium_driver):
    """Selenium 导航测试"""
    selenium_driver.navigate_to("https://www.python.org")
    assert "Python" in selenium_driver.get_title()

@pytest.mark.playwright
def test_playwright_screenshot(playwright_page):
    """Playwright 截图测试"""
    playwright_page.navigate_to("https://www.python.org")
    playwright_page.take_screenshot("page.png")
```

## Robot Framework 快速参考

### 运行命令

```bash
# 运行所有 Robot 测试
python -m robot tests/robotframework/

# 运行特定文件
python -m robot tests/robotframework/test_layered_architecture.robot

# 运行指定标签
python -m robot -i smoke tests/robotframework/
python -m robot -i functional tests/robotframework/

# 指定输出目录
python -m robot --outputdir reports/robotframework tests/robotframework/

# 生成报告
python -m robot -d reports/robotframework tests/robotframework/
```

### Robot Framework 测试变量

```robot
*** Variables ***
${BASE_URL}    https://www.python.org
${SEARCH_KEYWORD}    pytest
${HEADLESS}    True
${TIMEOUT}    30

*** Test Cases ***
使用变量的测试
    Functional.Setup Browser And Navigate    ${BASE_URL}
    Steps.Fill Input By Name    search_input    ${SEARCH_KEYWORD}
    Steps.Wait For Element By Name    results    timeout=${TIMEOUT}
```

## API 测试快速参考

### REST 操作

```robot
# GET 请求
${response}=    GET    ${API_BASE_URL}/ip

# POST 请求
${payload}=    Create Dictionary    name=Test    age=25
${response}=    POST    ${API_BASE_URL}/post    json=${payload}

# PUT 请求
${response}=    PUT    ${API_BASE_URL}/put    json=${payload}

# DELETE 请求
${response}=    DELETE    ${API_BASE_URL}/delete

# 验证响应
Should Be Equal As Numbers    ${response.status_code}    200
Should Contain    ${response.json()}    key_name
```

### Python requests 库

```python
import requests

# GET
response = requests.get("https://httpbin.org/ip")

# POST
response = requests.post(
    "https://httpbin.org/post",
    json={"name": "Test"}
)

# 请求头
headers = {"Authorization": "Bearer token"}
response = requests.get(url, headers=headers)

# 查询参数
params = {"page": 1, "limit": 10}
response = requests.get(url, params=params)

# 验证
assert response.status_code == 200
data = response.json()
```

## 故障排除速查

| 问题 | 可能原因 | 解决方案 |
|------|--------|--------|
| 元素找不到 | 定位器错误或加载延迟 | 检查定位器，增加等待时间 |
| 超时异常 | 资源加载太慢 | 增加 timeout 参数 |
| 截图文件夹不存在 | 目录未创建 | `mkdir -p reports/selenium_screenshots` |
| 测试间歇性失败 | 网络不稳定 | 增加隐式/显式等待时间 |
| 模块导入错误 | 路径问题 | 检查 Python 路径和导入语句 |

## 文件位置速查

```
autotest/
├── tests/
│   ├── test_api_example.py           # API 测试
│   ├── test_selenium_example.py      # Selenium 测试
│   ├── test_playwright_example.py    # Playwright 基础测试
│   ├── test_playwright_advanced.py   # Playwright 高级测试
│   └── robotframework/
│       ├── test_layered_architecture.robot  # 分层架构演示
│       ├── test_api.robot                   # API 测试
│       └── baidu_search.robot               # 搜索测试
├── utils/
│   ├── robot_locators.py             # 定位器层
│   ├── robot_steps.py                # 操作层
│   ├── robot_functional.py           # 功能层
│   ├── playwright_helper.py          # Playwright 助手
│   └── selenium_helper.py            # Selenium 助手
├── reports/
│   ├── pytest_report.html            # pytest 报告
│   ├── selenium_screenshots/         # 失败截图
│   └── robotframework/               # Robot 报告
├── conftest.py                       # pytest 配置
├── run_test.py                       # 测试菜单脚本
├── pytest.ini                        # pytest 配置文件
└── docs/
    ├── LAYERED_TESTING_GUIDE.md      # 详细指南
    └── LAYERED_TESTING_CHEATSHEET.md # 本文件
```

## 快速开始步骤

### 1. 安装依赖
```bash
pip install -r requirements.txt
playwright install
```

### 2. 编写测试

选择合适的层级编写测试：
- **功能层**: 完整用户流程
- **操作层**: 详细交互步骤
- **定位器层**: 验证定位器

### 3. 运行测试

```bash
# 使用菜单
python run_test.py

# 或直接运行
python -m pytest tests/
python -m robot tests/robotframework/
```

### 4. 查看报告

- **pytest**: `reports/pytest_report.html`
- **Robot**: `reports/robotframework/report.html`
- **截图**: `reports/selenium_screenshots/`

## 关键概念

### 定位器定义规范

```python
# CSS 选择器
BUTTON = "css=button.submit"

# XPath
LINK = "xpath=//a[contains(text(), 'Search')]"

# ID
INPUT = "id=search-box"
```

### 关键字命名规范

```robot
# 操作层：动词 + 对象 + 修饰符
Click Element By Name
Fill Input By Name
Wait For Element By Name

# 功能层：业务动词 + 业务对象
Complete Search Flow
Verify Search Result
Setup Browser And Navigate
```

### 测试标签规范

```robot
[Tags]    functional     # 测试层级
[Tags]    smoke          # 测试类型
[Tags]    high_priority  # 优先级
[Tags]    robot          # 框架类型
```

## 扩展阅读

- **详细指南**: 见 `docs/LAYERED_TESTING_GUIDE.md`
- **CI/CD 配置**: 见 `docs/CI.md`
- **快速开始**: 见 `QUICKSTART.md`
- **贡献指南**: 见 `CONTRIBUTING.md`

---

**最后更新**: 2024-01-01  
**框架版本**: 1.0  
**维护者**: autotest team
