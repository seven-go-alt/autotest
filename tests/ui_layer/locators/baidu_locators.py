# -*- coding: utf-8 -*-
"""
百度搜索引擎定位器
URL: https://www.baidu.com
"""

from .base_locators import BaseLocators


class BaiduLocators(BaseLocators):
    """百度搜索页面的 UI 定位器"""
    
    # ========== 搜索框 ==========
    SEARCH_INPUT = "css=input#kw"
    SEARCH_BUTTON = "css=button#su"
    SEARCH_FORM = "id=form"
    
    # ========== 搜索结果 ==========
    SEARCH_RESULTS_CONTAINER = "css=#content_left"
    SEARCH_RESULT_ITEM = "css=.result"
    SEARCH_RESULT_TITLE = "css=.t a"
    SEARCH_RESULT_SNIPPET = "css=.c-snippet_newlayout"
    
    # ========== 页面链接 ==========
    NEWS_LINK = "css=a[href='https://news.baidu.com/']"
    IMAGES_LINK = "css=a[href='https://image.baidu.com/']"
    VIDEOS_LINK = "css=a[href='https://v.baidu.com/']"
    MAPS_LINK = "css=a[href='https://map.baidu.com/']"
