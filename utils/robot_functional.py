# -*- coding: utf-8 -*-
"""
功能层：高级业务操作
- 组合步骤层操作完成业务功能
- 例如：完整的搜索流程、登录流程等
"""
from robot.api.deco import keyword
from robot.api import logger
from utils.robot_steps import StepsLibrary

class FunctionalLibrary:
    """功能层库：业务流程操作"""

    ROBOT_LIBRARY_SCOPE = "SUITE"

    def __init__(self):
        self.steps = StepsLibrary()

    @keyword("Complete Search Flow")
    def complete_search_flow(self, search_term):
        """完整的搜索流程"""
        logger.info(f"Starting search flow for: {search_term}")
        self.steps.fill_input_by_name("search_input", search_term)
        self.steps.click_element_by_name("search_button")
        self.steps.wait_for_element_by_name("search_results", timeout=15)
        logger.info("Search flow completed")

    @keyword("Verify Search Result")
    def verify_search_result(self):
        """验证搜索结果"""
        results = self.steps.get_element_text("search_results")
        if not results:
            raise AssertionError("Search results are empty")
        logger.info("Search results verified")
        return results

    @keyword("Get And Verify Page Title")
    def get_and_verify_page_title(self, expected_keywords=None):
        """获取并验证页面标题"""
        title = self.steps.get_page_title()
        logger.info(f"Page title: {title}")
        
        if expected_keywords:
            for keyword in expected_keywords:
                if keyword.lower() not in title.lower():
                    raise AssertionError(f"Expected '{keyword}' in title: {title}")
        
        return title

    @keyword("Setup Browser And Navigate")
    def setup_browser_and_navigate(self, url, browser_type="chromium", headless=True):
        """初始化浏览器并导航"""
        self.steps.init_browser(browser_type, headless)
        self.steps.navigate_to(url)
        logger.info(f"Browser setup and navigation completed for: {url}")

    @keyword("Cleanup Browser")
    def cleanup_browser(self):
        """清理浏览器资源"""
        self.steps.close_browser()
        logger.info("Browser cleanup completed")
