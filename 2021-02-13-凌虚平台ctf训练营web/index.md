# 凌虚平台CTF训练营（Web）


## 0x00 前言

菜狗想打CTF。

## 0x01 hash attack

进入环境，给出了代码。

```php
<?php
echo "已知一组role为admin，salt长度为4，hash为c7813629f22b6a7d28a08041db3e80a9,想要扩展的字符串是joychou"."<br>";
$flag = "**********";
$role = $_REQUEST["role"];
$hash = $_REQUEST["hash"];
$salt = "***********"; //The length is 4

if ($hash !== md5($salt.$role)){
    echo 'wrong!';     
    exit;
}

if ( $role == 'admin'){
    echo 'no no no !, hash cann\'t be admin';
    exit;
}

//echo "You are ".$role.'</br>';
echo 'Congradulation! The flag is'.$flag;

?> wrong!
```

先把hash值解一下，得到`memeadmin`,salt的值应该就是meme，想要扩展的字符串是`joychou`，构造role=`adminjoychou`，在填上salt，进行md5加密，得到`189a928b5a79d07b96d464fb188eddc1`，在HackBar上构造url，成功拿到flag。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-90.png" alt="" class="wp-image-798" width="462" height="278" /></figure>
</div>

## 0x02 后台管理系统

现在SKCTF管理系统注册一个用户，登录出现提示。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="292" height="34" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-172.png" alt="" class="wp-image-1254" /></figure>
</div>

在注册页面注册admin，提示如下：

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="144" height="34" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-173.png" alt="" class="wp-image-1256" /></figure>
</div>

可以得到管理员的用户名为admin，这里需要用到sql约束攻击，数据库建表时约束了字段的长度，例如username如果约束长度是2的话，输入超长的长度是只会保留约束长度的。构造一个用户名为`admin` 且密码符合规范的用户，数据库只会存入admin，相当于存入了一个与admin的同名用户，而密码则是我们注册时所设定的密码。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-174.png" alt="" class="wp-image-1259" width="480" height="33" /></figure>
</div>

## 0x03 成绩单

一看就知道是sql注入，`1' order by 4#`时能够正常显示，`1' order by 5#`时无法显示，得出列数为4，下面猜解数据库名，输入`-1' union select 1,database(),3,4#`，成功得到web1。<figure class="wp-block-image size-large is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-175.png" alt="" class="wp-image-1265" width="710" height="104" /> </figure> 

再来猜解表名，输入`-1' union select 1,(select group_concat(table_name) from information_schema.tables where table_schema=database()),3,4#`，得到fl4g。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-176.png" alt="" class="wp-image-1271" width="279" height="75" /></figure>
</div>

根据fl4g表来查询列名，输入`-1' union select 1,(select group_concat(column_name) from information_schema.columns where table_name='fl4g'),3,4#`。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-177.png" alt="" class="wp-image-1275" width="288" height="86" /></figure>
</div>

取出flag的值，输入-`1' union select 1,(select flag from fl4g),3,4#`

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="841" height="101" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-178.png" alt="" class="wp-image-1280" /></figure>
</div>

## 0x04 这里有几首歌

先把两首歌下载到本地进行音频分析，没有什么异常。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-179.png" alt="" class="wp-image-1283" width="360" height="129" /></figure>
</div>

分析源代码发现下载链接为`download.php?url=目标文件的base64编码`，可以利用此漏洞进行任意文件下载。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="801" height="74" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-181.png" alt="" class="wp-image-1287" /></figure>
</div>

download.php的base64编码为`ZG93bmxvYWQucGhw`，尝试下载分析源码，发现了好东西。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="1040" height="448" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-182.png" alt="" class="wp-image-1290" /></figure>
</div>

hereiskey.php的base64加密为`aGVyZWlza2V5LnBocA==`，下载到本地，得到flag。

## 0x05 warmup

有个hint，点开后发现了有意思的东西，想到phpmyadmin 4.8.1任意文件包含漏洞，通过目录穿越包含任意文件，在url后添加`%253f/../../../../../../../../../ffffllllaaaagggg`。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="754" height="135" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-183.png" alt="" class="wp-image-1296" /></figure>
</div>

## 0x06 shop

题目购买flag需要21元，可是余额只有20元，因此使用条件竞争购买，抓包，发送到intrude，清空变量，设置payload为Null payload ，发包数量为10000，线程数为25，开始攻击。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-184.png" alt="" class="wp-image-1309" width="476" height="270" /></figure>
</div>

## 0x07 前女友

点开链接，得到

<pre class="wp-block-code"><code>&lt;?php
if(isset($_GET&#91;'v1']) && isset($_GET&#91;'v2']) && isset($_GET&#91;'v3'])){
    $v1 = $_GET&#91;'v1'];
    $v2 = $_GET&#91;'v2'];
    $v3 = $_GET&#91;'v3'];
    if($v1 != $v2 && md5($v1) == md5($v2)){
        if(!strcmp($v3, $flag)){
            echo $flag;
        }
    }
}
?&gt;</code></pre>

构造三个参数，v1和v2利用md5函数的特性，使用一个不可md5的数据类型传入的话那么md5函数将返回false,可以用两个值不同但不可md5的数据类型，v3利用strcmp函数的特性，如果出错，那么返回值是0，和字符串相等时返回值一致。构造`?v1[]=1&v2[]=2&v3[]=3`。

## 0x08 uploading

分析代码，name和password可以利用sha1的特性，使用不可处理的数据类型来绕过，设置payload为：`?name[]=1&password[]=2&file=upload.php`

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-186.png" alt="" class="wp-image-1311" width="490" height="382" /></figure>
</div>

又得到一片代码，展现了过滤的规则。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-187.png" alt="" class="wp-image-1315" width="559" height="702" /></figure>
</div>

## 0x09 排好队 绕过去

题目就是md5(uname)===md5(passwd)，这里直接上数值就完事了，`?uname[]=1&passwd[]=2`。
