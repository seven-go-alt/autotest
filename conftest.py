"""
pytest 配置文件
提供 fixtures 和测试钩子
"""
import pytest
import logging
from pathlib import Path
from utils.selenium_helper import SeleniumHelper
from utils.playwright_helper import PlaywrightHelper
import config.settings as settings

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def selenium_driver(request):
    """
    Selenium 驱动 fixture
    支持失败时自动截图
    """
    helper = SeleniumHelper(screenshot_on_failure=True)
    driver = helper.start_browser()
    
    yield helper
    
    # 如果测试失败，自动截图
    if request.node.rep_call.failed if hasattr(request.node, 'rep_call') else False:
        try:
            test_name = request.node.name
            screenshot_path = helper.take_failure_screenshot(test_name)
            logger.warning(f"测试失败: {test_name}，截图保存至: {screenshot_path}")
        except Exception as e:
            logger.error(f"截图保存失败: {str(e)}")
    
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
    return settings.BASE_URL


@pytest.fixture(scope="session")
def api_base_url():
    """API 基础 URL fixture"""
    import config.settings as settings
    return settings.API_BASE_URL

