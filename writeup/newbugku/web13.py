import requests
import base64
url='http://123.206.31.85:10013/index.php'
ss = requests.session()
headers = ss.get(url).headers
flag=str(base64.b64decode(headers['Password'])).split('{')[1][:-2]
print(flag)
payload={'password':flag}
content = ss.post(url,data=payload).content.decode('utf-8')
print(content)