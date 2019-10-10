v8=':"AL_RT^L*.?+6/46'
v7 = hex(28537194573619560)[2:]
j=0
s=''
for i in range(len(v8)):
    tmp = int(v7[14-2-j*2:14-j*2],16)
    mS = chr(tmp ^ ord(v8[i]))
    print("tmp:"+str(tmp)+",v8:"+str(ord(v8[i])))
    s += mS
    j = (j + 1)%7
print(s)
