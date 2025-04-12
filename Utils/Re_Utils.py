import re
'''
    findAll(): 匹配所有的字符串，把匹配结果作为一个列表返回
    match(): 匹配字符串的开始位置，如果开始位置没有，则返回None
    search():在字符串中搜索，返回搜索到的第一个
    finditer():匹配所有的字符串，返回迭代器
'''


def test1():
    res = 'h.'
    s = 'hello python'
    result = re.findall(res, s)
    print(result)  # \['he', 'ho'\]


def test2():
    res2 = r'[hon]'
    s = 'hello python'
    result = re.findall(res2, s)
    print(result)  # \['h', 'o', 'h', 'o', 'n'\]


def test3():
    res2 = r'[\d]'
    s = 'hell666o pyt999hon'
    result = re.findall(res2, s)
    print(result)  # \['6', '6', '6', '9', '9', '9'\]


def test4():
    res2 = r'[\D]'
    s = 'hello 3334 python 88'
    result = re.findall(res2, s)
    print(result)
    # \['h', 'e', 'l', 'l', 'o', ' ','
    #  ', 'p', 'y', 't', 'h', 'o', 'n', ' '\]


def test5():
    res2 = r'[\s]'
    s = 'hello 3334 python 88'
    result = re.findall(res2, s)
    print(result)  # \[' ', ' ', ' '\]


def test6():
    res2 = r'[\S]'
    s = 'hello 3334 python 88'
    result = re.findall(res2, s)
    print(result)
    # \['h', 'e', 'l', 'l', 'o', '3', '3', '3', '4',
    #  'p', 'y', 't', 'h', 'o', 'n', '8', '8'\]


def test7():
    # \w 匹配非特殊字符，即a-z、A-Z、0-9、_、汉字
    res2 = r'[\w]'
    s = 'hello#&\_ aa 8python中国'
    result = re.findall(res2, s)
    print(result)
    # \['h', 'e', 'l', 'l', 'o', '\_', 'a', 'a',
    #  '8', 'p', 'y', 't', 'h', 'o', 'n', '中', '国'\]


def test8():
    # W 匹配特殊字符 （ - ~@#$&*）空格也属于特殊字符
    res2 = r'[\W]'
    s = r'-hello#&\_ aa 8python中国'
    result = re.findall(res2, s)
    print(result)  # \['-', '#', '&', ' ', ' '\]


def test9():
    # *：匹配前一个字符出现一次，或无限次 贪婪模式
    res2 = r'h*'
    s = '-hhello hhh python'
    result = re.findall(res2, s)
    print(result)  
    # \['', 'hh', '', '', '', '', '', 'hhh',
    #  '', '', '', '', 'h', '', '', ''\]


def test10():
    # + :匹配前一个字符出现1次或无穷次
    res2 = r'h+'
    s = '-hhello hhh python'
    result = re.findall(res2, s)
    print(result)  # \['hh', 'hhh', 'h'\]


def test11():
    res2 = 'h?'
    s = '-hhello hhh python'
    result = re.findall(res2, s)
    print(result)
    # \['', 'h', 'h', '', '', '', '', '', 'h',
    #  'h', 'h', '', '', '', '', 'h', '', '', ''\]


def test12():
    # 匹配到前一个字符s 连续出现2次
    res2 = 'https{2}'
    s = '-hhello-httpssss-python'
    result = re.findall(res2, s)
    print(result)  # \['httpss'\]


def test13():
    # {n,m} :匹配前一个字符出现n-m次
    res2 = 'https{1,3}'
    s = '-hhello-httpssss-python'
    result = re.findall(res2, s)
    print(result)  # \['httpss'\]


def test14():
    # | :两个条件进行匹配，或的关系
    res2 = 'he|ll'
    s = 'hello python'
    result = re.findall(res2, s)
    print(result)  # \['he', 'll'\]


def test15():
    # ^ :匹配以哪个字符开头的
    res2 = '^he'
    s = 'hello python'
    result = re.findall(res2, s)
    print(result)  # \['he'\]


def test16():
    # $ : 匹配以哪个字符结尾的字符
    res2 = 'on$'
    s = 'hello python'
    result = re.findall(res2, s)
    print(result)  # \['on'\]


def test17():
    # （） ：只匹配（）里面的
    res2 = r'#(\w.+?)#'
    s = r"{'mobile\_phone':'#mobile\_phone#','pwd':'Aa123456'}"
    result = re.findall(res2, s)
    print(result)  # \['mobile\_phone'\]


def test18():
    str = "www.runoob.com"
    print(re.match('www', str).span())  # 在起始位置匹配 ，返回匹配到的区间下标  (0,3)
    print(re.match('com', str))  # 不在起始位置匹配  None


def test19():
    str = "www.runoob.com"
    print(re.search('www', str).span())  # 在起始位置匹配 ，返回匹配到的区间下标
    print(re.search('com', str).span())  # 不在起始位置匹配


def test20():
    res = 'h.'
    s = 'hello python'
    result = re.finditer(res, s)
    for str in result:
        print(str.group())


if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()
    test9()
    test10()
    test11()
    test12()
    test13()
    test14()
    test15()
    test16()
    test17()
    test18()
    test19()
    test20()
