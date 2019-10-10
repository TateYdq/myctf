import base64
cipher='e3nifIH9b_C@n@dH'
len_cipher=len(cipher)#16
s=''
for i in range(len_cipher):
    s+= chr(ord(cipher[i])-i)
#v1=s[0:40]
v=base64.b64decode(s)
print(v)