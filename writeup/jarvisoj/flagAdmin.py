#-*- coding:utf-8 -*-
#md5扩展长度攻击题
import requests
import hashpumpy
import urllib
ss = requests.session()
url = "http://web.jarvisoj.com:32778/"
hash = "3a4727d57463f122833d9e732f94e4e0"
str1 = 's:5:"guest";'
str2 = 's:5:"admin";'
rev_str1 = str1[::-1]
rev_str2 = str2[::-1]
for len in range(20):
    digest,msg = hashpumpy.hashpump(hash,rev_str1,rev_str2,len)
    role = msg[::-1]
    payload = {
        'role':urllib.quote(role),
        'hsh':digest
    }
    print("len:%d,payload:%s"%(len,str(payload)))
    res = requests.get(url,cookies=payload)
    content = res.content.decode("utf-8")
    if "Only" not in content:
        print(content)