# -*- coding: utf-8 -*-
"""
Robot Framework Listener 示例

职责（骨架版）：
- 在这里可以处理：用例依赖（depends on）、动态修改用例名（追加 env/platform 后缀）、
  将结果同步到外部测试平台等。

当前实现只做简单的日志输出与名称后缀示例，便于后续扩展。
"""

# Robot Framework Listener API 版本（必须在模块级别定义，在导入之前）
ROBOT_LISTENER_API_VERSION = 3


class WebTestListener:
    """Robot Framework Listener 类，用于处理测试执行过程中的事件"""

    def __init__(self):
        """初始化 Listener"""
        self.suite_name_suffix = ""

    def start_suite(self, name, attributes):
        """Suite 开始时触发，可以在这里读取变量 ENV/PLATFORM 等拼接后缀。"""
        variables = attributes.get("metadata", {}) or {}
        # 这里只是示例，真正环境可以通过 BuiltIn().get_variable_value 获取
        env = variables.get("ENV")
        platform = variables.get("PLATFORM")

        suffix_parts = []
        if env:
            suffix_parts.append(str(env))
        if platform:
            suffix_parts.append(str(platform))

        if suffix_parts:
            self.suite_name_suffix = " [" + "/".join(suffix_parts) + "]"

    def start_test(self, name, attributes):
        """用例开始时触发，可在这里解析自定义标签，如 depends_on。"""
        tags = [t.lower() for t in attributes.get("tags", [])]
        depends = [t for t in tags if t.startswith("depends_on=")]
        if depends:
            # 示例：depends_on=xxx，可在这里实现依赖检查逻辑
            pass

    def end_test(self, name, attributes):
        """用例结束时触发，可在这里采集状态并上报外部平台。"""
        status = attributes.get("status")
        message = attributes.get("message", "")
        # 在此处对接外部测试平台，例如通过 HTTP API 上报结果
        # 这里保留为注释，方便后续实现：
        # send_result_to_platform(name, status, message, attributes)
        pass

    def end_suite(self, name, attributes):
        """Suite 结束时触发。"""
        pass

    def close(self):
        """所有执行结束时触发。"""
        # 做一些清理或最终汇总
        pass
