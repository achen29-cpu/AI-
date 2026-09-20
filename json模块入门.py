import json
#写入json文件
user = {
    'name' : "张",
    'age' : 18,
    'hobby' : ['1',3,4]
}
with open("c:/Users/Administrator/Desktop/AI应用实战/API_test/resources/user.json","w",encoding="utf-8") as f:
    #esure_asciishi=False表示“非ASCII码不转义”（保留中文字符原样输出）
    #indent=2表示缩进(格式化)
    json.dump(user,f,ensure_ascii=False,indent=2)

#读取json文件
with open("c:/Users/Administrator/Desktop/AI应用实战/API_test/resources/user.json","r",encoding="utf-8") as f:
    user = json.load(f)
    print(user)
    print(type(user))
