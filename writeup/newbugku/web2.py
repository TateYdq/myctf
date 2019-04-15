import requests
from bs4 import BeautifulSoup
url='http://123.206.31.85:10002/'
ss = requests.session()
content = ss.get(url).content.decode('utf-8')
# print(content)
bp = BeautifulSoup(content,'html.parser')
strs = str(bp.p).split('<br/>')[1].split('</p>')[0][1:]
rs = eval(strs)
payload={'result':rs}
content = ss.post(url,data=payload).content.decode('utf-8')
print(content)