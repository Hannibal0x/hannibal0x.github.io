# NepNep Winter-CAMP（Misc合集）

<div class="has-toc have-toc">
</div>

## 0x00 前言 {.has-large-font-size}

从易到难的Misc大汇总，包含了很多常见的考点。

## 0x01 属性.jpg

右键搞定

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-54.png" alt="" class="wp-image-680" width="443" height="629" /></figure>
</div>

## 0x02 string.jpg

应该是考察strings命令，这里直接010打开，搜索Nep。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-55.png" alt="" class="wp-image-682" width="580" height="35" /></figure>
</div>

## 0x03 grep.jpg

应该是考察strings命令和grep的配合，上面同样的套路再来一遍。<figure class="wp-block-image size-large">

<img loading="lazy" width="729" height="40" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-56.png" alt="" class="wp-image-684" /> </figure> 

## 0x04 aaa.gif

明显看到GIF里插入了一张红色的图，Stegsolve逐帧分析。

flag{he11ohongke},但提交错误，有点儿懵。。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-57.png" alt="" class="wp-image-687" width="130" height="143" /></figure>
</div>

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-58.png" alt="" class="wp-image-688" width="133" height="147" /></figure>
</div>

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-59.png" alt="" class="wp-image-689" width="134" height="148" /></figure>
</div>

多次尝试后发现是`flag{hello hongke}`

## 0x05 lsb.jpg

stegslove查看lsb隐写，发现藏有图片，另存一下。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-60.png" alt="" class="wp-image-690" width="467" height="343" /></figure>
</div>

得到一个二维码，扫一下。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-61.png" alt="" class="wp-image-692" width="319" height="310" /></figure>
</div>

## 0x06 binwalk,foremost,dd.png

从名字可知要用到binwalk,foremost命令

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="843" height="212" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-62.png" alt="" class="wp-image-694" /></figure>
</div>

分离出图片

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-82.png" alt="" class="wp-image-768" width="182" height="177" /></figure>
</div>

`flag{Nepnep}`

## 0x07 上课认真听了吗？

先追踪udp流，得到`flag{254}`，再追踪http流。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="980" height="251" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-83.png" alt="" class="wp-image-770" /></figure>
</div>

得到`flag{340}`，追踪tcp流，在`tcp.stream eq 22`时，得到另一部分`flag{26}`。



## 0x08 pngcheck.png

先用png看一看，检查图片结构是否存在问题，发现在IDAT异常。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-84.png" alt="" class="wp-image-771" width="508" height="163" /></figure>
</div>

用代码解压一下。

<pre class="wp-block-code"><code>import zlib
s = '''
78 9C 4B CB 49 4C AF 4E 4B 36 32 4D 4E 4A 32 4F
B2 30 B5 34 B5 4C 4B 35 30 36 37 B6 30 32 31 4C
B4 34 4B 4A 33 32 4E A9 05 00 E9 E2 0B 5F D0 1C
68
'''
s = s.replace(' ','').replace('\n','')
b = bytes.fromhex(s)
flag = zlib.decompress(b)
print(flag)</code></pre>

`flag{fc25cbb7b85959fe03738241a96bf23d}`

## 0x09 westego4.3open (123456).bmp

使用wbs43open工具，输入密码。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-85.png" alt="" class="wp-image-776" width="417" height="277" /></figure>
</div>

得到`flag{我跟你讲，这个小甜瓜超甜der~}`

## 0x0A IHDR.png

IHDR块不对劲，CRC校验有问题。

<pre class="wp-block-code"><code>import os
import binascii
import struct

png= open("IHDR.png","rb").read()

for i in range(1024):
    data = png&#91;12:20] + struct.pack('&gt;i',i)+png&#91;24:29]
    crc32 = binascii.crc32(data) & 0xffffffff
    if crc32 == 0x1fcf9e8e:
        print (hex(i)&#91;2:])</code></pre>

更改高度为333

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-81.png" alt="" class="wp-image-763" width="306" height="405" /></figure>
</div>

又找了半天，结果发现提示说，flag包含nep，结果没想到flag是`flag{你发现了nep}`，行吧，俺想复杂了。

## 0x0B lsb（123456）.png

上神器。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-78.png" alt="" class="wp-image-754" width="511" height="376" /></figure>
</div>

发现文件头不对劲，找了下，发现题目可能类似这道题。<a rel="noreferrer noopener" href="https://blog.csdn.net/fuzz_nancheng/article/details/53384353" target="_blank" rel="nofollow" >https://blog.csdn.net/fuzz_nancheng/article/details/53384353</a>，下载<a rel="noreferrer noopener" href="https://github.com/livz/cloacked-pixel" data-type="URL" data-id="https://github.com/livz/cloacked-pixel" target="_blank" rel="nofollow" >cloacked-pixel</a>（Win10系统下无法使用，建议在kail使用）

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="783" height="52" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-79.png" alt="" class="wp-image-757" /></figure>
</div>

得到`flag{6e9fbfe27c40bbad06db30c42c04c4d6}`

## 0x0C bin.txt

打开是一大片01的二进制字符，通过CyberChef转换。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="1920" height="867" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-86.png" alt="" class="wp-image-780" /></figure>
</div>

得到一张图片。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-87.png" alt="" class="wp-image-782" width="182" height="323" /></figure>
</div>

## 0x0D 我是间谍

这题是间谍软件分析，运行后使用wireshark抓包，发现一条异常udp流。<figure class="wp-block-image size-large">

<img loading="lazy" width="1576" height="209" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-88.png" alt="" class="wp-image-787" /> </figure> 

打开后，显示`flag{11973526}`。

## 0x0E Stegsolve工具使用

上神器，发现二维码。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="642" height="177" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-107.png" alt="" class="wp-image-874" /></figure>
</div>

## 0x0F 监听消息

追踪Tcp流发现

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-109.png" alt="" class="wp-image-879" width="408" height="211" /></figure>
</div>

另存16进制字符，发现是png。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-110.png" alt="" class="wp-image-882" width="480" height="226" /></figure>
</div>

得到半截二维码，改高度。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="128" height="67" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-111.png" alt="" class="wp-image-883" /></figure>
</div>

得到完整的块儿后，贴个定位符。也可在<a rel="noreferrer noopener" href="https://merricx.github.io/qrazybox/" target="_blank" rel="nofollow" >https://merricx.github.io/qrazybox/</a>填充。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-113.png" alt="" class="wp-image-887" width="126" height="126" /></figure>
</div>

## 0x10 简单流量

**hint：关于ssl密钥导入：<a rel="noreferrer noopener" href="https://segmentfault.com/a/1190000018746027" target="_blank" rel="nofollow" >https://segmentfault.com/a/1190000018746027</a>**

按照提示配置环境变量和WireShark，因为pcapng文件名zstuctf，猜测此题flag也是zstuctf，过滤字符串，追踪tls流。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-114.png" alt="" class="wp-image-890" width="808" height="116" /></figure>
</div>

## 0x11 图片Base64编码

还原得到一张二维码，扫码得到flag。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-98.png" alt="" class="wp-image-844" width="177" height="177" /></figure>
</div>

## 0x12 Base编码

`LJWXQ2C2GN2EGTSIJZWFQ6SGPJMHUTTIMMZWW2DGKE6T2===`经过Base32解码得到`ZmxhZ3tCNHNlXzFzXzNhc3khfQ==`，再经过Base64解码得到`flag{B4se_1s_3asy!}`

## 0x13 zip伪加密<figure class="wp-block-image size-large">

<img loading="lazy" width="712" height="216" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-108.png" alt="" class="wp-image-876" /> </figure> 

改9为0，得到`flag{zip_is_funny!}`。

## 0x14 常见文件文件头补齐

PNG文件头`89 50 4E 47 0D 0A 1A 0A`，可以观察到，缺少了4个字节，补全。<figure class="wp-block-image size-large">

<img loading="lazy" width="653" height="73" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-116.png" alt="" class="wp-image-897" /> </figure> 

成功得到。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-117.png" alt="" class="wp-image-898" width="356" height="316" /></figure>
</div>

## 0x15 Morse编码

`..-. .-.. .- --. ----.-- .. .-.. --- ...- . -.-- --- ..- -----.-`转换得到`FLAG%u7bILOVEYOU%u7d`，`%u7b`就是`{`，`%u7d`就是`}`。`flag{ILOVEYOU}`

## 0x16 16进制查看

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="730" height="177" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-115.png" alt="" class="wp-image-896" /></figure>
</div>

## 0x17 二维码条形码

拼接扫码，得到`flag{winter_is_coming}`<figure class="wp-block-image size-large">

<img loading="lazy" width="558" height="160" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-118.png" alt="" class="wp-image-900" /> </figure> 

## 0x18 LSB图片隐写

可以看出藏了个压缩包，另存一下。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-120.png" alt="" class="wp-image-906" width="491" height="361" /></figure>
</div>

直接解压时失败，文件损坏，winrar修复后解压文件，搜索ctf字符。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="649" height="59" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/image-17.png" alt="" class="wp-image-999" /></figure>
</div>

## 0x19 电子文档隐写

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="238" height="58" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-119.png" alt="" class="wp-image-904" /></figure>
</div>

## 0x1A HTML实体编码

`\u66\u6c\u61\u67\u7b\u57\u33\u6c\u63\u30\u6d\u65\u21\u7d`通过ASCII转成`flag{W3lc0me!}`

## 0x1B 键盘密码

`ytfvbhn tgbgy hjuygbn yhnmki tgvhn uygbnjm uygbn yhnijm`对照键盘连线`areuhack`

## 0x1C Foremost && binwalk使用

使用binwalk和foremost<figure class="wp-block-image size-large">

<img loading="lazy" width="1079" height="245" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-121.png" alt="" class="wp-image-914" /> </figure> 

解压压缩包，得到`flag{ff17_is_funny!}`

## 0x1D LSB音频隐写

slienteye解码

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-122.png" alt="" class="wp-image-918" width="499" height="370" /></figure>
</div>

## 0x1E pyc反编译

在线反编译pyc，得到python代码。

<pre class="wp-block-code"><code>print 'Your input1 is your flag~'
l = len(input1)
code = &#91;]
for i in range(l):
    num = ((ord(input1&#91;i]) + i) % 128 + 128) % 128
    code += chr(num)

for i in range(l - 1):
    code&#91;i] = chr(ord(code&#91;i]) ^ ord(code&#91;i + 1]))

print code
code = &#91;'\x0b', '\x0e', '\t', '\x15', '0', '4', '\x01', '\x06', '\x14', '4', ',', '\x1b', 'U', '?', 'o', '6', '*', ':', '\x01', 'D', ';', '%', '\x13']</code></pre>

编写解码代码

<pre class="wp-block-code"><code>code = &#91;'\x0b', '\x0e', '\t', '\x15', '0', '4', '\x01', '\x06', '\x14', '4', ',', '\x1b', 'U', '?', 'o', '6', '*', ':', '\x01', 'D', ';', '%', '\x13']
l=len(code)
for i in range(l-2,-1,-1):
    code&#91;i]=chr(ord(code&#91;i])^ord(code&#91;i+1]))
for i in range(l):
                print(chr((ord(code&#91;i])-i)%128),end='')
</code></pre>

运行得到结果：`flag{Just_Re_1s_Ha66y!}`

## 0x1F zip口令爆破

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-124.png" alt="" class="wp-image-925" width="394" height="148" /></figure>
</div>

拿到`flag{zip_is_so_easy!}`

## 0x20 明文攻击

构造一个crc32值与压缩后文件大小一致的readme.txt，这里用一位师傅写的脚本，非常好用。

<pre class="wp-block-code"><code>from zlib import crc32
import random

char='0123456789'
def crc32_f(data):
    return hex(crc32(data)&0xffffffff)&#91;2:10]
length=input('length:')
crc32_=raw_input('crc32:').lower()

while True:
    text=''
    for i in range(length):
        text+=char&#91;random.randint(0,len(char)-1)]
    if crc32_f(text)==crc32_:
        raw_input('find it:'+text)
        exit</code></pre>



## 0x21 音频频谱隐写

用Audacity打开，显示频谱图。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="669" height="178" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/image.png" alt="" class="wp-image-933" /></figure>
</div>

## 0x22 MP3 隐写

爷青回，金刚葫芦娃可还行，文件是MP3，首先想到利用MP3Stege，但没有密码010打开后发现藏有东西，分离出jpg和zip。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/image-3.png" alt="" class="wp-image-940" width="517" height="162" /></figure>
</div>

压缩包是加密的，根据图片的提示，猜测密码是`GourdSmallDiamond`，解密MP3。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/image-2.png" alt="" class="wp-image-939" width="421" height="319" /></figure>
</div>

成功解开，打开1.mp3.txt，得到解压密码`j7v@8@8QUWG0FWU^`

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="810" height="282" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/image-4.png" alt="" class="wp-image-941" /></figure>
</div>

得到`MSTSEC{MSTSEC_DINGANN_KEY_IS_GSD}`，但通不过，改成flag即可。

## 0x23 音频波形隐写

用Audacity打开，显示波形图，发现异常，设高点为1，低点为0编码

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="1725" height="185" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/image-1.png" alt="" class="wp-image-936" /></figure>
</div>

得：`110011011011001100001110011111110111010111011000010101110101010110011011101011101110110111011110011111101`共105位，不能整除8，但能整除7，则以7个为一组分开，并且在最高位补0

得：`01100110 01101100 01100001 01100111 01111011 01010111 00110000 01010111 00101010 01100110 01110101 01101110 01101110 01111001 01111101`，转ASCII码得到flag。

## 0x24 流量分析(一)

直接搜索flag，结果出来一堆假flag，发现使用ftp协议传了两张图片，存一下。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/2.png" alt="" class="wp-image-958" width="285" height="190" /></figure>
</div>

发现第一张图片有缺陷，是第二张的部分，这里直接分析第二张。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/image-8.png" alt="" class="wp-image-959" width="347" height="232" /></figure>
</div>

多次尝试后发现是LSB隐写。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/image-9.png" alt="" class="wp-image-962" width="551" height="405" /></figure>
</div>

## 0x25 GIF图片隐写

补上文件头。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="648" height="38" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/image-10.png" alt="" class="wp-image-965" /></figure>
</div>

Stegslove打开逐帧查看,发现字符叠加，肉眼难以辨别，有师傅提到用工具Namo_GIF选择每一帧，然后编辑调色板，将第254帧改为同一个颜色，即可看清每一帧的内容，拼接得到`Y2F0Y2hfdGhlX2R5bmFtaWNfZmxhZ19pc19xdW10ZV9zaW1wbGU=`。

## 0x26 数字水印隐写

猜测是盲水印，需要找到另一张图片，pngcheck发现IEND后还有数据。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/image-5.png" alt="" class="wp-image-949" width="523" height="303" /></figure>
</div>

发现又有IHDRchunck块，导出，补全文件头，得到一张和原图一模一样的图。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/image-6.png" alt="" class="wp-image-951" width="520" height="287" /></figure>
</div>

运行`python bwm.py decode half.png half1.png wm.png`，得到：

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/image-7.png" alt="" class="wp-image-954" width="189" height="52" /></figure>
</div>

只有一半，找前半段。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="720" height="529" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/image-13.png" alt="" class="wp-image-980" /></figure>
</div>

## 0x27 python脚本使用(一)

用pngcheck发现高度有问题。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="636" height="133" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/image-15.png" alt="" class="wp-image-989" /></figure>
</div>

上python脚本爆破高度，得到`232`，再用pngcheck，发现异常数据。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="737" height="690" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/image-16.png" alt="" class="wp-image-991" /></figure>
</div>
找到数据，并进行zlib解压。

```
78 9C 5D 91 01 12 80 40 08 02 BF 04 FF FF 5C 75 29 4B 55 37 73 8A 21 A2 7D 1E 49 CF D1 7D B3 93 7A 92 E7 E6 03 88 0A 6D 48 51 00 90 1F B0 41 01 53 35 0D E8 31 12 EA 2D 51 C5 4C E2 E5 85 B1 5A 2F C7 8E 88 72 F5 1C 6F C1 88 18 82 F9 3D 37 2D EF 78 E6 65 B0 C3 6C 52 96 22 A0 A4 55 88 13 88 33 A1 70 A2 07 1D DC D1 82 19 DB 8C 0D 46 5D 8B 69 89 71 96 45 ED 9C 11 C3 6A E3 AB DA EF CF C0 AC F0 23 E7 7C 17 C7 89 76 67 D9 CF A5 A8 00 00 00 00
```



得到一串二进制代码，长度为625，想到画25X25的二维码，扫码得到flag。

```
from PIL import Image
from zlib import *

MAX = 25
pic = Image.new("RGB",(MAX,MAX))
str ="1111111000100001101111111100000101110010110100000110111010100000000010111011011101001000000001011101101110101110110100101110110000010101011011010000011111111010101010101111111000000001011101110000000011010011000001010011101101111010101001000011100000000000101000000001001001101000100111001111011100111100001110111110001100101000110011100001010100011010001111010110000010100010110000011011101100100001110011100100001011111110100000000110101001000111101111111011100001101011011100000100001100110001111010111010001101001111100001011101011000111010011100101110100100111011011000110000010110001101000110001111111011010110111011011"
i=0
for y in range(0,MAX):
    for x in range(0,MAX):
        if(str[i] == '1'):
            pic.putpixel([x,y],(0,0,0))
        else:pic.putpixel([x,y],(255,255,255))
        i = i+1
pic.save("flag.png")
```

## 0x28 内存取证

使用volatility，进行镜像分析，知道了系统。详细用法参考：<a href="https://www.cnblogs.com/jssi/p/13762308.html" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.cnblogs.com/jssi/p/13762308.html</a><figure class="wp-block-image size-large">

<img loading="lazy" width="806" height="269" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/image-11.png" alt="" class="wp-image-974" /> </figure> 

查看进程，发现可疑进程`TrueCrypt.exe`

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="942" height="471" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/image-12.png" alt="" class="wp-image-977" /></figure>
</div>

dump出来，`volatility -f mem.vmem --profile=WinXPSP2x86 memdump -p 2012 -D ./`2012为nc的进程号，./为保存的路径，用010打开文件，搜索ctf{。<figure class="wp-block-image size-large">

<img loading="lazy" width="644" height="77" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/image-14.png" alt="" class="wp-image-986" /> </figure>
