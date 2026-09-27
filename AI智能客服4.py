import streamlit as st
from pathlib import Path
import os
from openai import OpenAI
import datetime
import json

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
#定义一个生成新建会话标识的函数
def generate_session_name():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%m-%S") #格式化显示当前时间，生成唯一标识符

#定义一个保存会话信息的函数
def save_session():
    if st.session_state.current_session:
        #构建新的会话对象
        session_date = {
                    "nick_name": st.session_state.nick_name,
                    "nature": st.session_state.nature,
                    "current_session": st.session_state.current_session,
                    "messages": st.session_state.messages
                }     
     #如果 sessions 目录不存在，则创建
        if not os.path.exists("sessions"):
            os.makedirs("sessions")
     #保存会话数据
        with open(f"seesions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_date, f, ensure_ascii=False, indent=2) #将会话数据保存为json格式，确保中文不被转义，缩进2个空格



#大标题
st.title("AI智能客服")
#logo
st.logo(Path(__file__).parent / "resources" / "cat.jpg")

#创建与AI大模型交互的客户端对象（DEEPSEEK_API_KEY 环境变量的名字，值就是deepseek的apikey）
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'),base_url="https://api.deepseek.com")
#系统提示词，一会要传入请求体中
system_prompt ="""
    你叫%s，你是一个，现在是用户的真实伴侣，请完全代入伴侣角色。:
    规则
        1.每次只回1条消息
        2.禁止任何场景或状态描述性文字
        3.匹配用户的语言
        4.回复简短，像微信聊天一样
        5.有需要的话可以用等emoji表情
        .用符合伴侣性格的方式对话
        7.回复的内容，要充分体现伴侣的性格特征
    伴侣性格:
        -%s
        你必须严格遵守上述规则来回复用户
"""

#初始化聊天信息 不想每次刷新都保存的信息，均应该保存在st.session_state中
if 'messages' not in st.session_state:  #保存聊天记录的地方
        st.session_state['messages'] = []
    #昵称
if 'nick_name' not in st.session_state: #保存伴侣的昵称
    st.session_state['nick_name'] = '小甜甜' #昵称默认值
    #性格
if 'nature' not in st.session_state: #保存伴侣性格
    st.session_state['nature'] = '活泼开朗的东北姑娘'#性格默认值
    #会话标识
if 'current_session' not in st.session_state: #保存唯一会话标识
    st.session_state['current_session'] = datetime.datetime.now().strftime("%Y-%m-%d_%H-%m-%S")#格式化显示
  
    #展示聊天记录
for message in st.session_state.messages:  
    st.chat_message(message["role"]).write(message["content"])

#左侧的侧边栏 -with:streamlit中的上下文管理器
with st.sidebar:
    #侧边栏标题
    st.subheader('AI控制面板')
    #新建会话按钮
    if st.button("新建会话",width="stretch",icon="🔄"):
        #1.保存当前会话信息
        save_session()#调用保存会话信息的函数

        #2.创建一个新的会话
    st.session_state['messages'] = [] #清空聊天记录
    st.session_state.current_session = generate_session_name() #生成新的会话标识
   
   #当前会话伴侣信息
    st.subheader("伴侣信息")
    nick_name = st.text_input("昵称",placeholder="请输入昵称",value = st.session_state.nick_name)#昵称输入框，placeholder为提示信息，value为默认值
    if nick_name: #如果用户输入了昵称
        st.session_state['nick_name'] = nick_name
    nature  = st.text_area("性格",placeholder="请输入性格",value = st.session_state.nature) #性格输入框
    if nature: #如果用户输入了性格
        st.session_state['nature'] = nature
















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
            {"role": "system", "content":system_prompt % (st.session_state.nick_name,st.session_state.nature)},#系统提示词可以提前定义变量，方便用户动态修改
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
    
