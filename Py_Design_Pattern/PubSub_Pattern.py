import threading
import queue
import time
from typing import Callable, Dict, List


class ThreadSafePubSub:
    def __init__(self):
        # 主题注册表：key=主题名，value=订阅者列表（每个订阅者是一个消费函数）
        self.topics: Dict[str, List[Callable]] = {}
        # 每个主题对应一个线程安全的消息队列
        self.topic_queues: Dict[str, queue.Queue] = {}
        # 保护主题注册表的互斥锁（避免多线程同时修改订阅关系）
        self.registry_lock = threading.Lock()
        # 存储订阅者消费线程（用于优雅退出）
        self.consumer_threads: List[threading.Thread] = []
        # 控制消费线程退出的标志（原子操作）
        self.is_running = True

    def subscribe(self, topic: str, callback: Callable):
        """订阅主题：线程安全的订阅操作"""
        with self.registry_lock:  # 加锁保护注册表修改
            # 主题不存在则初始化
            if topic not in self.topics:
                self.topics[topic] = []
                self.topic_queues[topic] = queue.Queue()
                # 为新主题启动独立的消费线程
                consumer = threading.Thread(
                    target=self._consume_messages,
                    args=(topic,),
                    daemon=True  # 守护线程，主进程退出时自动结束
                )
                self.consumer_threads.append(consumer)
                consumer.start()
            # 添加订阅者（去重）
            if callback not in self.topics[topic]:
                self.topics[topic].append(callback)
                print(f"订阅者 {callback.__name__} 已订阅主题: {topic}")

    def unsubscribe(self, topic: str, callback: Callable):
        """取消订阅：线程安全"""
        with self.registry_lock:
            if topic in self.topics and callback in self.topics[topic]:
                self.topics[topic].remove(callback)
                print(f"订阅者 {callback.__name__} 已取消订阅主题: {topic}")
                # 若主题无订阅者，清空队列（可选）
                if not self.topics[topic]:
                    del self.topics[topic]
                    del self.topic_queues[topic]

    def publish(self, topic: str, message):
        """发布消息：线程安全，非阻塞"""
        with self.registry_lock:  # 加锁检查主题是否存在
            if topic not in self.topic_queues:
                print(f"警告：主题 {topic} 无订阅者，消息被丢弃")
                return
        # 放入队列（queue.Queue 本身线程安全，无需额外加锁）
        self.topic_queues[topic].put(message)
        print(f"发布者发布消息到 {topic}: {message}")

    def _consume_messages(self, topic: str):
        """内部消费逻辑：独立线程运行，分发消息给订阅者"""
        while self.is_running:
            try:
                # 非阻塞获取消息（超时1秒，避免死等）
                message = self.topic_queues[topic].get(timeout=1)
                # 加锁读取订阅者列表（防止遍历过程中订阅关系被修改）
                with self.registry_lock:
                    subscribers = self.topics.get(topic, [])[:]  # 复制列表，避免遍历中修改
                # 分发消息给所有订阅者
                for callback in subscribers:
                    try:
                        callback(topic, message)  # 执行订阅者的消费逻辑
                    except Exception as e:
                        print(f"订阅者 {callback.__name__} 处理消息失败: {e}")
                # 标记消息处理完成（配合 queue.join()）
                self.topic_queues[topic].task_done()
            except queue.Empty:
                # 队列为空时继续循环，等待新消息
                continue

    def stop(self):
        """停止所有消费线程，优雅退出"""
        self.is_running = False
        # 等待所有消费线程结束
        for thread in self.consumer_threads:
            thread.join(timeout=2)
        print("所有消费线程已停止")


# ---------------------- 测试示例 ----------------------
def subscriber1(topic: str, message):
    """订阅者1：处理消息"""
    print(f"[订阅者1] 收到 {topic} 消息: {message} (线程: {threading.current_thread().name})")
    time.sleep(0.5)  # 模拟处理耗时


def subscriber2(topic: str, message):
    """订阅者2：处理消息"""
    print(f"[订阅者2] 收到 {topic} 消息: {message} (线程: {threading.current_thread().name})")
    time.sleep(0.3)  # 模拟处理耗时


if __name__ == "__main__":
    # 初始化线程安全的 Pub/Sub 实例
    pubsub = ThreadSafePubSub()

    # 订阅主题
    pubsub.subscribe("news", subscriber1)
    pubsub.subscribe("news", subscriber2)
    pubsub.subscribe("weather", subscriber1)

    # 启动多个发布者线程
    def publisher_task(topic: str, messages: list):
        """发布者任务：批量发布消息"""
        for msg in messages:
            pubsub.publish(topic, msg)
            time.sleep(0.2)  # 模拟发布间隔

    # 发布者1：发布新闻消息
    publisher1 = threading.Thread(
        target=publisher_task,
        args=("news", ["Python 3.12 发布", "线程安全最佳实践", "Pub/Sub 模式详解"])
    )
    # 发布者2：发布天气消息
    publisher2 = threading.Thread(
        target=publisher_task,
        args=("weather", ["北京晴 25℃", "上海雨 20℃"])
    )

    # 启动发布者线程
    publisher1.start()
    publisher2.start()

    # 等待发布者完成
    publisher1.join()
    publisher2.join()

    # 等待所有消息处理完成
    for q in pubsub.topic_queues.values():
        q.join()

    # 取消订阅
    pubsub.unsubscribe("news", subscriber2)

    # 发布最后一条消息（仅订阅者1接收）
    pubsub.publish("news", "最后一条新闻：测试取消订阅")

    # 停止 Pub/Sub
    pubsub.stop()