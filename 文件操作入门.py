#打开文件
import os
print(os.getcwd())
f = open('./resources/静夜思.txt','r',encoding='utf-8') 
#读取文件内容
content = f.read()#读取所有内容
#关闭文件
f.close()