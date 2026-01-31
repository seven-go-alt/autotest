# 自动化测试框架（UI + API）

一个基于 pytest、Robot Framework，支持 Selenium 与 Playwright 的综合自动化测试框架，覆盖 UI 与接口测试，并可在 Docker 中无头运行。

## 📋 特性
- 多框架：pytest、Robot Framework
- 多引擎：Selenium + Playwright（chromium/firefox/webkit）
- 多类型：UI 测试（`tests/test_UI`）与接口测试（`tests/test_API`）
- Docker 友好：内置 `Dockerfile` 与 `docker-compose.yml`
- 参数化示例：SauceDemo 登录/购物流程，ReqRes 接口用例

## 🏗️ 项目结构
```
autotest/
├── config/                 # 配置
├── utils/                  # 工具（Selenium/Playwright/Robot 自定义库）
├── tests/
│   ├── test_UI/            # UI 用例（pytest）
│   ├── test_API/           # API 用例（pytest）
│   ├── robotframework/     # Robot Framework 套件
│   └── resources/          # Robot 关键字资源
├── docker-compose.yml      # Docker 一键运行（含 selenium/standalone-chrome）
├── Dockerfile              # Playwright 基础镜像
├── run_test.py             # 交互式运行脚本
├── requirements.txt
├── README.md
└── QUICKSTART.md
```

## 🚀 快速开始（本机）
```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install   # 安装浏览器

# UI + API 测试
pytest tests/test_API -m api -v
pytest tests/test_UI  -m selenium -v
pytest tests/test_UI  -m playwright -v

# Robot Framework
python -m robot --outputdir reports/robotframework tests/robotframework/
```

环境变量（可选，见 `config/settings.py`）：
```
BASE_URL=https://www.saucedemo.com/
API_BASE_URL=https://reqres.in/api
BROWSER=chrome
HEADLESS=true
SELENIUM_REMOTE_URL=http://selenium:4444/wd/hub  # 若使用 docker-compose
```

## 🐳 Docker 与 Docker Compose
```bash
# 直接构建并运行（Playwright 无头）
docker build -t autotest .
docker run --rm autotest

# 使用 docker-compose（Selenium 远程 + Playwright 本地）
docker-compose up --build --exit-code-from tests
```
`docker-compose` 会启动 `selenium/standalone-chrome`，测试容器通过 `SELENIUM_REMOTE_URL` 连接远程浏览器。

## 🧪 示例用例
- `tests/test_UI/test_saucedemo_selenium.py` & `test_saucedemo_playwright.py`
  - 参数化登录（成功/失败）
  - 加购商品、进入结账概览
- `tests/test_API/test_reqres_api.py`
  - 列表分页、创建用户、登录成功/失败
- `tests/robotframework/baidu_search.robot`（已改为 SauceDemo 登录/下单流程）

## 🛠️ 运行脚本
```bash
python run_test.py   # 交互式选择 Selenium / Playwright / API / Robot / 全部
```

## 🔧 配置说明
- `config/settings.py`：BASE_URL、API_BASE_URL、HEADLESS、PLAYWRIGHT_BROWSER、SELENIUM_REMOTE_URL 等
- `pytest.ini`：标记 `ui` / `api` / `selenium` / `playwright` / `smoke` / `regression`

## 🤝 提示
- 优先在容器中无头运行；本机调试可设置 `HEADLESS=false`
- Selenium 远程模式下使用 `SELENIUM_REMOTE_URL` 连接 Grid / Standalone
- 并行执行：`pytest -n auto`

Happy Testing! 🎉
