# -*- coding: utf-8 -*-
"""
SauceDemo 网站测试数据和配置
"""

# ========== SauceDemo 网站地址 ==========
SAUCEDEMO_URL = "https://www.saucedemo.com/"

# ========== 登录用户凭证 ==========
# 所有用户密码均为：secret_sauce

VALID_USER = {
    'username': 'standard_user',
    'password': 'secret_sauce'
}

LOCKED_OUT_USER = {
    'username': 'locked_out_user',
    'password': 'secret_sauce'
}

PROBLEM_USER = {
    'username': 'problem_user',
    'password': 'secret_sauce'
}

PERFORMANCE_GLITCH_USER = {
    'username': 'performance_glitch_user',
    'password': 'secret_sauce'
}

ERROR_USER = {
    'username': 'error_user',
    'password': 'secret_sauce'
}

VISUAL_USER = {
    'username': 'visual_user',
    'password': 'secret_sauce'
}

# ========== 所有测试用户 ==========
ALL_TEST_USERS = [
    VALID_USER,
    LOCKED_OUT_USER,
    PROBLEM_USER,
    PERFORMANCE_GLITCH_USER,
    ERROR_USER,
    VISUAL_USER,
]

# ========== 测试产品数据 ==========
PRODUCTS = {
    'sauce_labs_backpack': {
        'name': 'Sauce Labs Backpack',
        'price': '$29.99',
        'test_id': 'add-to-cart-sauce-labs-backpack'
    },
    'sauce_labs_bike_light': {
        'name': 'Sauce Labs Bike Light',
        'price': '$9.99',
        'test_id': 'add-to-cart-sauce-labs-bike-light'
    },
    'sauce_labs_bolt_t_shirt': {
        'name': 'Sauce Labs Bolt T-Shirt',
        'price': '$15.99',
        'test_id': 'add-to-cart-sauce-labs-bolt-t-shirt'
    },
    'sauce_labs_fleece_jacket': {
        'name': 'Sauce Labs Fleece Jacket',
        'price': '$49.99',
        'test_id': 'add-to-cart-sauce-labs-fleece-jacket'
    },
    'sauce_labs_onesie': {
        'name': 'Sauce Labs Onesie',
        'price': '$7.99',
        'test_id': 'add-to-cart-sauce-labs-onesie'
    },
    'test_all_products_are_expensive': {
        'name': 'Test.allProductsAreExpensive',
        'price': '$0',
        'test_id': 'add-to-cart-test-allProductsAreExpensive'
    },
}

# ========== 结账用户信息 ==========
CHECKOUT_INFO = {
    'standard': {
        'first_name': 'Auto',
        'last_name': 'Tester',
        'postal_code': '12345'
    },
    'another': {
        'first_name': 'John',
        'last_name': 'Doe',
        'postal_code': '98765'
    },
}

# ========== 排序选项 ==========
SORT_OPTIONS = {
    'a_to_z': {
        'label': 'Name (A to Z)',
        'value': 'az'
    },
    'z_to_a': {
        'label': 'Name (Z to A)',
        'value': 'za'
    },
    'low_to_high': {
        'label': 'Price (low to high)',
        'value': 'lohi'
    },
    'high_to_low': {
        'label': 'Price (high to low)',
        'value': 'hilo'
    },
}
