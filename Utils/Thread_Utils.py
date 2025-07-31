# coding: utf-8
import time
import threading


# Thread-safe dictionary implementation
class ThreadSafeDict:
    def __init__(self, *args, **kwargs):
        self._dict = dict(*args, **kwargs)
        self._lock = threading.Lock()

    def __len__(self):
        with self._lock:
            return len(self._dict)

    def __getitem__(self, key):
        with self._lock:
            return self._dict[key]

    def __setitem__(self, key, value):
        with self._lock:
            self._dict[key] = value

    def __delitem__(self, key):
        with self._lock:
            del self._dict[key]

    def __contains__(self, key):
        with self._lock:
            return key in self._dict

    def get(self, key, default=None):
        with self._lock:
            return self._dict.get(key, default)

    def setdefault(self, key, default=None):
        with self._lock:
            return self._dict.setdefault(key, default)


# Thread-safe list implementation
class ThreadSafeList:
    def __init__(self, *args):
        self._list = list(*args)
        self._lock = threading.Lock()

    def append(self, item):
        with self._lock:
            self._list.append(item)

    def extend(self, iterable):
        with self._lock:
            self._list.extend(iterable)

    def __getitem__(self, index):
        with self._lock:
            return self._list[index]

    def __len__(self):
        with self._lock:
            return len(self._list)

    def __iter__(self):
        with self._lock:
            return iter(self._list)

    def __delitem__(self, index):
        with self._lock:
            del self._list[index]

    def __contains__(self, item):
        with self._lock:
            return item in self._list
        
    def clear(self):
        with self._lock:
            self._list.clear()

    def index(self, item):
        with self._lock:
            return self._list.index(item)
        
    def pop(self, index=-1):
        with self._lock:
            return self._list.pop(index)
    
    def remove(self, item):
        with self._lock:
            self._list.remove(item)

    def sort(self, key=None, reverse=False):
        with self._lock:
            self._list.sort(key=key, reverse=reverse)

    def reverse(self):
        with self._lock:
            self._list.reverse()


class PausableThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._pause_event = threading.Event()
        self._pause_event.set()  # 开始时设置为非暂停状态
        self._running = threading.Event()
        self._running.set()  # 开始时设置为运行状态
        self._restart = threading.Event()

    def run(self):
        while self._running.is_set():
            self._pause_event.wait()  # 等待直到被暂停或重启事件触发
            if self._restart.is_set():
                self._restart.clear()  # 清除重启事件标志
                continue  # 重新开始循环
            while not self._pause_event.is_set():
                # 这里放置你的任务代码
                print("线程正在运行...")
                time.sleep(1)  # 模拟任务执行时间
            if not self._running.is_set():
                break  # 如果线程应该停止，则退出循环

    def pause(self):
        self._pause_event.clear()  # 设置暂停事件为False，暂停线程

    def resume(self):
        self._pause_event.set()  # 设置暂停事件为True，继续线程

    def stop(self):
        self._running.clear()  # 设置运行事件为False，停止线程
        self._pause_event.set()  # 确保线程在停止前可以被正确暂停（如果有必要）
        self.join()  # 等待线程真正停止

    def restart(self):
        self._restart.set()  # 设置重启事件为True，在下一个循环中重新开始
        self._pause_event.set()  # 确保线程可以被重新启动
        self._running.set()  # 确保线程处于运行状态


# 使用示例
if __name__ == "__main__":
    thread = PausableThread()
    thread.start()
    time.sleep(5)  # 等待线程运行一段时间
    print("暂停线程")
    thread.pause()  # 暂停线程
    time.sleep(3)  # 等待一段时间后继续
    print("继续线程")
    thread.resume()  # 继续线程
    time.sleep(5)  # 等待线程运行一段时间后停止
    print("停止并重启线程")
    thread.stop()  # 停止线程
    thread = PausableThread()  # 创建新的线程实例（如果要重新启动）
    thread.start()  # 重新启动线程（实际上是新的实例）
    time.sleep(5)  # 等待线程运行一段时间后停止并退出程序
    print("停止线程")
    thread.stop()  # 停止线程（对新实例）
