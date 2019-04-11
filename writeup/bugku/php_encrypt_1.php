<?php
function decrypt($str)
{
    $char = $data = '';
    $str = base64_decode($str);
    $key = md5('ISCC');#729623334f0aa2784a1599fd374c120d
    $x = 0;
    $len = strlen($str);
    $klen = strlen($key);#32
    for ($i=0; $i < $len; $i++) {
        if ($x == $klen)
        {
            $x = 0;
        }
        $char .= $key[$x];
        $x+=1;
    }

    for ($i=0; $i < $len; $i++) {
        $data .= chr((128 + ord($str[$i]) - ord($char[$i])) % 128);
    }
    echo $data;
    return $data;
}
$str = "fR4aHWwuFCYYVydFRxMqHhhCKBseH1dbFygrRxIWJ1UYFhotFjA=";
decrypt($str)
?>