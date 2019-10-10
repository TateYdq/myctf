def toHex(c):
    print(hex(c))
    return str(hex(c)[2:])

a =[84,-56,126,-29,100,-57,22,-102,-51,17,101,50,45,-29,-45,67,-110,-87,-99,-46,-26,109,44,-45,-74,-67,-2,106,19]
flag = 0x0040A080
s = ''
for i in range(6):
    b = '0x'+toHex(a[4*i])+toHex(a[4*i+1])+toHex(a[4*i+2])+toHex(a[4*i+3])
    #num = int(b,16)
    #b = hex(num ^ 0xDEADBEEF)
    print(b)
    #for j in range(3,0):
    #    s += chr(Byte(b+j)^ Byte(flag + 4*i+j))
print(s)




