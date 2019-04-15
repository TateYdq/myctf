import requests
import base64
url='http://123.206.31.85:10020/index.php'
ss = requests.session()
flag = ss.get(url).content.decode('utf-8').split('：')[1].split('<')[0]
print(flag)
rs = ss.get(url+'?'+'key='+flag)
content = rs.content.decode('utf-8')
headers = rs.headers
print(headers)
print(content)