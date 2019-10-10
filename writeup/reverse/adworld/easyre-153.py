import hashlib
a=[]
a.append('1')
for i in range(1,20):
    a.append('1')
    #a[int(i*(i+1)/2)] = 1
    for j in range(1,i):
        tmp = 0
        for k in range(j-1,i):
            tmp += int(a[int(k*(k+1)/2)+j-1])
        #a[int(i*(i+1)/2)+j] = tmp
        a.append(str(tmp))
    a.append('1')
plain = ''.join(a)
print(plain)
md5 = hashlib.md5()
md5.update(plain.encode("utf-8"))
print(md5.hexdigest())
