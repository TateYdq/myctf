import subprocess
mLists=[]
for seed in range(17,0xFFFF):
    i = seed
    v9 = 0
    while i:
        i = i & (i-1)
        v9 = v9+1
    if v9 == 10:
        mLists.append(seed)
for id in mLists:
    proc = subprocess.Popen(['./process'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    out = proc.communicate(("1\n%s\n"%id).encode('utf-8'))[0]
    if 'nullcon' in out:
        print("id:%s,flag:%s"%(id,out[str(out).find('nullcon'):]))

