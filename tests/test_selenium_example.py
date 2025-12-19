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
        """测试页面导航和元素检测"""
        import time
        helper = selenium_driver
        helper.navigate_to(base_url)
        
        time.sleep(2)
        
        # 检查页面标题
        title = helper.get_title()
        assert "Python" in title, f"页面标题应包含 'Python'，实际标题: {title}"
        
        # 检查页面内容
        page_source = helper.driver.page_source
        assert len(page_source) > 1000, "页面源代码过短，可能未正确加载"
        
        print(f"✓ 页面标题: {title}")
        print(f"✓ 页面内容字节数: {len(page_source)}")
    
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

