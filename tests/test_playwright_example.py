"""
Playwright 示例测试用例
使用 pytest 运行
"""
import pytest
from utils.playwright_helper import PlaywrightHelper
import config.settings as settings


@pytest.mark.playwright
@pytest.mark.smoke
class TestPlaywrightExample:
    """Playwright 示例测试类"""
    
    def test_baidu_search(self, playwright_page, base_url):
        """测试百度搜索功能"""
        helper = playwright_page
        helper.navigate_to(base_url)
        
        # 等待搜索框出现
        helper.wait_for_selector("#kw")
        
        # 输入搜索关键词
        helper.fill("#kw", "playwright")
        
        # 点击搜索按钮
        helper.click("#su")
        
        # 等待搜索结果
        helper.wait_for_selector("#content_left")
        
        # 验证页面标题
        title = helper.get_title()
        assert "playwright" in title.lower() or "百度" in title
    
    def test_page_navigation(self, playwright_page, base_url):
        """测试页面导航"""
        helper = playwright_page
        helper.navigate_to(base_url)
        
        # 等待页面加载完成
        helper.wait_for_load_state("networkidle")
        
        url = helper.get_url()
        assert base_url in url
    
    def test_take_screenshot(self, playwright_page, base_url):
        """测试截图功能"""
        helper = playwright_page
        helper.navigate_to(base_url)
        
        screenshot_path = helper.take_screenshot("playwright_screenshot.png")
        assert screenshot_path.exists()
    
    def test_javascript_execution(self, playwright_page, base_url):
        """测试 JavaScript 执行"""
        helper = playwright_page
        helper.navigate_to(base_url)
        
        # 执行 JavaScript 获取页面标题
        title = helper.evaluate("document.title")
        assert title is not None

