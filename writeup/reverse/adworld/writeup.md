1、re1
关键函数：
_mm_store_si128 ( __m128i *p, __m128i a);
将__m128i 变量a的值存储到p所指定的变量中去；
讲xmmword_413E34转换为string类型计得flag：
DUTCTF{We1c0met0DUTCTF}


2、Hello, CTF
（1）
if ( strlen(v9) > 0x11 )
    break;
输入长度小于等于17
（2）
do
{
    v4 = v9[v3];
    sprintf(&v8, "%x", v4);
    strcat(&v10, &v8);
    ++v3;
}while ( v3 < 17 );
v9的十六进制赋值给v10
（3）
 strcpy(&v13, "437261636b4d654a757374466f7246756e");
if ( !strcmp(&v10, &v13) )
    sub_40134B((int)aSuccess, v7);
如果v13和v10相等则成功
所以利用脚本helloCtf.py得到v4的值，此即为flag


3、open-source
（1）
if (argc != 4) {...}
四个参数
（2）
if (first != 0xcafe) {...}
第2个参数为0xcafe
（3）
if (second % 5 == 3 || second % 17 != 8) {...}
第三个参数模5不等于3，模17等于8 
（4）
if (strcmp("h4cky0u", argv[3])) {...}
第四个参数为h4cky0u
（5）计算key的方法
unsigned int hash = first * 31337 + (second % 17) * 11 + strlen(argv[3]) - 1615810207;
printf("%x\n", hash);
（6）解法：
hash=first * 31337 + (second % 17) * 11 + strlen(argv[3]) - 1615810207
    =1628458542+88+7-1615810207
    =12648430
hex(12648430)='0xc0ffee'

4、logmein
（1）核心代码
strcpy(v8, ":\"AL_RT^L*.?+6/46");
for ( i = 0; i < strlen(s); ++i )
{
if ( i >= strlen(v8) )
    printf("Incorrect password!\n");
if ( s[i] != (char)(*((_BYTE *)&v7 + i % 7) ^ v8[i]) )
    printf("Incorrect password!\n");
}
printf("You entered the correct password!\nGreat job!\n");
（2）
两种思路，一种是动态调试中求出s[i]，另一种是直接结算。
对于后面中方法脚本为:
推出解密代码logmein.py

5、insanity
直接看逆向的源码发现strs，发现像flag格式提交即可

6、
关键代码：
s2 = decrypt(&s, &dword_8048A90);
if ( fgetws(ws, 0x2000, stdin) )
{
ws[wcslen(ws) - 1] = 0;
if ( !wcscmp(ws, s2) )
    wprintf((int)&unk_8048B44);
else
    wprintf((int)&unk_8048BA4);
}
即输入的ws和s2相等即可

decrypt代码:
wchar_t *__cdecl decrypt(wchar_t *s, wchar_t *a2)
{
  ...
  while ( v4 < v6 )
  {
    for ( i = 0; i < v7 && v4 < v6; ++i )
      dest[v4++] -= a2[i];
  }
  ...
  return dest;
}

a1=
a2=0x14011402



7、dmd-50
关键代码

(1)
 if (*v41 != 55|| v41[1] != 56|| v41[2] != 48|| v41[3] != 52|| v41[4] != 51|| v41[5] != 56|| v41[6] != 100|| v41[7] != 53|| v41[8] != 98|| v41[9] != 54|| v41[10] != 101|| v41[11] != 50|| v41[12] != 57|| v41[13] != 100|| v41[14] != 98|| v41[15] != 48|| v41[16] != 56|| v41[17] != 57|| v41[18] != 56|| v41[19] != 98|| v41[20] != 99|| v41[21] != 52|| v41[22] != 102|| v41[23] != 48|| v41[24] != 50|| v41[25] != 50|| v41[26] != 53|| v41[27] != 57|| v41[28] != 51|| v41[29] != 53|| v41[30] != 99|| v41[31] != 48);
 推知v41为780438d5b6e29db0898bc4f0225935c0，
(2)
std::string::string(&v39, &v42, &v38);
md5((MD5 *)&v40, (const std::string *)&v39);
v41 = (_BYTE *)std::string::c_str((std::string *)&v40);
可以看出v41是经过v39进行md5生成的，通过cmd5网推知两次md5之前是grape.
所以再将grape进行md5一次即可。


8、Shuffle
题目提示：找到字符串在随机化之前.
找到随机化前的数组转化为字符串即可。
s=[69,67,67,79,78,123,87,101,108,99,111,109,101,32,116,111,32,116,104,101,32,83, 69,67,67,79,78,32,50,48,49,52,32,67,84,70,33,125,0]
转化后得：
SECCON{Welcome to the SECCON 2014 CTF!}


9、re2-cpp-is-awesome
（1）需要两个参数
if ( argc != 2 )
（2）简化后的代码：
v15=0
 for ( i = begin(&v11); ; add1(&i) )
  {
    v13 = end(&v11);
    if (i == v13)
      break;
    if ( *i != off_6020A0[dword_6020C0[v15]] )
      cout<<"Better luck next time.\n";
    ++v15;
  }
（3）add1函数
_QWORD *__fastcall sub_400D7A(_QWORD *a1)
{
  ++*a1;
  return a1;
}
可以看出题目的意思是让
off_6020A0[dword_6020C0[v15]]和输入字符串v11相等。

dword_6020C0={
24h, 0, 5, 36h, 65h, 7, 27h, 26h, 2Dh, 1, 3, 0, 0Dh,
56h, 1, 3, 65h, 3, 2Dh, 16h, 2, 15h, 3, 65h, 0, 29h,
2 dup(44h), 1, 44h, 2Bh
}
所以使用解密脚本re2-cpp-is-awesome.py解密即可



10、re-for-50-plz-50
打开后发现是MIPS不能反汇编。
利用retdec插件生成：


int main(int argc, char ** argv) {
    // 0x401398
    for (int32_t i = 0; i < 31; i++) {
        char v1 = *(char *)(i + (int32_t)"cbtcqLUBChERV[[Nh@_X^D]X_YPV[CJ"); // 0x4013d8
        char v2 = *(char *)(*(int32_t *)((int32_t)argv + 4) + i); // 0x4013f0
        if ((int32_t)v1 != ((int32_t)v2 ^ 55)) {
            // 0x401408
            print();
            exit_funct();
        }
    }
    // 0x401444
    exit_funct();
    return 1;
}
exp代码参见：re-for-50-plz-50.py

11、key（不会）

满足：
   if ( *(_BYTE *)this != *(_BYTE *)v7
      || v8 != -3
      && ((v10 = *((_BYTE *)this + 1), v9 = v10 < *(_BYTE *)(v7 + 1), v10 != *(_BYTE *)(v7 + 1))
       || v8 != -2
       && ((v11 = *((_BYTE *)this + 2), v9 = v11 < *(_BYTE *)(v7 + 2), v11 != *(_BYTE *)(v7 + 2))
        || v8 != -1 && (v12 = *((_BYTE *)this + 3), v9 = v12 < *(_BYTE *)(v7 + 3), v12 != *(_BYTE *)(v7 + 3)))) )
    



关键代码：
v46 = 15;
  v45 = 0;
  LOBYTE(v44) = 0;
  v53 = 0;
  v43 = 15;
  v42 = 0;
  LOBYTE(v41) = 0;
  LOBYTE(v53) = 1;
  v0 = 0;
  v48 = 1684630885;
  LOWORD(v49) = 97;
  *(_OWORD *)Memory = xmmword_40528C;
  v51 = 11836;
  v52 = 0;
  v50 = xmmword_4052A4;
  do
  {
    sub_4021E0(1u, (*((_BYTE *)Memory + v0) ^ *((_BYTE *)&v50 + v0)) + 22);
    ++v0;
  }
  while ( v0 < 18 );



v1 = 0;
  v49 = 15;
  v48 = 0;
  LOBYTE(Memory[0]) = 0;
  LOBYTE(v53) = 2;
  v2 = v43;
  v3 = (void **)v41;
  do
  {
    v4 = &v41;
    if ( v2 >= 0x10 )
      v4 = v3;
    sub_4021E0(1u, *((_BYTE *)v4 + v1++) + 9);
  }
  while ( v1 < 18 );
  memset(&Dst, 0, 0xB8u);
  sub_401620(v5, v6, v7, v8);
  LOBYTE(v53) = 3;
  if ( v32[*(_DWORD *)(Dst + 4)] & 6 )
  {
    v9 = sub_402A00(std::cerr, "?W?h?a?t h?a?p?p?e?n?", sub_402C50);
    std::basic_ostream<char,std::char_traits<char>>::operator<<(v9, v10);
    exit(-1);
  }
  sub_402E90(&Dst, &v44);
  v11 = &v33;


12、simple-check-100
简要分析逻辑，先根据输入判断check_key，如果输入正确则利用interesting_function输出flag。
所以要在用IDA远程linux调试时，在check_key调用结束后改变eax的值为1即可。


13、re1-100
bufParentRead总共40位
前10位
53fc275d81
后10位
4938ae4efd
混淆后的全部：daf29f59034938ae4efd53fc275d81053ed5be8c

confuseKey混淆函数关键：
 *szKey = 123;
  strcat(szKey, szPart3);
  strcat(szKey, szPart4);
  strcat(szKey, szPart1);
  strcat(szKey, szPart2);
  szKey[41] = 125;


所以可以推知混淆之前的szKey为53fc275d81053ed5be8cdaf29f59034938ae4efd,此即为flag


14、ReverseMe-120
分析下逻辑可知是输入的字符串经过base64解密后再与0x25异或后得：you_know_how_to_remove_junk_code
所以反推出flag:
XEpQek5LSlJ6TUpSelFKeldASEpTQHpPUEtOekZKQUA=


15、IgniteMe
（1）4位后才开始
strcpy(v11, "EIS{");
i = 4;
v6 = 0;
while ( i < strlen(a1) - 1 )
  v8[v6++] = a1[i++];    
v8[v6] = 0;
memset(v4, 0, 0x20u);
（2）
for ( i = 0; ; ++i )
{
  v2 = strlen(v8);
  if ( i >= v2 )
    break;
  #小写变为大写
  if ( v8[i] >= 97 && v8[i] <= 122 )
  {
    v8[i] -= 32;
    v3 = 1;
  }
  #大写变为小写
  if ( !v3 && v8[i] >= 65 && v8[i] <= 90 )
    v8[i] += 32;
  v4[i] = byte_4420B0[i] ^ ((v8[i]) ^ 0x55) + 72);
  v3 = 0;
}
return strcmp("GONDPHyGjPEKruv{{pj]X@rF", v4) == 0;

所以
假设a='GONDPHyGjPEKruv{{pj]X@rF'
v8=(a^byte_4420B0-72)^0x55
解密python脚本
a='GONDPHyGjPEKruv{{pj]X@rF'
b=0x4420B0
s=''
for i in range(len(a)):
  s += chr((int(ord(a[i])^Byte(b+i))-72) ^ 0x55)
print(s)


推知s为WADX_TDGK_AIHC_IHKN_PJLM
再大写转小写得出flag为：
EIS{wadx_tdgk_aihc_ihkn_pjlm}


16、Reversing-x64Elf-100

v3[0] = "Dufhbmf"
v3[1] = "pG`imos"
v3[2] = "ewUglpt";
for ( i = 0; i <= 11; ++i )
{
  if ( v3[i % 3][2*(i/3)] - a1[i] != 1 )
    return 1LL;
}
利用该算法反推即可知flag


17、zorropub
首先输入要多少瓶
再输入id号

s1=md5()
要求s1=5eba99aff105c9ff6a1a913e343fec67

所以就是爆破使得md5为5eba99aff105c9ff6a1a913e343fec67，然后会直接爆破出flag.
参考网上的爆破脚本写出exp脚本zorropub.py。
得出id号为59306,flag为nullcon{nu11c0n_s4yz_x0r1n6_1s_4m4z1ng}



18、gametime
题目是游戏，所以一般动态调试。
大部分代码是相同的。
关键代码：
sub_E31A73((int)"key is %s (%s)", &unk_E47D02, &v27);
sub_E31A73((int)"\b\b");
v16 = &v29;
v17 = 16;
do
{
  dwMilliseconds = *(unsigned __int8 *)v16;
  sub_E31A73((int)"%02x");
  v16 = (int *)((char *)v16 + 1);
  --v17;
}
while ( v17 );

强行将IP设置跳转到这里即可输出flag.或者直接改汇编指令改为程序能正常运行，且每次判断都正确。

key is  (no5c30416d6cf52638460377995c6a8cf5)


19、easyre-153
首先upx脱壳。
再注意关键代码：
（1）
 v5 = fork();
 对于fork函数，会创建出一个子进程，在父进程中返回子进程的id号，在子进程中返回0。
（2）if ( !v5 )  //子进程中
  {
    puts("\nOMG!!!! I forgot kid's id");
    write(pipedes[1], "69800876143568214356928753", 0x1Du);
    puts("Ready to exit     ");
    exit(0);
  }
（3）//父进程中
  read(pipedes[0], &buf, 0x1Du);
  __isoc99_scanf("%d", &v6); //如果输入的v6等于子进程号。
  if ( v6 == v5 )
  {
    if ( (*(_DWORD *)((_BYTE *)lol + 3) & 0xFF) == 204 )
    {
      puts(":D");
      exit(1);
    }
    printf("\nYou got the key\n ");
    lol(&buf);
  }


(2)然后发现前面的都没用，只用看lol(&buf)函数
a1=69800876143568214356928753
v2[0] = 2 * a1[1];=114=0x72
  v2[1] = a1[4] + a1[5];=104=0x68
  v2[2] = a1[8] + a1[9];=5=101=0x65
  v2[3] = 2 * a1[12];=12=108=0x6c
  v2[4] = a1[18] + a1[17];=104=0x68
  v2[5] = a1[10] + a1[21];=101=0x65
  v2[6] = a1[9] + a1[25];=103=0x67

分别用十六进制和ascii码进行提交
  7268656c686567
  或者为rhelheg
最后发现是用ascii码版本，而且还需要在外层加上RCTF{}

20、notsequence
代码分析
（1）对v3进行初始化，输入v3,以0结束
 memset(&unk_8049BE0, 0, 0x4000u);
  v3 = &unk_8049BE0;
  do
  {
    v0 = v3;
    ++v3;
    scanf("%d", v0);
  }
  while ( *(v3 - 1) != 0 );
（2）对v3进行func1操作,要求v2不等于-1.
  v2 = func1((int)&unk_8049BE0);
  if ( v2 == -1 )
  {
    printf("check1 not pass");
    system("pause");
  }

（3）对v3进行func2操作，要求返回值异或1等于0，即返回值为1.
  if ( (unsigned __int8)func2((int)&unk_8049BE0, v2) ^ 1 )
  {
    printf("check2 not pass!");
    exit(0);
  }
（4）要求v2为20，flag即为输入的数的Hash
  if ( v2 == 20 )
  {
    puts("Congratulations! fl4g is :\nRCTF{md5(/*what you input without space or \\n~*/)}");
    exit(0);
  }

(5)对于func1函数。
 v5 = 0;
  for ( i = 0; i <= 1024 && a1[i]; i = v5 * (v5 + 1) / 2 )
  {
    v3 = 0;
    for ( j = 0; j <= v5; ++j )
      v3 += a1[(j+i)];
    if ( 1 << v5 != v3 )
      return -1;
    ++v5;
  }
  return v5;

推理一下：
i=0;v5=0;a1[0]=v3=v5*2=1

v5=1,i=1;a1[1] + a1[2]=v3=v5*2=2

v5=2,i=3;a1[3] + a1[4] + a1[5]=v3=v5*2=4
...

最后通过v5*(v5+1)/2<=1024可以解出最后返回的v5等于44.但是又要求v5等于20所以当i=20*21/2=210时,a1[210]应该为空。

(6)对于func2
 v6 = 0;
  for ( i = 1; i < 20; ++i )
  {
    v4 = 0;
    v3 = i - 1;
    if ( !a1[i] )
      return 0;
    while ( 20 - 1 > v3 )
    {
      v4 += a1[v3*(v3+1)/2+v6];
      ++v3;    }
    if (a1[v3*(v3+1)/2+i] != v4 )
      return 0;
    ++v6;
  }
  return 1;

推一下：
i=1,v6=0,v3=0,a1[0] + a1[1] + a1[3] + a1[6] + ...+a1[9*19] = v4 = a1[10*19+1]
i=2,v6=1,v3=1,a1[1+1]+a1[3+1]+a1[6+1]+...+a1[9*19+1]=v4=a1[10*19+2]
i=3,v6=2.v3=2,a1[3+2]+a1[6+2]+...a1[9*19+2]=v4=a1[10*19+3]
...
（7）所以相当于解两个公式,这两个公式应该一个是行相加，一个是列相加。推断是某个著名公式。
查阅发现是杨辉三角
杨辉三角满足这几个性质
第i行有i个数，且相加之和等于2^i(第0行开始)
第i行的前n列相加等于第i行的第n+1列。
由于一共有20行,所以a可以通过脚本easere-153.py解出。
得到：
37894beff1c632010dd6d524aa9604db
