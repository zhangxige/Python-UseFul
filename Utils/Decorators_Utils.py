import os
import time
from datetime import datetime
import warnings
from loguru import logger


# -------------------------------- 函数装饰器 ------------------------ #
# 计时函数装饰器
def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds to "
              "execute.")
        return result
    return wrapper


# 处理废弃函数
def deprecated(func):
    def wrapper(*args, **kwargs):
        out_wrap = r'is deprecated and will be removed in future.'
        warnings.warn(f"{func.__name__} {out_wrap}", DeprecationWarning)
        return func(*args, **kwargs)
    return wrapper


# 错误处理
def suppress_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            return None
    return wrapper


# 多次重试执行
def retry(max_attempts, delay):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    info = f"Attempt {attempts + 1} failed. Retrying in {delay} seconds."
                    print(info)
                    print(f"{func.__name__} : {e}")
                attempts += 1
                time.sleep(delay)
            raise Exception(func.__name__ + " : Max retry attempts exceeded.")
        return wrapper
    return decorator


# debug 显示函数输入
def debug(func):
    def wrapper(*args, **kwargs):
        print(f"Debugging {func.__name__} - args: {args}, kwargs: {kwargs}")
        return func(*args, **kwargs)
    return wrapper
# -------------------------------- 函数装饰器 ------------------------ #


# 日志管理模块
# 使用时，只需要在主函数中定义一个实例即可
class Log_Rec():
    def __init__(self, file_mode=True) -> None:
        dt01 = datetime.today()
        self._file_mode = file_mode
        log_path = r'./log'
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        if self._file_mode:
            self._file_log = logger.add(
                f'log/runtime_{dt01.year}-{dt01.month}-{dt01.day}.log',
                rotation='00:00',
                retention='10 days'
                )
        else:
            self._file_log = None

    def __del__(self):
        if self._file_mode:
            logger.remove(self._file_log)
        else:
            pass


# 日志追踪
@logger.catch
def test_fun(a=0, b=1):
    a = Log_Rec()
    print(a.__doc__)
    c = 3 / 3
    logger.info("Test begin:")
    print(c)


# 测试计时
@timer
def test_record_runtime():
    s = 0
    for i in range(100000):
        s += 1


if __name__ == '__main__':
    test_record_runtime()
