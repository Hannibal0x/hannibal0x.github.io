# CTF练习Week2



<div class="has-toc have-toc">
</div>

## 0x00 [UTCTF2020]file header

修改文件头，得到flag<figure class="wp-block-image size-full">

<img loading="lazy" width="1338" height="267" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片.png" alt="" class="wp-image-5383" /> </figure> 

## 0x01 [GKCTF 2021]excel 骚操作

点击发现，有的空白格上的数值是1。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-1.png" alt="" class="wp-image-5384" width="264" height="124" /> </figure> 

设置单元格式，显示出所有的1<figure class="wp-block-image size-full">

<img loading="lazy" width="3070" height="924" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-2.png" alt="" class="wp-image-5385" /> </figure> 

然后设置突出显示，得到汉信码，扫描得到flag。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-4.png" alt="" class="wp-image-5387" width="392" height="335" /> </figure> 

## 0x02 [湖南省赛2019]Findme

tweakpng分析1.png发现chunk处存在问题<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-5.png" alt="" class="wp-image-5388" width="522" height="154" /> </figure> 

用010分析发现缺少IDAT的标识，手动添加一下。<figure class="wp-block-image size-full">

<img loading="lazy" width="850" height="112" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-6.png" alt="" class="wp-image-5390" /> </figure> 

脚本爆破宽高<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-7.png" alt="" class="wp-image-5391" width="585" height="554" /> </figure> 

<pre class="wp-block-code"><code>import zlib
import struct

filename = '1.png'
with open(filename, 'rb') as f:
    all_b = f.read()
    crc32key = int(all_b&#91;29:33].hex(),16)
    data = bytearray(all_b&#91;12:29])
    n = 4095           
    for w in range(n):          
        width = bytearray(struct.pack('&gt;i', w))    
        for h in range(n):
            height = bytearray(struct.pack('&gt;i', h))
            for x in range(4):
                data&#91;x+4] = width&#91;x]
                data&#91;x+8] = height&#91;x]
            crc32result = zlib.crc32(data)
            if crc32result == crc32key:
                print("宽为：",end="")
                print(width)
                print("高为：",end="")
                print(height)</code></pre>

得到<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-8.png" alt="" class="wp-image-5393" width="174" height="347" /> </figure> 

放到stegslover里面，在bule2时发现二维码，扫描得到`ZmxhZ3s0X3`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-9.png" alt="" class="wp-image-5394" width="229" height="478" /> </figure> 

在2.png的文件尾发现7z的字样，提取出来，而后发现PK被修改成7z，解压得到1000个txt。<figure class="wp-block-image size-full">

<img loading="lazy" width="1366" height="376" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-10.png" alt="" class="wp-image-5395" /> </figure> 

大小排序得到隐藏信息`1RVcmVfc`<figure class="wp-block-image size-full">

<img loading="lazy" width="1354" height="294" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-11.png" alt="" class="wp-image-5396" /> </figure> 

3.png的每一个chunk的crc32都是一个字符的ascii编码，得到`3RlZ30=`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-12.png" alt="" class="wp-image-5398" width="478" height="305" /> </figure> 

4.png和5.png直接用010查看即可<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-14.png" alt="" class="wp-image-5400" width="241" height="82" /></figure> 

按照P1-P5-P4-P2-P3拼接得到`ZmxhZ3s0X3Yzcllfc0lNcExlX1BsY1RVcmVfc3RlZ30=`，解码得到flag。

## 0x03 我爱Linux

图片FFD9后存在冗余数据，导出另存为。<figure class="wp-block-image size-full">

<img loading="lazy" width="1341" height="320" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-15.png" alt="" class="wp-image-5402" /> </figure> 

看了wp才知道得到的文件内容是Python Picke序列化内容，直接用脚本提取

<pre class="wp-block-code"><code>import pickle  
fp = open("123.txt","rb+")
fw = open('pickle.txt', 'w')
a=pickle.load(fp)
pickle=str(a)
fw.write( pickle )
fw.close()</code></pre>

得到一系列坐标代码

```
[[(3, 'm'), (4, '"'), (5, '"'), (8, '"'), (9, '"'), (10, '#'), (31, 'm'), (32, '"'), (33, '"'), (44, 'm'), (45, 'm'), (46, 'm'), (47, 'm'), (50, 'm'), (51, 'm'), (52, 'm'), (53, 'm'), (54, 'm'), (55, 'm'), (58, 'm'), (59, 'm'), (60, 'm'), (61, 'm'), (66, 'm'), (67, '"'), (68, '"'), (75, '#')], [(1, 'm'), (2, 'm'), (3, '#'), (4, 'm'), (5, 'm'), (10, '#'), (16, 'm'), (17, 'm'), (18, 'm'), (23, 'm'), (24, 'm'), (25, 'm'), (26, 'm'), (31, '#'), (37, 'm'), (38, 'm'), (39, 'm'), (43, '"'), (47, '"'), (48, '#'), (54, '#'), (55, '"'), (57, '"'), (61, '"'), (62, '#'), (64, 'm'), (65, 'm'), (66, '#'), (67, 'm'), (68, 'm'), (72, 'm'), (73, 'm'), (74, 'm'), (75, '#')], [(3, '#'), (10, '#'), (15, '"'), (19, '#'), (22, '#'), (23, '"'), (25, '"'), (26, '#'), (29, 'm'), (30, 'm'), (31, '"'), (36, '"'), (40, '#'), (47, 'm'), (48, '"'), (53, 'm'), (54, '"'), (59, 'm'), (60, 'm'), (61, 'm'), (62, '"'), (66, '#'), (71, '#'), (72, '"'), (74, '"'), (75, '#')], [(3, '#'), (10, '#'), (15, 'm'), (16, '"'), (17, '"'), (18, '"'), (19, '#'), (22, '#'), (26, '#'), (31, '#'), (36, 'm'), (37, '"'), (38, '"'), (39, '"'), (40, '#'), (45, 'm'), (46, '"'), (52, 'm'), (53, '"'), (61, '"'), (62, '#'), (66, '#'), (71, '#'), (75, '#')], [(3, '#'), (10, '"'), (11, 'm'), (12, 'm'), (15, '"'), (16, 'm'), (17, 'm'), (18, '"'), (19, '#'), (22, '"'), (23, '#'), (24, 'm'), (25, '"'), (26, '#'), (31, '#'), (36, '"'), (37, 'm'), (38, 'm'), (39, '"'), (40, '#'), (43, 'm'), (44, '#'), (45, 'm'), (46, 'm'), (47, 'm'), (48, 'm'), (51, 'm'), (52, '"'), (57, '"'), (58, 'm'), (59, 'm'), (60, 'm'), (61, '#'), (62, '"'), (66, '#'), (71, '"'), (72, '#'), (73, 'm'), (74, '#'), (75, '#')], [(23, 'm'), (26, '#'), (32, '"'), (33, '"')], [(24, '"'), (25, '"')], [], [(12, '#'), (17, 'm'), (18, '"'), (19, '"'), (23, 'm'), (24, 'm'), (25, 'm'), (26, 'm'), (33, '#'), (36, 'm'), (37, 'm'), (38, 'm'), (39, 'm'), (40, 'm'), (41, 'm'), (46, 'm'), (47, 'm'), (52, 'm'), (53, 'm'), (54, 'm'), (65, 'm'), (66, 'm'), (67, 'm'), (68, 'm'), (71, 'm'), (72, 'm'), (73, 'm'), (74, 'm'), (75, 'm'), (76, 'm')], [(2, 'm'), (3, 'm'), (4, 'm'), (9, 'm'), (10, 'm'), (11, 'm'), (12, '#'), (15, 'm'), (16, 'm'), (17, '#'), (18, 'm'), (19, 'm'), (22, '"'), (26, '"'), (27, '#'), (30, 'm'), (31, 'm'), (32, 'm'), (33, '#'), (40, '#'), (41, '"'), (45, 'm'), (46, '"'), (47, '#'), (50, 'm'), (51, '"'), (55, '"'), (58, 'm'), (59, 'm'), (60, 'm'), (64, '#'), (65, '"'), (68, '"'), (69, 'm'), (75, '#'), (76, '"')], [(1, '#'), (2, '"'), (5, '#'), (8, '#'), (9, '"'), (11, '"'), (12, '#'), (17, '#'), (24, 'm'), (25, 'm'), (26, 'm'), (27, '"'), (29, '#'), (30, '"'), (32, '"'), (33, '#'), (39, 'm'), (40, '"'), (44, '#'), (45, '"'), (47, '#'), (50, '#'), (51, 'm'), (52, '"'), (53, '"'), (54, '#'), (55, 'm'), (57, '#'), (58, '"'), (61, '#'), (64, '#'), (65, 'm'), (68, 'm'), (69, '#'), (74, 'm'), (75, '"')], [(1, '#'), (2, '"'), (3, '"'), (4, '"'), (5, '"'), (8, '#'), (12, '#'), (17, '#'), (26, '"'), (27, '#'), (29, '#'), (33, '#'), (38, 'm'), (39, '"'), (43, '#'), (44, 'm'), (45, 'm'), (46, 'm'), (47, '#'), (48, 'm'), (50, '#'), (55, '#'), (57, '#'), (58, '"'), (59, '"'), (60, '"'), (61, '"'), (65, '"'), (66, '"'), (67, '"'), (69, '#'), (73, 'm'), (74, '"')], [(1, '"'), (2, '#'), (3, 'm'), (4, 'm'), (5, '"'), (8, '"'), (9, '#'), (10, 'm'), (11, '#'), (12, '#'), (17, '#'), (22, '"'), (23, 'm'), (24, 'm'), (25, 'm'), (26, '#'), (27, '"'), (29, '"'), (30, '#'), (31, 'm'), (32, '#'), (33, '#'), (37, 'm'), (38, '"'), (47, '#'), (51, '#'), (52, 'm'), (53, 'm'), (54, '#'), (55, '"'), (57, '"'), (58, '#'), (59, 'm'), (60, 'm'), (61, '"'), (64, '"'), (65, 'm'), (66, 'm'), (67, 'm'), (68, '"'), (72, 'm'), (73, '"')], [], [], [], [(5, '#'), (8, '#'), (16, 'm'), (17, 'm'), (18, 'm'), (19, 'm'), (23, 'm'), (24, 'm'), (25, 'm'), (26, 'm'), (30, 'm'), (31, 'm'), (32, 'm'), (33, 'm'), (38, 'm'), (39, 'm'), (40, 'm'), (50, '#'), (57, '#'), (64, '#'), (71, 'm'), (72, 'm'), (73, 'm')], [(2, 'm'), (3, 'm'), (4, 'm'), (5, '#'), (8, '#'), (9, 'm'), (10, 'm'), (11, 'm'), (15, '#'), (16, '"'), (19, '"'), (20, 'm'), (22, 'm'), (23, '"'), (26, '"'), (27, 'm'), (29, '#'), (34, '#'), (36, 'm'), (37, '"'), (41, '"'), (44, 'm'), (45, 'm'), (46, 'm'), (50, '#'), (51, 'm'), (52, 'm'), (53, 'm'), (57, '#'), (58, 'm'), (59, 'm'), (60, 'm'), (64, '#'), (65, 'm'), (66, 'm'), (67, 'm'), (73, '#')], [(1, '#'), (2, '"'), (4, '"'), (5, '#'), (8, '#'), (9, '"'), (11, '"'), (12, '#'), (15, '#'), (16, 'm'), (19, 'm'), (20, '#'), (22, '#'), (25, 'm'), (27, '#'), (29, '"'), (30, 'm'), (31, 'm'), (32, 'm'), (33, 'm'), (34, '"'), (36, '#'), (37, 'm'), (38, '"'), (39, '"'), (40, '#'), (41, 'm'), (43, '#'), (44, '"'), (47, '#'), (50, '#'), (51, '"'), (53, '"'), (54, '#'), (57, '#'), (58, '"'), (60, '"'), (61, '#'), (64, '#'), (65, '"'), (67, '"'), (68, '#'), (73, '#')], [(1, '#'), (5, '#'), (8, '#'), (12, '#'), (16, '"'), (17, '"'), (18, '"'), (20, '#'), (22, '#'), (27, '#'), (29, '#'), (33, '"'), (34, '#'), (36, '#'), (41, '#'), (43, '#'), (44, '"'), (45, '"'), (46, '"'), (47, '"'), (50, '#'), (54, '#'), (57, '#'), (61, '#'), (64, '#'), (68, '#'), (73, '#')], [(1, '"'), (2, '#'), (3, 'm'), (4, '#'), (5, '#'), (8, '#'), (9, '#'), (10, 'm'), (11, '#'), (12, '"'), (15, '"'), (16, 'm'), (17, 'm'), (18, 'm'), (19, '"'), (23, '#'), (24, 'm'), (25, 'm'), (26, '#'), (29, '"'), (30, '#'), (31, 'm'), (32, 'm'), (33, 'm'), (34, '"'), (37, '#'), (38, 'm'), (39, 'm'), (40, '#'), (41, '"'), (43, '"'), (44, '#'), (45, 'm'), (46, 'm'), (47, '"'), (50, '#'), (51, '#'), (52, 'm'), (53, '#'), (54, '"'), (57, '#'), (58, '#'), (59, 'm'), (60, '#'), (61, '"'), (64, '#'), (65, '#'), (66, 'm'), (67, '#'), (68, '"'), (71, 'm'), (72, 'm'), (73, '#'), (74, 'm'), (75, 'm')], [], [], [], [(2, 'm'), (3, 'm'), (4, 'm'), (5, 'm'), (8, 'm'), (9, 'm'), (10, 'm'), (11, 'm'), (12, 'm'), (19, '#'), (24, 'm'), (25, 'm'), (26, 'm'), (29, '"'), (30, '"'), (31, 'm')], [(1, '#'), (2, '"'), (5, '"'), (6, 'm'), (8, '#'), (16, 'm'), (17, 'm'), (18, 'm'), (19, '#'), (22, 'm'), (23, '"'), (27, '"'), (31, '#')], [(1, '#'), (2, 'm'), (5, 'm'), (6, '#'), (8, '"'), (9, '"'), (10, '"'), (11, '"'), (12, 'm'), (13, 'm'), (15, '#'), (16, '"'), (18, '"'), (19, '#'), (22, '#'), (23, 'm'), (24, '"'), (25, '"'), (26, '#'), (27, 'm'), (31, '"'), (32, 'm'), (33, 'm')], [(2, '"'), (3, '"'), (4, '"'), (6, '#'), (13, '#'), (15, '#'), (19, '#'), (22, '#'), (27, '#'), (31, '#')], [(1, '"'), (2, 'm'), (3, 'm'), (4, 'm'), (5, '"'), (8, '"'), (9, 'm'), (10, 'm'), (11, 'm'), (12, '#'), (13, '"'), (15, '"'), (16, '#'), (17, 'm'), (18, '#'), (19, '#'), (23, '#'), (24, 'm'), (25, 'm'), (26, '#'), (27, '"'), (31, '#')], [(29, '"'), (30, '"')]]
```

再利用脚本进行转换

<pre class="wp-block-code"><code>fw = open("pickle.txt","r")
text=fw.read( )
i=0
a=0


while i&lt;len(text)+1:
    if(text&#91;i]==']'):
       print('\n')
       a=0
    elif(text&#91;i]=='('):
        if(text&#91;i+2]==','):
            b=text&#91;i+1]
            d=text&#91;i+1]
            b=int(b)-int(a)
            c=1
            while c&lt;b:
                print(" ", end="")
                c += 1
            print(text&#91;i+5], end="")
            a=int(d)
        else:
            b=text&#91;i+1]+text&#91;i+2]
            d=text&#91;i+1]+text&#91;i+2]
            b=int(b)-int(a)
            c=1
            while c&lt;b:
                print(" ", end="")
                c += 1
            print(text&#91;i+6], end="")
            a=int(d)
    i +=1</code></pre>

解出来的字符可以看出是flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="2448" height="1538" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-16.png" alt="" class="wp-image-5403" /> </figure> 

## 0x04 大流量分析（一）

某黑客对A公司发动了攻击，以下是一段时间内我们获取到的流量包，那黑客的攻击ip是多少？

下载流量包后通过wireshark的统计功能，筛选出最多的ip，得到183.129.152.140。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-17.png" alt="" class="wp-image-5405" width="589" height="145" /> </figure> 

## 0x05 大流量分析（二）

黑客对A公司发动了攻击，以下是一段时间内获取到的流量包，那黑客使用了哪个邮箱给员工发送了钓鱼邮件?

由于是邮件，所以首先过滤SMTP协议，然后一个个查看邮件的内容，最后确认邮箱为xsser@live.cn。<figure class="wp-block-image size-full">

<img loading="lazy" width="2337" height="674" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-18.png" alt="" class="wp-image-5406" /> </figure> 

## 0x06 [NPUCTF2020]碰上彩虹，吃定彩虹！

在lookatme.txt中发现空白字符，转换得到`.-/..-/-/---/-.-/./-.--`，解密得到`AUTOKEY`，应该使用了AUTOKEY加密<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-19.png" alt="" class="wp-image-5407" width="694" height="380" /> </figure> 

使用<a rel="noreferrer noopener" href="https://github.com/Yoshino-s/breakautokey" target="_blank" rel="nofollow" >https://github.com/Yoshino-s/breakautokey</a>来进行爆破，得到`iamthepassword`<figure class="wp-block-image size-full">

<img loading="lazy" width="2057" height="454" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-26.png" alt="" class="wp-image-5417" /> </figure> 

maybehint.txt 提示隐藏了一些信息,用 vim 查看<figure class="wp-block-image size-full">

<img loading="lazy" width="2741" height="408" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-20.png" alt="" class="wp-image-5408" /> </figure> 

零宽字符隐写，在<a rel="noreferrer noopener" href="http://330k.github.io/misc_tools/unicode_steganography.html" target="_blank" rel="nofollow" >http://330k.github.io/misc_tools/unicode_steganography.html</a>网站进行解密<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-22.png" alt="" class="wp-image-5410" /></figure> 

使用ntfsstreamseditor 发现隐藏信息<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-23.png" alt="" class="wp-image-5411" width="604" height="475" /> </figure> 

字符有限且不断循环，使用脚本计算词频，最后得到`ZW5jcnlwdG8=`，解base64得到`encrypto`

<pre class="wp-block-code"><code>from collections import Counter
f=open('out.txt','r')
f_read=f.read()
print (Counter(f_read))</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="1942" height="87" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-24.png" alt="" class="wp-image-5413" /> </figure> 

百度搜索发现这是一款软件，下载安装，其加密的文件后缀名为.crypto，打开得到hint，用autokey爆破得到的密码进行解压。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-25.png" alt="" class="wp-image-5416" width="404" height="407" /> </figure> 

解压发现解不出，进一步分析发现。<figure class="wp-block-image size-full">

<img loading="lazy" width="1297" height="312" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-30.png" alt="" class="wp-image-5423" /> </figure> 

得到一张彩虹.png<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-31.png" alt="" class="wp-image-5424" width="321" height="321" /> </figure> 

分析发现存在隐藏的zip，foremost提取出来。<figure class="wp-block-image size-full">

<img loading="lazy" width="1594" height="435" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-32.png" alt="" class="wp-image-5425" /> </figure> 

得到的图片，用snipate对分段的黄色进行屏幕取色，得到

<pre class="wp-block-code"><code>#ffff70
#ffff3f
#ffff73
#ffff73
#ffff57
#ffff64</code></pre>
将后两位拼凑在一起，转ascii得到密码`p@ssWd`，解压得到内容

```
eeeeeeeeeepaeaeeeaeAeeeeeeaeeeeeeeeeeccccisaaaaeejeeeeeejiiiiiiLiiiiijeeeeeejeeeeeeeeeeeeeeeeeeeejcceeeeeeeeeeePeeeeeeeejaaiiiiiiijcciiiiiiiiiijaaijiiiiiiiiiiiiiiiiiiiijeeeeeeHeeeeeeeeeeeeeeeeejcceeeeeeeeeeeejaaiiiijeeeeeeejceeeeeeeeeeeeeeeeeeeeeeeeejceeeeeeeeeeeeeeeeejaeeeeeejciiUiiiiiiiiiiiiiiiiijaeeeejceeeeeeeeeCeeeeeeeeejajciiiiiiiiiiiiiiiiiiijaaiiiijiijeeeeeeeeeeejKcciiiiiiiiiiiiiiijaaij
```

分析发现加密方式为Alphuck，进行转换即可得到flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="1686" height="426" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-33.png" alt="" class="wp-image-5427" /> </figure> 

## 0x07 [羊城杯 2020]signin

```
玩具总动员里面，巴斯光年成功上天，胡迪给他发了一段加密短信，但是不知道是什么？你能帮巴斯光年破解吗？胡迪给了一段明文，一表人才，二表倒立，相信聪明的你一定可以帮助他吧！
```

signin.txt里的内容如下

<pre class="wp-block-code"><code>BCEHACEIBDEIBDEHBDEHADEIACEGACFIBDFHACEGBCEHBCFIBDEGBDEGADFGBDEHBDEGBDFHBCEGACFIBCFGADEIADEIADFH</code></pre>

卡在这里很久，参考<a rel="noreferrer noopener" href="https://blog.csdn.net/mochu7777777/article/details/116056136" target="_blank" rel="nofollow" >https://blog.csdn.net/mochu7777777/article/details/116056136</a>才知道这个加密是Toy Cipher: <a href="https://eprint.iacr.org/2020/301.pdf" target="_blank"  rel="nofollow" >https://eprint.iacr.org/2020/301.pdf</a>

脚本如下：

```
cipherdic = {'M':'ACEG','R':'ADEG','K':'BCEG','S':'BDEG','A':'ACEH','B':'ADEH','L':'BCEH','U':'BDEH','D':'ACEI','C':'ADEI','N':'BCEI','V':'BDEI','H':'ACFG','F':'ADFG','O':'BCFG','W':'BDFG','T':'ACFH','G':'ADFH','P':'BCFH','X':'BDFH','E':'ACFI','I':'ADFI','Q':'BCFI','Y':'BDFI'}
ciphertext = ''
with open('signin.txt','r') as f:
    f = f.read()
    for i in range(0,len(f),4):
        block = f[i:i+4]
        for j in cipherdic:
            if block == cipherdic[j]:
                ciphertext += j
original_list = ['M','R','K','S','A','B','L','U','D','C','N','V','H','F','O','W','T','G','P','X','E','I','Q','Y']
reversed_list = original_list[::-1]

flag = ''
for char in ciphertext:
    for olist in original_list:
        if char == olist:
            oindex = original_list.index(olist)
            flag += reversed_list[oindex]
print(flag)
```

## 0x08 [WMCTF2020]行为艺术

解压得到hint.txt

<pre class="wp-block-code"><code>md5sum flag.zip 
17f5b08342cf65f6dc08ed0b4c9bd334  flag.zip</code></pre>

图片crc32存在问题，修改高度。<figure class="wp-block-image size-full">

<img loading="lazy" width="1199" height="144" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-28.png" alt="" class="wp-image-5420" /> </figure> 

最后的图很像机器学习数据集，504b的开头联想到压缩包，参考<a href="https://hachp1.github.io/posts/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0/20200814-wm2020.html#%E5%A6%82%E4%BD%95%E8%AF%86%E5%88%AB%E5%AD%97%E6%AF%8D" target="_blank"  rel="nofollow" >https://hachp1.github.io/posts/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0/20200814-wm2020.html#%E5%A6%82%E4%BD%95%E8%AF%86%E5%88%AB%E5%AD%97%E6%AF%8D</a><figure class="wp-block-image size-full">

<img loading="lazy" width="641" height="479" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-29.png" alt="" class="wp-image-5421" /> </figure> 

提取的数据为

```
504B0304140000000800DB93C55086A39007D8000000DF01000008000000666C61672E74787475504B0E823010DD93708771DDCCB0270D5BBD0371815A9148AC6951C2ED9D271F89C62E2693D7F76BB7DE9FC80D2E6E68E782A326D2E01F81CE6D55E76972E9BA7BCCB3ACEF7B89F7B6E90EA16A6EE2439D45179ECDD1C5CCFB6B9AA489C1218C92B898779D765FCCBB58CC920B6662C5F91749931132258F32BBA7C288C5AE103133106608409DAC419F77241A3412907814AB7A922106B8DED0D25AEC8A634929025C46A33FE5A1D3167A100323B1ABEE4A7A0708413A19E17718165F5D3E73D577798E36D5144B66315AAE315078F5E51A29246AF402504B01021F00140009000800DB93C55086A39007D8000000DF010000080024000000000000002000000000000000666C61672E7478740A00200000000000010018004A0A9A64243BD601F9D8AB39243BD6012D00CA13223BD601504B050600000000010001005A000000FE00000000000000
```

转换成压缩包，解开伪加密，得到的文本转brainfuck即可得到flag。

<pre class="wp-block-code"><code>Good eyes! Here is your flag:
https:&#47;&#47;www.splitbrain.org/services/ook

+++++ ++++&#91; ->+++ +++++ +&lt;]>+ +++++ .&lt;+++ &#91;->-- -&lt;]>- .&lt;+++ &#91;->-- -&lt;]>-
.&lt;+++ +&#91;->+ +++&lt;] >+.&lt;+ ++&#91;-> ---&lt;] >---- -.&lt;++ +++++ &#91;->++ +++++ &lt;]>++
++.-- --.&lt;+ +++&#91;- >---- &lt;]>-- ----. +++++ +++.&lt; +++&#91;- >---&lt; ]>-.+ ++.++
+++++ .&lt;+++ &#91;->-- -&lt;]>- .+++. -.... --.++ +.&lt;++ +&#91;->+ ++&lt;]> ++++. &lt;++++
++++&#91; ->--- ----- &lt;]>-- ----- ----- --.&lt;+ +++&#91;- >++++ &lt;]>+. +...&lt; +++++
+++&#91;- >++++ ++++&lt; ]>+++ +++++ +++.. .-.&lt;</code></pre>
