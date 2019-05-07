# 1.啊哒
解压后是个图像，binwalk -e 后发现是个压缩包，需要密码解压
用indentify -verbose  发现图像中有可疑字符串
exif:Model: 73646E6973635F32303138
将73646E6973635F32303138十六进制转ascii码得sdnisc_2018即为所求密码
解压后得到flag


# 2.又是一张图片还单纯吗？
同样下载后先用binwalk查看，发现又隐藏文件了
且binwalk -e 不能打开
用foremost 打开，在output下有两个图片.查看图片发现有flag

# 3.宽带信息泄露
发现是bin文件，应该是路由器的配置文件。用RoutePassView打开，发现有一些敏感信息，包括device password,Username,Password

题目提示宽带账号，所以直接将账号放进flag{}里就可以。

# 4.多种方法解决
下载后发现是个压缩包解压后是KEY.exe，通过File命令查看发现是个text文件
vim打开发现是个加密的图片格式。
网上搜索在线bas64还原图片
eg.http://tool.chinaz.com/tools/imgtobase
得到一张二维码，扫描后得到flag


# 5.白哥的格子
下载图片后用xxd打开，发现结尾比较有意思
fg2ivyo}l{2s3_o@aw__rcl@ 共24位
重新组合下
fg2ivyo}
l{2s3_o@
aw__rcl@
看见flag出现：
flag{w22_is_v3ry_cool}

# 6.隐写3
下载后是个zip文件，解压后发现是张图片
file和binwalk命令查看后发现没什么问题


打开图片发现打不开，猜想图片被改动过

用xxd查看发现宽是02a7，高是0100,将宽高改为一样试试.
然后发现在mac怎么都打不开
放进windows打开就能看到flag

# 7.爆照
下载图片后binwalk试下
发现里面有个压缩包，需要密码打开，但是直接用unzip解压可以解压
出现8个文件

file * 下发现5个bitmap，3个jpg文件

打开8个文件看，发现88文件存在个二维码，扫描后是bilibili,提交发现不正确
看下题目提示flag{xxx_xxx_xxx}，证明需要有三个flag

用file的时候发现一个问题：
5个bitmap都是同样的 PC bitmap, Windows 3.x format, 303 x 300 x 8
而三个jpg文件都不相同:

88 303x300
888 303x299
8888 293x303 

可以发现888和8888都被压缩了，都改为303x303试试,发现没用

binwalk 8*所有试试

发现8888中隐藏了压缩包
foremost提取，然后unzip解压后出现个文件，扫描后得到panama，接下来找最后个flag

再看888图片，放在windows环境下，加上后缀.jpg查看图片，发现没有二维码，右键属性备注处出现base64编码c2lsaXNpbGk=
解码后得到：silisilb，提交不对

三个flag排列组合下提交

flag{bilibili_silisili_panama}
（按88，888,8888的顺序即可）


# 8.想蹭网先破解wifi密码
下载后得到一个数据包，发现被加密的。
题目提示破解wifi密码，看来是用aircrack-ng爆破。
而且题目提示密码为手机号，为了不为难你，大佬特地让我悄悄地把前七位告诉你 1391040**
所以看来后面四位都是数字

crunch 11 11 0123456789  -t "1391040%%%%" > pass.txt
aircrack-ng -w pass.txt wifi.cap
选择有握手包那个
得到密码13910407686
