# Python-UseFul
创建这个项目的目的是为了更好更快的让人使用Python3的一些用法，将Python3语言中的特点更方便应用于Python构建的项目中。  
- 针对Python3语言中常用方法总结，方便快速部署  
- 常用库的使用和举例  
- 功能更容易迁移到其他项目中 
- 每种方法给出简易用例，方便应用在其他项目中并易于扩展

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

- 文件操作(举例)
```python
import os
import shutil
from tqdm import tqdm
from enum import Enum


class File_Type(Enum):
    ...


class File_OP():
    ...


# 测试一
def test_findfile():
    ...


# 测试二
def test_copyfiles():
    ...


if __name__ == '__main__':
    test_findfile()
    test_copyfiles()
```

### 记在最后:
- 项目代码管理：以 git 方式管理，同步代码更方便
- 关于markdown：.md 是一个很方便的结构说明文档，项目说明中需要采用