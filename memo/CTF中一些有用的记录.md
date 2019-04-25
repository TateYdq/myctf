# CTF中一些有用的记录

## 一.web

1.

MD5(string,True)值为' or '…    的字符串 ffifdyop

2.

0e开头的md5(string)

```
s878926199a
s214587387a
```

3.

sql注入万能密码(最好两种都试)：

```
' or '1'='
' or ''='
```


4.
[content-type对照表](http://tool.oschina.net/commons)
post类型:

- application/x-www-form-urlencoded 原生表单,类似于get提交请求
- multipart/form-data  特殊表单，常用于发送文件，有boundary边界
- application/json 消息主题是序列化的字符串，适合 RESTful 的接口
- text/xml 传输xml文件

5.
curl用法
curl url   #获取网页内容
参数:
- -X 用于指定数据发送方式，GET或者POST
- -d/--data 用于指定发送的数据，没有-X默认为POST类型
- --data-urlencode 对数据表单进行编码
- -I 只获取响应头
- -i 同时显示响应头和文件
- -A 自定义User-Agent
- -H/--header 自定义header头
- -c [filename] 保存cookie到文件
- -b [filename]|[strings] 从文件或字符串中读取cookie
- -L 自动跳转到要跳转的网址
- -v 显示一次通信的整个过程
- --trace 显示更详细通信信息

特殊方法:
上传文件：
curl --form upload=@[filename] --form [submit_name]=[submit_value] [URL]