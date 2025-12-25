#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一测试入口脚本（推荐使用这个脚本来运行 Web UI / 少量 API 自动化）

功能：
- 根据参数选择执行 UI / API 测试
- 通过 env / browser / platform / tags 等参数控制执行范围
- 统一构建 Robot Framework 命令，并复用现有 config.settings 配置
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path

from config.settings import REPORTS_DIR, get_env_config


def create_robot_reports_dir(output_dir: str) -> Path:
    """创建 Robot 报告目录"""
    base_dir = Path(output_dir)
    base_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Robot 报告目录已准备: {base_dir}/")
    return base_dir


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="统一测试入口脚本（Robot Framework 为主）"
    )

    parser.add_argument(
        "--test-type",
        choices=["ui", "api"],
        required=True,
        help="测试类型：ui 或 api",
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


def main() -> None:
    args = parse_args()

    # 创建报告目录
    create_robot_reports_dir(args.output_dir)

    # 构建并执行 Robot 命令
    cmd = build_robot_cmd(args)
    print("\n即将执行命令：")
    print(" ".join(cmd))
    print()

    completed = subprocess.run(cmd)
    sys.exit(completed.returncode)


if __name__ == "__main__":
    main()


