import streamlit as st
from pathlib import Path
import os
from openai import OpenAI

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

#创建与AI大模型交互的客户端对象（DEEPSEEK_API_KEY 环境变量的名字，值就是deepseek的apikey）
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'),base_url="https://api.deepseek.com")
#系统提示词，一会要传入请求体中
system_prompt = "你是阿辰，一个开发小助手"

#大标题
st.title("AI智能伴侣")

#logo
st.logo(Path(__file__).parent / "resources" / "cat.jpg")

#聊天输入框
prompt = st.chat_input("请输入你要问的问题")
if prompt:#字符串会自动转化为布尔值，如果字符串非空，则为True
    st.chat_message("user").write(prompt)#在网页中显示给用户
    print("--------->调用AI大模型，提示词",prompt)
    #调用AI大模型
    #与AI大模型进行交互
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content":system_prompt},#系统提示词可以提前定义变量，方便用户动态修改
            {"role": "user", "content": prompt},#用户提示词按照上面定义的prompt来输入
        ],
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
    print("----------->大模型返回的结果",response.choices[0].message.content)#控制台保留一份
    st.chat_message("assistant").write(response.choices[0].message.content)#在网页中显示给用户