# -*- coding: utf-8 -*-
"""
百度搜索关键字库
- 搜索操作
- 结果验证
- 导航
"""

from robot.api.deco import keyword
from robot.api import logger
from .base_keywords import BaseKeywords
from ..locators.baidu_locators import BaiduLocators


class BaiduKeywords(BaseKeywords):
    """百度搜索的业务关键字"""
    
    def __init__(self):
        super().__init__()
        self.locators = BaiduLocators()
    
    @keyword("搜索")
    def search(self, keyword_text):
        """在百度搜索框中输入关键词并搜索"""
        self.input_text(self.locators.SEARCH_INPUT, keyword_text)
        self.click(self.locators.SEARCH_BUTTON)
        logger.info(f"已搜索: {keyword_text}")
    
    @keyword("验证搜索结果存在")
    def verify_search_results_exist(self):
        """验证搜索结果页面存在结果"""
        self.element_should_exist(self.locators.SEARCH_RESULTS_CONTAINER)
        logger.info("搜索结果页面验证通过")
    
    @keyword("获取搜索结果数")
    def get_search_results_count(self):
        """获取搜索结果的数量"""
        results = self.page.query_selector_all(self.locators.SEARCH_RESULT_ITEM)
        count = len(results)
        logger.info(f"搜索结果数: {count}")
        return count
    
    @keyword("验证搜索结果包含关键词")
    def verify_results_contain_keyword(self, keyword_text):
        """验证搜索结果标题中包含关键词"""
        titles = self.page.query_selector_all(self.locators.SEARCH_RESULT_TITLE)
        if not titles:
            raise AssertionError("未找到搜索结果标题")
        
        # 检查至少一个结果包含关键词
        found = False
        for title in titles[:5]:  # 检查前5个结果
            title_text = title.text_content()
            if keyword_text in title_text:
                found = True
                break
        
        if not found:
            raise AssertionError(f"搜索结果中未找到关键词: {keyword_text}")
        logger.info(f"搜索结果验证通过: 包含关键词 '{keyword_text}'")
