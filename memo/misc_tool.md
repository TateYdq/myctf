# 1.mac端

## 1.1.自带命令
- file 查看文件类型
- grep 过滤
- xxd 查看文件的十六进制
- vim+xxd 按十六进制编辑文件 vim打开后用:%!xxd

- subl3+hexviewer 十六进制查看
-vscode + hexdump

- unzip  解压zip文件

- sips 处理图片命令
sips -s format [目标格式] --out [目标文件名] [输入文件] #转换格式
sips -r [度数] --out [目标文件名] [文件]  #顺时针旋转文件
sips -z [高度] [宽度] --out [目标文件名] [文件]  #调整大小
 


## 1.2 brew安装工具
提取隐藏文件
binwalk file  #识别文件

binwalk -e file #提取文件


## 1.2.1 imagemagick工具
查看图片信息

identify [文件名]  #显示基本信息
identify -verbose [文件名]  #打印图片全部信息

convert [src][dst]

convert -resize 高度（像素）x宽度（像素） 源文件 目标文件 #改变图片大小


## 1.2.2 foremost工具
分离文件工具

foremost [文件]

## 1.2.3 aircrack-ng 工具
wifi相关工具，可以用来爆破wifi密码

aircrack-ng [option] <input_file>
-a<amode> amode:1->WEP 2->WAP-PSK
-w 指定字典

## 1.2.4 crunch工具
   crunch <min> <max> [字符] [options] #min为字符串最小长度，max为最大长度，默认字符为26个小写字母，可以自己制定
    -s     指定一个开始的字符，即从自己定义的密码xxxx开始
    -t     指定密码输出的格式

     %      代表数字
     ^      代表特殊符号
     @      代表小写字母
     ,      代表大写字符   


## 1.2.5 stegsolve  图片查看器


# 2.windows端

## 2.1. 下载工具

RouterPassView 查看路由器配置信息工具



# 3.linux端（除mac外工具）

# 4.各种信息

## 4.1. 各种文件头

参考：https://ctf-wiki.github.io/ctf-wiki/misc/picture/png/


## 4.1.1 png

1. 文件头8950 4E47 0D0A 1A0A
2. 关键数据块
    - IHDR(0000 000d 4948 4452) 第一块 文件头数据块，包含有png文件中存储的图像数据的基本信息，由13字节组成，前八个字节分别是宽高（像素为单位）

3. 辅助数据块

每个数据库都有统一数据结构，由4部分组成：
（1）长度  4字节 数据块中数据块数据的长度
（2）数据块类型  4字节 eg.IHDR
 (3) 数据块数据 可变长度
 (4) 循环冗余检测 4字节  
