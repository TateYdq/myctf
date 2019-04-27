这部分讲下ctf中出现的利用特定软件漏洞可以达到某些目的的题：
# 一. FLASK模板注入(SSTI漏洞)

[漏洞环境搭建](https://github.com/vulhub/vulhub/tree/master/flask/ssti)

如何搭建writeup文件中已经有，不再赘述。

1.程序分析:
```
@app.route("/")
def index():
    name = request.args.get('name', 'guest')

    t = Template("Hello " + name)
    return t.render()
```
代码逻辑很简单：
将获取的值展现出来，由于没有过滤输入，所以可以被恶意利用。

2.漏洞尝试
正常尝试:
http://127.0.0.1:8000?name=123
结果Hello 123
http://127.0.0.1:8000/?name={{12*12}}
结果hello 114
看来真的执行了代码。
{{}}是jinja2模板里面的变量，告诉这个模板引擎变量的值从渲染模板时使用的数据中获取。
{% %}为jinja2中的控制结构
现在有三个目的看下能不能实现
第一，获取某特殊变量值
第二，查看目录下某文件的值
第三，getshell

3.漏洞利用
改下代码：
app.py:
```
from flask import Flask, request
from jinja2 import Template
import secret

app = Flask(__name__)
flag = secret.f1ag

@app.route("/")
def index():
    name = request.args.get('name', 'guest')
    t = Template("Hello " + name)
    return t.render()

if __name__ == "__main__":
    app.run()
```

首先补一波python知识:
```
__class__ python中的反射,返回变量的类型
__bases__ 返回父类的类型
__subclasses__() 获取所有子类集合
__globals__ 返回
```


现在尝试获取一些重要值