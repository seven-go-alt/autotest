# 自动化测试框架 (UI + API)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![pytest](https://img.shields.io/badge/pytest-7.4.3-green.svg)](https://pytest.org/)
[![Robot Framework](https://img.shields.io/badge/Robot%20Framework-6.1.1-orange.svg)](https://robotframework.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.40.0-purple.svg)](https://playwright.dev/)
[![Selenium](https://img.shields.io/badge/Selenium-4.15.2-yellow.svg)](https://www.selenium.dev/)

一个基于 pytest、Robot Framework 的综合自动化测试框架,支持 Selenium 与 Playwright 双引擎,覆盖 UI 与 API 测试,采用分层架构设计,提供 87+ 个测试用例,可在 Docker 中无头运行。

## 📋 目录

- [核心特性](#-核心特性)
- [快速开始](#-快速开始)
- [项目结构](#-项目结构)
- [测试执行](#-测试执行)
- [架构设计](#-架构设计)
- [测试覆盖](#-测试覆盖)
- [优化成果](#-优化成果)
- [Docker 支持](#-docker-支持)
- [文档导航](#-文档导航)
- [贡献指南](#-贡献指南)
- [更新历史](#-更新历史)

## ✨ 核心特性

### 多框架支持
- **pytest** - 灵活强大的 Python 测试框架
- **Robot Framework** - 自然语言风格的关键字驱动测试

### 多引擎支持
- **Selenium** - 成熟稳定的 Web 自动化工具
- **Playwright** - 现代化的跨浏览器自动化 (Chromium/Firefox/WebKit)

### 多测试类型
- **UI 测试** - 完整的 Web 应用测试 (SauceDemo, 百度搜索等)
- **API 测试** - RESTful API 测试 (ReqRes, HTTPBin, JSONPlaceholder)
- **性能测试** - 页面加载和操作响应时间测试

### 分层架构设计
- **UI 层三层架构**: 定位器层 → 关键字层 → 测试用例层
- **API 层四层架构**: 配置层 → 数据层 → 测试用例层
- **高可维护性**: 修改定位器或配置只需改一个地方
- **高复用性**: 关键字和配置可在多个测试中复用

### 企业级功能
- ✅ 失败自动截图 (Selenium)
- ✅ 重试机制和错误处理
- ✅ 测试数据管理器
- ✅ 多环境配置支持 (dev/test/stage/prod)
- ✅ 详细的 HTML 报告生成
- ✅ CI/CD 集成支持 (Jenkins, GitHub Actions)
- ✅ Docker 容器化部署

## 🚀 快速开始

### 环境准备

**前置条件**:
- Python 3.9+
- Git

### 本地安装

```bash
# 1. 克隆仓库
git clone https://github.com/your-org/autotest.git
cd autotest

# 2. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 安装 Playwright 浏览器
playwright install
```

### 快速运行测试

#### 方式 1: 交互式菜单 (推荐本地开发)

```bash
python3 run_tests.py
```

进入交互式菜单后,可以选择:
1. pytest (Selenium)
2. pytest (Playwright)
3. pytest (API)
4. pytest (全部)
5. Robot Framework
6. 全部运行

#### 方式 2: 命令行参数 (推荐 CI/CD)

```bash
# 运行 UI 测试 (P0 级别用户模块)
python3 run_tests.py --test-type ui --env dev --browser chrome --tags "P0ANDuser" --headless

# 运行 API 测试
python3 run_tests.py --test-type api --env dev

# 运行指定测试套件
python3 run_tests.py --test-type ui --suite ui_tests/testsuites/user/user_login_tests.robot
```

#### 方式 3: 直接使用 pytest/Robot

```bash
# pytest 测试
pytest tests/test_API -m api -v
pytest tests/test_UI -m selenium -v
pytest tests/test_UI -m playwright -v

# Robot Framework 测试
python -m robot --outputdir reports/robotframework tests/robotframework/

# 分层架构演示
robot tests/ui_layer/testsuites/saucedemo_testsuite.robot
robot tests/api_layer/testsuites/reqres_api_testsuite.robot
```

### 环境变量配置 (可选)

```bash
# 创建 .env 文件或设置环境变量
export BASE_URL="https://www.saucedemo.com/"
export API_BASE_URL="https://reqres.in/api"
export BROWSER="chrome"
export HEADLESS="true"
export SELENIUM_REMOTE_URL="http://selenium:4444/wd/hub"  # Docker Compose 使用
```

## 📁 项目结构

```
autotest/
├── config/                     # 配置文件
│   ├── settings.py             # 环境配置和设置
│   └── __init__.py
│
├── utils/                      # 工具库
│   ├── playwright_helper.py    # Playwright 辅助类
│   ├── selenium_helper.py      # Selenium 辅助类 (含失败截图)
│   ├── robot_locators.py       # Robot 定位器层
│   ├── robot_steps.py          # Robot 操作层
│   ├── robot_functional.py     # Robot 功能层
│   ├── retry_decorator.py      # 重试装饰器
│   └── test_data_manager.py    # 测试数据管理器
│
├── tests/                      # 测试用例
│   ├── test_UI/                # UI 测试 (pytest)
│   │   ├── test_saucedemo_selenium.py
│   │   └── test_saucedemo_playwright.py
│   ├── test_API/               # API 测试 (pytest)
│   │   └── test_reqres_api.py
│   ├── robotframework/         # Robot Framework 测试
│   │   ├── baidu_search.robot
│   │   ├── test_layered_architecture.robot
│   │   └── test_api.robot
│   ├── ui_layer/               # UI 分层测试
│   │   ├── locators/           # 定位器层
│   │   ├── keywords/           # 关键字层
│   │   └── testsuites/         # 测试套件
│   └── api_layer/              # API 分层测试
│       ├── config/             # API 配置
│       ├── data/               # 测试数据
│       └── testsuites/         # 测试套件
│
├── ui_tests/                   # 新版 UI 测试
│   ├── keywords/               # 分层关键字
│   │   ├── function_layer/     # 函数层
│   │   ├── pages_layer/        # 页面层
│   │   └── process_layer/      # 流程层
│   └── testsuites/             # 测试用例
│       └── user/               # 用户模块测试
│
├── api_tests/                  # 新版 API 测试
│   └── testsuites/             # API 测试套件
│
├── listeners/                  # Robot Framework 监听器
│   └── web_listener.py
│
├── reports/                    # 测试报告
│   ├── robotframework/         # Robot 报告
│   └── selenium_screenshots/   # 失败截图
│
├── logs/                       # 日志文件
├── tmp/                        # 临时文件和报告
│
├── docs/                       # 文档
│   ├── LAYERED_TESTING_GUIDE.md        # 分层测试详细指南
│   ├── LAYERED_TESTING_CHEATSHEET.md   # 快速参考手册
│   └── CI.md                           # CI/CD 配置指南
│
├── docker/                     # Docker 相关文件
├── Dockerfile                  # Docker 镜像定义
├── docker-compose.yml          # Docker Compose 配置
├── Jenkinsfile                 # Jenkins 流水线配置
│
├── run_tests.py                # 统一测试入口脚本
├── conftest.py                 # pytest 配置和 fixtures
├── pytest.ini                  # pytest 配置文件
├── requirements.txt            # Python 依赖
│
├── README.md                   # 本文件
├── CONTRIBUTING.md             # 贡献指南
├── ARCHITECTURE_DETAILS.md     # 架构详细说明
└── STRUCTURE_GUIDE.md          # 结构详细指南
```

### 核心目录说明

| 目录 | 说明 | 关键文件 |
|------|------|----------|
| `config/` | 环境配置和设置 | `settings.py` |
| `utils/` | 工具类和辅助函数 | `*_helper.py`, `robot_*.py` |
| `tests/` | 所有测试用例 | `test_*.py`, `*.robot` |
| `ui_tests/` | 新版 UI 测试 (分层架构) | `keywords/`, `testsuites/` |
| `api_tests/` | 新版 API 测试 | `testsuites/` |
| `reports/` | 测试报告输出 | `*.html`, `*.xml` |
| `docs/` | 详细文档 | `*.md` |

## 🧪 测试执行

### 标签系统

测试用例使用标签进行分类和过滤:

**等级标签**:
- `P0` - 核心功能测试
- `P1` - 重要功能测试
- `P2` - 边界和异常测试

**业务模块**:
- `user` - 用户相关
- `order` - 订单相关
- `product` - 产品相关

**功能标签**:
- `login` - 登录功能
- `create` - 创建操作
- `search` - 搜索功能

**平台标签**:
- `pc` - PC 端
- `mobile` - 移动端

**测试类型**:
- `smoke` - 冒烟测试
- `regression` - 回归测试
- `critical` - 关键测试
- `performance` - 性能测试

### 标签过滤示例

```bash
# 只运行 P0 级别的用户相关测试
python3 run_tests.py --test-type ui --tags "P0ANDuser"

# 运行 PC 端的用户登录测试
python3 run_tests.py --test-type ui --tags "userANDloginANDpc"

# 排除不稳定测试
python3 run_tests.py --test-type ui --exclude "flaky"

# pytest 标签过滤
pytest -m smoke -v                    # 冒烟测试
pytest -m "ui and selenium" -v        # Selenium UI 测试
pytest -m api -v                      # API 测试
```

### 环境配置

通过 `--env` 参数选择测试环境:

```bash
python3 run_tests.py --test-type ui --env dev      # 开发环境
python3 run_tests.py --test-type ui --env test     # 测试环境
python3 run_tests.py --test-type ui --env stage    # 预发布环境
python3 run_tests.py --test-type ui --env prod     # 生产环境
```

环境变量设置:
```bash
export DEV_BASE_URL="https://dev.example.com"
export TEST_BASE_URL="https://test.example.com"
export STAGE_BASE_URL="https://stage.example.com"
export PROD_BASE_URL="https://prod.example.com"
```

### 报告位置

**Robot Framework 报告**:
- `tmp/report.html` - 测试报告
- `tmp/log.html` - 详细日志
- `tmp/output.xml` - XML 格式输出

**pytest 报告**:
- `tmp/pytest_*.html` - HTML 报告

**失败截图**:
- `reports/selenium_screenshots/failure_*.png`

## 🏗️ 架构设计

### UI 测试三层架构

```
┌─────────────────────────────────────────────┐
│          测试用例层 (Test Cases)             │
│  - saucedemo_testsuite.robot                │
│  - test_ui_layer.py                         │
│  - 业务验证逻辑                              │
└─────────────────────────────────────────────┘
                    ↓ 调用
┌─────────────────────────────────────────────┐
│          关键字层 (Keywords)                 │
│  - saucedemo_keywords.py                    │
│  - base_keywords.py                         │
│  - 业务流程封装                              │
│  - 登录、添加购物车、结账等                   │
└─────────────────────────────────────────────┘
                    ↓ 使用
┌─────────────────────────────────────────────┐
│          定位器层 (Locators)                 │
│  - saucedemo_locators.py                    │
│  - base_locators.py                         │
│  - UI 元素定位器集中管理                     │
└─────────────────────────────────────────────┘
```

**优势**:
- ✅ 定位器改变只需修改一个地方
- ✅ 业务流程改变只需修改关键字
- ✅ 测试用例聚焦于测试逻辑
- ✅ 高度复用和易于维护

### API 测试四层架构

```
┌─────────────────────────────────────────────┐
│          测试用例层 (Test Cases)             │
│  - reqres_api_testsuite.robot               │
│  - test_api_layer.py                        │
└─────────────────────────────────────────────┘
                    ↓ 使用
┌─────────────────────────────────────────────┐
│          配置层 (Config)                     │
│  - api_config.py - API 端点、环境配置        │
│  - testcase_config.py - 测试用例配置         │
└─────────────────────────────────────────────┘
                    ↓ 参考
┌─────────────────────────────────────────────┐
│          数据层 (Data)                       │
│  - user_data.py - 用户测试数据               │
│  - post_data.py - 文章测试数据               │
│  - common_data.py - 通用数据和工具           │
└─────────────────────────────────────────────┘
```

**优势**:
- ✅ 配置和数据完全分离
- ✅ 支持多环境切换
- ✅ 易于参数化测试
- ✅ 数据生成工具函数

### 新版分层架构 (ui_tests/)

```
┌─────────────────────────────────────────────┐
│          用例层 (testsuites/)                │
│  - user_login_tests.robot                   │
│  - 只调用流程层关键字                        │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│          流程层 (process_layer/)             │
│  - user_flows.robot                         │
│  - 端到端业务流程                            │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│          页面层 (pages_layer/)               │
│  - login_page.robot                         │
│  - 按页面组织的关键字                        │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│          函数层 (function_layer/)            │
│  - web_functions.robot                      │
│  - 封装 Selenium 原子操作                    │
└─────────────────────────────────────────────┘
```

详细架构说明请参考 [ARCHITECTURE_DETAILS.md](ARCHITECTURE_DETAILS.md)

## 📊 测试覆盖

### 测试用例统计

| 测试类型 | 数量 | 说明 |
|---------|------|------|
| **UI 测试 (pytest)** | 15+ | Selenium + Playwright |
| **UI 测试 (Robot)** | 20+ | 分层架构演示 |
| **API 测试 (pytest)** | 40+ | RESTful API 测试 |
| **API 测试 (Robot)** | 20+ | RequestsLibrary |
| **性能测试** | 4+ | 页面加载和操作性能 |
| **总计** | **87+** | 全面覆盖 |

### UI 测试覆盖

✅ **登录功能**
- 正确账号密码登录
- 错误密码登录
- 特殊字符登录
- 大小写敏感性测试
- 不同用户类型登录 (数据驱动)

✅ **购物车操作**
- 添加单个产品
- 添加所有产品
- 重复添加同一产品
- 移除产品
- 购物车持久性验证

✅ **产品功能**
- 产品浏览
- 产品排序 (4种排序选项)
- 产品名称和价格验证

✅ **结账流程**
- 完整购买流程
- 不同数量产品购买 (参数化)
- 随机数据结账

✅ **搜索功能**
- 单关键词搜索
- 多关键词搜索
- 特殊字符搜索
- 长关键词搜索

✅ **会话管理**
- 登出和重新登录
- 购物车状态保持

### API 测试覆盖

✅ **HTTP 方法**
- GET 请求 (获取列表、单个资源)
- POST 请求 (创建资源)
- PUT 请求 (更新资源)
- PATCH 请求 (部分更新)
- DELETE 请求 (删除资源)

✅ **请求处理**
- 查询参数
- 自定义请求头
- JSON 数据提交
- Form 表单提交
- 文件上传

✅ **响应验证**
- 状态码验证
- 响应体验证
- 响应头验证
- 数据类型检查
- 字符编码验证

✅ **高级功能**
- Cookie 处理
- 重定向处理
- 并发请求
- 大数据负载测试
- 响应时间检测

✅ **错误处理**
- 404/500 错误
- 超时异常
- 连接错误
- 无效 JSON 响应
- 认证失败

## 🎯 优化成果

### 框架优化 (2025-12-21 完成)

#### 核心改进

| 方面 | 优化前 | 优化后 |
|------|--------|--------|
| **架构** | 扁平结构 | 分层架构 (4级) |
| **定位器管理** | 散布在测试中 | 集中管理 |
| **代码复用性** | 低 | 高 (关键字组合) |
| **维护性** | 困难 | 容易 (改一处生效) |
| **文档** | 基础 | 全面 (3个详细文档) |
| **测试类型** | UI + Robot | UI + API + Robot |
| **失败追踪** | 手动截图 | 自动截图 |
| **总测试数** | ~20 | 87+ |

#### 新增工具类

**1. 重试装饰器** (`utils/retry_decorator.py`)
```python
from utils.retry_decorator import retry_on_failure

@retry_on_failure(max_attempts=3, delay=1.0)
def unstable_operation():
    page.click("button")
```

**2. 测试数据管理器** (`utils/test_data_manager.py`)
```python
from utils.test_data_manager import TestDataManager

manager = TestDataManager()
user = manager.get_test_user("standard")
checkout = manager.get_checkout_data()
random_data = manager.generate_user_data()
```

**3. UIOperations 增强功能**
- 调试模式
- 智能等待
- 重试点击
- 自动截图
- 网络空闲等待

#### 测试增强 (2026-01-17 完成)

**新增 25 个测试用例**:
- 登录相关: 3个 (特殊字符、大小写、数据驱动)
- 购物车相关: 5个 (全部添加、重复添加、持久性等)
- 购买流程: 2个 (不同数量、随机数据)
- 产品相关: 3个 (排序、名称验证、价格验证)
- 会话导航: 2个 (登出重登、购物车清除)
- 性能测试: 2个 (添加性能、完整流程性能)
- 百度搜索: 3个 (多关键词、特殊字符、长关键词)

**测试类型分布**:
- smoke (冒烟测试): 4个
- critical (关键测试): 2个
- regression (回归测试): 26个
- integration (集成测试): 5个
- performance (性能测试): 4个
- parametrize (数据驱动): 5个

### 最佳实践应用

1. ✅ **数据驱动测试** - 使用 parametrize 减少重复
2. ✅ **Fixtures 使用** - 集中管理测试数据
3. ✅ **测试标记** - 便于选择性运行
4. ✅ **性能断言** - 确保响应时间
5. ✅ **边界条件** - 覆盖异常场景
6. ✅ **代码组织** - 逻辑分组清晰
7. ✅ **详细文档** - 每个测试都有说明

## 🐳 Docker 支持

### 使用 Dockerfile

```bash
# 构建镜像 (Playwright 无头模式)
docker build -t autotest .

# 运行测试
docker run --rm autotest
```

### 使用 Docker Compose

```bash
# 启动 Selenium Grid 和测试容器
docker-compose up --build --exit-code-from tests

# 后台运行
docker-compose up -d

# 查看日志
docker-compose logs -f tests

# 停止并清理
docker-compose down
```

**docker-compose.yml** 配置:
- `selenium` 服务: Selenium Standalone Chrome
- `tests` 服务: 测试执行容器
- 通过 `SELENIUM_REMOTE_URL` 连接远程浏览器

### 环境变量

在 Docker 中可以通过环境变量配置:

```yaml
environment:
  - BASE_URL=https://www.saucedemo.com/
  - API_BASE_URL=https://reqres.in/api
  - BROWSER=chrome
  - HEADLESS=true
  - SELENIUM_REMOTE_URL=http://selenium:4444/wd/hub
```

## 📚 文档导航

### 快速开始 (5-10 分钟)

1. **[PROJECT_TREE.txt](PROJECT_TREE.txt)** - 项目结构一览
2. **[QUICK_RUN.md](QUICK_RUN.md)** - 快速运行指南

### 深入学习 (30-45 分钟)

3. **[STRUCTURE_GUIDE.md](STRUCTURE_GUIDE.md)** - 详细结构指南
   - 完整的目录结构说明
   - 各层级的详细说明
   - 最佳实践和扩展指南

4. **[ARCHITECTURE_DETAILS.md](ARCHITECTURE_DETAILS.md)** - 架构详解
   - 整体架构图
   - UI 层三层结构详解
   - API 层四层结构详解
   - 数据流向示意图

### 专题文档

5. **[CONTRIBUTING.md](CONTRIBUTING.md)** - 贡献指南
   - 开发环境设置
   - 提交工作流
   - CI/CD 配置
   - 代码规范

6. **[docs/LAYERED_TESTING_GUIDE.md](docs/LAYERED_TESTING_GUIDE.md)** - 分层测试详细指南
7. **[docs/LAYERED_TESTING_CHEATSHEET.md](docs/LAYERED_TESTING_CHEATSHEET.md)** - 快速参考手册
8. **[docs/CI.md](docs/CI.md)** - CI/CD 配置详解

### 学习路径

**路径 1: "我想快速开始" (⏱️ 15 分钟)**
```
PROJECT_TREE.txt (5 分钟) 
    ↓
QUICK_RUN.md (10 分钟)
    ↓
开始运行测试
```

**路径 2: "我想深入理解" (⏱️ 90 分钟)**
```
PROJECT_TREE.txt (5 分钟)
    ↓
QUICK_RUN.md (10 分钟)
    ↓
STRUCTURE_GUIDE.md (30 分钟)
    ↓
ARCHITECTURE_DETAILS.md (35 分钟)
    ↓
浏览源代码,运行测试
```

**路径 3: "我想立即扩展框架" (⏱️ 45 分钟)**
```
PROJECT_TREE.txt (5 分钟)
    ↓
查看源代码示例 (15 分钟)
    ↓
STRUCTURE_GUIDE.md 的扩展指南部分 (15 分钟)
    ↓
按照扩展指南创建新的测试
```

### 常见场景快速查找

| 我想... | 查看文档 |
|---------|----------|
| 快速运行一个测试 | [QUICK_RUN.md](QUICK_RUN.md) |
| 理解整个架构 | [ARCHITECTURE_DETAILS.md](ARCHITECTURE_DETAILS.md) |
| 添加新的 UI 测试 | [STRUCTURE_GUIDE.md](STRUCTURE_GUIDE.md) - 扩展指南 |
| 添加新的 API 测试 | [STRUCTURE_GUIDE.md](STRUCTURE_GUIDE.md) - 扩展指南 |
| 了解最佳实践 | [STRUCTURE_GUIDE.md](STRUCTURE_GUIDE.md) - 最佳实践 |
| 遇到问题排查 | [QUICK_RUN.md](QUICK_RUN.md) - 常见问题 |
| 配置 CI/CD | [CONTRIBUTING.md](CONTRIBUTING.md) - CI/CD 配置 |

## 🤝 贡献指南

欢迎为本项目做出贡献!详细的贡献指南请参考 [CONTRIBUTING.md](CONTRIBUTING.md)

### 快速开始贡献

1. Fork 本仓库
2. 创建 feature 分支: `git checkout -b feature/your-feature`
3. 编写/修改测试用例
4. 运行本地测试确保通过
5. 提交 commit: `git commit -m "feat: add new feature"`
6. Push 到分支: `git push origin feature/your-feature`
7. 创建 Pull Request

### 代码规范

- **Python**: 遵循 PEP 8,使用 4 空格缩进
- **Robot Framework**: 使用 2 空格缩进,关键字首字母大写
- **提交信息**: 使用语义化提交 (feat/fix/docs/refactor 等)

### CI/CD 集成

本项目支持:
- **GitHub Actions** - 自动化测试和部署
- **Jenkins** - 持续集成流水线
- **Slack/Email 通知** - 测试结果通知

详细配置请参考 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [docs/CI.md](docs/CI.md)

## 📝 更新历史

### 版本 2.0 - 分层架构完整版 (2024-01-01)

**主要更新**:
- ✨ 实现完整的三层分层架构 (定位器 → 操作 → 功能)
- ✨ 新增 40+ 个 API 测试用例 (pytest + Robot)
- ✨ 新增 10+ 个 Playwright 高级场景测试
- ✨ 新增失败自动截图功能
- ✨ 新增重试机制和测试数据管理器
- 📚 新增 3 个详细文档 (14K+ 字)
- 🎯 总测试用例达到 87+

### 版本 1.5 - 测试增强版 (2026-01-17)

**主要更新**:
- ✨ 新增 25 个测试用例 (总计 40 个)
- ✨ 实现数据驱动测试 (parametrize)
- ✨ 新增性能测试
- ✨ 新增边界条件和异常测试
- 📊 测试覆盖率大幅提升

### 版本 1.0 - 初始版本 (2025-12-21)

**主要功能**:
- ✅ 基础 UI 测试 (Selenium + Playwright)
- ✅ 基础 API 测试
- ✅ Robot Framework 集成
- ✅ Docker 支持
- ✅ 基础文档

详细更新说明请参考项目历史记录。

## 🔧 常用命令速查

```bash
# ========== 运行测试 ==========

# 交互式菜单
python3 run_tests.py

# UI 测试 (命令行)
python3 run_tests.py --test-type ui --env dev --browser chrome --tags "P0"

# API 测试
python3 run_tests.py --test-type api --env dev

# pytest 测试
pytest tests/ -v                      # 所有测试
pytest -m smoke -v                    # 冒烟测试
pytest -m api -v                      # API 测试
pytest -m "ui and selenium" -v        # Selenium UI 测试

# Robot Framework 测试
robot tests/robotframework/           # 所有 Robot 测试
robot --include smoke tests/          # 按标签运行
robot tests/ui_layer/testsuites/      # UI 分层测试
robot tests/api_layer/testsuites/     # API 分层测试

# ========== 并行和重试 ==========

pytest -n auto -v                     # 并行运行
pytest --reruns 2 -v                  # 失败重试 2 次
pytest -n auto --reruns 2 -v          # 并行 + 重试

# ========== 生成报告 ==========

pytest --html=reports/report.html -v  # HTML 报告
robot --outputdir reports/ tests/     # Robot 报告

# ========== Docker ==========

docker build -t autotest .            # 构建镜像
docker run --rm autotest              # 运行测试
docker-compose up --build             # Docker Compose

# ========== 验证安装 ==========

python3 -m robot --version            # 检查 Robot Framework
python3 -c "import selenium; print(selenium.__version__)"  # 检查 Selenium
robot --dryrun ui_tests/testsuites/user/user_login_tests.robot  # 语法检查
```

## 📞 获取帮助

### 常见问题

**Q: 如何切换不同的环境?**  
A: 使用 `--env` 参数或编辑 `config/settings.py` 中的配置

**Q: 如何添加新的定位器?**  
A: 在对应的 `*_locators.py` 文件中添加新的类属性

**Q: 如何选择最佳的选择器?**  
A: 优先级: ID > Class > CSS Selector > XPath

**Q: 如何并发运行测试?**  
A: 使用 `pytest -n auto` 或 Robot Framework 的 `--processes` 参数

**Q: 测试失败如何调试?**  
A: 查看失败截图 (`reports/selenium_screenshots/`),查看详细日志,使用 `--log-cli-level=DEBUG`

### 问题反馈

遇到 Bug 或有功能建议?欢迎提交 Issue 或 PR,请附上:
- 问题描述
- 复现步骤
- 预期行为 vs 实际行为
- 环境信息 (OS、Python 版本、浏览器等)

## 📄 许可证

本项目使用 MIT 许可证。详见 LICENSE 文件。

---

**Happy Testing! 🎉**

**维护者**: autotest team  
**最后更新**: 2026-01-24  
**版本**: 2.0  
**质量评分**: ⭐⭐⭐⭐⭐ (5/5)
