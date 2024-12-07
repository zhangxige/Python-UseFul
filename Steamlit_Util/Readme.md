### 常用库 streamlit 简介

***
> ***Notes***: 一定要注意使用的Python版本，低版本的Python对 ***streamlit*** 库的支持版本不高。实测3.8、3.9版本支持不了最新版本 ***streamlit*** 
***

- 项目的构建结构
```shell
# 项目结构
Streamlit_Project
-.streamlit
-- config.toml # 配置文件
- pages
-- page1.py # 页面1
-- page2.py # 页面2
   ...
- main.py # 主界面
```

```shell
# 执行项目
(conda_env) streamlit run main.py
```

- 非常简单的界面构建

```python
# code example
import streamlit as st
st.title('title')
st.caption('caption')
```

- 非常简单的界面布局

```python
# code example
import streamlit as st

# container control the page
with st.container():
    st.write("This is inside the container")
    ...
```

- 嵌入公式（latex）
- 嵌入Markdown 
- 插入控制按钮

