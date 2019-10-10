import base64
a='you_know_how_to_remove_junk_code'
s=''
for i in range(len(a)):
    s += chr(ord(a[i])^0x25)
s=base64.b64encode(s.encode('utf-8'))
print(s)