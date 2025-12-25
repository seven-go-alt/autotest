#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一测试运行脚本（合并 run_test.py 与 run_tests.py 的功能）

支持：
- 命令行调用运行 Robot（复用 run_tests.py 的 CLI）
- 交互式菜单运行 pytest / Robot（复用 run_test.py 的交互菜单）
"""

import argparse
import sys
import subprocess
from pathlib import Path

try:
    from config.settings import REPORTS_DIR, get_env_config
except Exception:
    # 在某些环境下 import 可能失败；延迟处理时可捕获并提示
    def get_env_config(name):
        class C: pass
        c = C()
        c.name = name
        c.base_url = "http://localhost"
        c.api_base_url = "http://localhost"
        return c


def create_reports_dir():
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    (reports_dir / "robotframework").mkdir(exist_ok=True)
    tmp_dir = Path("tmp")
    tmp_dir.mkdir(exist_ok=True)
    print(f"✓ 报告目录已准备: {reports_dir}/ 和 {tmp_dir}/")


def run_pytest_selenium():
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


def create_robot_reports_dir(output_dir: str):
    base_dir = Path(output_dir)
    base_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Robot 报告目录已准备: {base_dir}/")
    return base_dir


def build_robot_cmd_from_args(args: argparse.Namespace):
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
    if args.include:
        cmd += ["--include", args.include]
    if args.exclude:
        cmd += ["--exclude", args.exclude]
    listener_path = "listeners/web_listener.py"
    if Path(listener_path).exists():
        cmd += ["--listener", listener_path]
    if args.test_type == "ui":
        target = args.suite or "ui_tests/testsuites"
    else:
        target = args.suite or "api_tests/testsuites"
    cmd.append(target)
    return cmd


def run_robot_framework_with_args(args: argparse.Namespace):
    create_robot_reports_dir(args.output_dir)
    cmd = build_robot_cmd_from_args(args)
    print("\n即将执行 Robot 命令：")
    print(" ".join(cmd))
    return subprocess.run(cmd)


def run_all_tests_interactive():
    create_reports_dir()
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
    result3 = subprocess.run([sys.executable, "-m", "robot", "--outputdir", "tmp", "tests/robotframework/"])
    results.append(("Robot Framework", result3.returncode))
    print("\n测试执行总结")
    for test_name, returncode in results:
        status = "✓ 通过" if returncode == 0 else "✗ 失败"
        print(f"{test_name}: {status}")
    return all(code == 0 for _, code in results)


def interactive_menu():
    create_reports_dir()
    while True:
        print("\n==========================================")
        print("自动化测试运行脚本 - 交互式模式")
        print("==========================================")
        print("1) pytest (Selenium)")
        print("2) pytest (Playwright)")
        print("3) pytest (API)")
        print("4) pytest (全部)")
        print("5) Robot Framework")
        print("6) 全部运行")
        print("0) 退出")
        choice = input("请选择: ").strip()
        if choice == "1":
            r = run_pytest_selenium()
            if r.returncode != 0:
                print("pytest Selenium 测试失败")
        elif choice == "2":
            r = run_pytest_playwright()
            if r.returncode != 0:
                print("pytest Playwright 测试失败")
        elif choice == "3":
            r = run_pytest_api()
            if r.returncode != 0:
                print("pytest API 测试失败")
        elif choice == "4":
            r = run_pytest_all()
            if r.returncode != 0:
                print("pytest 全部测试失败")
        elif choice == "5":
            subprocess.run([sys.executable, "-m", "robot", "--outputdir", "tmp", "tests/robotframework/"])
        elif choice == "6":
            if not run_all_tests_interactive():
                print("部分测试失败，请查看 tmp/ 下报告")
        elif choice == "0":
            break
        else:
            print("无效选项")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="统一测试入口脚本（合并版）")
    parser.add_argument("--test-type", choices=["ui", "api"], help="测试类型：ui 或 api")
    parser.add_argument("--env", default="dev")
    parser.add_argument("--browser", default="chrome")
    parser.add_argument("--platform", choices=["pc", "mobile"], default="pc")
    parser.add_argument("--tags", dest="include")
    parser.add_argument("--exclude")
    parser.add_argument("--suite")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--output-dir", default=str(Path("tmp")))
    return parser.parse_args()


def main() -> None:
    # 如果有命令行参数则走 CLI，否则进入交互式菜单
    if len(sys.argv) > 1:
        args = parse_args()
        if args.test_type:
            run_robot_framework_with_args(args)
        else:
            print("未指定 --test-type，进入交互式菜单")
            interactive_menu()
    else:
        interactive_menu()


if __name__ == "__main__":
    main()
