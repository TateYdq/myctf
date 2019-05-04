# sqlmap指南
- -u 指定网址
- -r 从文件中加载http请求
- --data 数据以post方式提交
- --cookie 指定cookie
- --level 指定等级
- --threads 指定线程数
- --random-agent 随机agent头（很有用）
>= 2时会测试http cookie
>= 3时会测试User-Agent 和Referer

- --risk 风险等级
  - 1（默认） 会测试大部分语句
  - 2 增加基于事件的测试语句
  - 3 增加OR语句的SQL注入测试

- --technique 指定注入的技术
  - B 布尔型注入
  - E 报错型注入
  - U 联合查询型注入
  - T 基于时间延迟注入

- --dbms 列举数据库
- --tamper
指定脚本
- -p 手动指定要测试的参数

- --referer 伪造referer
- --headers 伪造请求头

- --dbs 枚举数据库名
- --tables 列举表名
- -T 指定表名
- --columns 列举列名
- -C 指定列名
- --schema  列举schema
- --dump 输出表
- --dump-all 导出所有表


页面比较参数：
- --string 正确的字符串
- --not-string 错误字符串
- --regexp  正确的正则表达式
- --code 响应码

--auth-type,--auth-cred http认证.

eg.--auth-type Basic --auth-cred "testuser:testpass"










参考:
https://www.waitalone.cn/sqlmap-users-manual.html
https://www.freebuf.com/sectool/164608.html