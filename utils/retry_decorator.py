# -*- coding: utf-8 -*-
"""
重试装饰器
提供通用的重试机制，用于处理偶发性失败
"""

import time
import logging
from functools import wraps
from typing import Callable, Type, Tuple, Optional

logger = logging.getLogger(__name__)


def retry_on_failure(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable] = None
):
    """
    重试装饰器 - 在操作失败时自动重试
    
    Args:
        max_attempts: 最大尝试次数（包括首次尝试）
        delay: 初始重试延迟（秒）
        backoff: 延迟倍增因子（每次重试后延迟时间乘以此因子）
        exceptions: 需要重试的异常类型元组
        on_retry: 重试时的回调函数，接收 (attempt, exception) 参数
    
    Returns:
        装饰后的函数
    
    Example:
        @retry_on_failure(max_attempts=3, delay=1, exceptions=(TimeoutError,))
        def unstable_operation():
            # 可能失败的操作
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts:
                        logger.error(
                            f"函数 {func.__name__} 在 {max_attempts} 次尝试后仍然失败: {str(e)}"
                        )
                        raise
                    
                    logger.warning(
                        f"函数 {func.__name__} 第 {attempt} 次尝试失败: {str(e)}. "
                        f"将在 {current_delay:.1f} 秒后重试..."
                    )
                    
                    # 调用重试回调
                    if on_retry:
                        try:
                            on_retry(attempt, e)
                        except Exception as callback_error:
                            logger.error(f"重试回调执行失败: {callback_error}")
                    
                    # 等待后重试
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            # 理论上不会到达这里，但为了类型安全
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator


def retry_with_screenshot(screenshot_func: Callable, max_attempts: int = 3):
    """
    带截图的重试装饰器 - 专门用于 UI 测试
    
    Args:
        screenshot_func: 截图函数，接收 attempt 参数
        max_attempts: 最大尝试次数
    
    Example:
        @retry_with_screenshot(lambda attempt: page.screenshot(f"retry_{attempt}.png"))
        def click_element(locator):
            page.click(locator)
    """
    def on_retry_callback(attempt: int, exception: Exception):
        try:
            screenshot_func(attempt)
            logger.info(f"已保存第 {attempt} 次重试的截图")
        except Exception as e:
            logger.error(f"截图保存失败: {e}")
    
    return retry_on_failure(
        max_attempts=max_attempts,
        delay=1.0,
        backoff=1.5,
        on_retry=on_retry_callback
    )
