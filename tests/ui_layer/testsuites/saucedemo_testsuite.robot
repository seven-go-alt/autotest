*** Settings ***
Documentation     SauceDemo 购买流程测试
...               演示完整的电商购买流程
...               包括：登录、选购、结账

Library    ../keywords/saucedemo_keywords.py

Suite Setup       打开浏览器    https://www.saucedemo.com
Suite Teardown    关闭浏览器

*** Test Cases ***

完整的购买流程
    [Documentation]    验证用户能够成功完成购买流程
    [Tags]    ui    saucedemo    smoke
    
    登录 SauceDemo    standard_user    secret_sauce
    添加产品到购物车    0
    添加产品到购物车    1
    验证购物车数量    2
    前往购物车
    前往结账
    填写结账信息    John    Doe    12345
    完成结账
    验证订单完成


仅登录测试
    [Documentation]    验证用户能够登录系统
    [Tags]    ui    saucedemo    login
    
    登录 SauceDemo    standard_user    secret_sauce
    验证元素存在    css=.inventory_container


登录失败测试 - 错误密码
    [Documentation]    验证错误的密码会导致登录失败
    [Tags]    ui    saucedemo    negative
    
    登录 SauceDemo    standard_user    wrong_password
    验证元素存在    css=h3[data-test='error']
