import inspect
import os
import re
import sys
from functools import wraps
from time import strftime
from time import perf_counter
# from base.singletonModel import Singleton
from loguru import logger


g_log_path = r"../logs"
g_log_ini = r"../config/log_config.ini"


# 单例模式
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class MyLogs(Singleton):
    LOG_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           g_log_path)  # 存放日志
    INI_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           g_log_ini)  # ini配置文件
    # ini_data = IniFile(INI_DIR).get_itemsAll()  # 获取ini配置中的数据
    ini_data = {'level': 5,
                'rotation': '500MB'
                }
    logger_h = logger.opt(colors=True)

    def __new__(cls, *args, **kwargs):
        # hasattr是Python的一个内置函数，用于检查对象是否具有指定的属性或方法。
        if not hasattr(cls, '_logger'):
            cls._setup_logger()
        return super().__new__(cls)

    @classmethod
    def _setup_logger(cls):
        logger.remove()
        # 设置日志文件路径和格式
        filename = strftime("%Y%m%d-%H%M%S")
        log_file_path = os.path.join(cls.LOG_DIR, f'{filename}.log')
        log_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | " \
                     "<level>{level}</level> " \
                     "| <level>{message}</level>"
        level_: str = MyLogs.ini_data["level"]
        rotation_: str = MyLogs.ini_data["rotation"]

        # 添加日志处理器：写入文件

        cls.logger_h.add(log_file_path,
                         enqueue=True,
                         backtrace=True,
                         diagnose=True,
                         encoding="utf8",
                         rotation=rotation_
                         )

        # 添加日志处理器：控制台输出
        cls.logger_h.add(
            sys.stderr,
            format=log_format,
            enqueue=True,
            colorize=True,
            backtrace=True,
            diagnose=True,
            level=level_,
            # filter=cls._debug_filter  # 使用自定义过滤器函数

        )

    # @staticmethod
    # def _debug_filter(record):
    #     """自定义过滤器函数，仅输出 DEBUG 级别的日志"""
    #     if record["level"].name == MyLogs.ini_data["filter_level"]:
    #         return True
    #     return False

    @classmethod
    def log(cls, level: str, msg: str):
        """
        ···

        :param level: 日志等级：info,debug,trace,error,warning,critical,exception
        :param msg: 要输出的内容
        :return: msg

        # 栗子
        MyLogs.log("info", "-----------分割线-----------")

        """
        getattr(cls.logger_h, level)(msg)

    @classmethod
    def log_decorator(cls, msg: str):
        """
         日志装饰器，记录函数的名称、参数、返回值、运行时间和异常信息

         栗子：
            @log.log_decorator("这里填写def功能")
                def test_zero_division_error(a, b):
                    return a / b
         """

        def decorator(func):
            func_line = inspect.currentframe().f_back.f_lineno

            @wraps(func)
            def wrapper(*args, **kwargs):
                # 处理报错：args中<>被识别为颜色标签而报错
                # 使用正则表达式替换<任意内容>为\<任意内容>
                args_str = re.sub(r"<([^<>]+)>", r"\<\1\>", str(args))
                # 使用正则表达式替换<任意内容>为\<任意内容>
                kwargs_str = re.sub(r"<([^<>]+)>", r"\<\1\>", str(kwargs))

                cls.log("info", "\n")
                cls.log("info", "<green>-----------分割线-----------</>")
                cls.log("info", f"<white>{msg}  ↓↓↓</>")
                cls.log("debug",
                        f'<red>{func.__qualname__}:' +
                        f'{func.__name__}:{func_line} |</>  <white> args:' +
                        f'{args_str}, kwargs:{kwargs_str}</>')
                start = perf_counter()
                try:
                    result = func(*args, **kwargs)
                    result_str = re.sub(r"<([^<>]+)>", r"\<\1\>", str(result))

                    end = perf_counter()
                    duration = end - start
                    cls.log("debug",
                            f'<red>{func.__qualname__}:{func.__name__}:' +
                            f'{func_line} |</>  <white> 返回结果：' +
                            f'{result_str}, 耗时：{duration:4f}s</>')
                    return result

                except Exception as e:
                    cls.log("exception",
                            f'<red>{func.__qualname__}:{func.__name__}:' +
                            f'{func_line} |</>: {msg}:报错 :{e}')
                    sys.exit(1)

                finally:
                    cls.logger_h.complete()
                    cls.log("info", "<green>-----------分割线-----------</>")

            return wrapper

        return decorator

    @classmethod
    def log_clear(cls):
        for it in os.listdir(cls.LOG_DIR):
            os.remove(os.path.join(cls.LOG_DIR, it))


if __name__ == '__main__':
    MyLogs.log("debug", "Executing step 3 of the algorithm")
    MyLogs.log("info", "Server started on port")
    MyLogs.log("warning", "Invalid input provided, using default values")
    MyLogs.log("error", "Invalid user input detected, unable to proceed")
    MyLogs.log("critical", "Database connection lost, terminating the app")
    MyLogs.log("exception", "exception connection lost, terminating the app")

    @MyLogs.log_decorator("1111111111111111111")
    def A(a, b):
        a / b

    A(1, 1)

    MyLogs.log_clear()
