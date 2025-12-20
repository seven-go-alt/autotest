# 快速开始指南

## 5 分钟上手（本机）
```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install   # 安装浏览器

# UI & API
pytest tests/test_API -m api -v
pytest tests/test_UI  -m selenium -v
pytest tests/test_UI  -m playwright -v

# Robot Framework
python -m robot --outputdir reports/robotframework tests/robotframework/
```

环境变量（可选）：
```
BASE_URL=https://www.saucedemo.com/
API_BASE_URL=https://reqres.in/api
BROWSER=chrome
HEADLESS=true
SELENIUM_REMOTE_URL=http://selenium:4444/wd/hub  # 使用 docker-compose 时
```

## 使用 Docker
```bash
# Playwright 基础镜像，无头运行
docker build -t autotest .
docker run --rm autotest

# docker-compose（Selenium 远程 + Playwright）
docker-compose up --build --exit-code-from tests
```

## 运行脚本
```bash
python run_test.py   # 交互式选择 Selenium / Playwright / API / Robot / 全部
```

## 目录关注点
- `tests/test_UI/`：SauceDemo UI 测试（参数化登录、购物车、Checkout）
- `tests/test_API/`：ReqRes API 测试（分页、创建、登录正反例）
- `tests/robotframework/`：Robot 套件，含 Playwright 自定义关键字

## 常见命令
```bash
pytest -m smoke -v               # 冒烟
pytest -m "ui and selenium" -v   # Selenium UI
pytest -m "ui and playwright" -v # Playwright UI
pytest -m api -v                 # 接口
```

