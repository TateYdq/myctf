import requests
from bs4 import BeautifulSoup
url = 'http://123.206.87.240:8002/qiumingshan/'
ss = requests.session()
content = ss.get(url).content.decode("utf-8")
bs = BeautifulSoup(content,'html.parser')
strs = bs.find('div').string[:-3]
print(strs)
num = eval(strs)
print(num)
payload={"value":num}
post = ss.post(url,data=payload)
content = post.content.decode("utf-8")
headers = post.headers
print(content)
print(headers)