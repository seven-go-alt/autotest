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


# pytest 钩子：在测试失败时自动生成报告和截图
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    在测试失败时生成报告
    """
    outcome = yield
    rep = outcome.get_result()
    
    # 记录失败信息
    if rep.failed:
        logger.error(f"测试失败: {item.name}")
        if call.excinfo:
            logger.error(f"异常信息: {call.excinfo.value}")


@pytest.fixture(scope="function", autouse=True)
def selenium_failure_screenshot(request, selenium_driver):
    """
    自动为 Selenium 测试失败的情况生成截图
    """
    yield
    
    # 检查测试是否失败
    if request.node.rep_call.failed if hasattr(request.node, 'rep_call') else False:
        try:
            if selenium_driver and selenium_driver.driver:
                screenshot_dir = Path(settings.REPORTS_DIR) / "selenium_screenshots"
                screenshot_dir.mkdir(parents=True, exist_ok=True)
                
                screenshot_name = f"failure_{request.node.name}.png"
                screenshot_path = screenshot_dir / screenshot_name
                
                selenium_driver.driver.save_screenshot(str(screenshot_path))
                logger.info(f"失败截图已保存: {screenshot_path}")
        except Exception as e:
            logger.warning(f"保存失败截图时出错: {str(e)}")
