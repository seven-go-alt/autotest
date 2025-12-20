# 分层测试框架 - 快速开始

## 目录结构

```
tests/
├── ui_layer/                    # UI 测试层
│   ├── locators/                # UI 元素定位器
│   ├── keywords/                # 业务操作关键字
│   ├── testsuites/              # 测试用例（Robot Framework）
│   └── test_ui_layer.py         # 测试用例（Python/pytest）
│
└── api_layer/                   # API 测试层
    ├── config/                  # API 配置和用例配置
    ├── data/                    # 测试数据
    ├── testsuites/              # 测试用例（Robot Framework）
    └── test_api_layer.py        # 测试用例（Python/pytest）
```

## 快速运行示例

### 运行 UI 测试 - SauceDemo

```bash
# Robot Framework
robot tests/ui_layer/testsuites/saucedemo_testsuite.robot

# Python/pytest
pytest tests/ui_layer/test_ui_layer.py::TestSauceDemoUI -v
```

### 运行 API 测试 - ReqRes

```bash
# Robot Framework
robot tests/api_layer/testsuites/reqres_api_testsuite.robot

# Python/pytest
pytest tests/api_layer/test_api_layer.py::TestReqResAPI -v
```

## 核心概念

### UI 层：三层架构

```
测试用例 (Test Cases)
    ↓ 调用
关键字库 (Keywords) - 业务流程
    ↓ 使用
定位器 (Locators) - UI 元素
```

**示例流程**:
```robot
*** Test Cases ***
完整的购买流程
    登录 SauceDemo    standard_user    secret_sauce     # 关键字
    添加产品到购物车    0
    前往结账
    # ...

*** Keywords ***
登录 SauceDemo    # 关键字定义
    Input Text    ${LOGIN_USERNAME_INPUT}    ${username}  # 使用定位器
    Input Text    ${LOGIN_PASSWORD_INPUT}    ${password}
    Click Button  ${LOGIN_BUTTON}
```

### API 层：四层架构

```
测试用例 (Test Cases)
    ↓ 使用
配置 (Config) - API 端点、期望结果
    ↓ 参考
测试数据 (Data) - 请求体、查询参数
```

**示例**:
```python
# 配置定义
REQRES_USER_CREATE = {
    'endpoint': '/api/users',
    'method': 'POST',
    'expected_status': 201
}

# 测试数据
NEW_USER = {'name': 'John Doe', 'job': 'Engineer'}

# 测试用例
def test_create_user():
    config = APITestCaseConfig.REQRES_USER_CREATE
    data = UserTestData.NEW_USER
    response = requests.post(config['endpoint'], json=data)
    assert response.status_code == config['expected_status']
```

## 关键文件说明

### UI 层关键文件

| 文件 | 说明 | 示例 |
|------|------|------|
| `base_locators.py` | 通用定位器（按钮、输入框等） | `LOGIN_BUTTON = "css=button#login"` |
| `saucedemo_locators.py` | SauceDemo 定位器 | `SHOPPING_CART_LINK = "id=shopping_cart_container"` |
| `base_keywords.py` | 基础操作关键字 | `open_browser()`, `click()`, `input_text()` |
| `saucedemo_keywords.py` | 业务操作关键字 | `login_saucedemo()`, `add_product_to_cart()` |
| `*_testsuite.robot` | 实际测试用例 | Robot Framework 格式的测试 |
| `test_ui_layer.py` | Python 格式测试用例 | pytest 格式的测试 |

### API 层关键文件

| 文件 | 说明 | 示例 |
|------|------|------|
| `api_config.py` | 环境、端点、认证配置 | `APIEndpoints.REQRES['users']` |
| `testcase_config.py` | 测试用例配置 | `REQRES_USER_CREATE['endpoint']` |
| `user_data.py` | 用户测试数据 | `NEW_USER = {'name': '...', 'job': '...'}` |
| `post_data.py` | 文章测试数据 | `NEW_POST = {'title': '...', 'body': '...'}` |
| `common_data.py` | 通用数据和工具 | `generate_user_data()`, `ErrorMessages` |
| `*_testsuite.robot` | Robot Framework 测试用例 | GET、POST、PUT、DELETE 等 |
| `test_api_layer.py` | Python/pytest 测试用例 | 类和方法形式的测试 |

## 添加新测试的步骤

### 添加新的 UI 测试（以新应用为例）

1. **创建定位器** (`tests/ui_layer/locators/newapp_locators.py`)
   ```python
   from .base_locators import BaseLocators
   
   class NewAppLocators(BaseLocators):
       ELEMENT_1 = "id=element1"
       ELEMENT_2 = "css=.element2"
   ```

2. **创建关键字** (`tests/ui_layer/keywords/newapp_keywords.py`)
   ```python
   from .base_keywords import BaseKeywords
   from ..locators.newapp_locators import NewAppLocators
   
   class NewAppKeywords(BaseKeywords):
       def __init__(self):
           super().__init__()
           self.locators = NewAppLocators()
       
       @keyword("我的业务操作")
       def my_business_operation(self):
           self.click(self.locators.ELEMENT_1)
           # 更多操作...
   ```

3. **创建测试套件** (`tests/ui_layer/testsuites/newapp_testsuite.robot`)
   ```robot
   *** Settings ***
   Library    ../keywords/newapp_keywords.py
   
   Suite Setup    打开浏览器    https://example.com
   Suite Teardown    关闭浏览器
   
   *** Test Cases ***
   我的测试
       我的业务操作
       验证元素存在    id=success
   ```

### 添加新的 API 测试（以新 API 为例）

1. **添加配置** (`tests/api_layer/config/testcase_config.py`)
   ```python
   NEW_API_TEST = {
       'name': '测试描述',
       'method': 'GET',
       'endpoint': '/api/endpoint',
       'base_url': 'https://api.example.com',
       'expected_status': 200
   }
   ```

2. **添加测试数据** (`tests/api_layer/data/mydata.py`)
   ```python
   class MyTestData:
       VALID_PAYLOAD = {'key': 'value'}
       INVALID_PAYLOAD = {}
   ```

3. **创建测试用例** (`tests/api_layer/testsuites/myapi_testsuite.robot`)
   ```robot
   *** Test Cases ***
   测试 API
       ${response}=    GET On Session    session    /api/endpoint
       Should Be Equal As Numbers    ${response.status_code}    200
   ```

   或在 `test_api_layer.py` 中添加：
   ```python
   def test_my_api():
       response = requests.get('https://api.example.com/api/endpoint')
       assert response.status_code == 200
   ```

## 常用命令

### Robot Framework

```bash
# 运行所有 UI 测试
robot tests/ui_layer/testsuites/

# 运行所有 API 测试
robot tests/api_layer/testsuites/

# 运行特定标签
robot --include smoke tests/

# 生成报告
robot --outputdir reports/ tests/
```

### pytest

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定文件
pytest tests/ui_layer/test_ui_layer.py -v

# 运行特定类或用例
pytest tests/ui_layer/test_ui_layer.py::TestSauceDemoUI::test_login_success -v

# 显示打印输出
pytest tests/ -v -s

# 生成覆盖率报告
pytest tests/ --cov=tests/ --cov-report=html
```

## 调试技巧

### UI 测试调试

```python
# 在 base_keywords.py 中添加
@keyword("打印调试信息")
def print_debug_info(self, message):
    logger.info(f"DEBUG: {message}")
    
@keyword("获取元素信息")
def get_element_info(self, locator):
    element = self.page.query_selector(locator)
    if element:
        logger.info(f"元素文本: {element.text_content()}")
        logger.info(f"元素属性: {element.get_attribute('class')}")
```

### API 测试调试

```python
# 打印响应详情
def test_api():
    response = requests.get('https://api.example.com/endpoint')
    print(f"状态码: {response.status_code}")
    print(f"响应头: {response.headers}")
    print(f"响应体: {response.json()}")
```

## 更多资源

- [完整结构指南](STRUCTURE_GUIDE.md) - 详细的架构说明
- [Playwright 文档](https://playwright.dev/)
- [Robot Framework 文档](https://robotframework.org/)
- [pytest 文档](https://docs.pytest.org/)

## 常见问题

**Q: 如何切换不同的环境？**
A: 编辑 `api_layer/config/api_config.py` 中的 `DEFAULT_ENV` 或在运行测试时传入环境变量。

**Q: 如何添加新的定位器？**
A: 在对应的 locators 文件中添加新的类属性，如 `NEW_ELEMENT = "css=..."` 

**Q: 定位器如何选择最佳的选择器？**
A: 优先级：ID > Class > CSS Selector > XPath。尽量选择稳定、不易变动的属性。

**Q: 如何并发运行测试？**
A: 使用 `pytest-xdist` 或 Robot Framework 的 `--processes` 参数。

---

**最后更新**: 2025-12-21
