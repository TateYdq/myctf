1.urllib模块
1.1.urllib.quote()
进行url编码
按照标准， URL 只允许一部分 ASCII 字符（数字字母和部分符号），其他的字符（如汉字）是不符合 URL 标准的。所以URL中使用其他字符就需要进行URL编码。URL编码的方式把需要编码的字符传唤为%xx的方式，服务器在接受到url请求后，会自动进行一次解码
1.2.urllib.unquote()
进行url解码

2.optparse模块
parser.add_option() #增加参数，参数一:-+字符;参数二：--+名词;参数action，储存方式;参数type，代表输入参数的类型;参数dest，代表目标参数名字
option,args = parser.parser_args()  #解析所有参数


3.
utf-8转二进制:
binascii.b2a_hex


4.base64解密
base64.b64decode

5.md5加密
import hashlib
m1=hashlib.md5()
m1.update(str)
m1.hexdigest()

6.十六进制和字符串互转
python2:
.decode('hex')
.encode('hex')