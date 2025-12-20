# Robot Framework 定位器层 (Locator Layer)

## 📁 项目结构

```
tests/robotframework/locators/
├── login_page_locators.robot          # 登录页面定位器
├── inventory_page_locators.robot      # 商品列表页面定位器
├── cart_page_locators.robot           # 购物车页面定位器
├── checkout_page_locators.robot       # 结账页面定位器
├── all_locators.robot                 # 定位器索引（统一导入）
└── locator_usage_examples.robot       # 使用示例和最佳实践
```

## 🎯 目的

定位器层的设计目的是：
- **集中管理** 所有页面元素定位
- **降低维护成本** - 元素改变时只需更新定位器，不需修改测试代码
- **提高代码可读性** - 使用有意义的变量名替代复杂的选择器
- **便于复用** - 所有测试文件都可以共享同一套定位器

## 📋 定位器分类

### 1. 登录页面 (`login_page_locators.robot`)

| 定位器名称 | 用途 | 选择器 |
|-----------|------|--------|
| `${LOGIN_USERNAME_INPUT}` | 用户名输入框 | `id=user-name` |
| `${LOGIN_PASSWORD_INPUT}` | 密码输入框 | `id=password` |
| `${LOGIN_BUTTON}` | 登录按钮 | `id=login-button` |
| `${LOGIN_ERROR_MESSAGE}` | 错误提示信息 | `css:[data-test="error"]` |

### 2. 商品列表页面 (`inventory_page_locators.robot`)

| 定位器名称 | 用途 | 选择器 |
|-----------|------|--------|
| `${INVENTORY_LIST}` | 商品列表容器 | `css=.inventory_list` |
| `${INVENTORY_CONTAINER}` | 商品容器 | `css=.inventory_container` |
| `${ADD_TO_CART_BACKPACK}` | 背包购物车按钮 | `css=button[data-test="add-to-cart-..."]` |
| `${SHOPPING_CART_LINK}` | 购物车链接 | `css=a.shopping_cart_link` |

### 3. 购物车页面 (`cart_page_locators.robot`)

| 定位器名称 | 用途 | 选择器 |
|-----------|------|--------|
| `${CART_LIST}` | 购物车列表 | `css=.cart_list` |
| `${CHECKOUT_BUTTON}` | 结账按钮 | `css=button#checkout` |
| `${REMOVE_FROM_CART}` | 移除按钮 | `css=button[data-test*="remove"]` |

### 4. 结账页面 (`checkout_page_locators.robot`)

| 定位器名称 | 用途 | 选择器 |
|-----------|------|--------|
| `${CHECKOUT_FIRST_NAME_INPUT}` | 名字输入框 | `css=input#first-name` |
| `${CHECKOUT_LAST_NAME_INPUT}` | 姓氏输入框 | `css=input#last-name` |
| `${CHECKOUT_POSTAL_CODE_INPUT}` | 邮编输入框 | `css=input#postal-code` |
| `${CONTINUE_BUTTON}` | 继续按钮 | `css=button#continue` |
| `${CHECKOUT_SUMMARY_CONTAINER}` | 订单概览容器 | `css=.summary_info` |

## 💻 使用示例

### 方式 1：导入所有定位器

```robotframework
*** Settings ***
Resource    ./locators/all_locators.robot

*** Test Cases ***
使用定位器进行登录
    Input Text      ${LOGIN_USERNAME_INPUT}    standard_user
    Input Text      ${LOGIN_PASSWORD_INPUT}    secret_sauce
    Click Button    ${LOGIN_BUTTON}
```

### 方式 2：导入特定页面定位器

```robotframework
*** Settings ***
Resource    ./locators/login_page_locators.robot
Resource    ./locators/inventory_page_locators.robot

*** Test Cases ***
登录并添加商品
    Input Text      ${LOGIN_USERNAME_INPUT}    standard_user
    Click Button    ${LOGIN_BUTTON}
    Click Element    ${ADD_TO_CART_BACKPACK}
```

### 方式 3：在自定义关键字中使用

```robotframework
*** Keywords ***
使用凭证登录
    [Arguments]    ${username}    ${password}
    Input Text      ${LOGIN_USERNAME_INPUT}    ${username}
    Input Text      ${LOGIN_PASSWORD_INPUT}    ${password}
    Click Button    ${LOGIN_BUTTON}
```

## 🔄 维护和更新

### 当页面元素改变时

**仅需更新定位器文件，无需修改测试用例：**

```robotframework
# 更新前
${LOGIN_BUTTON}    id=login-button

# 如果元素选择器改变，只需在定位器文件中修改：
${LOGIN_BUTTON}    css=button.login-btn  # 新的选择器
```

所有引用 `${LOGIN_BUTTON}` 的测试用例自动使用新的选择器。

## 📊 最佳实践

1. **命名规范**
   - 使用清晰、有意义的变量名
   - 格式：`${PAGE_ELEMENT_NAME}` (大写 + 下划线)
   - 示例：`${LOGIN_USERNAME_INPUT}`、`${CHECKOUT_FIRST_NAME_INPUT}`

2. **组织结构**
   - 按页面分类定位器
   - 每个页面一个独立文件
   - 使用 `all_locators.robot` 统一导入

3. **定位策略**
   - 优先使用 `id` 属性（最稳定）
   - 其次使用 `data-test` 属性（自动化友好）
   - 避免使用 XPath（易变且复杂）

4. **复用性**
   - 对于多个产品的相似按钮，定义通用格式
   - 示例：
    ```robotframework
    ${ADD_TO_CART_PATTERN}    css=button[data-test="add-to-cart-{product}"]
    ```

## 🎓 快速开始

1. **查看现有定位器**
   ```bash
   cat tests/robotframework/locators/*.robot
   ```

2. **在测试中使用定位器**
   ```robot
   Resource    ./locators/all_locators.robot
   
   Input Text    ${LOGIN_USERNAME_INPUT}    username
   ```

3. **添加新定位器**
   - 找到对应的页面文件（如 `checkout_page_locators.robot`）
   - 添加新的定位器变量
   - 在测试中直接引用

## 📚 相关资源

- **测试用例**：[baidu_search.robot](../baidu_search.robot)
- **使用示例**：[locator_usage_examples.robot](./locator_usage_examples.robot)
- **数据文件**：[../resources/saucedemo_data.robot](../resources/saucedemo_data.robot)

## 🔗 页面对象模型（POM）

这个定位器层实现了 Page Object Model 的概念，提供了：
- 👤 **单一责任** - 每个文件负责一个页面
- 🔧 **易于维护** - 集中管理定位器
- 📖 **高可读性** - 清晰的变量名
- 🚀 **易于扩展** - 新增定位器无需修改测试

## ❓ 常见问题

**Q: 如果元素选择器改变了怎么办？**
A: 只需在对应的定位器文件中更新选择器，所有引用该定位器的测试会自动应用新的选择器。

**Q: 可以对定位器进行参数化吗？**
A: 可以。参考 `locator_usage_examples.robot` 中的示例，使用 `[Arguments]` 传递参数。

**Q: 如何处理动态元素（如列表中的某一项）？**
A: 定义包含占位符的模式，如：
```robot
${PRODUCT_BUTTON_PATTERN}    css=button[data-test="add-to-cart-{product_id}"]
```

**Q: 是否可以在 Playwright 和 Selenium 之间共享定位器？**
A: 可以。定位器语法（如 CSS、ID）在两者中都通用。
