#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一测试入口脚本

功能：
1. 命令行参数模式（推荐用于 CI/CD 或脚本调用）：
   - 根据 --test-type 参数选择执行 UI / API 测试
   - 通过 env / browser / platform / tags 等参数控制执行范围
   - 统一构建 Robot Framework 命令

2. 交互式菜单模式（无参数时）：
   - 支持 pytest (Selenium/Playwright/API) 和 Robot Framework 测试
   - 适合本地开发和调试
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path

from config.settings import REPORTS_DIR, get_env_config


def create_reports_dir() -> None:
    """创建报告目录"""
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    robotframework_dir = reports_dir / "robotframework"
    robotframework_dir.mkdir(exist_ok=True)

    tmp_dir = Path("tmp")
    tmp_dir.mkdir(exist_ok=True)
    print(f"✓ 报告目录已准备: {reports_dir}/ 和 {tmp_dir}/")


def create_robot_reports_dir(output_dir: str) -> Path:
    """创建 Robot 报告目录"""
    base_dir = Path(output_dir)
    base_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Robot 报告目录已准备: {base_dir}/")
    return base_dir


# ========== pytest 相关函数（交互式菜单使用）==========

def run_pytest_selenium():
    """运行 pytest Selenium 测试"""
    print("\n运行 pytest Selenium 测试...")
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/test_UI",
        "-m",
        "selenium",
        "-v",
        "--html=tmp/pytest_selenium.html",
        "--self-contained-html",
    ]
    return subprocess.run(cmd)


def run_pytest_playwright():
    """运行 pytest Playwright 测试"""
    print("\n运行 pytest Playwright 测试...")
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/test_UI",
        "-m",
        "playwright",
        "-v",
        "--html=tmp/pytest_playwright.html",
        "--self-contained-html",
    ]
    return subprocess.run(cmd)


def run_pytest_all():
    """运行所有 pytest 测试"""
    print("\n运行所有 pytest 测试...")
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/",
        "-v",
        "--html=tmp/pytest_all.html",
        "--self-contained-html",
    ]
    return subprocess.run(cmd)


def run_pytest_api():
    """运行 API 测试"""
    print("\n运行 API 测试...")
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/test_API",
        "-m",
        "api",
        "-v",
        "--html=tmp/pytest_api.html",
        "--self-contained-html",
    ]
    return subprocess.run(cmd)


def run_robot_framework_legacy():
    """运行 Robot Framework 测试（旧版，交互式菜单使用）"""
    print("\n运行 Robot Framework 测试...")
    cmd = [
        sys.executable,
        "-m",
        "robot",
        "--outputdir",
        "tmp",
        "tests/robotframework/",
    ]
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

    print("\n--- pytest API ---")
    result_api = run_pytest_api()
    results.append(("pytest API", result_api.returncode))

    print("\n--- Robot Framework ---")
    result3 = run_robot_framework_legacy()
    results.append(("Robot Framework", result3.returncode))

    print("\n========================================")
    print("测试执行总结")
    print("========================================")
    for test_name, returncode in results:
        status = "✓ 通过" if returncode == 0 else "✗ 失败"
        print(f"{test_name}: {status}")

    return all(code == 0 for _, code in results)


# ========== Robot Framework 命令行参数模式相关函数 ==========

def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="统一测试入口脚本（支持 Robot Framework 参数模式和交互式菜单模式）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例（命令行参数模式）:
  # 运行 UI 测试（P0 用户模块）
  python run_tests.py --test-type ui --env dev --browser chrome --tags "P0ANDuser"

  # 运行 API 测试
  python run_tests.py --test-type api --env test

  # 运行指定 suite
  python run_tests.py --test-type ui --suite ui_tests/testsuites/user/user_login_tests.robot

交互式菜单模式:
  # 直接运行（无参数）进入交互式菜单
  python run_tests.py
        """,
    )

    parser.add_argument(
        "--test-type",
        choices=["ui", "api"],
        help="测试类型：ui 或 api（提供此参数时进入命令行参数模式）",
    )
    parser.add_argument(
        "--env",
        default="dev",
        help="测试环境标识，如 dev/test/stage/prod，默认 dev",
    )
    parser.add_argument(
        "--browser",
        default="chrome",
        help="浏览器类型，如 chrome/firefox/edge，默认 chrome",
    )
    parser.add_argument(
        "--platform",
        choices=["pc", "mobile"],
        default="pc",
        help="平台：pc 或 mobile，默认 pc",
    )
    parser.add_argument(
        "--tags",
        "--include",
        dest="include",
        help="需要包含的标签表达式，例如：P0ANDuser",
    )
    parser.add_argument(
        "--exclude",
        help="需要排除的标签表达式，例如：flaky",
    )
    parser.add_argument(
        "--suite",
        help="指定要执行的 testsuite 文件或目录（相对项目根目录）",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="是否以无头模式运行浏览器",
    )
    parser.add_argument(
        "--output-dir",
        default=str(Path("tmp")),
        help="Robot 报告输出目录，默认 tmp",
    )

    return parser.parse_args()


def build_robot_cmd(args: argparse.Namespace) -> list:
    """根据参数构建 Robot Framework 命令"""
    env_conf = get_env_config(args.env)

    cmd = [
        sys.executable,
        "-m",
        "robot",
        "--outputdir",
        args.output_dir,
        "--variable",
        f"ENV:{env_conf.name}",
        "--variable",
        f"BASE_URL:{env_conf.base_url}",
        "--variable",
        f"API_BASE_URL:{env_conf.api_base_url}",
        "--variable",
        f"BROWSER:{args.browser}",
        "--variable",
        f"PLATFORM:{args.platform}",
    ]

    if args.headless:
        cmd += ["--variable", "HEADLESS:True"]

    # 标签过滤
    if args.include:
        cmd += ["--include", args.include]
    if args.exclude:
        cmd += ["--exclude", args.exclude]

    # 监听器（用于用例依赖、用例名后缀、结果上报等，当前为骨架）
    listener_path = "listeners/web_listener.py"
    if Path(listener_path).exists():
        cmd += ["--listener", listener_path]

    # 选择测试目标路径
    if args.test_type == "ui":
        target = args.suite or "ui_tests/testsuites"
    else:
        target = args.suite or "api_tests/testsuites"

    cmd.append(target)
    return cmd


# ========== 交互式菜单模式 ==========

def display_menu():
    """显示交互式菜单"""
    print("\n==========================================")
    print("自动化测试框架运行脚本 - 交互式菜单")
    print("==========================================")
    print("请选择测试框架:")
    print("1) pytest (Selenium)")
    print("2) pytest (Playwright)")
    print("3) pytest (API)")
    print("4) pytest (全部)")
    print("5) Robot Framework (推荐用于功能型/关键字封装测试)")
    print("6) 全部运行")
    print("0) 退出")
    print("==========================================")
    print("\n提示：如需使用命令行参数模式，请使用 --test-type 参数")
    print("     例如: python run_tests.py --test-type ui --env dev --tags P0\n")


def run_interactive_mode():
    """运行交互式菜单模式"""
    create_reports_dir()

    while True:
        display_menu()
        try:
            choice = input("请输入选项 (0-6): ").strip()

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
                result = run_pytest_api()
                if result.returncode != 0:
                    print("\n✗ pytest API 测试失败")
                    sys.exit(result.returncode)
            elif choice == "4":
                result = run_pytest_all()
                if result.returncode != 0:
                    print("\n✗ pytest 测试失败")
                    sys.exit(result.returncode)
            elif choice == "5":
                result = run_robot_framework_legacy()
                if result.returncode != 0:
                    print("\n✗ Robot Framework 测试失败")
                    sys.exit(result.returncode)
            elif choice == "6":
                if not run_all_tests():
                    sys.exit(1)
            elif choice == "0":
                print("退出程序")
                sys.exit(0)
            else:
                print("✗ 无效选项，请重新输入 (0-6)")
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
    print("测试完成！报告位置: tmp/ （Robot 与 pytest 报告将生成到 tmp/ 下）")
    print("==========================================")


# ========== 命令行参数模式 ==========

def run_command_line_mode(args: argparse.Namespace) -> None:
    """运行命令行参数模式"""
    # 创建报告目录
    create_robot_reports_dir(args.output_dir)

    # 构建并执行 Robot 命令
    cmd = build_robot_cmd(args)
    print("\n即将执行命令：")
    print(" ".join(cmd))
    print()

    completed = subprocess.run(cmd)
    sys.exit(completed.returncode)


# ========== 主函数 ==========

def main() -> None:
    """主函数：根据是否有 --test-type 参数决定运行模式"""
    args = parse_args()

    # 如果提供了 --test-type 参数，进入命令行参数模式
    if args.test_type:
        run_command_line_mode(args)
    else:
        # 否则进入交互式菜单模式
        run_interactive_mode()


if __name__ == "__main__":
    main()
