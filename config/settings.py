"""
测试框架配置文件
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 项目根目录
BASE_DIR = Path(__file__).parent.parent

# 测试配置
BASE_URL = os.getenv("BASE_URL", "https://www.python.org")
BROWSER = os.getenv("BROWSER", "chrome").lower()
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
TIMEOUT = int(os.getenv("TIMEOUT", "30"))

# 浏览器选项
BROWSER_OPTIONS = {
    "chrome": {
        "headless": HEADLESS,
        "window_size": (1920, 1080),
        "options": [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled"
        ]
    },
    "firefox": {
        "headless": HEADLESS,
        "window_size": (1920, 1080),
        "options": []
    },
    "edge": {
        "headless": HEADLESS,
        "window_size": (1920, 1080),
        "options": []
    }
}

# 报告目录
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# 日志目录
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

