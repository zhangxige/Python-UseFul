# Anaconda 常用命令

![Static Badge](https://img.shields.io/badge/build-passing-brightgreen)


![Static Badge](https://img.shields.io/badge/zsr-codelab-red?logo=GitHub&label=hello)

### 1. 创建、删除和复制虚拟环境

创建名为 env_name 的虚拟环境：

```Shell
conda create --name env_name
```

创建名为 env_name 的虚拟环境并同时安装 python3.7 ：

```Shell
conda create --name env_name python=3.7
```

删除名为 env_name 的虚拟环境：

```Shell
conda remove --name env_name --all
```

复制名为 env_name 的虚拟环境：

```Shell
conda create --name env_name_old --clone env_name_new
```

PS：Anaconda没有重命名虚拟环境的操作，若要重命名虚拟环境，需要结合复制和删除虚拟环境两个命令实现。

### 2. 激活虚拟环境
激活名为 env_name 的虚拟环境：

```Shell
conda activate env_name
```

### 3. 查看当前虚拟环境列表

```Shell
conda env list 或 conda info -e
```

### 4 给虚拟环境装包
指定虚拟环境名进行装包：

```Shell
conda install -n env_name package_name
```

激活虚拟环境，并在该虚拟环境下装包：
```Shell
conda activate env_name

conda install package_name
```

安装指定版本号的包：

```Shell
conda install peckage_name==x.x
```

### 5 配置Anaconda的镜像网址
使用如下命令在家目录生成名为 .condarc 的配置文件：
```Shell
conda config

conda config --set show_channel_urls yes

conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/

conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
 ```
确保配置文件的格式如下：

```txt
ssl_verify: true
channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
show_channel_urls: true
 ```

查看当前镜像：

```Shell
conda config --show channels
```

查看配置文件路径及镜像：

```Shell
conda config --show-sources
```

### 6. 导出配置文件和通过配置文件安装
pip批量导出包含环境中所有组件的requirements.txt文件

```Shell
pip freeze > requirements.txt
```

pip批量安装requirements.txt文件中包含的组件依赖

```Shell
pip install -r requirements.txt
```

conda批量导出包含环境中所有组件的requirements.txt文件

```Shell
conda list -e > requirements.txt
```

conda批量安装requirements.txt文件中包含的组件依赖

```Shell
conda install --yes --file requirements.txt
```

### 7. 导出配置文件和通过配置文件安装
```Shell
conda env export > environment.yml
```

使用conda env create从environment.yml创建环境

```Shell
conda env create -f environment.yml
```

### 参考
[Anaconda官方文档](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html)

