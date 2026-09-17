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
f.write('窗前明月光\n')
f.write('窗前明光明\n')
f.write('窗前明明明\n')
f.close()