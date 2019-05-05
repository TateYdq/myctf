1.常量
__FILE__ 返回文件的完整路径+文件名
__DIR__ 返回文件目录

2.目录相关函数
scandir()
列出指定路径中的文件和目录
dirname()
返回目录中的路径部分

3.文件相关
file()
将目录读入一个数组,可以用var_dump(输出)
file_get_contents()
将整个文件读入一个字符串，可以用printf_r或者echo输出


4.打印函数

print()  #只能打印出简单类型变量
print_r() #可以打印出复杂类型变量，包括对象，数组等
echo  #输出一个或多个字符串
var_dump() 输出变量的类型或字符串的内容，常用来调试



5.转义函数

htmlentities  把指定要转换的字符转为html实体（&#xxx）
addslashes<>stripslashes   添加和删除反斜杠