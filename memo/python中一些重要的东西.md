1.urllib模块
1.1.urllib.quote()
进行url编码
按照标准， URL 只允许一部分 ASCII 字符（数字字母和部分符号），其他的字符（如汉字）是不符合 URL 标准的。所以URL中使用其他字符就需要进行URL编码。URL编码的方式把需要编码的字符传唤为%xx的方式，服务器在接受到url请求后，会自动进行一次解码
1.2.urllib.unquote()
进行url解码

2.optparse模块

from optparse import OptionParser
parser = OptionParser()
parser.add_option() #增加参数，参数一:-+字符;参数二：--+名词;参数action，储存方式;参数type，代表输入参数的类型;参数dest，代表目标参数名字
option,args = parser.parser_args()  #解析所有参数

3.转义字符相关:
字符串默认会经过转义，想要里面的所有字符都不经过转义用原始字符串，即在字符串前面加个r,r“str”

三个引号也可以定义字符串，其中所有的引号，换行符，制表符等特殊字符都被认为是普通字符

4.编码相关
u'str' 代表unicode编码，python3默认使用unicode格式编码,文本打开默认为ascii编码
字符串带有encode和decode函数，包括utf-8等格式


5.正则匹配


p1 = re.compile(pattern)  //pattern为正则表达式,返回的p1为定义的正则规则
m1 = p1.match(string)   //string为要匹配的语句,返回的m1为找到的表达式