#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化测试框架运行脚本
支持 pytest (Selenium/Playwright) 和 Robot Framework 测试
"""

import os
import sys
import subprocess
from pathlib import Path


def create_reports_dir():
    """创建报告目录"""
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    robotframework_dir = reports_dir / "robotframework"
    robotframework_dir.mkdir(exist_ok=True)
    print(f"✓ 报告目录已准备: {reports_dir}/")


def run_pytest_selenium():
    """运行 pytest Selenium 测试"""
    print("\n运行 pytest Selenium 测试...")
    cmd = [sys.executable, "-m", "pytest", "tests/test_selenium_example.py", "-m", "selenium", "-v"]
    return subprocess.run(cmd)


def run_pytest_playwright():
    """运行 pytest Playwright 测试"""
    print("\n运行 pytest Playwright 测试...")
    cmd = [sys.executable, "-m", "pytest", "tests/test_playwright_example.py", "-m", "playwright", "-v"]
    return subprocess.run(cmd)


def run_pytest_all():
    """运行所有 pytest 测试"""
    print("\n运行所有 pytest 测试...")
    cmd = [sys.executable, "-m", "pytest", "tests/", "-v"]
    return subprocess.run(cmd)


def run_robot_framework():
    """运行 Robot Framework 测试"""
    print("\n运行 Robot Framework 测试...")
    cmd = [sys.executable, "-m", "robot", "--outputdir", "reports/robotframework", "tests/robotframework/"]
    return subprocess.run(cmd)


def run_all_tests():
    """运行所有测试"""
    print("\n========================================")
    print("运行全部测试")
    print("========================================\n")
    
    results = []
    
    print("--- pytest Selenium ---")
    result1 = run_pytest_selenium()
    results.append(("pytest Selenium", result1.returncode))
    
    print("\n--- pytest Playwright ---")
    result2 = run_pytest_playwright()
    results.append(("pytest Playwright", result2.returncode))
    
    print("\n--- Robot Framework ---")
    result3 = run_robot_framework()
    results.append(("Robot Framework", result3.returncode))
    
    print("\n========================================")
    print("测试执行总结")
    print("========================================")
    for test_name, returncode in results:
        status = "✓ 通过" if returncode == 0 else "✗ 失败"
        print(f"{test_name}: {status}")
    
    return all(code == 0 for _, code in results)


def display_menu():
    """显示菜单"""
    print("\n==========================================")
    print("自动化测试框架运行脚本")
    print("==========================================")
    print("请选择测试框架:")
    print("1) pytest (Selenium)")
    print("2) pytest (Playwright)")
    print("3) pytest (全部)")
    print("4) Robot Framework")
    print("5) 全部运行")
    print("0) 退出")
    print("==========================================\n")


def main():
    """主函数"""
    # 创建报告目录
    create_reports_dir()
    
    while True:
        display_menu()
        try:
            choice = input("请输入选项 (0-5): ").strip()
            
            if choice == "1":
                result = run_pytest_selenium()
                if result.returncode != 0:
                    print("\n✗ pytest Selenium 测试失败")
                    sys.exit(result.returncode)
            elif choice == "2":
                result = run_pytest_playwright()
                if result.returncode != 0:
                    print("\n✗ pytest Playwright 测试失败")
                    sys.exit(result.returncode)
            elif choice == "3":
                result = run_pytest_all()
                if result.returncode != 0:
                    print("\n✗ pytest 测试失败")
                    sys.exit(result.returncode)
            elif choice == "4":
                result = run_robot_framework()
                if result.returncode != 0:
                    print("\n✗ Robot Framework 测试失败")
                    sys.exit(result.returncode)
            elif choice == "5":
                if not run_all_tests():
                    sys.exit(1)
            elif choice == "0":
                print("退出程序")
                sys.exit(0)
            else:
                print("✗ 无效选项，请重新输入 (0-5)")
                continue
            
            # 单个测试成功后询问是否继续
            again = input("\n是否继续运行其他测试? (y/n): ").strip().lower()
            if again != "y":
                break
        
        except KeyboardInterrupt:
            print("\n\n程序已中断")
            sys.exit(1)
        except Exception as e:
            print(f"\n✗ 发生错误: {e}")
            sys.exit(1)
    
    print("\n==========================================")
    print("测试完成！报告位置: reports/")
    print("==========================================")


if __name__ == "__main__":
    main()
