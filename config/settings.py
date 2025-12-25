"""
测试框架配置文件
"""
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 项目根目录
BASE_DIR = Path(__file__).parent.parent

# 测试配置
# UI 目标站点：使用公开的演示站点 SauceDemo
BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")
BROWSER = os.getenv("BROWSER", "chrome").lower()
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
TIMEOUT = int(os.getenv("TIMEOUT", "30"))

# Playwright 配置
PLAYWRIGHT_BROWSER = os.getenv("PLAYWRIGHT_BROWSER", "chromium").lower()
PLAYWRIGHT_HEADLESS = os.getenv("PLAYWRIGHT_HEADLESS", str(HEADLESS)).lower() == "true"

# Selenium 远程配置（用于 Docker + Selenium Grid/Standalone）
SELENIUM_REMOTE_URL = os.getenv("SELENIUM_REMOTE_URL")

# 浏览器选项
BROWSER_OPTIONS = {
    "chrome": {
        "headless": HEADLESS,
        "window_size": (1920, 1080),
        "options": [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled",
        ],
    },
    "firefox": {
        "headless": HEADLESS,
        "window_size": (1920, 1080),
        "options": [],
    },
    "edge": {
        "headless": HEADLESS,
        "window_size": (1920, 1080),
        "options": [],
    },
}

# 报告目录
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# 日志目录
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# API 基础地址（示例：reqres.in 提供公开接口）
API_BASE_URL = os.getenv("API_BASE_URL", "https://reqres.in/api")


@dataclass
class EnvConfig:
    """环境配置：用于入口脚本通过 env 选择 base_url 等。

    当前实现比较轻量级：
    - 优先读取形如 DEV_BASE_URL / TEST_BASE_URL 的环境变量
    - 否则回退到全局 BASE_URL / API_BASE_URL
    """

    name: str
    base_url: str
    api_base_url: str


def get_env_config(env: str) -> EnvConfig:
    """根据 env（dev/test/stage/prod 等）构造环境配置"""
    env_key = (env or "dev").strip().lower()
    upper = env_key.upper()

    base_url = os.getenv(f"{upper}_BASE_URL", BASE_URL)
    api_base_url = os.getenv(f"{upper}_API_BASE_URL", API_BASE_URL)

    return EnvConfig(name=env_key, base_url=base_url, api_base_url=api_base_url)


