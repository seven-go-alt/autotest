# -*- coding: utf-8 -*-
"""
定位器层：管理所有 UI 元素定位器（选择器）
- 按页面或功能模块组织
- 便于维护与修改定位器
"""
from robot.api.deco import keyword

class Locators:
    """UI 定位器管理类"""

    # ========== 搜索页面定位器 ==========
    SEARCH_INPUT = "css=input#kw"
    SEARCH_BUTTON = "css=button#su"
    SEARCH_RESULTS = "css=#content_left"
    
    # ========== 页面通用定位器 ==========
    PAGE_TITLE = "tag=title"
    PAGE_BODY = "tag=body"
    
    # ========== 测试站点定位器 ==========
    PYTHON_ORG_SEARCH = "css=form input[name='q']"
    PYTHON_ORG_SEARCH_BTN = "css=form button"
    
    @keyword("Get Locator")
    def get_locator(self, element_name: str) -> str:
        """返回指定元素的定位器"""
        locators_map = {
            "search_input": self.SEARCH_INPUT,
            "search_button": self.SEARCH_BUTTON,
            "search_results": self.SEARCH_RESULTS,
            "page_title": self.PAGE_TITLE,
            "page_body": self.PAGE_BODY,
            "python_search": self.PYTHON_ORG_SEARCH,
            "python_search_btn": self.PYTHON_ORG_SEARCH_BTN,
        }
        locator = locators_map.get(element_name.lower())
        if not locator:
            raise KeyError(f"Locator not found: {element_name}")
        return locator
