import requests
import base64
url='http://ctf5.shiyanbar.com/web/10/10.php'
ss=requests.session()
flag=ss.get(url).headers['FLAG']
flag = str(base64.b64decode(flag),encoding='utf-8').split(':')[1]
print(flag)
payload = {'key':flag}
content = ss.post(url,data=payload).content
print(content)