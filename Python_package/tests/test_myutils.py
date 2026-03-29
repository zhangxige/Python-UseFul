import myutils

# 测试版本
print('Version', myutils.__version__)

# 测试字符串工具
print(myutils.reverse_string('hello'))
print(myutils.to_upper('python'))

# 测试数学工具
print(myutils.add(1, 2))
print(myutils.multiply(3, 4))
print(myutils.is_odd(5))

# 测试文件工具
myutils.write_file('./test.txt', 'hello world')
print(myutils.read_file('./test.txt'))