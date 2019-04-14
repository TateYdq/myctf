import requests
from bs4 import BeautifulSoup
def parser():
    url="http://120.79.1.69:10005/index.php?check"
    username = "goodboy_g-60Hellowoorr"
    password = "ajahas&&*44askldajaj"
    ss = requests.session()
    payload={"username":username,"password":password,"code":""}
    content = ss.post(url,data=payload).content.decode("utf-8")
    bs=BeautifulSoup(content,"html.parser")
    rep = bs.find(attrs={"class":"rep"}).string
    print(rep)
    strs = rep.replace("（","(").replace("）",")").replace("X","*")
    code = int(eval(strs))
    payload["code"]=code
    content = ss.post(url,data=payload).content.decode("utf-8")
    print(content)

def decry_passwd(dictionary):
    strs = ''
    i = 1
    while i <= len(dictionary):
        strs = strs + dictionary[i-1]
        i = i + (i % 5)
    #print(strs)
    return strs

def decrypt():
    dictionary = "VmxSS05HSXhXbkpOV0VwT1YwVmFWRll3Wkc5VVJsbDNWMnhhYkZac1NqQlpNRll3VlRBeFNWRnNjRmRpUmtwSVZsY3hSMk14V2xsalJsSnBVakpvV0ZaR1dsWmxSbHBYWWtSYVZtRjZWbGRVVmxwelRrWmFTR1ZHWkZSaGVrWlhWR3hTVjFZeVJuSlhiRUpYWVRGYVYxcFhlRkprTVZaeVkwZHNVMDFWY0ZkV2JURXdWREZSZUZkcmFGVmlhelZvVlcxNFMxWXhjRlpXVkVaUFlrYzVObGt3VmpCWFJrcHpWbXBTVjFadFVqTldiWE4zWkRKT1IySkdaRmRTVm5CUVZtMTBhMVJyTVVkVmJrcFZZa2RTVDFac1VsZFdNVlY0Vld0a1ZVMXNXbGhXTVdodlZsZEtSMU5yWkZWV1JVVXhWV3hhWVZkSFZraGtSbVJUWWtoQ1JsWnJaRFJWTWtaMFUydG9WbUpHV2xoV01HUnZWVVp3V0UxWGNHeFdhelY2V1ZWYVlWUnNXbkpYYm1oWFlrWktVRlY2Um10U01WcFpZVVpXVjJKRmNIaFdSM1JXVFZVd2QyTkdWbFZoTVZwTVZtdFZNVkpuSlRORUpUTkU="
    dictionary = decry_passwd(dictionary)
    dictionary = decry_passwd(dictionary)
    print(dictionary)

decrypt()