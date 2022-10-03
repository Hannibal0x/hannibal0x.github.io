# OverTheWire:Bandit

<div class="has-toc have-toc">
</div>
<a href="https://overthewire.org/wargames/" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://overthewire.org/wargames/</a>是一个学习linux命令的WarGame，通过闯关的模式，不断的学习新的命令，对于学习安全和Linux的朋友是一个很好的练习游戏。

## 0x00 Level0

用MobaXterm设置ssh连接<figure class="wp-block-image size-full">

<img loading="lazy" width="967" height="271" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片.png" alt="" class="wp-image-2217" /> </figure> 

输入`bandit0`密码登录<figure class="wp-block-image size-full">

<img loading="lazy" width="512" height="341" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-1.png" alt="" class="wp-image-2218" /> </figure> 

## 0x01 level0->level1

<figure class="wp-block-image size-full">

<img loading="lazy" width="333" height="76" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-2.png" alt="" class="wp-image-2222" /> </figure> 

## 0x02 level1-> level2

修改用户名为后，重新连接ssh，密码为`boJ9jbbUNNfktd78OOpsqOltutMc3MY1`。<figure class="wp-block-image size-full">

<img loading="lazy" width="334" height="80" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-3.png" alt="" class="wp-image-2225" /> </figure> 

## 0x03 level2-> level3

<figure class="wp-block-image size-full">

<img loading="lazy" width="473" height="82" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-4.png" alt="" class="wp-image-2227" /> </figure> 

## 0x04 level3-> level4

<figure class="wp-block-image size-full">

<img loading="lazy" width="544" height="206" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-5.png" alt="" class="wp-image-2229" /> </figure> 

## 0x05 level4-> level5

file命令可以用于辨识文件类型<figure class="wp-block-image size-full">

<img loading="lazy" width="889" height="362" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-6.png" alt="" class="wp-image-2231" /> </figure> 

## 0x06 level5->level6

Linux find 命令用来在指定目录下查找文件。

<pre class="wp-block-code"><code>Usage: find &#91;-H] &#91;-L] &#91;-P] &#91;-Olevel] &#91;-D debugopts] &#91;path…] &#91;expression]</code></pre>

一些参数说明

<pre class="wp-block-code"><code>-mount, -xdev : 只检查和指定目录在同一个文件系统下的文件，避免列出其它文件系统中的文件

-amin n : 在过去 n 分钟内被读取过

-anewer file : 比文件 file 更晚被读取过的文件

-atime n : 在过去n天内被读取过的文件

-cmin n : 在过去 n 分钟内被修改过

-cnewer file :比文件 file 更新的文件

-ctime n : 在过去n天内被修改过的文件

-empty : 空的文件-gid n or -group name : gid 是 n 或是 group 名称是 name

-ipath p, -path p : 路径名称符合 p 的文件，ipath 会忽略大小写

-name name, -iname name : 文件名称符合 name 的文件。iname 会忽略大小写

-size n : 文件大小 是 n 单位，b 代表 512 位元组的区块，c 表示字元数，k 表示 kilo bytes，w 是二个位元组。

-type c : 文件类型是 c 的文件。
d: 目录
c: 字型装置文件
b: 区块装置文件
p: 具名贮列
f: 一般文件
l: 符号连结
s: socket

-pid n : process id 是 n 的文件</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="501" height="83" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-7.png" alt="" class="wp-image-2233" /> </figure> 

## 0x07 level6->level7

<figure class="wp-block-image size-full">

<img loading="lazy" width="680" height="766" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-8.png" alt="" class="wp-image-2234" /> </figure> 

后查阅资料发现，报错可用`2>/dev/null`隐藏。Linux系统预留可三个文件描述符：0——标准输入（stdin）、1——标准输出（stdout）和2标准错误（stderr）。`>`是重定向。`/dev/null`是一个特殊的设备文件，这个文件接收到任何数据都会被丢弃。这个设备通常也被称为位桶（bit bucket）或黑洞。<figure class="wp-block-image size-full">

<img loading="lazy" width="577" height="41" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-9.png" alt="" class="wp-image-2238" /> </figure> 

## 0x08 level7->level8

<figure class="wp-block-image size-full">

<img loading="lazy" width="500" height="45" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-10.png" alt="" class="wp-image-2239" /> </figure> 

## 0x09 level8->level9

uniq参数

<pre class="wp-block-code"><code>-c或--count 在每列旁边显示该行重复出现的次数。

-d或--repeated 仅显示重复出现的行列。

-f&lt;栏位&gt;或--skip-fields=&lt;栏位&gt; 忽略比较指定的栏位。

-s&lt;字符位置&gt;或--skip-chars=&lt;字符位置&gt; 忽略比较指定的字符。

-u或--unique 仅显示出一次的行列。

-w&lt;字符位置&gt;或--check-chars=&lt;字符位置&gt; 指定要比较的字符。

--help 显示帮助。

--version 显示版本信息。</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="396" height="44" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-11.png" alt="" class="wp-image-2241" /> </figure> 

## 0x0A level9->level10

<figure class="wp-block-image size-full">

<img loading="lazy" width="473" height="105" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-12.png" alt="" class="wp-image-2243" /> </figure> 

## 0x0B level10->level11

<figure class="wp-block-image size-full">

<img loading="lazy" width="494" height="43" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-13.png" alt="" class="wp-image-2244" /> </figure> 

## 0x0C level11->level12

ROT13加密<figure class="wp-block-image size-full">

<img loading="lazy" width="598" height="41" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-14.png" alt="" class="wp-image-2246" /> </figure> 

## 0x0D level12->level13

`xxd [options] [infile [outfile]]` 

`xxd -r[evert] [options] [infile [outfile]]` 

xxd 命令用于用二进制或十六进制显示文件的内容，如果没有指定outfile参数，则把结果显示在屏幕上，如果指定了outfile则把结果输出到 outfile中；如果infile参数为 – 或则没有指定infile参数，则默认从标准输入读入。 

`-r` 逆向操作: 把xxd的十六进制输出内容转换回原文件的二进制内容。<figure class="wp-block-image size-full">

<img loading="lazy" width="1169" height="244" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-15.png" alt="" class="wp-image-2250" /> </figure> 

发现文件是gzip格式，mv为.gz文件后，`gzip -d`解压缩。<figure class="wp-block-image size-full">

<img loading="lazy" width="515" height="115" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-16.png" alt="" class="wp-image-2251" /> </figure> 

发现文件是bzip2格式，mv为.bz2文件后，`bzip2 -d`解压缩。 <figure class="wp-block-image size-full">

<img loading="lazy" width="1141" height="119" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-17.png" alt="" class="wp-image-2253" /> </figure> 

接着是嵌套的解压缩<figure class="wp-block-image size-full">

<img loading="lazy" width="1184" height="697" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-18.png" alt="" class="wp-image-2254" /> </figure> 

## 0x0E level13->level14

发现存在ssh的私钥文件。<figure class="wp-block-image size-full">

<img loading="lazy" width="218" height="45" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-19.png" alt="" class="wp-image-2257" /> </figure> 

<pre class="wp-block-code"><code>usage: ssh &#91;-1246AaCfGgKkMNnqsTtVvXxYy] &#91;-b bind_address] &#91;-c cipher_spec]
           &#91;-D &#91;bind_address:]port] &#91;-E log_file] &#91;-e escape_char]
           &#91;-F configfile] &#91;-I pkcs11] &#91;-i identity_file]
           &#91;-J &#91;user@]host&#91;:port]] &#91;-L address] &#91;-l login_name] &#91;-m mac_spec]
           &#91;-O ctl_cmd] &#91;-o option] &#91;-p port] &#91;-Q query_option] &#91;-R address]
           &#91;-S ctl_path] &#91;-W host:port] &#91;-w local_tun&#91;:remote_tun]]
           &#91;user@]hostname &#91;command]</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="908" height="527" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-20.png" alt="" class="wp-image-2258" /> </figure> 

## 0x0F level14->level15

<pre class="wp-block-code"><code>Usage: telnet &#91;-4] &#91;-6] &#91;-8] &#91;-E] &#91;-L] &#91;-a] &#91;-d] &#91;-e char] &#91;-l user]
        &#91;-n tracefile] &#91; -b addr ] &#91;-r] &#91;host-name &#91;port]]</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="426" height="189" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-21.png" alt="" class="wp-image-2261" /> </figure> 

## 0x10 level15->level16

s\_client为一个SSL/TLS客户端程序，与s\_server对应，它不仅能与s_server进行通信，也能与任何使用ssl协议的其他服务程序进行通信。使用命令`openssl s_client`远程连接。

<pre class="wp-block-code"><code>-connect host:port - who to connect to (default is localhost:4433)</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="643" height="311" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-23.png" alt="" class="wp-image-2266" /></figure> 

## 0x11 level16->level17

使用`nmap -sV localhost -p 31000-32000`，-sV 显示详情，-p指定端口。<figure class="wp-block-image size-full">

<img loading="lazy" width="368" height="132" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-24.png" alt="" class="wp-image-2268" /> </figure> 

发现两个可疑目标，开始测试ssl连接。得到一段ssh私钥文件。<figure class="wp-block-image size-full">

<img loading="lazy" width="659" height="584" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-25.png" alt="" class="wp-image-2269" /> </figure> 

提示权限问题<figure class="wp-block-image size-full">

<img loading="lazy" width="920" height="363" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-26.png" alt="" class="wp-image-2270" /> </figure> 

修改权限后再次连接，`chmod 600 ssh.priv`，

## 0x12 level17->level18

<figure class="wp-block-image size-full">

<img loading="lazy" width="524" height="142" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-27.png" alt="" class="wp-image-2273" /> </figure> 

## 0x13 level18->level19

无法直接使用密码登录。可以用命令直接读取文件。也可以使用`ssh bandit18@localhost -T`禁用伪终端方式登录。<figure class="wp-block-image size-full">

<img loading="lazy" width="918" height="323" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-28.png" alt="" class="wp-image-2277" /> </figure> 

## 0x14 level19->level20

id命令用于显示用户的ID，以及所属群组的ID。<figure class="wp-block-image size-full">

<img loading="lazy" width="842" height="461" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-29.png" alt="" class="wp-image-2278" /> </figure> 

## 0x15 level20->level21

nc是netcat的简写，可以用来取代telnet进行某些服务端口的检测工作。

服务端：`nc -l 端口号 > 文件名`  
客户端：`nc 主机的ip或域名 端口号 < 文件名`

<pre class="wp-block-code"><code>常用参数：
-l：用于指定nc将处于侦听模式。指定该参数，则意味着nc被当作server
-s：指定发送数据的源IP地址，适用于多网卡机
-u：指定nc使用UDP协议，默认为TCP
-v：输出交互或出错信息，新手调试时尤为有用
-w：超时秒数，后面跟数字
-z：表示zero，表示扫描时不发送任何数据</code></pre>

使用 `&` 号将下面这个命令放到后台运行<figure class="wp-block-image size-full">

<img loading="lazy" width="656" height="204" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-31.png" alt="" class="wp-image-2443" /> </figure> 

## 0x16 level21->level22

在LINUX中，周期执行的任务一般由cron这个守护进程来处理。cron读取一个或多个配置文件，这些配置文件中包含了命令行及其调用时间。cron的配置文件称为“crontab”，是“cron table”的简写。

在crontab文件中如何输入需要执行的命令和时间。该文件中每行都包括六个域，其中前五个域是指定命令被执行的时间，最后一个域是要被执行的命令。每个域之间使用空格或者制表符分隔。格式如下：&nbsp;  
`minute hour day-of-month month-of-year day-of-week commands&nbsp;`  
合法值 00-59 00-23 01-31 01-12 0-6 (0 is sunday)&nbsp;  
除了数字还有几个个特殊的符号就是"\*"、"/"和"-"、","，\*代表所有的取值范围内的数字，"/"代表每的意思,"/5"表示每5个单位，"-"代表从某个数字到某个数字,","分开几个离散的数字。<figure class="wp-block-image size-full">

<img loading="lazy" width="1217" height="243" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-32.png" alt="" class="wp-image-2446" /> </figure> 

## 0x17 level22->level23

<figure class="wp-block-image size-full">

<img loading="lazy" width="1222" height="379" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-33.png" alt="" class="wp-image-2448" /> </figure> 

## 0x18 level23->level24

<figure class="wp-block-image size-full">

<img loading="lazy" width="651" height="437" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-34.png" alt="" class="wp-image-2450" /> </figure> 

stat命令主要用于显示文件或文件系统的详细信息。

语法：`stat [option] file`

option参数说明：

<pre class="wp-block-code"><code>-L, --dereference 显示符号链接 
-f, --file-system 显示文件系统状态而不是文件状态
-c  --format=FORMAT 自定义输出格式，结尾有换行 
--printf=FORMAT
          如同 --format, 但是解释反斜杠转义，而不是
          输出强制性的换行符; 如果你想换行，
          在FORMAT中包含\n

-t, --terse 以简洁的形式打印信息
--显示此帮助并退出
--version 输出版本信息并退出</code></pre>

其中format可以自定义个数数组的有：

<pre class="wp-block-code"><code>%a     八进制表示的访问权限
%A     可读格式表示的访问权限
%b     分配的块数（参见 %B）
%B     %b 参数显示的每个块的字节数
%d     十进制表示的设备号
%D     十六进制表示的设备号
%f     十六进制表示的 Raw 模式
%F     文件类型
%g     属主的组 ID
%G     属主的组名
%h     硬连接数
%i     Inode 号
%n     文件名
%N     如果是符号链接，显示器所链接的文件名
%o     I/O 块大小
%s     全部占用的字节大小
%t     十六进制的主设备号
%T     十六进制的副设备号
%u     属主的用户 ID
%U     属主的用户名
%x     最后访问时间
%X     最后访问时间，自 Epoch 开始的秒数
%y     最后修改时间
%Y     最后修改时间，自 Epoch 开始的秒数
%z     最后改变时间
%Z     最后改变时间，自 Epoch 开始的秒数

针对文件系统还有如下格式选项：
%a     普通用户可用的块数
%b     文件系统的全部数据块数
%c     文件系统的全部文件节点数
%d     文件系统的可用文件节点数
%f     文件系统的可用节点数
%C     SELinux 的安全上下文
%i     十六进制表示的文件系统 ID
%l     文件名的最大长度
%n     文件系统的文件名
%s     块大小（用于更快的传输）
%S     基本块大小（用于块计数）
%t     十六进制表示的文件系统类型
%T     可读格式表示的文件系统类型</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="592" height="57" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-37.png" alt="" class="wp-image-2458" /> </figure> 

这里参考了大佬的博客，/var/spool/cron/ 这个目录下存放的是每个用户包括root的crontab任务，每个任务以创建者的名字命名，一般一个用户最多只有一个crontab文件。在/var/spool/bandit24目录下就可以运行bandit24的定时任务。

创建脚本，写入`cat /etc/bandit_pass/bandit24 > /tmp/bandit24pass`

## 0x19 level24->level25

<figure class="wp-block-image size-full">

<img loading="lazy" width="1509" height="42" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-38.png" alt="" class="wp-image-2463" /> </figure> 

做出字典，然后执行`nc localhost 30002 < 1.txt`

<pre class="wp-block-code"><code>for i in {1000..9999}
  do
    echo "UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ $i " &gt;&gt; 1.txt
  done</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="676" height="110" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-39.png" alt="" class="wp-image-2464" /> </figure> 

## 0x1A level25->level26

<figure class="wp-block-image size-full">

<img loading="lazy" width="221" height="40" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-40.png" alt="" class="wp-image-2466" /> </figure> 

发现存在密钥，执行`ssh -i bandit26.sshkey bandit26@localhost`，返回失败。

```
账号名称：即登陆时的用户名

密码：早期UNIX系统的密码是放在这个文件中的，但因为这个文件的特性是所有程序都能够读取，所以，这样很容易造成数据被窃取，因此后来就将这个字段的密码数据改放到/etc/shadow中了

UID：用户ID，每个账号名称对应一个UID，通常UID=0表示root管理员

GID：组ID，与/etc/group有关，/etc/group与/etc/passwd差不多，是用来规范用户组信息的

用户信息说明栏： 用来解释这个账号是干什么的

家目录：home目录，即用户登陆以后跳转到的目录，以root用户为例，/root是它的家目录，所以root用户登陆以后就跳转到/root目录这里

Shell：用户使用的shell，通常使用/bin/bash这个shell，这也就是为什么登陆Linux时默认的shell是bash的原因，就是在这里设置的，如果要想更改登陆后使用的shell，可以在这里修改。另外一个很重要的东西是有一个shell可以用来替代让账号无法登陆的命令，那就是/sbin/nologin。
```

<figure class="wp-block-image size-full">

<img loading="lazy" width="728" height="179" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-44.png" alt="" class="wp-image-2472" /> </figure> 

将终端对话框缩放小，这样可以自动执行more<figure class="wp-block-image size-full">

<img loading="lazy" width="552" height="176" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-42.png" alt="" class="wp-image-2470" /> </figure> 

在exit 0前，按v进入vim编辑模式，通过:e file，可以导入文件到编辑器内，执行

<pre class="wp-block-code"><code>:e  /etc/bandit_pass/bandit26</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="372" height="35" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-43.png" alt="" class="wp-image-2471" /> </figure> 

## 0x1B level26->level27

将终端对话框缩放小，以bandit26登录

<pre class="wp-block-code"><code>vim模式下
:set shell=/bin/sh
:sh</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="471" height="141" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-45.png" alt="" class="wp-image-2474" /> </figure> 

## 0x1C level27->level28 

<figure class="wp-block-image size-full">

<img loading="lazy" width="912" height="463" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-46.png" alt="" class="wp-image-2475" /> </figure> 

## 0x1D level28->level29

git clone后查看文件<figure class="wp-block-image size-full">

<img loading="lazy" width="337" height="325" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-48.png" alt="" class="wp-image-2479" /></figure> 

## 0x1E level29->level30

`git branch -a`查看分支，一般dev是development开发者的分支，`git checkout`切换分支<figure class="wp-block-image size-full">

<img loading="lazy" width="761" height="386" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-50.png" alt="" class="wp-image-2482" /></figure> 

## 0x1F level30->level31

`git show-ref`显示本地存储库中可用的引用以及关联的提交ID。<figure class="wp-block-image size-full">

<img loading="lazy" width="826" height="140" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-51.png" alt="" class="wp-image-2483" /> </figure> 

## 0x20 level31->level32

<figure class="wp-block-image size-full">

<img loading="lazy" width="566" height="207" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-56.png" alt="" class="wp-image-2490" /></figure> 

## 0x21 level32->level33

linux shell下的特殊用法及参数的说明：

<pre class="wp-block-code"><code>$$      Shell本身的PID（ProcessID）
$!      Shell最后运行的后台Process的PID
$?      最后运行的命令的结束代码（返回值）
$-      使用Set命令设定的Flag一览
$*      所有参数列表。如"$*"用「"」括起来的情况、以"$1 $2 … $n"的形式输出所有参数。
$@      所有参数列表。如"$@"用「"」括起来的情况、以"$1" "$2" … "$n" 的形式输出所有参数。
$#      添加到Shell的参数个数
$0      Shell本身的文件名
$1～$n  添加到Shell的各参数值。$1是第1参数、$2是第2参数…。</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="359" height="162" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-57.png" alt="" class="wp-image-2492" /> </figure> 

## 0x22 level33->level34

<figure class="wp-block-image size-full">

<img loading="lazy" width="473" height="130" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-58.png" alt="" class="wp-image-2494" /> </figure> 
