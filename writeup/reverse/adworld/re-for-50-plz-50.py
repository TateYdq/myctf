s=''
a='cbtcqLUBChERV[[Nh@_X^D]X_YPV[CJ'
for i in range(31):
  v1 = ord(a[i])^55
  s += chr(v1)
print(s)