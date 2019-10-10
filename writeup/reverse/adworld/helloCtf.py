a='437261636b4d654a757374466f7246756e'
s=''
for i in range(len(a)):
    if i % 2 != 0:
        continue
    s += chr(int(a[i:i+2],16)) 
print(s)