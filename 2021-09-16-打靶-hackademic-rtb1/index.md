# 打靶-Hackademic: RTB1



<div class="has-toc have-toc">
</div>

## 0x00 准备工作

Description里面有一条信息，After all, try to read the contents of the file 'key.txt' in the root directory.VMware提示选择“我已移动该虚拟机”，设置NAT后重启。

## 0x01 key.txt

通过二层地址发现靶机的三层IP地址，nmap扫描发现只开放了80端口，这应该是一台web漏洞的靶机。<figure class="wp-block-image size-full">

<img loading="lazy" width="735" height="349" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-93.png" alt="" class="wp-image-3731" /> </figure> 

浏览器访问页面<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-94.png" alt="" class="wp-image-3732" width="656" height="384" /> </figure> 

点击超链接跳转，站内链接给出了目标，与描述一致。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-95.png" alt="" class="wp-image-3733" width="574" height="348" /> </figure> 

点击`Uncategorized`，url为`http://192.168.92.133/Hackademic_RTB1/?cat=1`，怀疑存在SQL注入。输入'，确实报错。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-97.png" alt="" class="wp-image-3735" width="674" height="361" /> </figure> 

SqlMap一把梭，得到数据库。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-98.png" alt="" class="wp-image-3736" width="239" height="94" /> </figure> 

进一步获取表，字段，最后得到如下的账号密码，最后一个密码的md5在线解密后得到PUPPIES。<figure class="wp-block-image size-full">

<img loading="lazy" width="617" height="238" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-104.png" alt="" class="wp-image-3744" /> </figure> 

dirsearch找到 wordpress 的后台。<figure class="wp-block-image size-full">

<img loading="lazy" width="957" height="350" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-100.png" alt="" class="wp-image-3739" /> </figure> 

开始登录权限最高的用户，进行测试。<figure class="wp-block-image size-full">

<img loading="lazy" width="383" height="296" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-101.png" alt="" class="wp-image-3740" /> </figure> 

然后到Options->Miscellaneous可以设置Allow File Uploads，并在Allowed file extensions添加php。<figure class="wp-block-image size-full">

<img loading="lazy" width="1032" height="546" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-107.png" alt="" class="wp-image-3747" /> </figure> 

利用kali自带的webshell,`/usr/share/webshells/php-reverse-shell.php`。

<pre class="wp-block-code"><code>cp /usr/share/webshells/php/php-reverse-shell.php .

vim php-reverse-shell.ph
#修改ip</code></pre>

上传木马成功<figure class="wp-block-image size-full">

<img loading="lazy" width="598" height="213" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-109.png" alt="" class="wp-image-3750" /> </figure> 

监听目标端口，浏览器访问给出的路径地址。id发现此时的权限为apache的权限，需要进一步提权，`uname -a`显示电脑以及操作系统的内核的全部信息。<figure class="wp-block-image size-full">

<img loading="lazy" width="848" height="366" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-110.png" alt="" class="wp-image-3751" /> </figure> 

“searchsploit”是一个用于Exploit-DB的命令行搜索工具，可以帮助我们查找渗透模块。构造`searchsploit 2.6.3 | grep "Local Privilege Escalation"`搜索提权的exp。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-118.png" alt="" class="wp-image-3768" width="986" height="196" /> </figure> 

复制15285.c到网页存储位置，开启apache服务。<figure class="wp-block-image size-full">

<img loading="lazy" width="680" height="31" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-119.png" alt="" class="wp-image-3769" /> </figure> 

下载exp，并编译运行。<figure class="wp-block-image size-full">

<img loading="lazy" width="607" height="508" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-120.png" alt="" class="wp-image-3771" /> </figure> 

成功读取到内容<figure class="wp-block-image size-full">

<img loading="lazy" width="1037" height="372" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-121.png" alt="" class="wp-image-3772" /> </figure>
