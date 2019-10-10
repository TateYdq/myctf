(1)stheasy题

逆向源码：
  if ( v1 == 29 )
      {
        v3 = 0;
        while ( s[v3] == aLk2j9ghAgfy4ds[(unsigned __int8)((unsigned __int8)byte_8049B15[v3] / 3u - 2)] )
        {
          if ( ++v3 == 29 )
            return 1;
        }
      }

exp脚本：
s=''
b2=0x08049B15
b1=0x08049AE0
for i in range(29):
    s += chr(Byte(b1+Byte(b2+i)/3-2))
print(s)

(2)Classical Crackme
把软件放入ExeInfo Pe,发现有ConfuserEx壳
网上寻找解壳软件，发现ILSpy可以解壳。然后找到关键代码

private void ‬​⁪‪⁭⁫‭⁯‭‌‎⁫‮‮‬‫⁪⁭⁮‫⁮‏‭‎‬‏‍‏‫‌‪⁭⁪⁮‭‍‌⁫‪‭‮(object obj, EventArgs eventArgs)
	{
		string s = this.‎⁯⁪‏⁮‬⁬‌⁪​⁮‭⁫‭‏⁫‫‌⁫‭⁭‫⁫‌⁯⁭⁪‭‏‮​⁭‬‍‍‬‏‮‮⁪‮.Text.ToString();
		byte[] bytes = Encoding.Default.GetBytes(s);
		string a = Convert.ToBase64String(bytes);
		string b = "UENURntFYTV5X0RvX05ldF9DcjRjazNyfQ==";
		if (a == b)
		{
			MessageBox.Show("注册成功！", "提示", MessageBoxButtons.OK);
		}
		else
		{
			MessageBox.Show("注册失败！", "提示", MessageBoxButtons.OK, MessageBoxIcon.Hand);
		}
	}

其实就是字符串Base64加密后为UENURntFYTV5X0RvX05ldF9DcjRjazNyfQ==，解密即可。


（3）DD - Hello
逆向后为：
 v2 = ((unsigned __int64)((char *)start - (char *)sub_100000C90) >> 2) ^ byte_100001040[0];
通过以下计算可知v2=49h
0C90
0CB0
0100 0001 41h
0000 1000 8h 
0100 1001 49h

关键源码：
  v1 = 0;
    while ( v1 < 55 )
    {
      byte_100001040[v1] -= 2;
      byte_100001040[v1] ^= v2;
      ++v1;
      ++v2;
    }

exp脚本：
b=0x100001040
v2=0x49
s=''
for i in range(55):
    s += chr((Byte(b+i)-2) ^ v2)
    v2 = v2 + 1
print(s)
    
