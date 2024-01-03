from operator import itemgetter
from functools import cmp_to_key
from pprint import pprint
from decimal import Decimal


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


def test_searchfun():
    import re
    str = "Hello, world!"
    pattern = r'world'
    result = re.findall(pattern, str)
    print(result)
    pass


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


if __name__ == "__main__":
    # res = test_decimal()
    test_using_next()
    pass
