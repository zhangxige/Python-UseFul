# 基于 flask 的任务提交系统
import time
import random
import queue
import threading
from collections import defaultdict

from flask import Blueprint
from flask import request, jsonify


# 线程安全的默认字典
class ThreadSafeDefaultDict:
    def __init__(self, default_factory=None):
        self._dict = defaultdict(default_factory)
        self._lock = threading.Lock()

    def get(self, key, default=None):
        with self._lock:
            return self._dict.get(key, default)

    def set(self, key, value):
        with self._lock:
            self._dict[key] = value

    def delete(self, key):
        with self._lock:
            if key in self._dict:
                del self._dict[key]

    def items(self):
        with self._lock:
            return list(self._dict.items())

    def __len__(self):
        with self._lock:
            return len(self._dict)

    def __getitem__(self, key):
        with self._lock:
            return self._dict[key]
    
    def __setitem__(self, key, value):
        with self._lock:
            self._dict[key] = value


class Task:
    """任务类，代表一个具体的任务"""
    def __init__(self, name, duration, safe_dict: ThreadSafeDefaultDict):
        self.name = name  # 任务名称
        self.duration = duration  # 任务执行时长（秒）
        self.safe_dict = safe_dict  # 线程安全的默认字典

    def run(self):
        """模拟任务的执行过程"""
        self.safe_dict[self.name] = self.duration  # 将任务信息存入线程安全字典
        print(f"任务 {self.name} 开始，预计 {self.duration} 秒")
        time.sleep(self.duration)  # 模拟任务的执行
        print(f"任务 {self.name} 完成")
        self.safe_dict.delete(self.name)


class Worker(threading.Thread):
    """工作线程类，负责执行任务"""
    def __init__(self, worker_id, task_queue):
        super().__init__()
        self.worker_id = worker_id  # 工作线程ID
        self.task_queue = task_queue  # 任务队列

    def run(self):
        """从任务队列中获取任务并执行"""
        while True:
            if self.task_queue.empty():
                # print(f"工作线程 {self.worker_id} 暂时无任务休息5S!")
                time.sleep(5)
            else:
                task = self.task_queue.get()  # 获取任务
                if task is not None:  # 如果是空任务，说明要停止该线程
                    print(f"工作线程 {self.worker_id} 正在执行任务 {task.name}")
                    task.run()
                    self.task_queue.task_done()  # 标记任务完成


class TaskScheduler:
    """任务调度器类，负责管理任务分配和执行"""
    def __init__(self, num_workers):
        self.num_workers = num_workers  # 工作线程数量
        self.task_queue = queue.Queue()  # 任务队列
        self.workers = list()  # 保存工作线程
        self.tasks = ThreadSafeDefaultDict()  # 保存任务

    def add_task(self, name, duration):
        """添加任务到任务队列"""
        task = Task(name, duration, self.tasks)
        self.task_queue.put(task)

    def start(self):
        """启动所有工作线程并分配任务"""
        for i in range(self.num_workers):
            worker = Worker(i + 1, self.task_queue)
            worker.daemon = True
            worker.start()
            self.workers.append(worker)

    def view_queue_content(self):
        content = list()
        names = list()
        """查看任务队列中的内容"""
        while True:
            try:
                item = self.task_queue.get_nowait()  # 非阻塞方式获取元素
                content.append(item)
                names.append((item.name, item.duration))
                self.task_queue.task_done()  # 标记任务已完成，以便正确地计数等待的任务数
            except queue.Empty:
                break  # 队列为空时退出循环
        for item in content:
            self.task_queue.put(item)
        return names

    def wait_for_completion(self):
        """等待所有任务完成"""
        self.task_queue.join()  # 阻塞，直到所有任务完成
        for worker in self.workers:
            self.task_queue.put(None)  # 向每个工作线程发送停止信号
        for worker in self.workers:
            worker.join()  # 等待工作线程退出

    def display_task_status(self):
        """显示当前任务队列中的任务状态"""
        print(f"当前共有 {len(self.tasks)} 个任务：")
        for key, value in self.tasks.items():
            print(f"- 任务: {key}, 执行时长: {value} 秒")


class worker_blueprint:
    work = Blueprint("work", __name__, url_prefix="/work")
    scheduler = TaskScheduler(num_workers=3)  # 创建任务调度器，3个工作线程
    scheduler.start()

    def __init__(self, app):
        self.app = app

    # 提交任务
    @work.route("/add", methods=["POST"])
    def add_job():
        data = request.json  # 这是一个字典类型，可以直接访问键值对
        task_name = data.get('name', 'new_name')  # 获取'name'，如果没有则使用默认值'World'
        task_duration = random.randint(100, 200)  # 随机任务执行时长
        worker_blueprint.scheduler.add_task(task_name, task_duration)
        return jsonify({'message': f'Received name: {task_name}'})

    # 提交任务
    @work.route("/query", methods=["GET"])
    def query_job():
        task_nums = worker_blueprint.scheduler.task_queue.qsize()
        task_list = worker_blueprint.scheduler.view_queue_content()
        working_tasks = worker_blueprint.scheduler.tasks.items()
        print(f"当前任务队列中的任务数量: {task_nums}, 任务列表: {task_list}")
        return jsonify({'message': f'{task_nums} of jobs are waiting!',
                        'task_list': task_list,
                        'working_task': working_tasks})
