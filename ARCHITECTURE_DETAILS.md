# 分层自动化测试框架 - 架构详解

## 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                     自动化测试框架总体架构                        │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                      UI 测试层 (UI Layer)                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Test Cases / Test Suites                    │   │
│  │  (测试用例 - 可以用 Robot Framework 或 Python 编写)    │   │
│  │  - 完整的购买流程                                       │   │
│  │  - 登录测试                                            │   │
│  │  - 搜索功能                                            │   │
│  └──────────────────────┬──────────────────────────────────┘   │
│                         │                                        │
│                         │ 使用                                   │
│                         ▼                                        │
│  ┌──────────────────────────────────────────────────────┐      │
│  │           Keywords / Business Operations             │      │
│  │  (关键字库 - 业务流程操作)                          │      │
│  │  - 登录 SauceDemo                                    │      │
│  │  - 添加产品到购物车                                 │      │
│  │  - 搜索                                              │      │
│  │  - 验证购物车数量                                    │      │
│  └──────────────────────┬──────────────────────────────┘      │
│                         │                                        │
│                         │ 使用                                   │
│                         ▼                                        │
│  ┌──────────────────────────────────────────────────────┐      │
│  │              Locators / UI Elements                   │      │
│  │  (定位器 - UI 元素选择器)                           │      │
│  │  - LOGIN_BUTTON = "id=login-button"                  │      │
│  │  - SEARCH_INPUT = "css=input#kw"                     │      │
│  │  - SHOPPING_CART_LINK = "id=shopping_cart_container"│      │
│  └──────────────────────┬──────────────────────────────┘      │
│                         │                                        │
│                         │ 选中                                   │
│                         ▼                                        │
│  ┌──────────────────────────────────────────────────────┐      │
│  │         Browser / Playwright Engine                  │      │
│  │  (浏览器引擎 - 实际执行交互)                        │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                      API 测试层 (API Layer)                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Test Cases / Test Suites                    │   │
│  │  (测试用例 - 可以用 Robot Framework 或 Python 编写)    │   │
│  │  - 获取用户列表                                        │   │
│  │  - 创建用户                                            │   │
│  │  - 登录验证                                            │   │
│  └──────────────────────┬──────────────────────────────────┘   │
│                         │                                        │
│                         │ 参考                                   │
│                         ▼                                        │
│  ┌──────────────────────────────────────────────────────┐      │
│  │          Config & Data Management                      │      │
│  │  (配置和数据管理)                                     │      │
│  │                                                        │      │
│  │  ┌────────────────┐         ┌────────────────┐       │      │
│  │  │ Config         │         │ Test Data      │       │      │
│  │  │ • API 端点     │         │ • 用户数据     │       │      │
│  │  │ • 环境配置     │         │ • 文章数据     │       │      │
│  │  │ • 期望结果     │         │ • 凭证         │       │      │
│  │  │ • HTTP 方法    │         │ • 查询参数     │       │      │
│  │  └────────────────┘         └────────────────┘       │      │
│  └──────────────────────┬──────────────────────────────┘      │
│                         │                                        │
│                         │ 使用                                   │
│                         ▼                                        │
│  ┌──────────────────────────────────────────────────────┐      │
│  │         HTTP Client / Requests Library                │      │
│  │  (HTTP 客户端 - 发送请求)                           │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

## UI 层详细设计

### 三层结构

```
Layer 3: Test Cases (测试层)
┌─────────────────────────────────────────┐
│  完整的购买流程                         │
│  ├─ 登录 SauceDemo                      │
│  ├─ 添加产品到购物车                   │
│  ├─ 前往购物车                         │
│  └─ 完成结账                           │
└──────────────┬──────────────────────────┘
               │
               │ 调用业务关键字
               │
Layer 2: Keywords (业务操作层)
┌──────────────┴──────────────────────────┐
│  SauceDemoKeywords                       │
│  ├─ @keyword("登录 SauceDemo")          │
│  │   ├─ input_text(SEARCH_INPUT, ...)   │
│  │   ├─ click(LOGIN_BUTTON)             │
│  │   └─ ...                              │
│  ├─ @keyword("添加产品到购物车")        │
│  │   ├─ query_selector_all(PRODUCT_ITEM)│
│  │   ├─ click(PRODUCT_ADD_BTN)          │
│  │   └─ ...                              │
│  └─ ...                                  │
└──────────────┬──────────────────────────┘
               │
               │ 使用定位器
               │
Layer 1: Locators (UI 元素层)
┌──────────────┴──────────────────────────┐
│  SauceDemoLocators                       │
│  ├─ LOGIN_USERNAME_INPUT = "id=user-name"
│  ├─ LOGIN_PASSWORD_INPUT = "id=password"
│  ├─ LOGIN_BUTTON = "id=login-button"    │
│  ├─ PRODUCT_ITEM = "css=.inventory_item"│
│  ├─ PRODUCT_ADD_BTN = "css=.btn_..."    │
│  └─ ...                                  │
└──────────────┬──────────────────────────┘
               │
               │ 通过 Playwright 执行
               │
Browser Automation Layer
┌──────────────┴──────────────────────────┐
│  Playwright Browser Engine               │
│  • Click elements                        │
│  • Input text                            │
│  • Wait for elements                     │
│  • Take screenshots                      │
└──────────────────────────────────────────┘
```

### 具体示例流程

```
Test Case: 完整的购买流程
    │
    ├─ 步骤1: 登录 SauceDemo (standard_user, secret_sauce)
    │   └─> SauceDemoKeywords.login_saucedemo()
    │       ├─ input_text(SauceDemoLocators.LOGIN_USERNAME_INPUT, ...)
    │       │  └─ page.fill("id=user-name", "standard_user")
    │       ├─ input_text(SauceDemoLocators.LOGIN_PASSWORD_INPUT, ...)
    │       │  └─ page.fill("id=password", "secret_sauce")
    │       └─ click(SauceDemoLocators.LOGIN_BUTTON)
    │          └─ page.click("id=login-button")
    │
    ├─ 步骤2: 添加产品到购物车 (0)
    │   └─> SauceDemoKeywords.add_product_to_cart(0)
    │       ├─ query_selector_all(SauceDemoLocators.PRODUCT_ITEM)
    │       │  └─ page.query_selector_all("css=.inventory_item")
    │       └─ click(products[0].query_selector(...))
    │          └─ page.click("css=.btn_primary.btn_inventory")
    │
    ├─ 步骤3: 验证购物车数量 (2)
    │   └─> SauceDemoKeywords.verify_cart_count(2)
    │       ├─ get_text(SauceDemoLocators.SHOPPING_CART_BADGE)
    │       │  └─ page.text_content("css=.shopping_cart_badge")
    │       └─ 比较: "2" == 2 ✓
    │
    └─ 步骤4: ...

关键点:
  • 定位器是 UI 元素的选择器字符串
  • 关键字是封装的操作函数
  • 测试用例通过调用关键字来组织测试流程
  • 这样做的好处:
    - 修改 UI 定位器时只需改 locators 文件
    - 业务流程在 keywords 文件中易于复用
    - 测试用例清晰易读
```

## API 层详细设计

### 四层结构

```
Layer 4: Test Cases (测试层)
┌────────────────────────────────────────┐
│  def test_get_users():                 │
│    url = "https://reqres.in/api/users" │
│    response = session.get(url, ...)    │
│    assert response.status_code == 200  │
│    assert 'data' in response.json()    │
└──────────┬───────────────────────────┬─┘
           │                           │
        参考配置                    参考数据
           │                           │
           ▼                           ▼
Layer 3: Config          Layer 2: Test Data
┌──────────────────────┐  ┌────────────────────┐
│ APITestCaseConfig    │  │ UserTestData       │
│                      │  │                    │
│ REQRES_USERS_GET = {│  │ NEW_USER = {       │
│   'method': 'GET'    │  │   'name': '...'    │
│   'endpoint': '/...''│  │   'job': '...'     │
│   'base_url': '...'  │  │ }                  │
│   'expected_status'  │  │                    │
│     : 200            │  │ VALID_LOGIN = {    │
│   'expected_fields'  │  │   'email': '...'   │
│     : [...]          │  │   'password': '...'
│ }                    │  │ }                  │
└──────────┬───────────┘  └────────────────────┘
           │                      │
           └──────────┬───────────┘
                      │
                      │ 组织测试请求
                      │
Layer 1: HTTP Client
┌──────────┴──────────────────────────────┐
│  requests.Session()                      │
│  • GET /api/users                        │
│  • POST /api/users (payload: NEW_USER)   │
│  • PUT /api/users/1 (payload: ...)       │
│  • DELETE /api/users/1                   │
│  • 验证响应状态码和内容                 │
└──────────────────────────────────────────┘
```

### 具体示例流程

```
Test Case: test_create_user()
    │
    ├─ 参考 Config
    │   APITestCaseConfig.REQRES_USER_CREATE
    │   {
    │     'name': '创建用户',
    │     'method': 'POST',
    │     'endpoint': '/api/users',
    │     'base_url': 'https://reqres.in',
    │     'expected_status': 201,
    │     'expected_fields': ['id', 'createdAt']
    │   }
    │
    ├─ 参考 Test Data
    │   UserTestData.NEW_USER
    │   {
    │     'name': 'John Doe',
    │     'job': 'Software Engineer'
    │   }
    │
    ├─ 构建请求
    │   POST https://reqres.in/api/users
    │   JSON: {
    │     'name': 'John Doe',
    │     'job': 'Software Engineer'
    │   }
    │
    ├─ 发送请求
    │   response = session.post(url, json=payload)
    │
    ├─ 验证响应
    │   assert response.status_code == 201 ✓
    │   assert 'id' in response.json() ✓
    │   assert 'createdAt' in response.json() ✓
    │
    └─ 测试通过

关键点:
  • Config 定义了 API 的 endpoint 和期望的响应
  • Test Data 定义了请求体和查询参数
  • 测试用例组合 Config 和 Data 来执行和验证 API
  • 这样做的好处:
    - 配置和数据分离易于维护
    - 同一个配置和数据可以被多个测试使用
    - 添加新的 API 测试只需添加配置和数据
```

## 文件映射关系

### UI 层映射

```
saucedemo_testsuite.robot
├─ Library: ../keywords/saucedemo_keywords.py
│  ├─ 导入: from ..locators.saucedemo_locators import SauceDemoLocators
│  │  └─ 使用: self.locators = SauceDemoLocators()
│  └─ 执行: @keyword("登录 SauceDemo")
│     └─ 使用定位器: self.page.fill(self.locators.LOGIN_USERNAME_INPUT, ...)
│
└─ Test Cases
   ├─ 完整的购买流程
   │  ├─ 登录 SauceDemo (keyword from saucedemo_keywords.py)
   │  ├─ 添加产品到购物车
   │  └─ ...
   └─ 仅登录测试
```

### API 层映射

```
reqres_api_testsuite.robot
├─ Variables
│  └─ ${REQRES_BASE_URL} = "https://reqres.in"
│
├─ Keywords
│  └─ 创建 API 会话 (Create Session)
│
└─ Test Cases
   ├─ 获取用户列表
   │  └─ GET On Session: /api/users?page=1
   │     参考: APIEndpoints.REQRES['users']
   │
   ├─ 创建用户
   │  ├─ payload = UserTestData.NEW_USER
   │  └─ POST On Session: /api/users
   │
   └─ 登录成功
      ├─ payload = UserTestData.VALID_LOGIN
      └─ POST On Session: /api/login
```

## 关键优势

### 1. 分离关注点 (Separation of Concerns)

```
定位器        关键字        测试用例
   │            │            │
   ├─ 只关心    ├─ 只关心    ├─ 只关心
   │  UI 元素   │  业务流程  │  测试场景
   │  的选择器  │           │
   │           │            │
   └─ 易于     └─ 易于      └─ 易于
      维护        复用        理解
```

### 2. 提高可维护性

```
场景1: UI 元素位置改变
  修改: saucedemo_locators.py
  影响: 只有一个地方需要改
  
场景2: 需要重复某个操作
  复用: 关键字已经定义，直接调用
  
场景3: 添加新的测试
  组合: 使用已有的关键字，快速构建新测试
```

### 3. 提高可读性

```
Robot Framework:
  登录 SauceDemo    standard_user    secret_sauce
  添加产品到购物车    0
  前往购物车

Python:
  keywords.login_saucedemo('standard_user', 'secret_sauce')
  keywords.add_product_to_cart(0)
  keywords.go_to_cart()
  
即使不了解实现细节，也能理解测试在做什么
```

### 4. 便于扩展

```
添加新的页面:
  1. 新建定位器文件 (xxx_locators.py)
  2. 新建关键字文件 (xxx_keywords.py)
  3. 新建测试套件 (xxx_testsuite.robot)
  
添加新的 API:
  1. 新建配置 (testcase_config.py)
  2. 新建数据 (xxx_data.py)
  3. 新建测试 (xxx_testsuite.robot)
  
都是按照相同的模式，学习曲线平缓
```

## 数据流向示意

### UI 测试数据流

```
Test Case
    │
    ├─> 调用关键字方法
    │   SauceDemoKeywords.login_saucedemo(username, password)
    │   │
    │   ├─> 获取定位器
    │   │   locators.LOGIN_USERNAME_INPUT
    │   │
    │   ├─> 执行基础操作
    │   │   BaseKeywords.input_text(locator, text)
    │   │   │
    │   │   └─> Playwright 执行
    │   │       page.fill("id=user-name", "standard_user")
    │   │
    │   └─> 返回结果
    │
    └─> 测试验证
        是否成功登录？
        ✓ 验证成功
```

### API 测试数据流

```
Test Case
    │
    ├─> 获取配置信息
    │   APITestCaseConfig.REQRES_USER_CREATE
    │   {endpoint: '/api/users', method: 'POST', expected_status: 201}
    │
    ├─> 获取测试数据
    │   UserTestData.NEW_USER
    │   {name: 'John Doe', job: 'Engineer'}
    │
    ├─> 组建请求
    │   POST https://reqres.in/api/users
    │   {name: 'John Doe', job: 'Engineer'}
    │
    ├─> 发送请求
    │   requests.post(url, json=data)
    │
    ├─> 获得响应
    │   {id: 123, name: 'John Doe', job: 'Engineer', createdAt: '...'}
    │
    └─> 验证响应
        状态码 201 ✓
        包含 id 字段 ✓
        包含 createdAt ✓
        测试通过
```

## 最佳实践总结

| 方面 | 最佳实践 | 说明 |
|------|--------|------|
| 定位器选择 | ID > Class > CSS Selector > XPath | 优先使用 ID，最后才用 XPath |
| 关键字设计 | 表达业务逻辑而非底层操作 | 好: `登录`, 坏: `点击按钮` |
| 测试用例 | 原子性、独立性 | 每个用例验证一个功能 |
| 测试数据 | 与测试逻辑分离 | 集中在 data 文件中管理 |
| 配置管理 | 支持多环境 | dev, staging, prod |

---

**版本**: 1.0  
**更新日期**: 2025-12-21
