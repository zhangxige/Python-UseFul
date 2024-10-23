from operator import itemgetter
from functools import cmp_to_key
from pprint import pprint
from decimal import Decimal
from textwrap import dedent


# 常用排序方法
def test_sortkey():
    def compare(x, y):
        if x[1] < y[1]:
            return -1
        elif x[1] > y[1]:
            return 1
        else:
            if x[0] < y[0]:
                return -1
            else:
                return 1

    '''
    实际当中经常会遇到多个关键词按序排列的情况
    比如 成绩排序的时候 按照 语、数、外，排序
    '''
    data = [{'name': 'a', 'chinese': 89, 'math': 43, 'english': 21},
            {'name': 'b', 'chinese': 60, 'math': 78, 'english': 34},
            {'name': 'c', 'chinese': 99, 'math': 43, 'english': 21},
            {'name': 'd', 'chinese': 60, 'math': 43, 'english': 21}
            ]
    input_key = ('english', 'math', 'name')
    sorted_data = sorted(data, key=itemgetter(*input_key), reverse=True)
    pprint(sorted_data)

    '''
        常用的lamda函数方法
    '''
    data = [('Tom', 23), ('Jerry', 21), ('Alice', 23), ('Bob', 22)]
    sorted_data = sorted(data, key=lambda x: (x[1], x[0]), reverse=True)
    pprint(sorted_data)

    data = [('abc', 23, 1), ('ef', 22, 4), ('ds', 23, 3), ('re', 22, 4)]
    sorted_data = sorted(data, key=lambda x: (x[2], x[1], x[0]), reverse=True)
    pprint(sorted_data)

    '''
        cmp_to_key 方法
    '''
    data = [('Tom', 23),
            ('Jerry', 24),
            ('Alice', 23),
            ('Bob', 22),
            ('None', 18)]
    sorted_data = sorted(data, key=cmp_to_key(compare))
    pprint(sorted_data)

    '''
        lamda 方法
    '''
    data = [('Tom', 23, 2),
            ('Jerry', 24, 4),
            ('Alice', 23, 5),
            ('Bob', 22, 12),
            ('None', 18, 23)]
    sort_col = [1, 2]
    data.sort(key=lambda x: [x[i] for i in sort_col])
    pprint(sorted_data)

    '''
        lamda 方法
    '''
    data = [('Tom', 23, 2),
            ('Jerry', 24, 4),
            ('Alice', 23, 5),
            ('Bob', 22, 12),
            ('None', 18, 23)]
    data.sort(key=lambda x: (x[1], -x[2]))
    pprint(sorted_data)


def test_decimal():

    a = Decimal('2.3')
    b = Decimal('4.5')
    result = a * b
    print(result)


def test_using_next():
    a = range(1, 100)
    expr = (i for i in a if i % 2 == 0)
    print(next(expr))
    print(next(expr))


def Better_Ways_Dataclass():
    from collections import namedtuple
    Player = namedtuple('Player',
                        ['name', 'number', 'position', 'age', 'grade'])
    jordan = Player('Micheal Jordan', 23, 'PG', 29, 'S+')
    print(jordan)

    from dataclasses import dataclass, field
    from typing import Any, List

    @dataclass(order=True)
    class Player:
        name: str
        number: int
        position: str
        age: int
        grade: str
        info: Any = 'abc'

    james = Player('Lebron James', 23, 'SF', 25, 'S')
    paul = Player('pauls', 23, 'SF', 25, 'S')
    james.position = 'changge'
    james.number = '12345'
    print(paul == james)
    print(paul < james)

    class Team:
        name: str
        players: List[Player] = field(default_factory=lambda: [james])
    myteam = Team()
    print(myteam)
    print(james)


def test_printtext():
    a = dedent("""
        -- list 1
        -- list 2
        -- list 3
        """)
    print(a)


def test_functiontools_lru_cache():
    from functools import lru_cache

    @lru_cache(maxsize=30)  # maxsize参数告诉lru_cache缓存最近多少个返回值
    def fib(n):
        if n < 2:
            return n
        return fib(n-1) + fib(n-2)
    print([fib(n) for n in range(100)])
    fib.cache_clear()


def test_map_filter():
    def map_fun(x):
        return x

    def filter_fun(x):
        return x % 2 == 0

    def fibnancc_fun(x):
        i = 0
        a, b = 1, 1
        while i < x:
            yield a
            a = a + b
            a, b = b, a
            i += 1

    genrate = fibnancc_fun(10)
    f = list(map(map_fun, genrate))
    print(f)
    f = list(filter(filter_fun, f))
    print(f)


def test_dataclass():
    from dataclasses import dataclass
    from dataclasses import field

    @dataclass
    class Player:
        name: str
        number: int
        position: set
        age: int
        grade: float

    james = Player('james', 1, 'abc', 10, 20)

    @dataclass
    class Team:
        name: str
        players: list[Player] = field(default_factory=lambda: [james])

    nyk = Team('New York Knicks')
    print(nyk)


def test_namedtuple():
    from collections import namedtuple

    # 定义一个具名元组类
    Person = namedtuple("Person", ["name", "age", "gender"])

    # 创建一个 Person 类的实例
    person = Person("Alice", 28, "female")

    # 访问某个属性
    print(person.name)     # 输出：Alice
    print(person.age)      # 输出：28
    print(person.gender)   # 输出：female

    # 通过索引访问属性
    print(person[0])       # 输出：Alice
    print(person[1])       # 输出：28
    print(person[2])       # 输出：female

    # 获取某个属性的值
    print(getattr(person, "name"))    # 输出：Alice

    # 将具名元组对象转换成字典对象
    person_dict = person._asdict()
    print(person_dict)
    # 输出：{'name': 'Alice', 'age': 28, 'gender': 'female'}

    # 通过字典创建具名元组类的实例
    person_dict = {"name": "Bob", "age": 30, "gender": "male"}
    person2 = Person(**person_dict)
    print(person2)
    # 输出：Person(name='Bob', age=30, gender='male')


def test_deque():
    from collections import deque

    # 创建一个空的 deque 队列
    d = deque()
    print(d)  # deque([])

    # 可以通过传入一个可迭代对象，创建一个 deque 队列
    d1 = deque([1, 2, 3, 4, 5])
    print(d1)    # deque([1, 2, 3, 4, 5])

    # 在双端队列的左边添加元素
    d.appendleft(0)
    print(d)     # deque([0])

    # 在双端队列的右边添加元素
    d.append(6)
    print(d)     # deque([0, 6])

    # 扩展双端队列
    d.extend([7, 8, 9])
    print(d)     # deque([0, 6, 7, 8, 9])

    # 扩展双端队列，从左边添加元素
    d.extendleft([-1, -2, -3])
    print(d)     # deque([-3, -2, -1, 0, 6, 7, 8, 9])

    # 删除最左边的元素
    d.popleft()  # -3
    print(d)   # deque([-2, -1, 0, 6, 7, 8, 9])

    # 删除最右边的元素
    d.pop()    # 9
    print(d)   # deque([-2, -1, 0, 6, 7, 8])

    # 查找元素并返回所在位置的索引
    print(d.index(-1))   # 1

    # 返回元素出现的次数
    print(d.count(3))    # 0

    # 反转 deque 队列
    d.reverse()
    print(d)    # deque([8, 7, 6, 0, -1, -2])


def test_chainmap():
    from collections import ChainMap

    # 创建多个字典
    dict1 = {"a": "apple", "b": "banana"}
    dict2 = {"c": "cat", "d": "dog"}
    dict3 = {"e": "elephant", "f": "fox"}

    # 使用 ChainMap 将多个字典合并
    ch_map = ChainMap(dict1, dict2, dict3)

    # 查找某个键对应的值
    print(ch_map.get("a"))
    print(ch_map.get("c"))
    print(ch_map.get("e"))

    # 修改某个键对应的值
    dict1["a"] = "ant"
    print(ch_map.get("a"))

    # 新增某个键值对
    dict2["g"] = "goose"
    print(ch_map)

    # 组合链
    dict4 = {"a": "apple_new", "d": "dog_new"}
    ch_map2 = ch_map.new_child(dict4)
    print(ch_map2)
    print(ch_map2.get('a'))


def test_counter():
    from collections import Counter

    # 使用 Counter 对当前列表中的元素进行计数
    lst = ["apple", "banana", "apple", "apple", "orange", "banana", "pear"]
    cnt = Counter(lst)
    print(cnt)   # Counter({'apple': 3, 'banana': 2, 'orange': 1, 'pear': 1})

    # 查看某个元素在给定的列表中出现的次数
    print(cnt["apple"])   # 3
    print(cnt["orange"])  # 1
    print(cnt["pear"])    # 1
    print(cnt["grape"])   # 0

    # 给 Counter 添加元素
    cnt["grape"] = 2
    print(cnt)
    # Counter({'apple': 3, 'banana': 2, 'grape': 2, 'orange': 1, 'pear': 1})

    # 获取计数结果中的最高频元素，并返回出现的次数
    print(cnt.most_common(1))  # [('apple', 3)]
    print(cnt.most_common(2))  # [('apple', 3), ('banana', 2)]

    # 已知计数结果字典，获取对应的键
    print(list(cnt.elements()))


def test_defaultdict():
    from collections import defaultdict

    # 创建一个 defaultdict 对象
    dd = defaultdict(int)

    # 往 defaultdict 中添加元素
    dd["a"] = 1
    dd["b"] = 2
    dd["c"] = 3

    print(dd)  # defaultdict(<class 'int'>, {'a': 1, 'b': 2, 'c': 3})
    print(dd["d"])  # 0

    # 利用 lambda 函数作为工厂函数来创建 defaultdict
    dd2 = defaultdict(lambda: "None")

    dd2["a"] = "apple"
    dd2["b"] = "banana"

    print(dd2)
    print(dd2["c"])  # None

    dd3 = defaultdict(lambda: [])
    dd3["a"] = ["apple"]
    dd3["b"] = ["banana"]
    dd3['c']
    print(dd3)  # None

    dd4 = defaultdict(list)
    a = ['a', 'b', 'c', 'd', 'a']
    for it in a:
        dd4[it].append(it)
    print(dd4)  # None


def test_heapq():
    import heapq
    test1 = [51, 1, 4, 5, 6, 61, 8]
    heapq.heapify(test1)
    print(test1)
    heapq.heappop(test1)
    print(test1)
    heapq.heappush(test1, 3)
    print(test1)

    test2 = [(11, 'a'),
             (4, 'b'),
             (5, 'c'),
             (6, 'd'),
             (61, 'e'),
             (8, 'f')]
    heapq.heapify(test2)
    print(test2)
    heapq.heappop(test2)
    print(test2)
    res = heapq.nsmallest(3, test2)
    print(res)


def test_graph():
    import heapq

    graph = {
        '0': {'1': 4, '2': 8},
        '1': {'0': 4, '2': 3, '3': 8},
        '2': {'0': 8, '1': 3, '4': 1, '5': 6},
        '3': {'1': 8, '4': 2, '6': 7, '7': 4},
        '4': {'2': 1, '3': 2, '5': 6},
        '5': {'2': 6, '4': 6, '7': 2},
        '6': {'3': 7, '7': 14, '8': 9},
        '7': {'3': 4, '5': 2, '6': 14, '8': 10},
        '8': {'6': 9, '7': 10}
    }

    def dijkstra(graph, start):
        distances = {vertex: float('infinity') for vertex in graph}
        distances[start] = 0

        # 初始化父亲节点
        parent = {vertex: None for vertex in graph}
        priority_queue = [(0, start)]

        while priority_queue:
            # 弹出堆中距离最小的节点
            current_distance, current_vertex = heapq.heappop(priority_queue)
            # print("距离最小的节点是:",current_distance,
            #  current_vertex, "更新后的队列:",priority_queue)

            # 如果当前距离已经大于已知的最短距离，则跳过
            if current_distance > distances[current_vertex]:
                continue

            # 更新相邻节点的距离
            for neighbor, weight in graph[current_vertex].items():
                distance = current_distance + weight
                # print("相邻节点的距离:",neighbor,distance)

                # 如果找到更短的路径，则更新距离，并将节点加入优先队列
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    parent[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (distance, neighbor))
                    # print("加入后的队列:",priority_queue)
        return distances, parent

    distances, parent = dijkstra(graph, '0')
    # print(parent)
    # print(distances)

    # 输出路径回溯
    def get_path(parent, start, end):
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        return path

    end_node = '8'
    path = get_path(parent, '0', end_node)
    print(f"从节点 '0' 到节点 {end_node} 的路径:", path)


def test_erfensearch():
    def search(nums: list, target: int) -> int:
        left, right = 0, len(nums) - 1
        while left + 1 < right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid
            else:
                right = mid
        if nums[right] == target:
            return right
        else:
            return -1

    in_list = list(map(int, input().strip().split(',')))
    target_num = int(input())
    res = search(in_list, target_num)
    print(res)


def test_re_findstr():
    import re
    s_str = 'dfjsi AAb89432d fs'
    pattern = '[A-Z]+[a-z][0-9]'
    p1 = re.compile(pattern)
    res = re.findall(p1, s_str)
    print(res)

    s_str = 'af-cd-13-fc-z3'
    pattern = '[a-f0-9][a-z0-9]'
    p1 = re.compile(pattern)
    res = re.findall(p1, s_str)
    print(res)

    s_str = 'school 30 student 39 name 123'
    pattern = r'(\d+)'
    res = re.split(pattern, s_str)
    print(res)

    s_str = 'school 30 student 39 name 123'
    pattern = r'\d+'
    res = re.split(pattern, s_str)
    print(res)

    s_str = "Hello, world!"
    pattern = r'world'
    result = re.findall(pattern, s_str)
    print(result)
    # example
    s_str = "Hello, world! 89934 , niha2o,3 world!"
    pattern = r'\d'
    result = re.sub(pattern, 'x', s_str)
    print(result)


if __name__ == "__main__":
    # res = test_decimal()
    test_sortkey()
    pass
