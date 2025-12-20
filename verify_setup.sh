#!/bin/bash
# 分层测试架构验证脚本
# 验证所有新增组件是否正常工作

set -e

echo "================================"
echo "分层测试架构验证脚本"
echo "================================"
echo ""

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# 检查 Python 版本
if command -v python3 &> /dev/null; then
    PYTHON="python3"
elif command -v python &> /dev/null; then
    PYTHON="python"
else
    echo "❌ 未找到 Python 环境"
    exit 1
fi

echo "使用 Python: $PYTHON"
echo ""

# 1. 检查文件结构
echo "✓ 检查文件结构..."
files_to_check=(
    "utils/robot_locators.py"
    "utils/robot_steps.py"
    "utils/robot_functional.py"
    "tests/test_api_example.py"
    "tests/test_playwright_advanced.py"
    "tests/robotframework/test_layered_architecture.robot"
    "tests/robotframework/test_api.robot"
    "docs/LAYERED_TESTING_GUIDE.md"
    "docs/LAYERED_TESTING_CHEATSHEET.md"
)

for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ 找到: $file"
    else
        echo "  ❌ 缺失: $file"
        exit 1
    fi
done

echo ""

# 2. 检查 Python 语法
echo "✓ 检查 Python 文件语法..."
python_files=(
    "utils/robot_locators.py"
    "utils/robot_steps.py"
    "utils/robot_functional.py"
    "tests/test_api_example.py"
    "tests/test_playwright_advanced.py"
    "conftest.py"
)

for file in "${python_files[@]}"; do
    if $PYTHON -m py_compile "$file" 2>/dev/null; then
        echo "  ✅ 语法正常: $file"
    else
        echo "  ❌ 语法错误: $file"
        exit 1
    fi
done

echo ""

# 3. 检查 Robot 文件语法
echo "✓ 检查 Robot Framework 文件语法..."
robot_files=(
    "tests/robotframework/test_layered_architecture.robot"
    "tests/robotframework/test_api.robot"
)

for file in "${robot_files[@]}"; do
    if $PYTHON -m robot --dryrun "$file" >/dev/null 2>&1; then
        echo "  ✅ 语法正常: $file"
    else
        echo "  ⚠️  需要在 Robot 环境中运行完整检查: $file"
    fi
done

echo ""

# 4. 检查导入依赖
echo "✓ 检查 Python 导入..."

# 检查 requests 是否安装
if $PYTHON -c "import requests" 2>/dev/null; then
    echo "  ✅ requests 库已安装"
else
    echo "  ⚠️  requests 库未安装（可选），请运行: pip install requests"
fi

# 检查 robotframework 是否安装
if $PYTHON -c "import robot" 2>/dev/null; then
    echo "  ✅ Robot Framework 已安装"
else
    echo "  ⚠️  Robot Framework 未安装（可选），请运行: pip install robotframework"
fi

# 检查 selenium 是否安装
if $PYTHON -c "import selenium" 2>/dev/null; then
    echo "  ✅ Selenium 已安装"
else
    echo "  ⚠️  Selenium 未安装（可选），请运行: pip install selenium"
fi

# 检查 playwright 是否安装
if $PYTHON -c "import playwright" 2>/dev/null; then
    echo "  ✅ Playwright 已安装"
else
    echo "  ⚠️  Playwright 未安装（可选），请运行: pip install playwright && playwright install"
fi

echo ""

# 5. 检查配置文件
echo "✓ 检查配置文件..."
config_files=(
    "pytest.ini"
    "robotframework.ini"
    "config/settings.py"
)

for file in "${config_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ 配置存在: $file"
    else
        echo "  ❌ 配置缺失: $file"
    fi
done

echo ""

# 6. 检查报告目录
echo "✓ 检查报告目录..."
mkdir -p reports/selenium_screenshots
mkdir -p reports/robotframework
echo "  ✅ 报告目录已创建/存在"

echo ""

# 7. 显示项目统计
echo "✓ 项目统计..."
python_test_count=$(find tests -name "*.py" -type f | wc -l)
robot_test_count=$(find tests -name "*.robot" -type f | wc -l)

echo "  📊 Python 测试文件: $python_test_count"
echo "  🤖 Robot 测试文件: $robot_test_count"

echo ""
echo "================================"
echo "✅ 验证完成！"
echo "================================"
echo ""
echo "📌 快速开始命令:"
echo "   1. 运行所有测试:"
echo "      python run_test.py"
echo ""
echo "   2. 运行 API 测试:"
echo "      pytest tests/test_api_example.py -v"
echo ""
echo "   3. 运行分层架构演示:"
echo "      python -m robot tests/robotframework/test_layered_architecture.robot"
echo ""
echo "   4. 运行 Playwright 高级场景:"
echo "      pytest tests/test_playwright_advanced.py -v"
echo ""
echo "📖 查看文档:"
echo "   - 快速开始: cat QUICKSTART.md"
echo "   - 分层架构指南: cat docs/LAYERED_TESTING_GUIDE.md"
echo "   - 快速参考: cat docs/LAYERED_TESTING_CHEATSHEET.md"
echo ""
