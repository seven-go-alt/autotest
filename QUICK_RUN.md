# 快速运行指南

## 运行方式

### 方式 1：命令行参数模式（推荐用于 CI/CD 或精确控制）

#### 运行新的 UI 测试（ui_tests/）
```bash
# 运行所有 UI 测试（P0 用户模块）
python3 run_tests.py --test-type ui --env dev --browser chrome --tags "P0ANDuser"

# 运行所有 UI 测试（不限标签）
python3 run_tests.py --test-type ui --env dev --browser chrome

# 运行指定测试套件
python3 run_tests.py --test-type ui --env dev --browser chrome --suite ui_tests/testsuites/user/user_login_tests.robot

# 无头模式运行
python3 run_tests.py --test-type ui --env dev --browser chrome --headless --tags "P0"
```

#### 运行 API 测试（api_tests/）
```bash
python3 run_tests.py --test-type api --env dev
```

### 方式 2：交互式菜单模式（适合本地开发调试）

直接运行脚本，进入交互式菜单：
```bash
python3 run_tests.py
```

菜单选项：
- 1) pytest (Selenium)
- 2) pytest (Playwright)
- 3) pytest (API)
- 4) pytest (全部)
- 5) Robot Framework（运行 tests/robotframework/ 下的旧测试）
- 6) 全部运行
- 0) 退出

## 测试分层结构

项目采用分层关键字设计：

```
ui_tests/
  keywords/
    function_layer/     # 函数层：封装 Selenium 原子操作
      web_functions.robot
    pages_layer/        # 页面层：按页面组织的关键字
      login_page.robot
    process_layer/      # 流程层：端到端业务流程
      user_flows.robot
  testsuites/           # 用例层：测试用例，只调用流程层关键字
    user/
      user_login_tests.robot
```

## 标签使用

测试用例使用标签进行分类：

- **等级标签**：`P0`（核心功能）、`P1`（重要功能）、`P2`（边界/异常）
- **业务模块**：`user`、`order`、`product` 等
- **功能标签**：`login`、`create`、`search` 等
- **平台标签**：`pc`、`mobile`

### 标签过滤示例

```bash
# 只运行 P0 级别的用户相关测试
--tags "P0ANDuser"

# 运行 PC 端的用户登录测试
--tags "userANDloginANDpc"

# 排除不稳定测试
--exclude "flaky"
```

## 环境配置

环境配置通过 `config/settings.py` 和 `--env` 参数管理：

- `dev`：开发环境（默认）
- `test`：测试环境
- `stage`：预发布环境
- `prod`：生产环境

环境变量设置（可选）：
```bash
export DEV_BASE_URL="https://dev.example.com"
export TEST_BASE_URL="https://test.example.com"
```

## 报告位置

- Robot Framework 报告：`tmp/` 或 `reports/robotframework/`
  - `report.html` - 测试报告
  - `log.html` - 详细日志
  - `output.xml` - XML 格式输出

- pytest 报告：`tmp/`
  - `pytest_*.html` - HTML 报告

## 常见问题

### 1. 关键字冲突
如果遇到 "Multiple keywords with name 'XXX' found" 错误，在关键字前加上库名前缀：
```robotframework
SeleniumLibrary.Input Text    id=username    ${username}
```

### 2. 变量未定义
确保在测试文件中引入必要的资源文件：
```robotframework
Resource    ../../../tests/resources/saucedemo_data.robot
```

### 3. 浏览器驱动问题
确保已安装浏览器驱动，或使用 webdriver-manager（SeleniumLibrary 会自动处理）。

## 验证安装

检查环境是否正确配置：
```bash
# 检查 Robot Framework
python3 -m robot --version

# 检查 Selenium
python3 -c "import selenium; print(selenium.__version__)"

# 语法检查（dryrun）
python3 -m robot --dryrun ui_tests/testsuites/user/user_login_tests.robot
```

