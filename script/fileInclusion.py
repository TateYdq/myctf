#-*- coding:utf-8 -*-
from argparse import ArgumentParser
import requests

def isPageExists(url,true_length=None,false_length=None,encoding="utf-8"):
    rs = requests.get(url)
    if rs.status_code >= 300:
        return False
    content = rs.content.decode(encoding)
    # print("[len]:%d"%len(content))
    if true_length != None:
        if str(len(content)) in true_length:
            return True
    if false_length != None:
        if str(len(content)) in false_length:
            return False
    return True

def pageWalker(url,dirlist,true_length,false_length,unextension=''):
    f = open(dirlist,"r")
    lines = f.readlines()
    for item in lines:
        item = item.strip('\n')
        try:
            if '.' in item and unextension != '' and str(unextension) in item:
                item = item.split('.')[0]
            real_url = url.replace('(*)',item)
            # print(real_url)
            if isPageExists(real_url,true_length,false_length):
                print("[+]%s"%real_url)
        except Exception as e:
            print("error:%s"%str(e))
    f.close()

        

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-u', '--url', help='爆破的url,(*)为要爆破的地方', required=True)
    parser.add_argument('-dl', '--dirlist', help='字典', required=True)
    parser.add_argument('-ue', '--unextension',help='自动去掉的后缀', required=False)
    parser.add_argument('-tl', '--truelength',help='正确的长度',nargs='+',required=False)
    parser.add_argument('-fl', '--falselength',help='错误的长度',nargs='+',required=False)
    args = parser.parse_args()
    pageWalker(args.url,args.dirlist,args.truelength,args.falselength,args.unextension)