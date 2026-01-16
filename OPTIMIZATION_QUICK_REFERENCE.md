# 框架优化快速参考指南

## 新增工具类

### 1. 重试装饰器
```python
from utils.retry_decorator import retry_on_failure

@retry_on_failure(max_attempts=3, delay=1.0)
def unstable_operation():
    page.click("button")
```

### 2. 测试数据管理器
```python
from utils.test_data_manager import TestDataManager

manager = TestDataManager()
user = manager.get_test_user("standard")
checkout = manager.get_checkout_data()
```

## UIOperations 新功能

```python
# 调试模式
ui = UIOperations(debug_mode=True)

# 智能等待
ui.smart_wait("css=.button", condition="visible")

# 重试点击
ui.click_with_retry("css=.submit")

# 自动截图
ui.auto_screenshot("test_name")

# 等待网络空闲
ui.wait_for_network_idle()
```

## 使用 Fixtures

```python
def test_login(self, standard_user, checkout_data):
    # standard_user 和 checkout_data 由 fixture 提供
    self.saucedemo.login(
        standard_user['username'], 
        standard_user['password']
    )
```

## 测试标记

```python
@pytest.mark.smoke      # 冒烟测试
@pytest.mark.critical   # 关键测试
@pytest.mark.regression # 回归测试
@pytest.mark.slow       # 慢速测试
@pytest.mark.performance # 性能测试
def test_example():
    pass
```

## 运行测试

```bash
# 按标记运行
pytest -m smoke -v
pytest -m critical -v

# 并行运行
pytest -n auto -v

# 失败重试
pytest --reruns 2 -v

# 生成报告
pytest --html=reports/report.html -v
```

## 查看日志

```bash
# 实时日志
pytest -v --log-cli-level=INFO

# 日志文件
cat logs/pytest.log
```
