#!/bin/bash
# 测试运行脚本

echo "=========================================="
echo "自动化测试框架运行脚本"
echo "=========================================="

# 创建报告目录
mkdir -p reports

# 选择测试框架
echo "请选择测试框架:"
echo "1) pytest (Selenium)"
echo "2) pytest (Playwright)"
echo "3) pytest (全部)"
echo "4) Robot Framework"
echo "5) 全部运行"
read -p "请输入选项 (1-5): " choice

case $choice in
    1)
        echo "运行 pytest Selenium 测试..."
        pytest tests/test_selenium_example.py -m selenium -v
        ;;
    2)
        echo "运行 pytest Playwright 测试..."
        pytest tests/test_playwright_example.py -m playwright -v
        ;;
    3)
        echo "运行所有 pytest 测试..."
        pytest tests/ -v
        ;;
    4)
        echo "运行 Robot Framework 测试..."
        robot --outputdir reports/robotframework tests/robotframework/
        ;;
    5)
        echo "运行所有测试..."
        echo "--- pytest Selenium ---"
        pytest tests/test_selenium_example.py -m selenium -v
        echo "--- pytest Playwright ---"
        pytest tests/test_playwright_example.py -m playwright -v
        echo "--- Robot Framework ---"
        robot --outputdir reports/robotframework tests/robotframework/
        ;;
    *)
        echo "无效选项"
        exit 1
        ;;
esac

echo "=========================================="
echo "测试完成！报告位置: reports/"
echo "=========================================="

