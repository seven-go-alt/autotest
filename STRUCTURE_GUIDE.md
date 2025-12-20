# 自动化测试框架 - 分层结构

## 项目结构概览

```
tests/
├── ui_layer/                      # UI 测试层
│   ├── locators/                  # 定位器层
│   │   ├── __init__.py
│   │   ├── base_locators.py       # 基础定位器
│   │   ├── saucedemo_locators.py  # SauceDemo 定位器
│   │   └── baidu_locators.py      # 百度定位器
│   │
│   ├── keywords/                  # 关键字库（业务操作层）
│   │   ├── __init__.py
│   │   ├── base_keywords.py       # 基础关键字（浏览器操作）
│   │   ├── saucedemo_keywords.py  # SauceDemo 业务关键字
│   │   └── baidu_keywords.py      # 百度业务关键字
│   │
│   ├── testsuites/                # 测试套件
│   │   ├── __init__.py
│   │   ├── saucedemo_testsuite.robot
│   │   └── baidu_testsuite.robot
│   │
│   └── test_ui_layer.py           # Python 版本的 UI 测试
│
└── api_layer/                     # API 测试层
    ├── config/                    # 测试用例配置
    │   ├── __init__.py
    │   ├── api_config.py          # API 基础配置（环境、端点）
    │   └── testcase_config.py     # 测试用例详细配置
    │
    ├── data/                      # 测试数据
    │   ├── __init__.py
    │   ├── user_data.py           # 用户相关测试数据
    │   ├── post_data.py           # 文章相关测试数据
    │   └── common_data.py         # 通用测试数据和工具函数
    │
    ├── testsuites/                # 测试套件
    │   ├── __init__.py
    │   ├── reqres_api_testsuite.robot
    │   └── httpbin_api_testsuite.robot
    │
    └── test_api_layer.py          # Python 版本的 API 测试
```

## 分层设计说明

### UI 测试层结构

#### 1. 定位器层 (Locators)
- **用途**: 集中管理所有 UI 元素定位器
- **特点**:
  - 将定位器与测试逻辑分离
  - 易于维护和更新
  - 支持多个应用/网站

**文件说明**:
- `base_locators.py`: 通用元素定位器（按钮、输入框、提示信息等）
- `saucedemo_locators.py`: SauceDemo 应用特定的定位器
- `baidu_locators.py`: 百度搜索特定的定位器

```python
# 示例
from tests.ui_layer.locators.saucedemo_locators import SauceDemoLocators

locators = SauceDemoLocators()
# 使用定位器
page.click(locators.LOGIN_BUTTON)
```

#### 2. 关键字层 (Keywords)
- **用途**: 封装 UI 交互操作和业务流程
- **分为两级**:
  - **基础关键字** (base_keywords.py): 浏览器操作（点击、输入、等待等）
  - **业务关键字** (saucedemo_keywords.py 等): 应用特定的业务流程

**特点**:
- Robot Framework 和 Python 都支持
- 提供易读的操作名称
- 自动日志记录

```python
# 示例 - Robot Framework 风格
Login SauceDemo    standard_user    secret_sauce
Add Product To Cart    0
Verify Cart Count    1

# 示例 - Python 调用
keywords = SauceDemoKeywords()
keywords.login_saucedemo('standard_user', 'secret_sauce')
keywords.add_product_to_cart(0)
```

#### 3. 测试套件 (Test Suites)
- **用途**: 实际的测试用例
- **支持格式**:
  - Robot Framework (.robot 文件)
  - Python (pytest)

**文件示例**:
- `saucedemo_testsuite.robot`: SauceDemo 电商流程测试
- `baidu_testsuite.robot`: 百度搜索功能测试
- `test_ui_layer.py`: Python 版本的 UI 测试

---

### API 测试层结构

#### 1. 配置层 (Config)
- **用途**: 集中管理 API 配置和测试用例配置

**文件说明**:
- `api_config.py`: 
  - API 基础配置（环境、端点、认证等）
  - HTTP 方法枚举
  - 响应状态码常量
  - 支持多环境配置

- `testcase_config.py`:
  - 各个 API 测试用例的详细配置
  - 期望的响应状态和字段
  - 请求参数等

```python
# 示例
config = APITestCaseConfig.REQRES_USER_CREATE
print(config['method'])        # 'POST'
print(config['endpoint'])      # '/api/users'
print(config['expected_status'])  # 201
```

#### 2. 数据层 (Data)
- **用途**: 管理所有测试数据
- **特点**:
  - 将测试数据与测试逻辑分离
  - 支持数据生成函数
  - 便于数据维护和管理

**文件说明**:
- `user_data.py`: 用户相关的测试数据（登录凭证、用户对象等）
- `post_data.py`: 文章相关的测试数据
- `common_data.py`: 通用数据和工具函数

```python
# 示例
from tests.api_layer.data.user_data import UserTestData

payload = UserTestData.NEW_USER  # {'name': 'John Doe', 'job': '...'}
```

#### 3. 测试套件 (Test Suites)
- **用途**: 实际的 API 测试用例
- **支持格式**:
  - Robot Framework (.robot 文件)
  - Python (pytest)

**文件示例**:
- `reqres_api_testsuite.robot`: ReqRes API 测试
- `httpbin_api_testsuite.robot`: HTTPBin API 测试
- `test_api_layer.py`: Python 版本的 API 测试

---

## 使用示例

### 运行 UI 测试

#### Robot Framework
```bash
# 运行所有 UI 测试
robot tests/ui_layer/testsuites/

# 运行特定的测试套件
robot tests/ui_layer/testsuites/saucedemo_testsuite.robot

# 运行特定的测试用例
robot --test "完整的购买流程" tests/ui_layer/testsuites/saucedemo_testsuite.robot

# 运行特定标签的测试
robot --include smoke tests/ui_layer/testsuites/
```

#### Python/pytest
```bash
# 运行所有 UI 测试
pytest tests/ui_layer/test_ui_layer.py -v

# 运行特定的测试类
pytest tests/ui_layer/test_ui_layer.py::TestSauceDemoUI -v

# 运行特定的测试用例
pytest tests/ui_layer/test_ui_layer.py::TestSauceDemoUI::test_login_success -v
```

### 运行 API 测试

#### Robot Framework
```bash
# 运行所有 API 测试
robot tests/api_layer/testsuites/

# 运行特定的测试套件
robot tests/api_layer/testsuites/reqres_api_testsuite.robot

# 运行特定标签的测试
robot --include smoke tests/api_layer/testsuites/
```

#### Python/pytest
```bash
# 运行所有 API 测试
pytest tests/api_layer/test_api_layer.py -v

# 运行特定的测试类
pytest tests/api_layer/test_api_layer.py::TestReqResAPI -v

# 运行特定的测试用例
pytest tests/api_layer/test_api_layer.py::TestReqResAPI::test_get_users -v
```

---

## 扩展指南

### 添加新的 UI 测试应用

1. **在 locators 目录下创建定位器文件**
   ```python
   # tests/ui_layer/locators/myapp_locators.py
   from .base_locators import BaseLocators
   
   class MyAppLocators(BaseLocators):
       # 定义应用特定的定位器
       LOGIN_BUTTON = "css=button#login"
       # ...
   ```

2. **在 keywords 目录下创建关键字库**
   ```python
   # tests/ui_layer/keywords/myapp_keywords.py
   from .base_keywords import BaseKeywords
   from ..locators.myapp_locators import MyAppLocators
   
   class MyAppKeywords(BaseKeywords):
       def __init__(self):
           super().__init__()
           self.locators = MyAppLocators()
       
       @keyword("登录")
       def login(self, username, password):
           # 实现登录逻辑
           pass
   ```

3. **创建测试套件**
   ```robot
   # tests/ui_layer/testsuites/myapp_testsuite.robot
   *** Settings ***
   Library    ../keywords/myapp_keywords.py
   
   *** Test Cases ***
   测试用例
       登录    user    pass
       # ...
   ```

### 添加新的 API 测试

1. **在 config 目录下添加配置**
   ```python
   # tests/api_layer/config/testcase_config.py
   MYAPI_ENDPOINT = {
       'name': '获取数据',
       'method': 'GET',
       'endpoint': '/api/data',
       'expected_status': 200
   }
   ```

2. **在 data 目录下添加测试数据**
   ```python
   # tests/api_layer/data/mydata.py
   class MyTestData:
       VALID_PAYLOAD = {...}
       INVALID_PAYLOAD = {...}
   ```

3. **创建测试套件**
   ```robot
   # tests/api_layer/testsuites/myapi_testsuite.robot
   或
   # tests/api_layer/test_api_layer.py 中添加测试类
   ```

---

## 最佳实践

### UI 测试层
1. ✅ 定位器应该尽可能稳定和易维护（优先使用 ID > Class > CSS Selector > XPath）
2. ✅ 关键字应该表达业务逻辑而不是低级操作
3. ✅ 避免在测试用例中硬编码等待时间，使用显式等待
4. ✅ 使用描述性的测试用例名称

### API 测试层
1. ✅ 将配置、数据、测试逻辑分离
2. ✅ 使用配置文件管理不同环境的 API 端点
3. ✅ 验证响应的状态码、字段、数据类型
4. ✅ 使用装置(fixtures)管理前置和清理工作
5. ✅ 参数化测试以覆盖多个场景

### 通用
1. ✅ 添加适当的文档和注释
2. ✅ 使用有意义的标签分类测试
3. ✅ 定期审查和重构测试代码
4. ✅ 保持测试的独立性和原子性

---

## 相关技术栈

- **UI 测试**: Playwright, Robot Framework, pytest
- **API 测试**: requests, Robot Framework (RequestsLibrary), pytest
- **测试运行**: pytest, Robot Framework
- **报告生成**: pytest-html, Robot Framework 内置报告
- **CI/CD 集成**: Jenkins, GitHub Actions 等

---

## 更新历史

- **2025-12-21**: 初始化分层结构设计
  - 创建 UI 层（定位器、关键字、测试套件）
  - 创建 API 层（配置、数据、测试套件）
  - 支持 Robot Framework 和 Python 双框架
  - 完整的示例和文档
