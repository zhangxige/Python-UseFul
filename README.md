<p align = "center"> 
<img src="./Image/python.jpg" ”height = “200 width="400" >
</p>

**Python-UseFul** 希望可以帮助到更多的人，无论是初学者还是项目老手

![Generic badge](https://img.shields.io/badge/Python-v3-blue.svg) ![Generic badge](https://img.shields.io/badge/pip-v3-red.svg)



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
<details>
<summary>装饰器</summary>

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
</details>

<details>
<summary>文件操作(举例)</summary>

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
</details>

<details>
<summary>多字段排序</summary>

```python
some code ...
```
</details>

<details>
<summary>map/reduce/filter</summary>

```python
some code ...
```
</details>

<details>
<summary>内置数据格式</summary>

```python
some code ...
```
</details>

<details>
<summary>collections模块</summary>
一定要像熟悉内置关键词一样熟悉的模块

```python
some code ...
```
</details>

<details>
<summary>functools模块</summary>
一定要像熟悉内置关键词一样熟悉的模块

```python
some code ...
```
</details>

### 更多模块(非常优秀的模块)

<details open>
<summary>
Gradio模块
</summary>

[Gradio](https://www.gradio.app/ "Gradio 方便部署你的Web UI快速展示后端功能")：
Python中还拥有着非常多的、方便使用的模块，项目收集的一些模块放在Utils中，可以参考快速实现一些功能原型。最近发现了一个Web UI相关的模块，

</details>

<details open>
<summary>
Boken模块
</summary>

[Boken](https://docs.bokeh.org/en/latest/docs/user_guide.html#userguide "交互式可视化web图表")：
Bokeh is a Python library for creating interactive visualizations for modern web browsers. It helps you build beautiful graphics, ranging from simple plots to complex dashboards with streaming datasets. With Bokeh, you can create JavaScript-powered visualizations without writing any JavaScript yourself.
</details>

<details open>
<summary>Pytorch</summary>

[Pytorch](https://pytorch.org  "交互式可视化web图表")：
是一个开源的Python机器学习库，基于Torch，用于自然语言处理等应用程序。PyTorch既可以看作加入了GPU支持的numpy，同时也可以看成一个拥有自动求导功能的强大的深度神经网络。除了Facebook外，它已经被Twitter、CMU和Salesforce等机构采用深度学习库，
</details>

<details>
[Pytorch](https://pytorch.org  "交互式可视化web图表")：

</details>


### 记在最后:
- 项目代码管理：以 git 方式管理，同步代码更方便。[git代码至Github](https://blog.csdn.net/qq_24990383/article/details/127608245 "CSDN")
- 关于[markdown](https://www.markdownguide.org/ "markdown官网")：.md 是一个很方便的结构说明文档，项目说明中需要采用。