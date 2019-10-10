import requests
ss=requests.session()
data={'b':2}
res=ss.post("http://111.198.29.45:36851/?a=1",data=data).content.decode("utf-8")
print(res)