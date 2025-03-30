# 基于 flask 的任务提交系统
import time
import random
import queue
import threading

from flask import Blueprint
from flask import request, jsonify


class Task:
    """任务类，代表一个具体的任务"""
    def __init__(self, name, duration):
        self.name = name  # 任务名称
        self.duration = duration  # 任务执行时长（秒）

    def run(self):
        """模拟任务的执行过程"""
        print(f"任务 {self.name} 开始，预计 {self.duration} 秒")
        time.sleep(self.duration)  # 模拟任务的执行
        print(f"任务 {self.name} 完成")


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
        self.workers = []  # 保存工作线程
        self.tasks = []  # 保存任务

    def add_task(self, name, duration):
        """添加任务到任务队列"""
        task = Task(name, duration)
        self.tasks.append(task)
        self.task_queue.put(task)

    def start(self):
        """启动所有工作线程并分配任务"""
        for i in range(self.num_workers):
            worker = Worker(i + 1, self.task_queue)
            worker.daemon = True
            worker.start()
            self.workers.append(worker)

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
        for task in self.tasks:
            print(f"- 任务: {task.name}, 执行时长: {task.duration} 秒")


class worker_blueprint:
    work = Blueprint("work", __name__, url_prefix="/work")
    scheduler = TaskScheduler(num_workers=3)  # 创建任务调度器，3个工作线程
    scheduler.start()

    def __init__(self, app):
        self.app = app
        pass

    # 提交任务
    @work.route("/add", methods=["POST"])
    def get_json():
        data = request.json  # 这是一个字典类型，可以直接访问键值对
        task_name = data.get('name', 'new_name')  # 获取'name'，如果没有则使用默认值'World'
        task_duration = random.randint(5, 20)  # 随机任务执行时长
        worker_blueprint.scheduler.add_task(task_name, task_duration)
        return jsonify({'message': f'Received name: {task_name}'})