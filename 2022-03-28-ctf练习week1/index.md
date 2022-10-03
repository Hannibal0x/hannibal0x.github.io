# CTF练习Week1

<div class="has-toc have-toc">
</div>

## 0x00 WEB-[NCTF2019]True XML cookbook

访问网页源码<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-24.png" alt="" class="wp-image-5289" width="730" height="523" /> </figure> 

发现是以xml格式传入用户名密码的，且输入的用户名信息会返回到前端，尝试XXE注入，成功读取到文件。<figure class="wp-block-image size-full">

<img loading="lazy" width="2121" height="726" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-23.png" alt="" class="wp-image-5288" /> </figure> 

查看/etc/hosts，探测内网存活的主机。hosts文件是Linux系统上一个负责ip地址与域名快速解析的文件，以ascii格式保存在/etc/目录下。hosts文件包含了ip地址与主机名之间的映射，还包括主机的别名。但是没有发现有效的信息。<figure class="wp-block-image size-full">

<img loading="lazy" width="1952" height="683" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-26.png" alt="" class="wp-image-5292" /> </figure> 

然后查看arp缓存列表/proc/net/arp文件，发现一个ip地址，但爆破后没有得到有效结果。查看路由缓存表proc/net/fib_trie文件，获取服务器IP和网络架构。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-27.png" alt="" class="wp-image-5293" width="227" height="696" /> </figure> 

爆破10.244.80C段的ip得到flag<figure class="wp-block-image size-full">

<img loading="lazy" width="1523" height="1289" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-25.png" alt="" class="wp-image-5291" /> </figure> 

## 0x01 MISC-[HackingClubCTF 2022]你能看懂音符吗？

修改文件头<figure class="wp-block-image size-full">

<img loading="lazy" width="1221" height="116" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-28.png" alt="" class="wp-image-5296" /> </figure> 

解压得到<figure class="wp-block-image size-full">

<img loading="lazy" width="1150" height="342" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-29.png" alt="" class="wp-image-5297" /> </figure> 

把音符在<a rel="noreferrer noopener" href="https://www.qqxiuzi.cn/bianma/wenbenjiami.php?s=yinyue" target="_blank" rel="nofollow" >https://www.qqxiuzi.cn/bianma/wenbenjiami.php?s=yinyue</a>解密即可得到flag。

## 0x02 Crypto-[HackingClubCTF 2022]影子系统

我们得到了一串神秘字符串：TASC?O3RJMV?WDJKX?ZM,问号部分是未知大写字母，为了确定这个神秘字符串，我们通过了其他途径获得了这个字串的32位MD5码。但是我们获得它的32位MD5码也是残缺不全，E903???4DAB????08?????51?80??8A?,请猜出神秘字符串的原本模样，并且提交这个字串的32位MD5码作为答案。

这个写脚本爆破就出来了。

<pre class="wp-block-code"><code>import hashlib
import string

def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()

for i in string.ascii_uppercase:
    for j in string.ascii_uppercase:
        for k in string.ascii_uppercase:
            c = 'TASC' + i + 'O3RJMV' + j + 'WDJKX' + k + 'ZM'
            x = md5(c).upper()
            if 'E903' in x and '4DAB' in x and '08' in x and '51' in x and '80' in x and '8A' in x:
                print(x)
                break</code></pre>

## 0x03 取证-[HackingClubCTF 2022]后门！！OMG！

上D盾开扫，发现可疑文件<figure class="wp-block-image size-full">

<img loading="lazy" width="1880" height="540" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-30.png" alt="" class="wp-image-5299" /> </figure> 

查看webshell密码`0578b19a3360292c22bede3cf6a79272`，md5后`76a8753e02d1503213172ef838372365`。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-31.png" alt="" class="wp-image-5300" width="695" height="334" /> </figure> 

## 0x04 Crypto-[HackingClubCTF 2022]异性相吸

buu原题，key和密文同为奇数或偶数相减，一奇一偶相加，脚本如下：

<pre class="wp-block-code"><code>key = open("key.txt", 'rb').read()
cipher = open("密文.txt", "rb").read()

flag = &#91;]
result = ""
for i in range(len(key)):
    flag.append(key&#91;i] ^ cipher&#91;i])
    result += chr(flag&#91;i])
print(flag)
print(result)</code></pre>

## 0x05 Misc-[HackingClubCTF 2022]美丽的烟火

zip伪加密，得到`am5QWDVwNVp0ZkRKdW14U3NFSw==`，解码得到`t_hp1ass_s1wsd`<figure class="wp-block-image size-full">

<img loading="lazy" width="1640" height="1020" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-32.png" alt="" class="wp-image-5302" /> </figure> 

栅栏编码得到`th1s_1s_passwd`，在firework.png发现可疑字样`stegpy:shumu`<figure class="wp-block-image size-full">

<img loading="lazy" width="1201" height="153" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-33.png" alt="" class="wp-image-5303" /> </figure> 

使用stegpy提取下隐藏信息，得到`aZgs8ImPpQOzO3CVA/wIUVq/M7X8C33ptNZSW2Blenc=`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-34.png" alt="" class="wp-image-5304" width="530" height="64" /> </figure> 

尝试base64解码，未果，想到上面的密码还没用，使用AES解密得到flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="1447" height="835" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-35.png" alt="" class="wp-image-5305" /> </figure> 

## 0x06 Web-[HackingClubCTF 2022]Find my Friend

目录扫描发现data.txt文件，访问得到flag<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-36.png" alt="" class="wp-image-5309" /></figure> 

## 0x07 Crypto-[HackingClubCTF 2022]乌拉

<figure class="wp-block-image size-full">

<img loading="lazy" width="2098" height="677" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-39.png" alt="" class="wp-image-5313" /> </figure> 

## 0x08 MISC-[HackingClubCTF 2022]看看这是什么星号东西

给了一张原图和2340张分割后的小图，根据图片序列猜测是宽高都按0-49分的，也就是说，图片是50x50。<figure class="wp-block-image size-full">

<img loading="lazy" width="3000" height="565" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-40.png" alt="" class="wp-image-5315" /> </figure> 

执行`magick montage *.png -tile 50x50 -geometry +0+0 flag.png`，得到一张图片<figure class="wp-block-image size-full">

<img loading="lazy" width="433" height="813" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-41.png" alt="" class="wp-image-5316" /> </figure> 

其实隐隐约约能看到部分flag了，使用gaps没有达到理想的效果，没办法，简单手撕一下。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-42.png" alt="" class="wp-image-5317" width="519" height="421" /> </figure> 

得到部分细节，最终的flag为`flag{Hello_word_给HackingClub}`，有中文属实是没想到，卡了很久。

## 0x09 Crypto-[HackingClubCTF 2022]RC小车车嘟嘟嘟

<figure class="wp-block-image size-full">

<img loading="lazy" width="1235" height="384" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-44.png" alt="" class="wp-image-5319" /> </figure> 

## 0x0A Web-[HackingClubCTF 2022]Easy-yinkelude

<pre class="wp-block-code"><code> &lt;?php
include('./flag.php');
show_source('./index.php');
$file=@$_POST&#91;'file'];
class hello{
    public $falg='tql123';
}
$a=new hello();
$shit=serialize($a);
if(@file_get_contents($file) == $shit){
    echo $flag;
}else{
    echo "what are u doing? just a qian dao";
}

?&gt; </code></pre>

分析代码可知，需要上传一个$file变量，使得它的值等于a的序列化，猜测是用data协议传序列化后的值，payload为：`data://text/plain,O:5:"hello":1:{s:4:"falg";s:6:"tql123";}`<figure class="wp-block-image size-full">

<img loading="lazy" width="1966" height="1650" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-45.png" alt="" class="wp-image-5322" /> </figure> 

## 0x0B 取证-[HackingClubCTF 2022]WebShell大马

上D盾<figure class="wp-block-image size-full">

<img loading="lazy" width="1456" height="442" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-49.png" alt="" class="wp-image-5327" /> </figure> 

## 0x0C MISC-[HackingClubCTF 2022]史上第一难倒直男的题目

小明正在上班，想要小红的微信，但是小红给了一个32位的微信号码，请你帮帮她。

<blockquote class="wp-block-quote">
  <p>
    （有人说这是Crypto！但是我觉得Misc的含量更多！）
  </p>
</blockquote>

题目信息：63c44dde47a3f48927ddddc88fb489ad

解md5，得到一串字符，以为是flag但不是，想到题目说更像MISC和微信的提示，就加wx了。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-50.png" alt="" class="wp-image-5328" width="447" height="204" /> </figure> 

## 0x0D MISC-[HackingClubCTF 2022]给你康个好康的~

ppt里面有几张很刺激的图片，修改文件后缀为zip，解压后在\ppt\media下看jpg，在image6里发现藏有压缩包。<figure class="wp-block-image size-full">

<img loading="lazy" width="1359" height="857" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-51.png" alt="" class="wp-image-5329" /> </figure> 

解压后得到一个Flag.docx，但文件有加密，打不开，队友爆出密码PLJJ，解压得到flag。

## 0x0E Crypto-[红明谷杯]easy_ya

```python
from Crypto.Util.number import *
import os

from flag import flag
def gen():
    e = 3
    while True:
        try:
            p = getPrime(512)
            q = getPrime(512)
            n = p*q
            phi = (p-1)*(q-1)
            d = inverse(e,phi)
            return p,q,d,n,e
        except:
            continue
    return
p,q,d,n,e = gen()
r = getPrime(512)
m = bytes_to_long(flag+os.urandom(32))
M = m%r
c = pow(m,e,n)
print("r = %d"%r)
print("M = %d"%M)
print("n = %d"%n)
print("e = %d"%e)
print("c = %d"%c)
'''
r = 7996728164495259362822258548434922741290100998149465194487628664864256950051236186227986990712837371289585870678059397413537714250530572338774305952904473
M = 4159518144549137412048572485195536187606187833861349516326031843059872501654790226936115271091120509781872925030241137272462161485445491493686121954785558
n = 131552964273731742744001439326470035414270864348139594004117959631286500198956302913377947920677525319260242121507196043323292374736595943942956194902814842206268870941485429339132421676367167621812260482624743821671183297023718573293452354284932348802548838847981916748951828826237112194142035380559020560287
e = 3
c = 46794664006708417132147941918719938365671485176293172014575392203162005813544444720181151046818648417346292288656741056411780813044749520725718927535262618317679844671500204720286218754536643881483749892207516758305694529993542296670281548111692443639662220578293714396224325591697834572209746048616144307282
'''
```

e=3首先想到的是低指数的爆破，但是稍稍分析就知道这个位数不太能爆破出来，Coppersmith发现的短填充攻击，即在消息尾部或头部直接填充随机串，如果填充的随机串r的长度低于消息长度的1/9，那么攻击者便能够有效地恢复出明文M。

**Coppersmith定理：令N为大整数，f是度为e的多项式。给定N和f，可以有效地计算出方程f(x)=0 mod N所有小于N^(1/e)的解。**构造如下的多项式：f = (M+r*x)^e -c 在 Zmod(n)的多项式环上有小根x = k,由于k < 2^79 < n^(1/e)

<pre class="wp-block-code"><code>PR.&lt;x&gt; = PolynomialRing(Zmod(N))
g = (M + r * x) ** e - c
g = g.monic() #monic()表示首系数为1的单项式
k = g.small_roots()&#91;0]
m = k * r + M</code></pre>

## 0x0F Crypto-[HackingClubCTF 2022]老套路

mvlxhirlszq{eof\_eof\_bvjf\_jd\_jd}，仿射密码<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-52.png" alt="" class="wp-image-5334" width="311" height="252" /> </figure> 

## 0x10 MISC-[HackingClubCTF 2022]逃离东南亚

得到三个日记的压缩包，先解压第一个，发现图片，修改高度得到密码`wdnmd`。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-53.png" alt="" class="wp-image-5337" width="286" height="335" /> </figure> 

第一段日记的markdown<figure class="wp-block-image size-full">

<img loading="lazy" width="2400" height="1562" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-54.png" alt="" class="wp-image-5338" /> </figure> 

第二段日记的markdown<figure class="wp-block-image size-full">

<img loading="lazy" width="2400" height="1754" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-55.png" alt="" class="wp-image-5339" /> </figure> 

文中提到了信息隐藏，看看test文件很像brainfuck，但是少了`++++++++`的开头，补上后成功解码，得到的字符串，形似base64加密，cyberchef转换后发现ELF的字样，保存得到可执行文件。<figure class="wp-block-image size-full">

<img loading="lazy" width="1910" height="1589" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-56.png" alt="" class="wp-image-5340" /> </figure> 

运行暂无有效信息<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-58.png" alt="" class="wp-image-5342" width="450" height="93" /> </figure> 

SilentEye分析打架.wav得到`This1sThe3rdZIPpwd`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-57.png" alt="" class="wp-image-5341" width="394" height="304" /> </figure> 

解压日记3，得到最后的markdown<figure class="wp-block-image size-full">

<img loading="lazy" width="2314" height="1303" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-59.png" alt="" class="wp-image-5343" /> </figure> 

这里卡了很久，题目说是原题改的，就去查了下wp，发现需要用脚本搜索tab和空格，同时要过滤到常见的双空格和双/t，因此考虑用 `\t \t`作为搜索字符。参考：<a rel="noreferrer noopener" href="https://www.bilibili.com/read/cv14000314" target="_blank" rel="nofollow" >https://www.bilibili.com/read/cv14000314</a>

<pre class="wp-block-code"><code>import os

def get_file_list(dir_path):
    _file_list = os.listdir(dir_path)
    file_list = &#91;]
    for file_str in _file_list:
        new_dir_path = dir_path+'\\'+file_str
        if os.path.isdir(new_dir_path):
            file_list.extend(get_file_list(new_dir_path))
        else:
            file_list.append(new_dir_path)
    return file_list

file_list = get_file_list(r'.\source_code')
for file_str in file_list:
    f = open(file_str, 'r', encoding='utf-8')
    try:
        data = f.read()
        if ' \t \t' in data:
            print(file_str)
    except:
        pass</code></pre>

得到三个可疑的文件，在}后面有隐藏信息。

<pre class="wp-block-code"><code>.\source_code\elf\rtld.c
.\source_code\malloc\arena.c
.\source_code\malloc\malloc.c</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="3192" height="911" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-60.png" alt="" class="wp-image-5344" /> </figure> 

使用脚本读出\t和空格，然后二进制转字符得到flag。

<pre class="wp-block-code"><code>f_list = r'''.\source_code\elf\rtld.c
.\source_code\malloc\arena.c
.\source_code\malloc\malloc.c'''
f_list = f_list.split('\n')

result = ''

for f in f_list:
    for data in open(f, 'r').readlines():
        data = data&#91;:-1]
        if '}' in data:
            data = data.split('}')&#91;-1]
            if '\t' in data:
                data1 = data&#91;::].replace('\t', '')
                data1 = data1.replace(' ', '')
                if not data1:
                    result += data

result = result.replace('\t', '1')
result = result.replace(' ', '0')
print(result)</code></pre>

## 0x11 Misc-[WUSTCTF2020]spaceclub

<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-61.png" alt="" class="wp-image-5346" width="186" height="544" /> </figure> 

只有长空格和短空格，转成0和1 ，转二进制即可得到flag。

## 0x12 Misc-[WUSTCTF2020]girlfriend

wav播放后是很明显的拨号声，使用dtmf2num识别得到`999*666*88*2*777*33*6*999*4*444*777*555*333*777*444*33*66*3*7777`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-62.png" alt="" class="wp-image-5347" width="722" height="434" /> </figure> 

分析numbers结合拨号的键，猜想是手机的九键输入法，依次对着输就能得到flag。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-63.png" alt="" class="wp-image-5349" width="625" height="419" /> </figure> 

## 0x13 Misc-[WUSTCTF2020]爬

发现文件头是PDF，修改后缀名。<figure class="wp-block-image size-full">

<img loading="lazy" width="1362" height="255" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-64.png" alt="" class="wp-image-5350" /> </figure> 

打开文件，显示flag被图片挡住了。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-65.png" alt="" class="wp-image-5353" width="400" height="430" /> </figure> 

用word打开，另存为docx，再把爬字拖动，得到一串16进制，转换得到flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="1145" height="57" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-66.png" alt="" class="wp-image-5354" /> </figure> 

## 0x14 Misc-[WUSTCTF2020]find_me

在属性里发现疑似盲文的符号，直接转换得到flag<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-67.png" alt="" class="wp-image-5356" width="492" height="190" /> </figure> 

## 0x15 Misc-[WUSTCTF2020]alison\_likes\_jojo

给了两张图，先在boki里面发现有压缩包，分离一下。<figure class="wp-block-image size-full">

<img loading="lazy" width="1943" height="248" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-68.png" alt="" class="wp-image-5357" /> </figure> 

分离后，确认不是未加密，先进行爆破，得到密码`888866`，解压得到beisi.txt的文件内容`WVRKc2MySkhWbmxqV0Zac1dsYzBQUT09`，应该是base64没跑了，直接丢到cyberchef里面，自动解了3层，得到`killerqueen`。

分析jljy，多次尝试后发现为outguess加密，执行`outguess -k killerqueen -r jljy.jpg 1.txt`得到flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="1128" height="140" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-69.png" alt="" class="wp-image-5358" /> </figure> 

## 0x16 Misc-[UTCTF2020]basic-forensics

文件是ebook，直接strings搜索得到flag。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-70.png" alt="" class="wp-image-5359" width="606" height="43" /> </figure> 

## 0x17 Misc-[UTCTF2020]File Carving

binwalk分离png，得到hidden_binary<figure class="wp-block-image size-full">

<img loading="lazy" width="2258" height="342" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-71.png" alt="" class="wp-image-5360" /> </figure> 

file查看文件类型，运行可执行文件得到flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="2262" height="215" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-72.png" alt="" class="wp-image-5361" /> </figure> 

## 0x18 Misc-[MRCTF2020]pyFlag

给了三张图，010点开分析发现文件尾都有一个SecretFilePart<figure class="wp-block-image size-full">

<img loading="lazy" width="1365" height="639" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-73.png" alt="" class="wp-image-5362" /> </figure> 

拼接得到压缩包，发现加密，爆破出密码。<figure class="wp-block-image size-full">

<img loading="lazy" width="1588" height="806" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-74.png" alt="" class="wp-image-5364" /> </figure> 

hint.txt内容为

<pre class="wp-block-code"><code>我用各种baseXX编码把flag套娃加密了，你应该也有看出来。
但我只用了一些常用的base编码哦，毕竟我的智力水平你也知道...像什么base36base58听都没听过
提示：0x10,0x20,0x30,0x55</code></pre>
flag.txt的内容为

```
G&eOhGcq(ZG(t2*H8M3dG&wXiGcq(ZG&wXyG(j~tG&eOdGcq+aG(t5oG(j~qG&eIeGcq+aG)6Q<G(j~rG&eOdH9<5qG&eLvG(j~sG&nRdH9<8rG%++qG%__eG&eIeGc+|cG(t5oG(j~sG&eOlH9<8rH8C_qH9<8oG&eOhGc+_bG&eLvH9<8sG&eLgGcz?cG&3|sH8M3cG&eOtG%_?aG(t5oG(j~tG&wXxGcq+aH8V6sH9<8rG&eOhH9<5qG(<E-H8M3eG&wXiGcq(ZG)6Q<G(j~tG&eOtG%+<aG&wagG%__cG&eIeGcq+aG&M9uH8V6cG&eOlH9<8rG(<HrG(j~qG&eLcH9<8sG&wUwGek2)
```

根据提示猜测用到了base16、base32、base64(感觉上面应该是0x40才对，这里是个小bug，但没有base48)、base85，只需要试出第一层，剩下的交给cyberchef即可解出flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="3054" height="1396" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-75.png" alt="" class="wp-image-5365" /> </figure> 

## 0x19 Misc-[MRCTF2020]千层套路

压缩包第一层是0573.zip，爆破发现密码就是0573，下一层是0114.zip，密码也和文件名相同，需要编写脚本来解决套娃。

<pre class="wp-block-code"><code>from os import system
import zipfile

zipname = "0573.zip"
f = zipfile.ZipFile(zipname, 'r')


while 1:
	try:
		name = f.namelist()&#91;0]
		f.extractall(pwd=bytes(zipname&#91;0:4],'utf-8'))
		system('rm -rf '+ str(zipname))
		f = zipfile.ZipFile(name, 'r')
		zipname = name
	except:
		break</code></pre>

跑了几分钟最后得到qr.txt，可以看到是rgb的数据<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-76.png" alt="" class="wp-image-5366" width="296" height="507" /> </figure> 

把前后括号都删去，然后用下面的脚本，得到一张二维码，扫描得到flag。

<pre class="wp-block-code"><code>from PIL import Image

x = y = 200
img = Image.new("RGB",(x,y))
file = open('./qr.txt','r')

for width in range(0,x):
    for height in range(0,y):
        line = file.readline()
        rgb = line.split(',')
        img.putpixel((width,height),(int(rgb&#91;0]),int(rgb&#91;1]),int(rgb&#91;2])))
img.save('flag.jpg')</code></pre>

## 0x1A MISC-[HackingClubCTF 2022]我说这是莫斯

扫描二维码得到swpuctf{flag\_is\_not_here}，假的，yongbinwalk发现图片藏有4个rar，分离一下。

先在encode.txt得到一段base64编码`YXNkZmdoamtsMTIzNDU2Nzg5MA==`，`asdfghjkl1234567890`。

flag.doc中发现一段多重base64加密的字符串，解密后得到`comEON_YOuAreSOSoS0great`。

解压压缩包得到一段音频文件，只有长短两种，怀疑是莫斯电码。<figure class="wp-block-image size-full">

<img loading="lazy" width="1899" height="296" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/image-21.png" alt="" class="wp-image-5370" /> </figure> 

记录得到`--/---/.-./…/./../…/…-/./.-./-.--/…-/./.-./-.--/./.-/…/-.--`，转换得到`MORSEISVERYVERYEASY`

## 0x1B MISC-[HackingClubCTF 2022]我的路由器

下载得到conf.bin文件，使用RouterPassView打开，得到flag。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/image-22.png" alt="" class="wp-image-5372" width="488" height="346" /> </figure> 

## 0x1C Crypto-[HackingClubCTF 2022]无AC保护

仔细观察发现字符串里都包含`5x55303030303030`

```
5x5530303030303036365x5530303030303036435x5530303030303036315x5530303030303036375x5530303030303037425x5530303030303037375x5530303030303036355x5530303030303036435x5530303030303036335x5530303030303036465x5530303030303036445x5530303030303036355x5530303030303035465x5530303030303037345x5530303030303036465x5530303030303035465x5530303030303036385x5530303030303036315x5530303030303036335x5530303030303036425x5530303030303036395x5530303030303036455x5530303030303036375x5530303030303036335x5530303030303036435x5530303030303037355x5530303030303036325x5530303030303035465x5530303030303034335x5530303030303035345x5530303030303034365x5530303030303035465x5530303030303036355x5530303030303036315x5530303030303037335x5530303030303037395x5530303030303035465x5530303030303034335x5530303030303037325x5530303030303037395x5530303030303037305x5530303030303037345x5530303030303036465x553030303030303744
```

全部删除得到

```
36363643363136373742373736353643363336463644363535463734364635463638363136333642363936453637363336433735363235463433353434363546363536313733373935463433373237393730373436463744
```

转换得到flag<figure class="wp-block-image size-full">

<img loading="lazy" width="3058" height="560" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/image-23.png" alt="" class="wp-image-5375" /> </figure> 

## 0x1E Crypto-[HackingClubCTF 2022]Beautiful<figure class="wp-block-image size-full">

<img loading="lazy" width="1604" height="1024" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/image-24.png" alt="" class="wp-image-5376" /> </figure>
