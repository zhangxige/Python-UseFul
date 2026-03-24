# Python 软件包标准结构示例教程

我给你**完整写好、结构最标准、可直接复制保存为 ** **`.md`** ** 文件**的完整版 Python 包教程，你直接全选复制 → 新建文件 → 保存为 `python_package_example.md` 就能用。

下面是**完整可下载 Markdown 内容**：

---

# Python 软件包完整示例：标准结构 + 详细讲解

## 前言

本文带你从零创建一个**可安装、可导入、可发布**的标准 Python 软件包，适合学习、项目使用或发布到 PyPI。

包名：`myutils`  

功能：包含字符串工具、数学工具、文件工具。

---

## 一、最终文件结构（标准 Python 包）

```Plain Text

myutils_project/            # 项目根目录
├── myutils/                # 包源码目录（真正的包）
│   ├── __init__.py         # 包标识文件（必须）
│   ├── __version__.py      # 版本号
│   ├── string_tools.py     # 字符串工具
│   ├── math_tools.py       # 数学工具
│   └── file_tools.py       # 文件工具
├── tests/                  # 测试目录
│   └── test_myutils.py
├── README.md               # 说明文档
└── pyproject.toml          # 包安装配置（必须）
```

---

## 二、逐文件实现与功能讲解

### 1. pyproject.toml（安装配置文件）

**作用**：定义包名、版本、依赖、安装方式。

```TOML

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "myutils"
version = "0.1.0"
author = "your name"
description = "A simple Python utility package"
readme = "README.md"
requires-python = ">=3.7"
```

---

### 2. 包源码目录：myutils/

#### ① **init**.py（包的入口）

**作用**：

- 标记文件夹为 Python 包

- 控制对外暴露的接口

```Python

# 导入版本
from .__version__ import __version__

# 导入工具函数
from .string_tools import reverse_string, to_upper
from .math_tools import add, multiply, is_odd
from .file_tools import read_file, write_file

# 公开接口列表
__all__ = [
    "reverse_string",
    "to_upper",
    "add",
    "multiply",
    "is_odd",
    "read_file",
    "write_file",
    "__version__",
]
```

---

#### ② **version**.py（版本管理）

```Python

__version__ = "0.1.0"
```

---

#### ③ [string_tools.py](string_tools.py)（字符串工具）

```Python

def reverse_string(s: str) -> str:
    """反转字符串"""
    return s[::-1]

def to_upper(s: str) -> str:
    """转大写"""
    return s.upper()
```

---

#### ④ [math_tools.py](math_tools.py)（数学工具）

```Python

def add(a: int | float, b: int | float) -> int | float:
    """加法"""
    return a + b

def multiply(a: int | float, b: int | float) -> int | float:
    """乘法"""
    return a * b

def is_odd(n: int) -> bool:
    """判断是否为奇数"""
    return n % 2 != 0
```

---

#### ⑤ [file_tools.py](file_tools.py)（文件工具）

```Python

def read_file(file_path: str, encoding: str = "utf-8") -> str:
    """读取文本文件"""
    with open(file_path, "r", encoding=encoding) as f:
        return f.read()

def write_file(file_path: str, content: str, encoding: str = "utf-8"):
    """写入文本文件"""
    with open(file_path, "w", encoding=encoding) as f:
        f.write(content)
```

---

## 三、测试文件

### tests/[test_myutils.py](test_myutils.py)

```Python

import myutils

# 测试版本
print("Version:", myutils.__version__)

# 测试字符串工具
print(myutils.reverse_string("hello"))
print(myutils.to_upper("python"))

# 测试数学工具
print(myutils.add(1, 2))
print(myutils.multiply(3, 4))
print(myutils.is_odd(5))

# 测试文件工具
myutils.write_file("test.txt", "hello world")
print(myutils.read_file("test.txt"))
```

---

## 四、[README.md](README.md)（说明文档）

```Markdown

# myutils
A simple Python utility package.

## Install
pip install .

## Usage
import myutils

print(myutils.add(1, 2))
```

---

## 五、安装与使用方法

### 1. 安装包

进入项目根目录，执行：

```Bash

pip install .
```

### 2. 任意位置使用

```Python

import myutils

print(myutils.add(10, 20))
print(myutils.reverse_string("markdown"))
```

---

## 六、文件功能说明表

|文件/目录|作用|是否必须|
|---|---|---|
|myutils/|包源码|✅|
|**init**.py|标记为包、定义接口|✅|
|**version**.py|版本号|推荐|
|[string_tools.py](string_tools.py)|功能模块|否|
|[math_tools.py](math_tools.py)|功能模块|否|
|[file_tools.py](file_tools.py)|功能模块|否|
|pyproject.toml|安装配置|✅|
|tests/|测试|推荐|
|[README.md](README.md)|说明|推荐|
---

## 七、这个包的特点

- 标准结构，可直接发布到 PyPI

- 接口清晰，用户使用简单

- 模块化设计，易扩展

- 支持全局 `pip` 安装

- 适合企业项目、个人工具、开源库

---
