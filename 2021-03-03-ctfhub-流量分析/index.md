# CTFHub-流量分析

<div class="has-toc have-toc">
</div>

## 0x00 前言

菜鸡记录汇总下流量分析的学习过程。

## 0x01 MySQL流量

用wireshark打开文件进行分析。

首先观察到，用户进行了登录的尝试操作，成功后查询信息等。<figure class="wp-block-image size-large">

<img loading="lazy" width="244" height="65" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/image-1.png" alt="" class="wp-image-1895" /> </figure> 

追踪tcp流，发现flag。<figure class="wp-block-image size-large">

<img loading="lazy" width="1250" height="614" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/image.png" alt="" class="wp-image-1894" /> </figure> 

## 0x02 Redis流量

Redis 是完全开源的，遵守 BSD 协议，是一个高性能的 key-value 数据库。

打开文件后，直接开始追踪tcp流。修改整个对话后，我们能看到用户对redis的操作，例如info返回关于 Redis 服务器的各种信息和统计数值等等，也可以发现SET的flag值。<figure class="wp-block-image size-large">

<img loading="lazy" width="228" height="759" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/image-2.png" alt="" class="wp-image-1901" /> </figure> 

## 0x03 MongoDB流量

MongoDB 是一个基于分布式文件存储的数据库。由 C++ 语言编写。旨在为 WEB 应用提供可扩展的高性能数据存储解决方案。MongoDB 是一个介于关系数据库和非关系数据库之间的产品，是非关系数据库当中功能最丰富，最像关系数据库的。

追踪流，发现用户在执行ismaster、showPrivileges等命令，慢慢往下看。发现插入了flag的文档。<figure class="wp-block-image size-large">

<img loading="lazy" width="969" height="95" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/image-3.png" alt="" class="wp-image-1906" /> </figure> 

## 0x04 Data

题目：ping 也可以携带数据?

打开wireshark，发现每个响应包的data字段有一个字节不对劲。<figure class="wp-block-image size-large">

<img loading="lazy" width="200" height="432" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/image-4.png" alt="" class="wp-image-1910" /> </figure> 

把所有的拼接在一起，得到`ctfhub{c87eb99796406ac0b}`。

## 0x04 Length

题目：ping 包的大小有些奇怪<figure class="wp-block-image size-large">

<img loading="lazy" width="734" height="431" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/image-5.png" alt="" class="wp-image-1916" /> </figure> 

将所有ICMP数据包的Length字段取出来，转换为ASCII码值，即可得到`ctfhub{acb659f023}`

## 0x05 LengthBinary

题目：ping 包的大小有些奇怪

打开后发现响应包的length只有106和74两种，根据题目binary可知，代表了0和1的二进制。<figure class="wp-block-image size-large">

<img loading="lazy" width="747" height="195" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/image-6.png" alt="" class="wp-image-1918" /> </figure> 

可以手动处理，也可以借助脚本。

<pre class="wp-block-code"><code>import subprocess
a=subprocess.check_output("tshark.exe -r icmp_len_binary.pcap -Y icmp.type==8 -T fields -e data.len")
b=a.split()
s=""
res=""
for i in b:
if b'64' in i:
s=s+"1"
if b'32' in i:
s=s+"0"
if len(s) ==8:
res=res+chr(int(s,2))
s=""
print("result:"+res)</code></pre>
