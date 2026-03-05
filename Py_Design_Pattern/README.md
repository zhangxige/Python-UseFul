<p> love <strong>bold text</strong> </p>

love __bold text__.

<p> <em>cat</em> meow</p>

The _cat's meow_.

>  Dorothy followed her through many rooms.
>  And this is the second paragraph.
>> Andthisisthenestedparagraph.

>##### The quarterly results look great!
>
> - Revenuewasoffthechart.
> - Profitswerehigherthanever.
> 
> *Everything* is going **well**.

1. First item
2. Seconditem
3. Third item
4. Fourthitem

+ First item
- Seconditem
* Third item
- Fourthitem


1. Open the file.
2. Find the following code block online 21:

        <html>
            <head>
                <title>Test</title>
            </head>
        </html>
 
3. Update the title to match the name of your website

 <ol>
    <li><p>Open the file.</p></li>
    <li><p>Find the following code block online 21::</p>
    <pre><code>
    &lt;html&gt;
        &lt;head&gt;
            &lt;title&gt;Test&lt;/title&gt;
        &lt;/head&gt;
    &lt;/html&gt;
    </code></pre>
    </li>
    <li><p>Update the title to match the name of your website.</p></li>
 </ol>


<blockquote>
    <p>Dorothy followed her through many rooms.</p>
</blockquote>

<blockquote>
    <h5>Thequarterlyresultslookgreat!</h5>
        <ul>
            <li>Revenuewasoffthechart.</li>
            <li>Profitswerehigherthanever.</li>
        </ul>
    <p>
        <em>Everything</em>
        isgoing<strong>well<strong>.
    </p>
</blockquote>

### 执行doctest
```script
# 执行文档测试
python -m doctest -v Catolog.py

# 同样的测试
python -m doctest -v Chain_of responsbility_Pattern.py
```

# Python 中线程安全的设计模式解析

# Python 线程安全的单例模式与观察者模式

## 前言

本文将详细介绍 Python 中两种常用的设计模式：**线程安全的单例模式** 和 **线程安全的观察者模式**，包含核心原理、实现代码及使用示例，所有代码均考虑多线程场景下的安全性，适合 Python 开发者学习和实际项目使用。

## 一、线程安全的单例模式

### 1. 单例模式核心概念

单例模式的核心目标是**确保一个类在程序运行期间只有一个实例**，并提供全局访问点。普通单例模式在单线程下可用，但多线程并发创建实例时，可能因竞争条件创建多个实例，因此需要实现线程安全的版本。

### 2. 实现方案：基于锁 + 双重检查（推荐）

Python 中通过 `threading.Lock` 加锁，结合**双重检查（Double-Checked Locking）** 机制，既保证线程安全，又避免每次获取实例都加锁的性能损耗。

```Python

import threading

class ThreadSafeSingleton:
    # 类变量存储唯一实例
    _instance = None
    # 锁对象，保证多线程下实例创建的原子性
    _lock = threading.Lock()

    def __new__(cls):
        # 第一层检查：如果实例已存在，直接返回（避免每次加锁，提升性能）
        if cls._instance is None:
            # 加锁：保证同一时间只有一个线程进入创建逻辑
            with cls._lock:
                # 第二层检查：防止多个线程等待锁后重复创建实例
                if cls._instance is None:
                    # 创建唯一实例
                    cls._instance = super().__new__(cls)
        return cls._instance

    # 示例方法：验证实例唯一性
    def show_id(self):
        print(f"实例ID: {id(self)}")

# 多线程测试函数
def test_singleton():
    singleton = ThreadSafeSingleton()
    singleton.show_id()

# 测试代码
if __name__ == "__main__":
    # 创建5个线程并发获取实例
    threads = []
    for _ in range(5):
        t = threading.Thread(target=test_singleton)
        threads.append(t)
        t.start()
    
    # 等待所有线程执行完毕
    for t in threads:
        t.join()
```

### 3. 代码解释

- `_instance`：类级别的变量，用于存储唯一的实例对象，初始值为 `None`。

- `_lock`：`threading.Lock` 实例，用于锁定实例创建的关键代码块，避免多线程竞争。

- `__new__` 方法：Python 中创建实例的核心方法，重写该方法实现单例逻辑：

    - 第一层检查：快速返回已创建的实例，避免不必要的锁竞争；

    - `with cls._lock`：加锁保证原子性，同一时间只有一个线程进入；

    - 第二层检查：防止多个线程等待锁后，重复创建实例。

- 测试结果：所有线程输出的实例 ID 完全相同，证明线程安全。

### 4. 其他实现方式（补充）

- **装饰器方式**：通过装饰器封装单例逻辑，代码复用性更高；

- **模块级单例**：Python 模块天然是单例（导入时仅加载一次），简单场景可直接使用模块代替类单例。

## 二、线程安全的观察者模式

### 1. 观察者模式核心概念

观察者模式（发布-订阅模式）定义了**一对多的依赖关系**：当一个对象（主题/发布者）的状态发生变化时，所有依赖它的对象（观察者/订阅者）都会收到通知并自动更新。

多线程场景下，需保证：

- 订阅/取消订阅操作的线程安全；

- 通知观察者时，避免阻塞主线程（可选）；

- 观察者列表的修改不会引发迭代异常。

### 2. 实现方案：基于锁 + 异步通知

```Python

import threading
import time

# 观察者抽象类（定义观察者的核心方法）
class Observer:
    def update(self, message):
        """接收主题通知并处理，子类需实现该方法"""
        raise NotImplementedError("子类必须实现 update 方法")

# 主题（发布者）类：维护观察者列表，提供订阅/取消订阅/通知方法
class ThreadSafeSubject:
    def __init__(self):
        # 存储观察者的列表
        self._observers = []
        # 锁：保证对观察者列表操作的线程安全
        self._lock = threading.Lock()

    def attach(self, observer):
        """订阅：添加观察者（线程安全）"""
        with self._lock:
            if observer not in self._observers:
                self._observers.append(observer)
                print(f"观察者 {observer.__class__.__name__} 已订阅")

    def detach(self, observer):
        """取消订阅：移除观察者（线程安全）"""
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)
                print(f"观察者 {observer.__class__.__name__} 已取消订阅")

    def notify(self, message):
        """通知所有观察者（线程安全，异步执行）"""
        # 加锁复制观察者列表：避免迭代时列表被修改（如取消订阅）引发异常
        with self._lock:
            # 复制一份列表，迭代副本而非原列表
            observers_copy = self._observers.copy()
        
        # 异步通知：每个观察者的 update 方法在独立线程中执行，避免阻塞
        for observer in observers_copy:
            threading.Thread(target=observer.update, args=(message,)).start()

# 具体观察者1：邮件通知
class EmailObserver(Observer):
    def update(self, message):
        print(f"[邮件通知] 收到消息：{message}，线程ID：{threading.current_thread().ident}")
        # 模拟处理耗时
        time.sleep(0.1)

# 具体观察者2：短信通知
class SmsObserver(Observer):
    def update(self, message):
        print(f"[短信通知] 收到消息：{message}，线程ID：{threading.current_thread().ident}")
        # 模拟处理耗时
        time.sleep(0.1)

# 测试代码
if __name__ == "__main__":
    # 创建主题实例
    subject = ThreadSafeSubject()

    # 创建观察者实例
    email_observer = EmailObserver()
    sms_observer = SmsObserver()

    # 订阅（主线程）
    subject.attach(email_observer)
    subject.attach(sms_observer)

    # 多线程发布消息
    def publish_message(msg):
        print(f"\n发布者发布消息：{msg}，主线程ID：{threading.current_thread().ident}")
        subject.notify(msg)

    # 创建3个线程并发发布消息
    threads = []
    for i in range(3):
        t = threading.Thread(target=publish_message, args=(f"新消息{i+1}",))
        threads.append(t)
        t.start()

    # 等待所有线程执行完毕
    for t in threads:
        t.join()

    # 取消订阅
    subject.detach(email_observer)
    # 再次发布消息，仅短信观察者收到
    publish_message("最终消息")
```

### 3. 代码解释

#### （1）核心组件

- `Observer` 抽象类：定义观察者的统一接口 `update`，所有具体观察者必须实现该方法，保证接口一致性。

- `ThreadSafeSubject` 主题类：

    - `_observers`：存储所有订阅的观察者；

    - `_lock`：保证 `attach`/`detach`/`notify` 方法中对 `_observers` 操作的线程安全；

    - `attach`/`detach`：加锁实现订阅/取消订阅，避免多线程同时修改列表；

    - `notify`：

        - 先加锁复制观察者列表，避免迭代原列表时因修改（如取消订阅）引发 `RuntimeError`；

        - 异步通知：每个观察者的 `update` 方法在独立线程中执行，避免单个观察者处理耗时阻塞整个通知流程。

#### （2）具体观察者

- `EmailObserver`/`SmsObserver`：实现 `update` 方法，处理具体的通知逻辑（如模拟邮件/短信发送）。

#### （3）测试结果

- 多线程发布消息时，所有观察者都能正确收到通知，且线程 ID 不同（证明异步执行）；

- 取消订阅后，对应的观察者不再收到通知，保证操作有效性。

### 4. 关键线程安全点

- **列表操作加锁**：`attach`/`detach`/`notify` 中对 `_observers` 的修改/读取都加锁，避免竞争条件；

- **迭代副本**：通知时迭代观察者列表的副本，而非原列表，防止迭代过程中列表被修改；

- **异步通知**：避免单个观察者处理耗时过长，导致主题线程阻塞。

## 三、总结

### 1. 线程安全单例模式

- 核心：通过 `threading.Lock` + 双重检查，保证多线程下类只有一个实例；

- 关键：双重检查既保证线程安全，又减少锁竞争带来的性能损耗；

- 适用场景：配置管理、数据库连接池、日志器等需要全局唯一实例的场景。

### 2. 线程安全观察者模式

- 核心：通过锁保证观察者列表的修改安全，通过复制列表 + 异步通知避免迭代异常和阻塞；

- 关键：订阅/取消订阅操作加锁，通知时迭代列表副本，异步执行观察者逻辑；

- 适用场景：事件通知、消息推送、状态监控等需要一对多通知的场景（如系统告警、UI 状态更新）。

### 3. 通用原则

Python 中实现线程安全设计模式的核心是：**对共享资源（如单例实例、观察者列表）的操作加锁，避免多线程竞争条件**，同时兼顾性能和代码可读性。
> （注：文档部分内容由 AI 帮助生成）