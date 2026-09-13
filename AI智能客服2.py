import streamlit as st
from pathlib import Path
import os
from openai import OpenAI

#设置页面配置项
st.set_page_config(
page_title="AI智能客服",
page_icon="🤖",
#布局
layout="wide",
#控制的是侧边栏的状态
initial_sidebar_state="expanded",
menu_items={}
)
#大标题
st.title("AI智能客服")
#logo
st.logo(Path(__file__).parent / "resources" / "cat.jpg")

#创建与AI大模型交互的客户端对象（DEEPSEEK_API_KEY 环境变量的名字，值就是deepseek的apikey）
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'),base_url="https://api.deepseek.com")
#系统提示词，一会要传入请求体中
system_prompt = "你是阿辰，一个开发小助手"

#初始化聊天信息
if 'messages' not in st.session_state:
        st.session_state['messages'] = []
#展示聊天记录
for message in st.session_state.messages:  
    st.chat_message(message["role"]).write(message["content"])
      
#聊天输入框
prompt = st.chat_input("请输入你要问的问题")
if prompt:#字符串会自动转化为布尔值，如果字符串非空，则为True
    st.chat_message("user").write(prompt)#在网页中显示给用户
    st.session_state.messages.append({"role": "user", "content": prompt})#存入用户输入的提示词
    print("--------->调用AI大模型，提示词",prompt)
    #调用AI大模型
    #与AI大模型进行交互
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content":system_prompt},#系统提示词可以提前定义变量，方便用户动态修改
            *st.session_state.messages #用户输入的提示词，和AI大模型返回的结果，都保存在session_state.messages这个列表中，且存储结构刚好是一个个字典，直接将这个列表解包，则得到一个个字典
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
   
     #输出大模型返回的结果(非流式输出的解析方式)
        #print("----------->大模型返回的结果",response.choices[0].message.content)#控制台保留一份
        #st.chat_message("assistant").write(response.choices[0].message.content)#在网页中显示给用户


    #输出大模型返回的结果(流式输出的解析方式)
    response_message = st.empty()#创建一个空对象，用于展示AI的回复
    full_response = ""#用于接收拼接起来的完整回复
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            response_message.chat_message("assistant").write(full_response)#展示给用户AI的回复
    #存入AI大模型返回的结果
    print("----------->大模型返回的结果",full_response)#控制台保留一份
    st.session_state.messages.append({"role": "assistant", "content": full_response})#存入我们建立的缓存容器中
    
