# Singleton Design Pattern
# 单例模式

import threading
import time


# 单例基类
class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class Bus(Singleton):
    lock = threading.RLock()

    def sendData(self, data):
        self.lock.acquire()
        time.sleep(3)
        print("Sending Signal Data...", data)
        self.lock.release()


class VisitEntity(threading.Thread):
    my_bus = ""
    name = ""

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def run(self):
        self.my_bus = Bus()
        self.my_bus.sendData(self.name)


# 使用元类
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # 创建一个新的实例，并将其存入_instances字典中
            cls._instances[cls] = \
                super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# 使用元类实现单例模式的类
class SingletonClass(metaclass=SingletonMeta):
    def __init__(self):
        print("Instance created")


# 多线程安全的单例
class SafeSingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()  # 锁对象用于同步

    def __call__(cls, *args, **kwargs):
        with cls._lock:  # 确保线程安全
            if cls not in cls._instances:
                cls._instances[cls] = \
                    super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SafeSingletonClass(metaclass=SafeSingletonMeta):
    def __init__(self):
        print("Instance created")


if __name__ == "__main__":
    for i in range(3):
        print("Entity %d begin to run..." % i)
        my_entity = VisitEntity()
        my_entity.setName("Entity_"+str(i))
        my_entity.start()
    a = SingletonClass()
    b = SingletonClass()
    print(a is b)
