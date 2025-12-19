# 自动化测试框架

一个基于 Robot Framework、pytest、Selenium 和 Playwright 的综合测试框架，用于学习和实践自动化测试。

## 📋 框架特性

- **多框架支持**: 同时支持 pytest 和 Robot Framework
- **多浏览器引擎**: 支持 Selenium 和 Playwright
- **灵活配置**: 通过环境变量和配置文件管理测试环境
- **丰富的工具类**: 封装常用操作，提高测试编写效率
- **完善的报告**: 支持 HTML 报告和多种报告格式

## 🏗️ 项目结构

```
autotest/
├── config/                 # 配置文件目录
│   ├── __init__.py
│   └── settings.py        # 测试配置
├── utils/                 # 工具类目录
│   ├── __init__.py
│   ├── selenium_helper.py # Selenium 工具类
│   └── playwright_helper.py # Playwright 工具类
├── tests/                 # 测试用例目录
│   ├── __init__.py
│   ├── test_selenium_example.py  # pytest Selenium 示例
│   ├── test_playwright_example.py # pytest Playwright 示例
│   ├── robotframework/    # Robot Framework 测试
│   │   └── baidu_search.robot
│   └── resources/         # Robot Framework 资源文件
│       └── common.robot
├── reports/               # 测试报告目录（自动生成）
├── logs/                  # 日志目录（自动生成）
├── requirements.txt       # Python 依赖
├── pytest.ini            # pytest 配置
├── robotframework.ini    # Robot Framework 配置
├── conftest.py           # pytest fixtures
├── run_tests.sh          # 测试运行脚本
└── README.md             # 项目说明

```

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- pip
- 操作系统: Windows/macOS/Linux

### 2. 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器（首次使用需要）
playwright install chromium
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
BASE_URL=https://www.baidu.com
BROWSER=chrome
HEADLESS=false
TIMEOUT=30
```

### 4. 运行测试

#### 使用 pytest 运行 Selenium 测试

```bash
# 运行所有 Selenium 测试
pytest tests/test_selenium_example.py -m selenium -v

# 运行所有测试
pytest tests/ -v

# 生成 HTML 报告
pytest tests/ --html=reports/pytest_report.html --self-contained-html
```

#### 使用 pytest 运行 Playwright 测试

```bash
# 运行所有 Playwright 测试
pytest tests/test_playwright_example.py -m playwright -v

# 运行特定标记的测试
pytest -m smoke -v
```

#### 使用 Robot Framework 运行测试

```bash
# 运行 Robot Framework 测试
robot --outputdir reports/robotframework tests/robotframework/

# 运行特定标签的测试
robot --include selenium --outputdir reports/robotframework tests/robotframework/
```

#### 使用运行脚本

```bash
# 给脚本添加执行权限（Linux/macOS）
chmod +x run_tests.sh

# 运行脚本
./run_tests.sh
```

## 📝 使用示例

### pytest + Selenium 示例

```python
import pytest
from utils.selenium_helper import SeleniumHelper

@pytest.mark.selenium
def test_example(selenium_driver, base_url):
    helper = selenium_driver
    helper.navigate_to(base_url)
    helper.input_text("id", "kw", "pytest")
    helper.click("id", "su")
    helper.wait_for_element_visible("id", "content_left")
    assert "pytest" in helper.get_title().lower()
```

### pytest + Playwright 示例

```python
import pytest
from utils.playwright_helper import PlaywrightHelper

@pytest.mark.playwright
def test_example(playwright_page, base_url):
    helper = playwright_page
    helper.navigate_to(base_url)
    helper.fill("#kw", "playwright")
    helper.click("#su")
    helper.wait_for_selector("#content_left")
    assert "playwright" in helper.get_title().lower()
```

### Robot Framework 示例

```robotframework
*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
示例测试
    Open Browser    https://www.baidu.com    chrome
    Input Text      id=kw    Robot Framework
    Click Button    id=su
    Wait Until Element Is Visible    id=content_left
    Close Browser
```

## 🛠️ 工具类说明

### SeleniumHelper

提供常用的 Selenium 操作封装：

- `start_browser()`: 启动浏览器
- `navigate_to(url)`: 导航到指定 URL
- `find_element(locator_type, locator_value)`: 查找元素
- `click(locator_type, locator_value)`: 点击元素
- `input_text(locator_type, locator_value, text)`: 输入文本
- `get_text(locator_type, locator_value)`: 获取元素文本
- `take_screenshot(filename)`: 截图

### PlaywrightHelper

提供常用的 Playwright 操作封装：

- `start_browser()`: 启动浏览器
- `navigate_to(url)`: 导航到指定 URL
- `click(selector)`: 点击元素
- `fill(selector, text)`: 填充输入框
- `get_text(selector)`: 获取元素文本
- `take_screenshot(filename)`: 截图
- `evaluate(script)`: 执行 JavaScript

## 📊 测试标记

框架支持以下测试标记：

- `@pytest.mark.selenium`: Selenium 测试
- `@pytest.mark.playwright`: Playwright 测试
- `@pytest.mark.smoke`: 冒烟测试
- `@pytest.mark.regression`: 回归测试

使用标记运行测试：

```bash
# 运行冒烟测试
pytest -m smoke

# 运行 Selenium 测试
pytest -m selenium

# 排除某些标记
pytest -m "not smoke"
```

## 📁 报告查看

测试完成后，报告会保存在 `reports/` 目录：

- **pytest 报告**: `reports/pytest_report.html`
- **Robot Framework 报告**: `reports/robotframework/robotframework_report.html`
- **截图**: `reports/*.png`

## 🔧 配置说明

### 浏览器配置

在 `config/settings.py` 中可以配置：

- `BROWSER`: 浏览器类型 (chrome/firefox/edge)
- `HEADLESS`: 是否无头模式
- `TIMEOUT`: 默认超时时间（秒）
- `BASE_URL`: 测试基础 URL

### 环境变量

通过 `.env` 文件配置：

```env
BASE_URL=https://example.com
BROWSER=chrome
HEADLESS=false
TIMEOUT=30
```

## 📚 学习资源

### pytest
- [pytest 官方文档](https://docs.pytest.org/)
- [pytest 最佳实践](https://docs.pytest.org/en/stable/goodpractices.html)

### Robot Framework
- [Robot Framework 官方文档](https://robotframework.org/)
- [SeleniumLibrary 文档](https://robotframework.org/SeleniumLibrary/)

### Selenium
- [Selenium 官方文档](https://www.selenium.dev/documentation/)
- [Selenium Python 绑定](https://selenium-python.readthedocs.io/)

### Playwright
- [Playwright 官方文档](https://playwright.dev/python/)
- [Playwright Python API](https://playwright.dev/python/docs/api/class-playwright)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 💡 提示

1. **首次使用**: 确保安装了所有浏览器驱动（Selenium）和浏览器二进制文件（Playwright）
2. **虚拟环境**: 建议使用虚拟环境隔离依赖
3. **报告目录**: 报告目录会自动创建，无需手动创建
4. **调试模式**: 设置 `HEADLESS=false` 可以看到浏览器操作过程
5. **并行执行**: 使用 `pytest-xdist` 可以并行执行测试：`pytest -n auto`

## 🐛 常见问题

### Q: 浏览器驱动找不到？
A: 框架使用 `webdriver-manager` 自动管理驱动，首次运行会自动下载。

### Q: Playwright 浏览器未安装？
A: 运行 `playwright install chromium` 安装浏览器。

### Q: 如何切换浏览器？
A: 修改 `.env` 文件中的 `BROWSER` 配置，或在代码中指定。

### Q: 测试失败时如何调试？
A: 设置 `HEADLESS=false`，查看浏览器操作过程；查看 `reports/` 目录中的截图和日志。

---

Happy Testing! 🎉
