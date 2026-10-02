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
        with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_date, f, ensure_ascii=False, indent=2) #将会话数据保存为json格式，确保中文不被转义，缩进2个空格

#加载所有的会话列表信息函数
def load_sessions():
    session_list = []
    #加载sessions目录下的所有json文件
    if os.path.exists("sessions"):#健壮性判断
        file_list = os.listdir("sessions") #获取sessions目录下的所有文件名
        for filename in file_list:
            if filename.endswith(".json"):#如果文件名以.json结尾
                session_list.append(filename[0:-5]) #将文件名去掉后缀.json，作为文件名新增到要展示的会话信息列表里
    return session_list #返回会话信息列表    

#加载指定会话函数
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):#健壮性判断,先判断存不存在
            #读取会话数据
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_date = json.load(f) #将json格式的数据加载为python字典
                st.session_state.messages = session_date["messages"] #将加载的会话数据中的消息列表，赋值给st.session_state.messages
                st.session_state.nick_name = session_date["nick_name"] #将加载的会话数据中的昵称，赋值给st.session_state.nick_name
                st.session_state.nature = session_date["nature"] #将加载的会话数据中的性格，赋值给st.session_state.nature
                st.session_state.current_session = session_name #将加载的会话数据中的会话标识，赋值给st.session_state.current_session
    except Exception as e:
        st.error(f"加载会话失败: {e}")

#删除会话信息的函数
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):#健壮性判断
            os.remove(f"sessions/{session_name}.json")#删除指定的json文件
            #如果删除的是当前会话，需要清空消息列表
            if session_name == st.session_state.current_session:
                st.session_state['messages'] = [] #清空聊天记录
                st.session_state.current_session = generate_session_name() #生成新的会话标识
            
    except Exception as e:
        st.error(f"删除会话失败: {e}")

#大标题
st.title("AI智能客服")
#logo
st.logo(Path(__file__).parent / "resources" / "cat.jpg")
#创建与AI大模型交互的客户端对象（DEEPSEEK_API_KEY 环境变量的名字，值就是deepseek的apikey）
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'),base_url="https://api.deepseek.com")
#系统提示词，一会要传入请求体中
system_prompt ="""
    你叫%s，你是一个，现在是用户的真实客服，请完全代入客服角色。:
    规则
        1.每次只回1条消息
        2.禁止任何场景或状态描述性文字
        3.匹配用户的语言
        4.回复简短，像微信聊天一样
        5.有需要的话可以用等emoji表情
        .用符合客服性格的方式对话
        7.回复的内容，要充分体现客服的性格特征
        -%s
        你必须严格遵守上述规则来回复用户
"""

#初始化聊天信息 不想每次刷新都保存的信息，均应该保存在st.session_state中
if 'messages' not in st.session_state:  #保存聊天记录的地方
        st.session_state['messages'] = []
    #昵称
if 'nick_name' not in st.session_state: #保存伴侣的昵称
    st.session_state['nick_name'] = '图小辰' #昵称默认值
    #性格
if 'nature' not in st.session_state: #保存伴侣性格
    st.session_state['nature'] = '专业严谨的客服'#性格默认值
    #会话标识
if 'current_session' not in st.session_state: #保存唯一会话标识
    st.session_state['current_session'] = datetime.datetime.now().strftime("%Y-%m-%d_%H-%m-%S")#格式化显示
  
    #展示聊天记录
st.text(f"会话名称：{st.session_state.current_session}")
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
        if st.session_state.messages: #如果之前有会话记录,再清空之前的聊天记录生成新的会话标识，再保存会话信息，再刷新页面，不然反复点击“新建会话”按钮会一下子创建很多的保存文件
            st.session_state['messages'] = [] #清空聊天记录
            st.session_state.current_session = generate_session_name() #生成新的会话标识
            save_session()#调用保存会话信息的函数，开启一个新文件保存新会话信息
            st.rerun()#刷新页面

    #会话历史
    st.text("会话历史")
    session_list = load_sessions() #加载所有的会话列表信息
    for session in session_list:
        col1,col2 = st.columns([4,1]) #通过columns函数，创建两个列，占比为4:1 (类似解包的动作)
        with col1:
            #三元运算符：如果条件表达式为真，则返回第一个表达式的值；否则，则返回第二个表达式的值 -->语法：表达式1 if 条件表达式 else 表达式2
            if st.button(session,width="stretch",icon="💌",key=f"load_{session}",type="primary" if session == st.session_state.current_session else "secondary"):#点击按钮，加载会话信息,使用三元运算符区分当前会话
                load_session(session)#调用加载会话信息的函数
                st.rerun()#刷新页面
        with col2:
            if st.button("删除",icon="🗑️",key=f"delete_{session}"):#点击按钮，删除会话信息(传入key参数，是因为目前每个按钮传入的参数都是相同的，所以可以使用key参数来区分不同的会话)
                delete_session(session)#调用删除会话信息的函数
                st.rerun()#刷新页面
   
    #当前会话伴侣信息
    st.subheader("客服信息")
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
    #保存会话信息
    save_session()#调用保存会话信息的函数,保存最新的会话信息(因为实时保存信息不能只靠“新建会话”按钮,而是大模型响应完之后就立即保存)

