### 常用库 streamlit 简介

***
> ***Notes***: 一定要注意使用的Python版本，低版本的Python对 ***streamlit*** 库的支持版本不高。实测3.8、3.9版本支持不了最新版本 ***streamlit*** 
***

非常简单的界面构建

```python
# code example
import streamlit as st
st.title('title')
st.caption('caption')
```

非常简单的界面布局

```python
# code example
import streamlit as st

# container control the page
with st.container():
    st.write("This is inside the container")
    ...
```
