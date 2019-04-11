import requests

headers={
    "scheme": "https",
    "version": "HTTP/1.1",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate",
    "accept-language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "User-Agent" : "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
    "X-Forwared-For":"1.1.1.1"
}
url='http://ctf5.shiyanbar.com/phpaudit/'
ss=requests.session()
key='MTU1NDI2MDIwMw3D%3D'
payload={'pass_key':key}
pres = ss.get(url,headers=headers)
content = pres.content
header = pres.headers
print("header:\n")
print(header)
print("content:\n")
print(content)