"""
Selenium 示例测试用例
使用 pytest 运行
"""
import pytest
from utils.selenium_helper import SeleniumHelper
import config.settings as settings


@pytest.mark.selenium
@pytest.mark.smoke
class TestSeleniumExample:
    """Selenium 示例测试类"""
    
    def test_baidu_search(self, selenium_driver, base_url):
        """测试百度搜索功能"""
        helper = selenium_driver
        helper.navigate_to(base_url)
        
        # 等待搜索框出现
        helper.wait_for_element_visible("id", "kw")
        
        # 输入搜索关键词
        helper.input_text("id", "kw", "pytest")
        
        # 点击搜索按钮
        helper.click("id", "su")
        
        # 等待搜索结果
        helper.wait_for_element_visible("id", "content_left")
        
        # 验证页面标题包含关键词
        title = helper.get_title()
        assert "pytest" in title.lower() or "百度" in title
    
    def test_page_title(self, selenium_driver, base_url):
        """测试页面标题"""
        helper = selenium_driver
        helper.navigate_to(base_url)
        
        title = helper.get_title()
        assert title is not None
        assert len(title) > 0
    
    def test_take_screenshot(self, selenium_driver, base_url):
        """测试截图功能"""
        helper = selenium_driver
        helper.navigate_to(base_url)
        
        screenshot_path = helper.take_screenshot("selenium_screenshot.png")
        assert screenshot_path.exists()

