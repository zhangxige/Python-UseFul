import time
import random
import queue
from blinker import Namespace
from threading import Thread


# 定义队列资源此 与 触发信号
q = queue.Queue()
my_namespace = Namespace()
my_signal = my_namespace.signal('my-event')


# 注册一个回调函数
def my_callback(sender, **extra):
    print(f'Event received from {sender}, with extra data: {extra}')
    work_time = random.randint(0, 7)
    time.sleep(work_time)
    print(f'after {work_time} seconds, work done!')


my_signal.connect(my_callback)


# 工作类
class Worker(Thread):
    def __init__(self, name):
        super().__init__()  # 调用Thread类的__init__方法
        self.name = name

    def run(self):
        while True:
            event = q.get()
            if event is None:  # Sentinel to stop the worker thread.
                break
            name, datas = event
            my_signal.send(name, **datas)
            q.task_done()


# 管理类
class Manager():
    def __init__(self):
        self._groups = list()

    def add_worker(self, workname: str, deamonmark: bool = True):
        w = Worker(name=workname)
        w.daemon = deamonmark
        self._groups.append(w)
        w.start()

    def send_event(self, sender, **extra):
        q.put((sender, extra))  # Send event to the worker thread.
        # q.task_done()  # Ensure the queue is cleared after processing.
        # q.join()  # Wait for the event to be processed.


if __name__ == '__main__':
    testm = Manager()
    testm.add_worker('Tom')
    testm.add_worker('Lisa')
    testm.send_event('job1', filter_out=True, tt='1', mm='aaa')
    testm.send_event('job2', ss='3', mm='bbb')
    time.sleep(20)
