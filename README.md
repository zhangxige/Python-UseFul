# Python-UseFul
创建这个项目的目的是为了更好更快的让人使用Python3的一些用法，将Python3语言中的特点更方便应用于Python构建的项目中。  
- 针对Python3语言中常用方法总结，方便快速部署  
- 常用库的使用和举例  
- 功能更容易迁移到其他项目中 

### 依赖库安装命令
```shell
pip install -r requirements.txt
```

### 举例:
- 装饰器
```python
import time

# 计时函数装饰器
def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds to "
              "execute.")
        return result
    return wrapper

# 测试计时
@timer
def test_record_runtime():
    s = 0
    for i in range(100000):
        s += 1


if __name__ == '__main__':
    test_record_runtime()
```