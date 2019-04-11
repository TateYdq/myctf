import requests
import base64
url='http://123.206.87.240:8002/web6/'
ss = requests.session()
headers = ss.get(url=url).headers
flag = base64.b64decode(headers['flag']).decode("utf-8")
flag = base64.b64decode(flag.split(': ')[1])
print(flag)
payload={"margin":flag}
post=ss.post(url=url,data=payload)
headers = post.headers
content = post.content.decode('utf-8')
print(content)

# flag=headers['flag']
# print(flag)
# payload={"margin":flag}
# post=ss.post(url=url,data=payload)
# headers = post.headers
# content = post.content.decode('utf-8')
# print(content)
