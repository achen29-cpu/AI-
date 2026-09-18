#打开文件
#import os
#print(os.getcwd())
#f = open('C:/Users/LH/Desktop/API_test/API_test/resources/静夜思.txt', 'r', encoding='utf-8')
#读取文件内容
#content = f.readlines()#读取所有内容
#关闭文件
#for line in content:
 #   print(line.strip())#strip()去掉每行末尾的换行符
#f.close()

#如何写入数据
f = open('C:/Users/LH/Desktop/API_test/API_test/resources/静夜思.txt', 'w', encoding='utf-8')
#资源释放方案 1
try:
    f.write('窗前明月光\n')
    f.write('窗前明光明\n')
    f.write('窗前明明明\n')
finally:
    f.close()

#项目中推荐的资源释放方案
#with语句（上下文管理器）的核心作用就是确保资源的总是被正确获取和释放（即便运行过程中发生异常，也会被正确释放）
with open('C:/Users/LH/Desktop/API_test/API_test/resources/静夜思.txt', 'w', encoding='utf-8') as f:
    f.write('窗前明月光\n')
    f.write('窗前明光明\n')
    f.write('窗前明明明\n')