import streamlit as st
from pathlib import Path
#设置页面配置项
st.set_page_config(
page_title="AI智能伴侣",
page_icon="🤖",

#布局
layout="wide",
#控制的是侧边栏的状态
initial_sidebar_state="expanded",
menu_items={}
)
#大标题
st.title("AI智能伴侣")
#logo
st.logo(Path(__file__).parent / "resources" / "cat.jpg")
#聊天输入框
prompt = st.chat_input("请输入你要问的问题")
if prompt:#字符串会自动转化为布尔值，如果字符串非空，则为True
    st.chat_message("用户").write(prompt)
    print("--------->调用AI大模型，提示词",prompt)