# -*- coding: utf-8 -*-
"""
    ThreadEx.py
    A thread management utility for Windows, providing advanced control over
    threads.
    https://blog.csdn.net/sunxiaocongming/article/details/149659717
"""
import inspect
import threading
import ctypes
import time
from ctypes import wintypes
import os


# Windows API 定义
THREAD_SUSPEND_RESUME = 0x0002
THREAD_QUERY_INFORMATION = 0x0040
WAIT_TIMEOUT = 0x00000102
WAIT_OBJECT_0 = 0x00000000
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)


# 定义 Windows API 函数原型
OpenThread = kernel32.OpenThread
OpenThread.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
OpenThread.restype = wintypes.HANDLE


# 定义其他 Windows API 函数原型
SuspendThread = kernel32.SuspendThread
SuspendThread.argtypes = [wintypes.HANDLE]
SuspendThread.restype = wintypes.DWORD


# 定义 ResumeThread 函数原型
ResumeThread = kernel32.ResumeThread
ResumeThread.argtypes = [wintypes.HANDLE]
ResumeThread.restype = wintypes.DWORD


WaitForSingleObject = kernel32.WaitForSingleObject
WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
WaitForSingleObject.restype = wintypes.DWORD


CloseHandle = kernel32.CloseHandle


# 定义 PyThreadState_SetAsyncExc 函数原型
class ThreadEx(threading.Thread):
    def __init__(self,
                 target=None,
                 args=(),
                 start=True,
                 kwargs=None,
                 group=None,
                 name=None,
                 daemon=True):
        """
             self.tid: 系统级别的id 这个 类创建的 对象
                 python thread类对象，通常也称为 线程id 他是 thread操作的句柄对象。 这里我在执行thread对象时候执行获取了线程在系统里面的id
                 然后通过系统api 根据 系统里面的线程id来控制线程的 暂停 停止 继续，结束 。这里对于默认的Thread 线程类的继承 完全继承了6个初始化对象
                 的参数： group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None
            通过 self.status  记录线程的状态。
            这个类适合 创建 操作 单个线程， 如果需要多个线程同时操作，可以使用 ThreadManage 类来实现更高级的功能。
        """
        if os.name != 'nt':
            raise NotImplementedError("当前仅支持 Windows 平台")
 
        self.status = ''
        self.target_function = target
        self.tid = None
        #  守护线程。  daemon=True
        super().__init__(target=self.__target_function, args=args, kwargs=kwargs, group=group, name=name, daemon=daemon)
        # 启动线程 默认True
        if start:
            self.status = 'running'
            try:
                self.start()
            except Exception as e:
                self.status = 'stopped'
                print(f'线程start 操作出现错误：{e}')
        # 如果不想直接启动线程，也可以仅创建一个线程对象，返回 被继承后的 Thread 对象， 拥有全部Thread原本方法和属性 和新增的方法。

    def suspend(self):
        """ 调用系统api 暂停线程"""
        try:
            h_thread = OpenThread(THREAD_SUSPEND_RESUME, False, self.tid)
            if h_thread:
                SuspendThread(h_thread)
                CloseHandle(h_thread)
            self.status = "suspended"
        except Exception as e:
            print(f'线程暂停操作出现错误：{e}')
            pass

    def resume(self):
        """ 调用系统api 恢复线程"""
        try:
            h_thread = OpenThread(THREAD_SUSPEND_RESUME, False, self.tid)
            if h_thread:
                ResumeThread(h_thread)
                CloseHandle(h_thread)
            self.status = "running"
        except Exception as e:
            print(f'线程恢复操作出现错误：{e}')
            pass

    def stop(self, try_times=1, message=''):
        """ 强制停止线程 返回布尔值 和 错误信息"""
        result = self.__class__.stop_thread(self.tid, try_times=try_times, message=message )
        if result:
            self.status = 'stopped'
        return result

    @classmethod
    def stop_thread(cls, target_thread_id,  try_times=2,  message=''):
        result = False
        for i in range(try_times):
            try:
                result = cls._async_raise(target_thread_id, SystemExit)
                if result:
                    if message:
                        print(f'线程 {message} 停止成功')
                    break
            except Exception as e:
                result = False
                print(f'线程 {message} 停止失败: {e}')
                time.sleep(3)
        return result

    def __target_function(self, *args, **kwargs):
        """
            里用__target_function 调用 target_function 在调用之前这样不需要修改 原版的 thread库，可以再调用之前。
            # 准确获取到系统级的 线程id
            这里完全复刻了 子类的 参数传递。
        """
        try:
            self.tid = ctypes.windll.kernel32.GetCurrentThreadId()
            self.target_function(*args, **kwargs)
        finally:
            self.status = 'stopped'

    @classmethod
    def _async_raise(cls, tid, exc_type):
        """ 尝试根据线程 id 强制停止 线程 返回布尔值 是否成功"""
        try:
            """raises the exception, performs cleanup if needed"""
            tid = ctypes.c_long(tid)
            if not inspect.isclass(exc_type):
                exc_type = type(exc_type)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exc_type))
            if res == 0:
                raise ValueError("invalid thread id")
            elif res != 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")
            return True
        except Exception as e:
            print(f"线程强制停止失败: {e}")
            pass
        return False

    def get_status(self):
        """
            使用 Windows API 判断线程是否仍在运行（未终止）。
            注意：挂起的线程也会被认为是“仍在运行”。
            实际应用中 有待测试
        """
        if not self.tid:
            self.status = ''
            return self.status  # 线程尚未启动
        h_thread = OpenThread(THREAD_QUERY_INFORMATION, False, self.tid)
        if h_thread and h_thread != 0:
            result = WaitForSingleObject(h_thread, 0)
            CloseHandle(h_thread)
            if result == WAIT_TIMEOUT and self.status != "suspended":
                self.status = 'running'
            elif result == WAIT_OBJECT_0:
                self.status = 'stopped'
        else:
            self.status = 'stopped'
        return self.status


# ThreadEx 类的使用示例
class ThreadManage:
    """
        调用 包含更多功能的 ThreadEx 类。 创建对象 线程， 并记录线程a
        这个类适合在需要管理多个线程时候使用, 可以停止全部线程，暂停全部线程，恢复全部线程运行，
    """
    _lock = threading.Lock()
    thread_list = []  # 全局线程列表

    def __init__(self):
        pass

    @classmethod
    def create_thread(cls, target, start=True, args=(), kwargs=None, group=None,  name=None, daemon=True):
        cls.cleanup()
        with cls._lock:
            thread_id = ThreadEx(target=target, start=start, args=args,
                                kwargs=kwargs, group=group, name=name, daemon=daemon)
            ThreadManage.thread_list.append(thread_id)  # 添加到全局列表
            return thread_id

    @classmethod
    def suspend_all(cls):
        """ 暂停全部线程 进入休眠状态"""
        cls.cleanup()
        for t in cls.thread_list:
            t.suspend()

    @classmethod
    def resume_all(cls):
        """ 恢复全部线程 从休眠状态中"""
        cls.cleanup()
        for t in cls.thread_list:
            t.resume()

    @classmethod
    def stop_all(cls):
        cls.cleanup()
        """ 强制停止 全部线程"""
        for index in range(len(cls.thread_list)-1, -1, -1):
            if cls.thread_list[index].stop():
                cls.thread_list.pop(index)

    @classmethod
    def stop(cls, t):
        cls.cleanup()
        index_ = -1
        for index in range(len(cls.thread_list)):
            if cls.thread_list[index] == t:
                index_ = index
                break
        if t.stop():
            cls.thread_list.pop(index_)

    @classmethod
    def cleanup(cls):
        with cls._lock:
            cls.thread_list = [t for t in cls.thread_list 
                               if t.status != 'stopped']

    @classmethod
    def update_thread_status(cls):
        """ 动态更新线程状态，更准确的更新线程状态 """
        for t in cls.thread_list:
            t.get_status()
        cls.cleanup()


def test_worker(startwith):
    count = 0
    for ii in range(5):
        print(f"{startwith} 运行: {count}")
        count += 1
        time.sleep(1)
        if ii == 10:
            exit()
            # raise Exception('adqweqrqh')
    time.sleep(1)
    print("运行结束")


if __name__ == '__main__':
    t = ThreadManage.create_thread(target=test_worker, args=('子线程 1',))
    t2 = ThreadManage.create_thread(target=test_worker, args=('子线程 2', ))
    # print(f't.tid={t.tid}')
    time.sleep(3)
    print("暂停线程 1")
    ThreadManage.suspend_all()  # 暂停

    ThreadManage.stop(t)
    time.sleep(3)
    print("恢复线程")
    # t.resume()   # 恢复

    time.sleep(3)
    t.stop()
    count = 0
    while True:
        print(f"主线程： Running: {count}")
        print('t.status=', t.status)
        # print('t.get_status()=', t2.get_status())
        count += 1
        time.sleep(1)
