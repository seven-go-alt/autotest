# 快速开始指南

## 5 分钟快速上手

### 步骤 1: 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install
```

### 步骤 2: 创建环境配置文件

创建 `.env` 文件（在项目根目录）：

```env
BASE_URL=https://www.python.org
BROWSER=chrome
HEADLESS=false
TIMEOUT=30
```

### 步骤 3: 运行第一个测试

#### 方式 1: 使用测试菜单（推荐）

```bash
python run_test.py
```

然后选择：
- 选项 1: 运行 pytest 测试
- 选项 2: 运行 Robot Framework 测试
- 选项 3: 运行所有测试

#### 方式 2: 直接运行 pytest

```bash
# 运行 API 测试
pytest tests/test_api_example.py -v

# 运行 Selenium UI 测试
pytest tests/test_selenium_example.py -m selenium -v

# 运行 Playwright UI 测试（基础）
pytest tests/test_playwright_example.py -m playwright -v

# 运行 Playwright 高级场景
pytest tests/test_playwright_advanced.py -m playwright -v
```

#### 方式 3: 运行 Robot Framework 测试

```bash
# 运行分层架构演示（推荐）
python -m robot tests/robotframework/test_layered_architecture.robot

# 运行 API 测试
python -m robot tests/robotframework/test_api.robot

# 运行所有 Robot 测试
python -m robot --outputdir reports/robotframework tests/robotframework/
```

### 步骤 4: 查看测试报告

- **pytest 报告**: `reports/pytest_report.html`
- **Robot Framework 报告**: `reports/robotframework/report.html`
- **失败截图**: `reports/selenium_screenshots/failure_*.png`

## 框架结构

### 分层测试架构

该框架采用**三层架构**设计，从下到上分别为：

```
┌────────────────────────────────────┐
│  测试用例层（Test Cases）          │
├────────────────────────────────────┤
│  功能层（robot_functional.py）     │
│  业务流程关键字                    │
├────────────────────────────────────┤
│  操作层（robot_steps.py）          │
│  原子 UI 操作关键字                │
├────────────────────────────────────┤
│  定位器层（robot_locators.py）     │
│  元素定位器定义                    │
├────────────────────────────────────┤
│  辅助层（*_helper.py）             │
│  低级驱动程序                      │
└────────────────────────────────────┘
```

### 文件组织

```
autotest/
├── tests/
│   ├── test_api_example.py              # API 测试（pytest）
│   ├── test_selenium_example.py         # Selenium 测试（pytest）
│   ├── test_playwright_example.py       # Playwright 基础测试（pytest）
│   ├── test_playwright_advanced.py      # Playwright 高级场景（pytest）
│   └── robotframework/
│       ├── test_layered_architecture.robot  # 分层架构演示（Robot）
│       ├── test_api.robot                   # API 测试（Robot）
│       └── baidu_search.robot               # 旧项目搜索测试
├── utils/
│   ├── robot_locators.py             # 定位器层
│   ├── robot_steps.py                # 操作层
│   ├── robot_functional.py           # 功能层
│   ├── playwright_helper.py          # Playwright 驱动
│   └── selenium_helper.py            # Selenium 驱动
├── config/
│   └── settings.py                   # 配置文件
├── reports/
│   ├── pytest_report.html            # pytest 报告
│   ├── selenium_screenshots/         # 失败截图
│   └── robotframework/               # Robot 报告
├── conftest.py                       # pytest 配置
├── pytest.ini                        # pytest 设置
├── robotframework.ini                # Robot Framework 设置
└── run_test.py                       # 测试菜单
```

## 测试类型说明

### 1. API 测试

测试 RESTful API，包括 GET、POST、PUT、DELETE 等。

```bash
# 使用 pytest
python -m pytest tests/test_api_example.py -m api -v

# 使用 Robot Framework
python -m robot tests/robotframework/test_api.robot
```

**特点**:
- 使用 `requests` 库进行 HTTP 请求
- 支持请求头、查询参数、JSON 数据
- 包含错误处理和性能测试
- 可独立于 UI 测试运行

### 2. UI 测试 - Selenium

使用 Selenium WebDriver 进行浏览器自动化测试。

```bash
python -m pytest tests/test_selenium_example.py -m selenium -v
```

**特点**:
- 支持多浏览器（Chrome、Firefox、Edge）
- 包含防自动化检测参数
- 测试失败自动截图（保存在 `reports/selenium_screenshots/`）
- 适合复杂的用户交互场景

### 3. UI 测试 - Playwright

使用 Playwright 进行现代浏览器自动化。

```bash
# 基础场景
python -m pytest tests/test_playwright_example.py -m playwright -v

# 高级场景（多标签页、动态等待、网络拦截等）
python -m pytest tests/test_playwright_advanced.py -m playwright -v
```

**特点**:
- 支持多浏览器和多标签页
- 强大的网络拦截和监控能力
- JavaScript 执行和 Cookie 管理
- 更快的执行速度

### 4. 集成测试 - Robot Framework

使用 Robot Framework 进行高级集成测试。

```bash
python -m robot tests/robotframework/test_layered_architecture.robot
```

**特点**:
- 使用业务语言编写测试（BDD 风格）
- 支持分层架构（定位器 → 操作 → 功能）
- 易于维护和扩展
- 自动生成 HTML 报告

## 常用命令

### pytest 命令

```bash
# 运行所有测试
pytest tests/ -v

# 按标记运行
pytest tests/ -m api           # API 测试
pytest tests/ -m selenium      # Selenium 测试
pytest tests/ -m playwright    # Playwright 测试
pytest tests/ -m smoke         # 冒烟测试

# 运行特定文件
pytest tests/test_api_example.py

# 显示详细输出
pytest tests/ -v -s

# 快速失败（第一个失败时停止）
pytest tests/ -x

# 查看可用标记
pytest --markers

# 生成 HTML 报告
pytest tests/ --html=reports/pytest_report.html
```

### Robot Framework 命令

```bash
# 运行所有 Robot 测试
python -m robot --outputdir reports/robotframework tests/robotframework/

# 按标记运行
python -m robot -i smoke tests/robotframework/       # 冒烟测试
python -m robot -i functional tests/robotframework/  # 功能测试

# 运行特定文件
python -m robot tests/robotframework/test_api.robot

# 查看可用标记
python -m robot --list tests/robotframework/
```

## 下一步

1. **学习分层架构**: 阅读 `docs/LAYERED_TESTING_GUIDE.md`
2. **快速参考**: 查看 `docs/LAYERED_TESTING_CHEATSHEET.md`
3. **修改定位器**: 编辑 `utils/robot_locators.py` 适应你的应用
4. **添加关键字**: 扩展 `utils/robot_steps.py` 和 `utils/robot_functional.py`
5. **编写测试**: 参考 `tests/robotframework/` 中的示例创建你的测试

## CI / CD

项目已提供 GitHub Actions 工作流和 Jenkinsfile 示例：

- **GitHub Actions**: `.github/workflows/ci.yml`
- **Jenkins Pipeline**: `Jenkinsfile`
- **CI 配置指南**: `docs/CI.md`
- **贡献指南**: `CONTRIBUTING.md`

## 常见问题

### Q: 定位器找不到元素？
**A**: 检查定位器是否正确。使用浏览器开发者工具查看元素的 CSS 选择器或 XPath，然后更新 `utils/robot_locators.py`。

### Q: 测试间歇性失败？
**A**: 可能是网络延迟或资源加载不稳定。增加等待时间：
```python
Steps.Wait For Element By Name    element_name    timeout=30
```

### Q: 如何手动检查截图？
**A**: 失败截图保存在 `reports/selenium_screenshots/`，文件名为 `failure_<test_name>.png`。

### Q: 如何在 CI 环境中运行？
**A**: 参阅 `docs/CI.md` 了解 Secrets 配置和 CI/CD 最佳实践。

## 完整命令参考

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
playwright install

# 运行测试菜单
python run_test.py

# 运行 API 测试
python -m pytest tests/test_api_example.py -v

# 运行 UI 测试（Selenium）
python -m pytest tests/test_selenium_example.py -v

# 运行 UI 测试（Playwright）
python -m pytest tests/test_playwright_advanced.py -v

# 运行 Robot Framework
python -m robot tests/robotframework/test_layered_architecture.robot

# 生成报告
pytest tests/ --html=reports/pytest_report.html
python -m robot --outputdir reports/robotframework tests/robotframework/

# 查看报告（macOS）
open reports/pytest_report.html
open reports/robotframework/report.html
```

---

**需要帮助?** 
- 详细指南: 见 `docs/LAYERED_TESTING_GUIDE.md`
- 快速参考: 见 `docs/LAYERED_TESTING_CHEATSHEET.md`
- CI/CD 配置: 见 `docs/CI.md`
- 贡献指南: 见 `CONTRIBUTING.md`
pytest -m playwright -v

# 生成 HTML 报告
pytest tests/ --html=reports/pytest_report.html --self-contained-html

# 使用运行脚本（交互式）
python run_test.py
```

