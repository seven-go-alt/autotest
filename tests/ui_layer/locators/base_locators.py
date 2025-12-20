# -*- coding: utf-8 -*-
"""
定位器基类：通用的页面元素定位器
"""

class BaseLocators:
    """基础定位器 - 通用元素"""
    
    # 页面通用元素
    PAGE_TITLE = "tag=title"
    PAGE_BODY = "tag=body"
    PAGE_HEADER = "tag=header"
    PAGE_FOOTER = "tag=footer"
    
    # 通用按钮和链接
    BUTTON_SUBMIT = "css=button[type='submit']"
    BUTTON_CANCEL = "css=button[type='button']"
    BUTTON_CLOSE = "css=button.close"
    LINK_HOME = "css=a[href='/']"
    
    # 通用输入框
    INPUT_TEXT = "css=input[type='text']"
    INPUT_EMAIL = "css=input[type='email']"
    INPUT_PASSWORD = "css=input[type='password']"
    
    # 通用消息和弹框
    ALERT_MESSAGE = "css=.alert"
    SUCCESS_MESSAGE = "css=.alert-success"
    ERROR_MESSAGE = "css=.alert-error"
    MODAL_DIALOG = "css=.modal"
    MODAL_CLOSE_BTN = "css=.modal button.close"
