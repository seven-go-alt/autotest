"""
pytest 配置文件
提供 fixtures 和测试钩子
"""
import pytest
import logging
from pathlib import Path
from datetime import datetime
from utils.selenium_helper import SeleniumHelper
from utils.playwright_helper import PlaywrightHelper
from utils.test_data_manager import TestDataManager
import config.settings as settings

logger = logging.getLogger(__name__)


# ========== 浏览器 Fixtures ==========

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


# ========== 配置 Fixtures ==========

@pytest.fixture(scope="session")
def base_url():
    """基础 URL fixture"""
    return settings.BASE_URL


@pytest.fixture(scope="session")
def api_base_url():
    """API 基础 URL fixture"""
    return settings.API_BASE_URL


@pytest.fixture(scope="session")
def test_environment():
    """
    测试环境配置 fixture
    提供环境相关的配置信息
    """
    return {
        "base_url": settings.BASE_URL,
        "api_base_url": settings.API_BASE_URL,
        "browser": settings.BROWSER,
        "headless": settings.HEADLESS,
        "timeout": settings.TIMEOUT,
        "reports_dir": settings.REPORTS_DIR,
        "logs_dir": settings.LOGS_DIR,
    }


# ========== 测试数据 Fixtures ==========

@pytest.fixture(scope="session")
def test_data_manager():
    """
    测试数据管理器 fixture
    提供测试数据的加载和生成功能
    """
    return TestDataManager()


@pytest.fixture(scope="function")
def standard_user(test_data_manager):
    """标准测试用户"""
    return test_data_manager.get_test_user("standard")


@pytest.fixture(scope="function")
def invalid_user(test_data_manager):
    """无效测试用户"""
    return test_data_manager.get_test_user("invalid")


@pytest.fixture(scope="function")
def checkout_data(test_data_manager):
    """结账信息数据"""
    return test_data_manager.get_checkout_data()


@pytest.fixture(scope="function")
def random_user_data(test_data_manager):
    """随机用户数据"""
    return test_data_manager.generate_user_data()


# ========== 截图管理 Fixtures ==========

@pytest.fixture(scope="function")
def screenshot_manager(request):
    """
    截图管理器 fixture
    自动管理测试截图
    """
    screenshots = []
    
    def take_screenshot(page_or_driver, name: str = None):
        """保存截图"""
        if name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = request.node.name
            name = f"{test_name}_{timestamp}.png"
        
        screenshot_dir = settings.REPORTS_DIR / "screenshots"
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        filepath = screenshot_dir / name
        
        # 根据不同的驱动类型保存截图
        if hasattr(page_or_driver, 'screenshot'):  # Playwright
            page_or_driver.screenshot(path=str(filepath))
        elif hasattr(page_or_driver, 'save_screenshot'):  # Selenium
            page_or_driver.save_screenshot(str(filepath))
        
        screenshots.append(filepath)
        logger.info(f"截图已保存: {filepath}")
        return filepath
    
    yield take_screenshot
    
    # 清理（可选）
    logger.info(f"测试 {request.node.name} 共保存 {len(screenshots)} 张截图")


# ========== 测试报告增强 ==========

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    pytest 钩子：生成测试报告
    用于在 fixture 中访问测试结果
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="function", autouse=True)
def log_test_info(request):
    """
    自动记录测试信息
    在每个测试前后记录日志
    """
    test_name = request.node.name
    logger.info(f"{'='*60}")
    logger.info(f"开始测试: {test_name}")
    logger.info(f"{'='*60}")
    
    yield
    
    # 测试结束后记录结果
    if hasattr(request.node, 'rep_call'):
        if request.node.rep_call.passed:
            logger.info(f"✓ 测试通过: {test_name}")
        elif request.node.rep_call.failed:
            logger.error(f"✗ 测试失败: {test_name}")
        elif request.node.rep_call.skipped:
            logger.warning(f"⊘ 测试跳过: {test_name}")
    
    logger.info(f"{'='*60}\n")


# ========== 失败重试配置 ==========

def pytest_configure(config):
    """
    pytest 配置钩子
    配置测试运行参数
    """
    # 添加自定义标记
    config.addinivalue_line(
        "markers", "flaky: 标记不稳定的测试，自动重试"
    )
    config.addinivalue_line(
        "markers", "slow: 标记慢速测试"
    )
    config.addinivalue_line(
        "markers", "critical: 标记关键测试用例"
    )
    config.addinivalue_line(
        "markers", "performance: 标记性能测试"
    )


# ========== 清理 Fixtures ==========

@pytest.fixture(scope="session", autouse=True)
def cleanup_old_reports():
    """
    清理旧的测试报告
    在测试会话开始前执行
    """
    # 可选：清理超过 N 天的旧报告
    logger.info("测试会话开始")
    yield
    logger.info("测试会话结束")


