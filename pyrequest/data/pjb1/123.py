# -*- coding:utf-8 -*-
import os,sys
import json

mydict={'name':'leon','age':'785','email':'xxxx@163.com'}
file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"123.json")
print(file)
with open(file,'w',encoding='utf-8') as f:
    json.dump(mydict,f)
    print("完成")
