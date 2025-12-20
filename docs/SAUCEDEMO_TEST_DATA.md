# SauceDemo 测试数据指南

## 概述

本项目为 **SauceDemo** 网站（https://www.saucedemo.com/）提供了完整的测试数据集，包含所有官方测试账户、产品数据和结账信息。

## 📋 登录用户数据

所有用户的密码均为：**`secret_sauce`**

### 1. **标准用户** (`standard_user`)
- **用途**：正常的功能测试
- **特点**：完全正常的购物体验
- **使用场景**：所有主流程测试（登录、浏览、购物、结账）

### 2. **被锁定用户** (`locked_out_user`)
- **用途**：验证登录失败处理
- **特点**：登录时显示错误提示："Epic sadface: Sorry, this user has been locked out."
- **使用场景**：错误处理、安全验证测试

### 3. **问题用户** (`problem_user`)
- **用途**：测试渲染问题处理
- **特点**：页面元素可能加载不正常，图片可能不显示
- **使用场景**：兼容性测试、容错能力验证

### 4. **性能问题用户** (`performance_glitch_user`)
- **用途**：测试性能缓慢的场景
- **特点**：页面加载会显著延迟（模拟网络慢）
- **使用场量**：超时处理、性能测试、超时重试逻辑验证
- **建议超时时间**：> 30 秒

### 5. **错误用户** (`error_user`)
- **用途**：测试后端错误处理
- **特点**：某些操作会返回 500 错误
- **使用场景**：异常处理、错误提示验证

### 6. **可视问题用户** (`visual_user`)
- **用途**：测试界面差异
- **特点**：页面样式/布局与其他用户不同
- **使用场景**：视觉回归测试、截图对比

## 📦 产品数据

| 产品 ID | 产品名称 | 价格 | Test ID |
|--------|--------|------|---------|
| `sauce_labs_backpack` | Sauce Labs Backpack | $29.99 | `add-to-cart-sauce-labs-backpack` |
| `sauce_labs_bike_light` | Sauce Labs Bike Light | $9.99 | `add-to-cart-sauce-labs-bike-light` |
| `sauce_labs_bolt_t_shirt` | Sauce Labs Bolt T-Shirt | $15.99 | `add-to-cart-sauce-labs-bolt-t-shirt` |
| `sauce_labs_fleece_jacket` | Sauce Labs Fleece Jacket | $49.99 | `add-to-cart-sauce-labs-fleece-jacket` |
| `sauce_labs_onesie` | Sauce Labs Onesie | $7.99 | `add-to-cart-sauce-labs-onesie` |
| `test_all_products_are_expensive` | Test.allProductsAreExpensive | $0 | `add-to-cart-test-allProductsAreExpensive` |

## 📝 结账信息

### 标准结账数据
```
名：Auto
姓：Tester
邮编：12345
```

### 备选结账数据
```
名：John
姓：Doe
邮编：98765
```

## 🔄 排序选项

| 选项 | 标签 | 值 |
|-----|------|-----|
| A 到 Z | Name (A to Z) | `az` |
| Z 到 A | Name (Z to A) | `za` |
| 低到高 | Price (low to high) | `lohi` |
| 高到低 | Price (high to low) | `hilo` |

## 📂 文件位置

### Python 数据文件
- **UI 层数据**：`tests/ui_layer/data/saucedemo_users.py`
  - `SauceDemoUsers` 类：所有用户信息
  - `SauceDemoCheckoutData` 类：结账表单数据

- **pytest 测试配置**：`tests/test_UI/saucedemo_config.py`
  - 常量定义（URL、凭证、产品数据等）
  - 适合 pytest 直接导入使用

### Robot Framework 资源文件
- **Robot 数据资源**：`tests/resources/saucedemo_data.robot`
  - 变量定义（${SAUCEDEMO_STANDARD_USER} 等）
  - `获取用户凭证` 关键字

### Robot Framework 测试文件
- **测试套件**：`tests/robotframework/baidu_search.robot`
  - 引入所有测试数据资源
  - 包含 6 个用户场景的测试用例

## 💻 使用示例

### Python (pytest) 中使用

```python
from tests.test_UI.saucedemo_config import VALID_USER, LOCKED_OUT_USER, PRODUCTS

def test_login_with_standard_user():
    username = VALID_USER['username']  # 'standard_user'
    password = VALID_USER['password']  # 'secret_sauce'
    # ... 测试代码

def test_login_with_locked_user():
    username = LOCKED_OUT_USER['username']  # 'locked_out_user'
    # ... 测试代码
```

### Python (UI 层) 中使用

```python
from tests.ui_layer.data.saucedemo_users import SauceDemoUsers, SauceDemoCheckoutData

user = SauceDemoUsers.STANDARD_USER
print(user['username'])  # 'standard_user'

checkout = SauceDemoCheckoutData.STANDARD_CHECKOUT
print(checkout['first_name'])  # 'Auto'
```

### Robot Framework 中使用

```robotframework
*** Test Cases ***
使用标准用户登录
    [Documentation]    使用测试数据登录
    Open Browser    ${SAUCEDEMO_BASE_URL}    chrome
    Input Text      id=user-name    ${SAUCEDEMO_STANDARD_USER}
    Input Text      id=password     ${SAUCEDEMO_COMMON_PASSWORD}
    Click Button    id=login-button
    
验证被锁定用户的错误提示
    Open Browser    ${SAUCEDEMO_BASE_URL}    chrome
    Input Text      id=user-name    ${SAUCEDEMO_LOCKED_USER}
    Input Text      id=password     ${SAUCEDEMO_LOCKED_PASSWORD}
    Click Button    id=login-button
    Page Should Contain    Epic sadface
```

## 🎯 推荐的测试场景覆盖

| 场景 | 用户 | 标签 | 优先级 |
|-----|------|------|--------|
| 正常登录并购物 | standard_user | smoke | 高 |
| 锁定用户错误处理 | locked_out_user | regression | 高 |
| 页面加载缓慢 | performance_glitch_user | performance | 中 |
| 渲染问题处理 | problem_user | compatibility | 中 |
| 后端错误处理 | error_user | error-handling | 中 |
| 视觉差异验证 | visual_user | visual | 低 |

## 🔗 相关资源

- **SauceDemo 官网**：https://www.saucedemo.com/
- **SauceDemo 文档**：https://github.com/saucelabs/sample-app-web
- **测试报告**：见 `reports/` 目录

## 📌 常见问题

### Q: 我应该如何快速测试所有 6 个用户？
**A**：运行以下命令：
```bash
python3 -m robot tests/robotframework/baidu_search.robot
```
这将自动运行所有 6 个用户的测试用例。

### Q: 性能问题用户需要设置多长的超时时间？
**A**：建议设置 **30 秒或以上**。参考：`tests/robotframework/baidu_search.robot` 中的 `性能问题用户登录验证` 测试用例。

### Q: 如何在 pytest 中使用参数化测试所有用户？
**A**：参考 `tests/test_UI/saucedemo_config.py` 的 `ALL_TEST_USERS` 列表，使用 pytest 的 `@pytest.mark.parametrize` 装饰器。

### Q: 这些数据是否可以离线使用？
**A**：否，这些是官方 SauceDemo 网站的账户。需要网络连接才能访问网站。
