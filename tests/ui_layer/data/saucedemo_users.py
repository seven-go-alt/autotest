# -*- coding: utf-8 -*-
"""
SauceDemo 网站测试用户数据
数据来源：https://www.saucedemo.com/
所有用户密码：secret_sauce
"""


class SauceDemoUsers:
    """SauceDemo 测试用户集合"""

    # ========== 用户账户 ==========
    STANDARD_USER = {
        'username': 'standard_user',
        'password': 'secret_sauce',
        'description': '标准用户（正常用户）'
    }

    LOCKED_OUT_USER = {
        'username': 'locked_out_user',
        'password': 'secret_sauce',
        'description': '被锁定的用户，登录会显示错误提示'
    }

    PROBLEM_USER = {
        'username': 'problem_user',
        'password': 'secret_sauce',
        'description': '问题用户，会遇到渲染问题'
    }

    PERFORMANCE_GLITCH_USER = {
        'username': 'performance_glitch_user',
        'password': 'secret_sauce',
        'description': '性能问题用户，页面加载会缓慢'
    }

    ERROR_USER = {
        'username': 'error_user',
        'password': 'secret_sauce',
        'description': '错误用户，会显示 500 错误'
    }

    VISUAL_USER = {
        'username': 'visual_user',
        'password': 'secret_sauce',
        'description': '可视用户，界面会有差异'
    }

    # ========== 用户列表（方便遍历） ==========
    ALL_USERS = [
        STANDARD_USER,
        LOCKED_OUT_USER,
        PROBLEM_USER,
        PERFORMANCE_GLITCH_USER,
        ERROR_USER,
        VISUAL_USER,
    ]

    # ========== 登录相关的通用密码 ==========
    COMMON_PASSWORD = 'secret_sauce'


class SauceDemoCheckoutData:
    """SauceDemo 结账表单测试数据"""

    STANDARD_CHECKOUT = {
        'first_name': 'Auto',
        'last_name': 'Tester',
        'postal_code': '12345',
        'description': '标准结账信息'
    }

    VALID_CHECKOUT_1 = {
        'first_name': 'John',
        'last_name': 'Doe',
        'postal_code': '98765',
        'description': '有效的结账信息 1'
    }

    VALID_CHECKOUT_2 = {
        'first_name': '张',
        'last_name': '三',
        'postal_code': '100000',
        'description': '有效的结账信息 2（中文名字）'
    }

    # ========== 无效的结账数据 ==========
    INVALID_CHECKOUT_NO_FIRST_NAME = {
        'first_name': '',
        'last_name': 'Doe',
        'postal_code': '12345',
        'description': '缺少名字'
    }

    INVALID_CHECKOUT_NO_LAST_NAME = {
        'first_name': 'John',
        'last_name': '',
        'postal_code': '12345',
        'description': '缺少姓氏'
    }

    INVALID_CHECKOUT_NO_POSTAL_CODE = {
        'first_name': 'John',
        'last_name': 'Doe',
        'postal_code': '',
        'description': '缺少邮编'
    }

    VALID_CHECKOUTS = [
        STANDARD_CHECKOUT,
        VALID_CHECKOUT_1,
        VALID_CHECKOUT_2,
    ]
