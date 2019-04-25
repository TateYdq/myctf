[Natas](http://overthewire.org/wargames/natas/)

1、
http://natas0.natas.labs.overthewire.org/
输入账号密码登录后，查看源代码：
The password for natas1 is gtVrDuiDfck831PqWsLEZy5gyDz1clto

2、
http://natas1.natas.labs.overthewire.org/
同样查看源代码：
The password for natas2 is ZluruAthQk7Q2MqmDeTiUij2ZvWy2mBi

3、
http://natas2.natas.labs.overthewire.org/
查看源码：
发现有个图片，还有个目录files
**敏感目录很重要**
打开后发现两个文件
点击users.txt得到密码：
```
alice:BYNdCesZqW
bob:jw2ueICLvT
charlie:G5vCxkVV3m
natas3:sJIJNW6ucpu6HPZ1ZAchaDtwd7oGrD14
eve:zo4mJWyNj2
mallory:9urtcpzBmH
```

4、
http://natas3.natas.labs.overthewire.org/
提示：
Not even Google will find it this time
联想robots.txt,网站通过robots协议告诉搜索引擎哪些页面可以爬取。
谷歌不能爬取，证明robots中定义了不能爬取

打开robots.txt

Disallow: /s3cr3t/

访问：
打开users.txt
发现：
natas4:Z9tkRkWmpt9Qr7XrR5jWRkgOU901swEZ

5、
Access disallowed. You are visiting from "" while authorized users should come only from "http://natas5.natas.labs.overthewire.org/" 
提示Referer头
请求头中加入：
Referer:http://natas5.natas.labs.overthewire.org/
结果：
Access granted. The password for natas5 is iX6IOfmpN7AYOQGPwtn3fXpbaJVJcHfq

6、
访问发现响应头中有：
Set-Cookie: loggedin=0
且响应Body中显示没登录
证明登不登录是根据cookie设置的（不安全）
请求头中加入
Cookie:loggedin=1
结果：
The password for natas6 is aGoY4q2Dc6MgDq4oL4YtoKtyAg9PeHa1
7、
