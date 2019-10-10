1.

打开后直接逆向为c语言，出现flag





2.游戏过关

（1）正面破解

玩游戏，让8个灯都开着。

n变化，n-1和n+1都变化。

初始时，所有都关。

要达到的效果是所有都开。

（2）逆向方式

用IDA分析处代码逻辑，发现flag是两个数组和一个常数，三者之间进行异或产生的。

正向编写代码游戏过关.py产生flag即可。



3.love

IDA打开软件分析逻辑，发现是要求输入的值经过一系列运算后和已知字符串比较，正确即可。证明这道题是一道解迷题，已知密文和算法，获取明文。

思路是将算法还原下，再反过来解。

主要算法：

str为输入字符串，v0为该字符串长度。

（1） v1 = (const char *)sub_4110BE((int)&Str, len_Str, (int)&v11);

仔细观看sub_4110BE函数发现其实是base64加密。

（2）strncpy(Dest, v1, 0x28u);

取v1得40个字节拷贝给Dst



（3） for ( j = 0; j < v8; ++j )
    			Dest[j] += j;

​	len_Dest = j_strlen(Dest);

​	if ( !strncmp(Dest, Str2, len_Dest) )
​    	sub_41132F("rigth flag!\n")

(4)















