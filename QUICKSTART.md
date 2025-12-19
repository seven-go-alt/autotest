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

# 如果你使用 Robot Framework 的 robotframework-browser 库，还需初始化：
rfbrowser init
```

### 步骤 2: 创建环境配置文件

创建 `.env` 文件（在项目根目录）：

```env
BASE_URL=https://www.baidu.com
BROWSER=chrome
HEADLESS=false
TIMEOUT=30
```

### 步骤 3: 运行第一个测试

#### 方式 1: 使用 pytest 运行 Selenium 测试

```bash
pytest tests/test_selenium_example.py -m selenium -v
```

#### 方式 2: 使用 pytest 运行 Playwright 测试

```bash
pytest tests/test_playwright_example.py -m playwright -v
```

#### 方式 3: 使用 Robot Framework

Robot Framework 使用建议：

1. 将复杂、功能型测试用例编写为 Robot 测试套件并使用关键字封装（项目中 `utils/robot_custom_library.py` 提供了 Playwright 关键字示例）。
2. 运行 Robot 测试：

```bash
# 使用 Python 模块方式，避免 PATH 问题
python -m robot --outputdir reports/robotframework tests/robotframework/
```

在 CI 中，请确保执行 `playwright install` 与 `rfbrowser init`（如果使用 robotframework-browser）。

### 步骤 4: 查看测试报告

- pytest 报告: `reports/pytest_report.html`
- Robot Framework 报告: `reports/robotframework/robotframework_report.html`

## 下一步

1. 阅读 `README.md` 了解详细功能
2. 查看 `tests/` 目录中的示例测试
3. 修改示例测试以适应你的需求
4. 编写自己的测试用例

## 常见命令

```bash
# 运行所有测试
pytest tests/ -v

# 运行冒烟测试
pytest -m smoke -v

# 运行 Selenium 测试
pytest -m selenium -v

# 运行 Playwright 测试
pytest -m playwright -v

# 生成 HTML 报告
pytest tests/ --html=reports/pytest_report.html --self-contained-html

# 使用运行脚本（交互式）
python run_test.py
```

