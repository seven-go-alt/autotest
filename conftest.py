"""
pytest 配置文件
提供 fixtures 和测试钩子
"""
import pytest
from utils.selenium_helper import SeleniumHelper
from utils.playwright_helper import PlaywrightHelper


@pytest.fixture(scope="function")
def selenium_driver():
    """Selenium 驱动 fixture"""
    helper = SeleniumHelper()
    driver = helper.start_browser()
    yield helper
    helper.quit()


@pytest.fixture(scope="function")
def playwright_page():
    """Playwright 页面 fixture"""
    helper = PlaywrightHelper()
    page = helper.start_browser()
    yield helper
    helper.quit()


@pytest.fixture(scope="session")
def base_url():
    """基础 URL fixture"""
    import config.settings as settings
    return settings.BASE_URL

