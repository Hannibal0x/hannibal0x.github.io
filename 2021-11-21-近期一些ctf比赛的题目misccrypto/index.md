# 近期一些CTF比赛的题目（MISC+CRYPTO）

## 0x00 深育杯-Login

在页面下载example.zip，用winrar查看<figure class="wp-block-image size-full">

<img loading="lazy" width="220" height="120" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-46.png" alt="" class="wp-image-4398" /> </figure> 

010editor尝试修改伪加密，得到示例副本<figure class="wp-block-image size-full">

<img loading="lazy" width="1590" height="297" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-47.png" alt="" class="wp-image-4400" /> </figure> 

然后使用ARCHPR进行已知明文攻击，得到压缩包的密码为`qwe@123`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-49.png" alt="" class="wp-image-4404" width="427" height="182" /> </figure> 

得到password.zip，查看发现里面的三个TXT文件非常小，猜测可以用crc32爆破。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-48.png" alt="" class="wp-image-4402" width="991" height="58" /> </figure> 

<pre class="wp-block-code"><code>python crc32.py reverse crc32密文</code></pre><figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-52.png" alt="" class="wp-image-4407" width="561" height="343" /></figure> 

组合在一起就是`welc0me_sangforctf`，解压得到.password.swp，kali下执行`vim -r .password.swp`恢复出原文件，得到：

<pre class="wp-block-code"><code>账号：Admin
密码：5f4dcc3b5aa765d61d8327deb882cf99</code></pre>

登录页面，查看源代码即可获得flag。

## 0x01 深育杯-GeGe

<pre class="wp-block-code"><code>from Crypto.Util.number import *
import gmpy2
from flag import flag

def encrypt(plaintext):
    p = getStrongPrime(3072) 
    m = bytes_to_long(plaintext)
    r = getRandomNBitInteger(1024)
    while True:
        f = getRandomNBitInteger(1024)
        g = getStrongPrime(768)
        h = gmpy2.invert(f, p) * g % p
        c = (r * h + m * f) % p
        return (h, p, c)

h, p, c = encrypt(flag)
with open("cipher.txt", "w") as f:
    f.write("h = " + str(h) + "\n")
    f.write("p = " + str(p) + "\n")
    f.write("c = " + str(c) + "\n")</code></pre>

参考<a rel="noreferrer noopener" href="https://xz.aliyun.com/t/7163" target="_blank" rel="nofollow" >https://xz.aliyun.com/t/7163</a>、<a rel="noreferrer noopener" href="https://mp.weixin.qq.com/s/1V5BEsfdZNRKwWP1mCs8wQ" target="_blank" rel="nofollow" >https://mp.weixin.qq.com/s/1V5BEsfdZNRKwWP1mCs8wQ</a>整理如下：<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-58.png" alt="" class="wp-image-4414" width="413" height="226" /></figure> 

现在只要求f、g，就能解出m，看做格来求解SVP问题。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-60.png" alt="" class="wp-image-4416" width="311" height="64" /></figure> 

可以构造一个由下面这个矩阵M中的两个行向量(1,h), (0,p)所张成的格<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-61.png" alt="" class="wp-image-4417" width="308" height="119" /> </figure> 

在<a href="https://cocalc.com" target="_blank"  rel="nofollow" >https://cocalc.com</a>上在线运行sage代码

<pre class="wp-block-code"><code># Construct lattice.
v1 = vector(ZZ, &#91;1, h])
v2 = vector(ZZ, &#91;0, p])
m = matrix(&#91;v1,v2]);

# Solve SVP.
shortest_vector = m.LLL()&#91;0]
f, g = shortest_vector
if f &lt; 0:
    f = -f
if g &lt; 0:
    g = -g

# Decrypt.
a = f * c % p % g
m = a * inverse_mod(f, g) * inverse_mod(f, g) % g
print(hex(m))</code></pre>

解得：`0x666c61677b70666132733166363561647334667765763173326433763163787861767165737d`，转十六进制，得到

<pre class="wp-block-code"><code>SangFor{pfa2s1f65ads4fwev1s2d3v1cxxavqes}</code></pre>

## 0x02 深育杯-Disk

解压文件得到文件名`zse456tfdyhnjimko0-=[;.,.vera`，官方的hint，文件名初级磁盘密码。

根据文件名在键盘上画出图形，得到密码。

使用VeraCrypt挂载后得到两个文件<figure class="wp-block-image size-full">

<img loading="lazy" width="197" height="91" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-62.png" alt="" class="wp-image-4422" /> </figure> 

用010editor打开good，发现文件头是7z。<figure class="wp-block-image size-full">

<img loading="lazy" width="1189" height="155" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-63.png" alt="" class="wp-image-4424" /> </figure> 

解压得到附件gooood，分析发现为windows下的分区。<figure class="wp-block-image size-full">

<img loading="lazy" width="2274" height="141" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-64.png" alt="" class="wp-image-4426" /> </figure> 

重命名为vhd文件，用DiskGenius打开发现存在BitLocker加密。<figure class="wp-block-image size-full">

<img loading="lazy" width="392" height="109" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-65.png" alt="" class="wp-image-4427" /> </figure> 

使用`bitlocker2john -i gooood.vhd`，将User Password hash的第一个值或第二个值保存成hash.txt<figure class="wp-block-image size-full">

<img loading="lazy" width="2268" height="434" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-66.png" alt="" class="wp-image-4428" /> </figure> <figure class="wp-block-image">![image-20210119143922423][2]</figure> 

```
$bitlocker$0$16$6c1fbe8314e64b4042110147cb1632d2$1048576$12$a0348897f591d70103000000$60$fb026c1039aec7a85c77964d9cf2b63f6261579f431dfdb675322ab91e44acab870c75a64b5722be3500b35bcee969dc59e31ffdf88c1cb3a07776fa

$bitlocker$1$16$6c1fbe8314e64b4042110147cb1632d2$1048576$12$a0348897f591d70103000000$60$fb026c1039aec7a85c77964d9cf2b63f6261579f431dfdb675322ab91e44acab870c75a64b5722be3500b35bcee969dc59e31ffdf88c1cb3a07776fa
```

使用`hashcat -m 22100 hash.txt rockyou.txt --show`，指定哈希类型后爆破。<figure class="wp-block-image size-full">

<img loading="lazy" width="1447" height="86" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-70.png" alt="" class="wp-image-4437" /></figure> 

得到密码是`abcd1234`，解锁打开回收站，发现hint和一个7z文件。<figure class="wp-block-image size-full">

<img loading="lazy" width="1461" height="100" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-71.png" alt="" class="wp-image-4438" /> </figure> 

rdp协议默认开启位图缓存功能，会产生bmc文件，使用bmc-tool或者BMC Viewer能够恢复出缓存的图像。

7c解压后用BMC Viewer查看，得到`cmRwY2FjaGUtYm1j`，解密base64得到flag<figure class="wp-block-image size-full">

<img loading="lazy" width="1485" height="902" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-72.png" alt="" class="wp-image-4441" /> </figure> 

或者使用`bmc-tools.py -s bcache24 -d 1`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-73.png" alt="" class="wp-image-4442" width="628" height="98" /> </figure> 

找到 flag 缩略图<figure class="wp-block-image size-full">

<img loading="lazy" width="426" height="148" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-75.png" alt="" class="wp-image-4445" /> </figure> 

## 0x03 深育杯-Brige

用Stegsolve发现存在LSB隐写，导出PNG文件<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-76.png" alt="" class="wp-image-4447" width="730" height="565" /> </figure> 

010editor删除文件头多余的部分后得到图片<figure class="wp-block-image size-full">

<img loading="lazy" width="416" height="416" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-77.png" alt="" class="wp-image-4449" /> </figure> 

分析其像素

<pre class="wp-block-code"><code>from PIL import Image

img = Image.open('1.png')
height = img.size&#91;0]
width = img.size&#91;1]
pixeltxt = open('pixel.txt','a')
for x in range(height):
    for y in range(width):
        pixel = img.getpixel((x,y))
        pixeltxt.write(str(pixel) + '\n')</code></pre>

发现像素的第三部分存在问题，。<figure class="wp-block-image size-full">

<img loading="lazy" width="183" height="307" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-85.png" alt="" class="wp-image-4459" /> </figure> 

将前四个数据，处理后得到zip文件的文件头<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-86.png" alt="" class="wp-image-4461" width="565" height="305" /> </figure> 

提取生成数据，用010editor生成压缩包文件

<pre class="wp-block-code"><code>from PIL import Image

img = Image.open('1.png')
height = img.size&#91;0]
width = img.size&#91;1]
pixeltxt = open('pixel.txt','a')
zipstrings = ''
for x in range(height):
    for y in range(width):
        pixel = img.getpixel((x,y))&#91;2]
        hexnum = hex(pixel)
        zipstrings +=str(hexnum)&#91;2:].zfill(2)
zip = open('flag.txt','a')
zip.write(zipstrings)</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="2173" height="145" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-87.png" alt="" class="wp-image-4462" /> </figure> 

分析brige.png发现存在异常的chunk，结合pngcheck发现IDAT数据块存在问题<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-81.png" alt="" class="wp-image-4455" width="589" height="140" /> </figure> 

010editor中看到最后一个IDAT数据块长度异常，将IDAT标识后面的`87 9C`两个字节，恢复成zlib数据头标识`78 9C`，导出这段zlib数据。<figure class="wp-block-image size-full">

<img loading="lazy" width="1456" height="1402" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-82.png" alt="" class="wp-image-4456" /> </figure> 

导出zlib数据为flag文件，用python脚本解出

<pre class="wp-block-code"><code>import zlib

file = open('flag','rb').read()
data = zlib.decompress(file)
rar = open('1.rar','wb')
rar.write(data)</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="1948" height="136" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-83.png" alt="" class="wp-image-4457" /> </figure> 

使用exiftool分析原图，发现异常数据。<figure class="wp-block-image size-full">

<img loading="lazy" width="1851" height="814" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-84.png" alt="" class="wp-image-4458" /> </figure> 

转16进制得到`dynamical-geometry`，解压之前获得的压缩包，看到stl文件，打开获得一半flag<figure class="wp-block-image size-full">

<img loading="lazy" width="1915" height="350" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-88.png" alt="" class="wp-image-4463" /> </figure> 

把flag2同样修改成stl文件预览，得到整个flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="1698" height="353" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-89.png" alt="" class="wp-image-4464" /> </figure> 

## 0x04 湖湘杯-signin

<pre class="wp-block-code"><code>from Crypto.Util.number import *
from secret import flag
import random

m1 = bytes_to_long(flag&#91;:len(flag) // 2])
m2 = bytes_to_long(flag&#91;len(flag) // 2:])

def gen(pbits, qbits):
    p1, q1 = getPrime(pbits), getPrime(qbits)
    n1 = p1**4*q1
    q2 = getPrime(qbits)
    bound = p1 // (8*q1*q2) + 1
    p2 = random.randrange(p1, p1 + bound)
    while not isPrime(p2):
        p2 = random.randrange(p1, p1 + bound)
    n2 = p2**4*q2
    return (n1, n2), (p1, q1), (p2, q2)

e = 0x10001
pbits = int(360)
qbits = int(128)
pk, sk1, sk2 = gen(pbits, qbits)
c1 = pow(m1, e, pk&#91;0])
c2 = pow(m2, e, pk&#91;1])
print(f'pk = {pk}')
print(f'c1, c2 = {c1, c2}')</code></pre>

给出了n1、n2、c1、c2、e，和[羊城杯 2020]RRRRRRRSA类似，用维纳攻击解，先得出

<pre class="wp-block-code"><code>from Crypto.Util.number import *
import gmpy2

def continuedFra(x, y): #不断生成连分数的项
    cF = &#91;]
    while y:
        cF += &#91;x // y]
        x, y = y, x % y
    return cF
    
def Simplify(ctnf): #化简
    numerator = 0
    denominator = 1
    for x in ctnf&#91;::-1]: #注意这里是倒叙遍历
        numerator, denominator = denominator, x * denominator + numerator
    return (numerator, denominator) #把连分数分成分子和算出来的分母
    
def getit(c):
    cf=&#91;]
    for i in range(1,len(c)):
        cf.append(Simplify(c&#91;:i])) #各个阶段的连分数的分子和分母
    return cf #得到一串连分数

def wienerAttack(e, n):
    cf=continuedFra(e,n)
    for (Q2,Q1) in getit(cf):#遍历得到的连分数，令分子分母分别是Q2，Q1
        if Q1 == 0:
            continue
        if N1%Q1==0 and Q1!=1:#满足这个条件就找到了
            return Q1,Q2
    print('not find!')

Q1,Q2 = wienerAttack(N1,N2)
P1 = gmpy2.iroot(N1//Q1,4)&#91;0]
P2 = gmpy2.iroot(N2//Q2,4)&#91;0]
phi1 = P1 * P1 * P1 * (P1-1) * (Q1-1)
phi2 = P2 * P2 * P2 * (P2-1) * (Q2-1)
d1 = gmpy2.invert(e,phi1)
d2 = gmpy2.invert(e,phi2)
m1 = long_to_bytes(gmpy2.powmod(c1,d1,N1))
m2 = long_to_bytes(gmpy2.powmod(c2,d2,N2))
print((m1 + m2))</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="1044" height="77" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-120.png" alt="" class="wp-image-4530" /> </figure> 

## 0x05 西湖论剑-YUSA的小秘密

stegsolver发现red plane 0和green plane 0都有数据<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-121.png" alt="" class="wp-image-4535" width="481" height="320" /> </figure> 

<pre class="wp-block-code"><code>from cv2 import cv2 as cv
img = cv.imread('yusa.png')
src = cv.cvtColor(img, cv.COLOR_BGR2YCrCb)
Y, Cr, Cb = cv.split(src)
cv.imwrite('Y.png', (Y % 2) * 255)
cv.imwrite('Cr.png', (Cr % 2) * 255)
cv.imwrite('Cb.png', (Cb % 2) * 255)</code></pre><figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-122.png" alt="" class="wp-image-4536" width="319" height="155" /> </figure> 

## 0x06 西湖论剑-Yusa的秘密 

`volatility -f Yusa-PC.raw --profile=Win7SP1x64 hashdump`,发现yusa用户，使用PTF爆破密码`YusaYusa520`，打开压缩包Who\_am\_I<figure class="wp-block-image size-full">

<img loading="lazy" width="1444" height="113" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-123.png" alt="" class="wp-image-4538" /> </figure> 

题目中提到Sakura组织，这里对文件进行搜索<figure class="wp-block-image size-full">

<img loading="lazy" width="1444" height="208" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-124.png" alt="" class="wp-image-4539" /> </figure> 

分别导出文件 Sakura-didi导出后是一个加密的压缩包 公告内容是`全体成员注意，我们将在11月20号，对地球发起总攻，请做好准备。` 备忘录的内容是`2021.11.15：请组织内的人务必删除所有不必要的联系方式，防止我们的计划出现问题。` 根据备忘录获取的信息，找一下联系方式有关的文件<figure class="wp-block-image size-full">

<img loading="lazy" width="1444" height="90" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-125.png" alt="" class="wp-image-4541" /> </figure> 

导出Mystery Man.contact，发现一串可疑的字符串<figure class="wp-block-image size-full">

<img loading="lazy" width="1444" height="212" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-126.png" alt="" class="wp-image-4542" /> </figure> 

```
LF2XGYPPXSGOPO4E465YPZMITLSYRGXGWS7OJOEL42O2LZFYQDSLRKXEXO56LCVB566IZ2FPW7S37K7HQK46LLUM42EJB354RTSL3IHFR6VONHEJ4S4ITZNEVHTJPNXJS62OHAECGZGCWWRVOBUXMNKMGJTTKTDZME2TKU3PGVMWS5ZVGVYUKYJSKY2TON3ZJU2VSK3WGVGHK3BVGVJW6NLBGZCDK33NKQ2WE6KBGU3XKRJVG52UQNJXOVNDKTBSM42TK4KFGVRGK3BVLFLTGNBUINBTKYTFNQ2VSVZTGVNEOOJVLJBU4NKMGZSDKNCXNY2UY4KHGVGHSZZVG52WMNSLMVCTKWLJLI2DIQ2DMEZFMNJXG54WCT2EJF3VSV2NGVGW2SJVLJVFKNCNKRIXSWLNJJUVS6SJGNMTERLZJ5KFM3KNK5HG2TSEM46Q====
```

解Base32得到<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-127.png" alt="" class="wp-image-4544" width="592" height="304" /> </figure> 

再解Base64得到一个key值`820ac92b9f58142bbbc27ca295f1cf48`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-128.png" alt="" class="wp-image-4545" width="589" height="259" /> </figure> 

解密压缩包得到key.bmp<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-129.png" alt="" class="wp-image-4547" width="195" height="195" /> </figure> 

在Yusa.contact中发现hint<figure class="wp-block-image size-full">

<img loading="lazy" width="1441" height="55" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-130.png" alt="" class="wp-image-4548" /> </figure> 

使用`pstree`查找下便笺相关的进程<figure class="wp-block-image size-full">

<img loading="lazy" width="1444" height="119" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-131.png" alt="" class="wp-image-4549" /> </figure> 

`volatility -f Yusa-PC.raw --profile=Win7SP1x64 memdump -p 2228 -D ./`导出进程，再使用`foremost -T 2228.dmp`进行分离 得到带密码的压缩包<figure class="wp-block-image size-full">

<img loading="lazy" width="1444" height="1099" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-132.png" alt="" class="wp-image-4550" /> </figure> 

在00003824.ole发现rtf文件<figure class="wp-block-image size-full">

<img loading="lazy" width="1444" height="244" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-133.png" alt="" class="wp-image-4551" /> </figure> 

删除掉多余的字符，构造rtf文件

```
{\rtf1\ansi\ansicpg936\deff0\deflang1033\deflangfe2052{\fonttbl{0\f0\fnil\fcharset134 \'ce\'a2\'c8\'ed\'d1\'c5\'ba\'da;}}{\*\generator Msftedit 5.41.21.2510;}\viewkind4\uc1\pard\tx336\tx672\tx1008\tx1344\tx1680\tx2016\tx2352\tx2688\tx3024\tx3360\tx3696\tx4032\tx4368\tx4704\tx5040\tx5376\tx5712\tx6048\tx6384\tx6720\tx7056\tx7392\tx7728\tx8064\tx8400\tx8736\tx9072\tx9408\tx9744\tx10080\tx10416\tx10752\highlight0\lang2052\f0\fs22\'d6\'d5\'d3\'da\'c4\'c3\'b5\'bd\'c1\'cb\'d7\'e9\'d6\'af\'b5\'c4\'ba\'cb\'d0\'c4\'c3\'dc\'c2\'eb\'a3\'ac\'ce\'d2\'b2\'bb\'cf\'eb\'d4\'d9\'b5\'b1\'ce\'d4\'b5\'d7\'c1\'cb\'a3\'ac\'ce\'d2\'cf\'eb\'b8\'cf\'bd\'f4\'c0\'eb\'bf\'aa\'d5\'e2\'b8\'f6\'b9\'ed\'b5\'d8\'b7\'bd\'a1\'a3\'ba\'cb\'d0\'c4\'c3\'dc\'c2\'eb\'ca\'c7\'a3\'ba\'ca\'c0\'bd\'e7\'c3\'bb\'c1\'cb\'d0\'c4\'cc\'f8\'a1\'a3\par }
```

打开得到`世界没了心跳`<figure class="wp-block-image size-full">

<img loading="lazy" width="1444" height="140" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-134.png" alt="" class="wp-image-4552" /> </figure> 

解压压缩包，得到exp，内容如下：

<pre class="wp-block-code"><code>from PIL import Image
import struct
pic = Image.open('key.bmp')
fp = open('flag', 'rb')
fs = open('Who_am_I', 'wb')

a, b = pic.size
list1 = &#91;]
for y in range(b):
    for x in range(a):
        pixel = pic.getpixel((x, y))
        list1.extend(&#91;pixel&#91;1], pixel&#91;0], pixel&#91;2], pixel&#91;2], pixel&#91;1], pixel&#91;0]])

data = fp.read()
for i in range(0, len(data)):
    fs.write(struct.pack('B', data&#91;i] ^ list1&#91;i % a*b*6]))
fp.close()
fs.close()</code></pre>

这是加密的过程，解密脚本如下：

<pre class="wp-block-code"><code>from PIL import Image
import struct
pic = Image.open('key.bmp')
fp = open('flag', 'wb')
fs = open('Who_am_I', 'rb')

a, b = pic.size
list1 = &#91;]
for y in range(b):
    for x in range(a):
        pixel = pic.getpixel((x, y))
        list1.extend(&#91;pixel&#91;1], pixel&#91;0], pixel&#91;2], pixel&#91;2], pixel&#91;1], pixel&#91;0]])

data = fs.read()
for i in range(0, len(data)):
    fp.write(struct.pack('B', data&#91;i] ^ list1&#91;i % a*b*6]))
fp.close()
fs.close()</code></pre>

得到flag，经过判断为gif文件<figure class="wp-block-image size-full">

<img loading="lazy" width="1444" height="84" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-135.png" alt="" class="wp-image-4554" /> </figure> 

我们用010editor打开，发现高度不对，6、7字节为宽， 8、9字节为高，且为小端序储存方式 ，修改为8、9字节为1D 10<figure class="wp-block-image size-full">

<img loading="lazy" width="1444" height="92" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-137.png" alt="" class="wp-image-4558" width="215" height="95" /></figure> 

打开可以看到flag<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-138.png" alt="" class="wp-image-4561" width="686" height="383" /> </figure> 

## 0x07 西湖论剑-hardrsa

[羊城杯 2020]Power魔改

```python
from Crypto.Util.number import *
import sympy
e = 0x10001
dp = 379476973158146550831004952747643994439940435656483772269013081580532539640189020020958796514224150837680366977747272291881285391919167077726836326564473
c = 57248258945927387673579467348106118747034381190703777861409527336272914559699490353325906672956273559867941402281438670652710909532261303394045079629146156340801932254839021574139943933451924062888426726353230757284582863993227592703323133265180414382062132580526658205716218046366247653881764658891315592607194355733209493239611216193118424602510964102026998674323685134796018596817393268106583737153516632969041693280725297929277751136040546830230533898514659714717213371619853137272515967067008805521051613107141555788516894223654851277785393355178114230929014037436770678131148140398384394716456450269539065009396311996040422853740049508500540281488171285233445744799680022307180452210793913614131646875949698079917313572873073033804639877699884489290120302696697425
c1 = 78100131461872285613426244322737502147219485108799130975202429638042859488136933783498210914335741940761656137516033926418975363734194661031678516857040723532055448695928820624094400481464950181126638456234669814982411270985650209245687765595483738876975572521276963149542659187680075917322308512163904423297381635532771690434016589132876171283596320435623376283425228536157726781524870348614983116408815088257609788517986810622505961538812889953185684256469540369809863103948326444090715161351198229163190130903661874631020304481842715086104243998808382859633753938512915886223513449238733721777977175430329717970940440862059204518224126792822912141479260791232312544748301412636222498841676742208390622353022668320809201312724936862167350709823581870722831329406359010293121019764160016316259432749291142448874259446854582307626758650151607770478334719317941727680935243820313144829826081955539778570565232935463201135110049861204432285060029237229518297291679114165265808862862827211193711159152992427133176177796045981572758903474465179346029811563765283254777813433339892058322013228964103304946743888213068397672540863260883314665492088793554775674610994639537263588276076992907735153702002001005383321442974097626786699895993544581572457476437853778794888945238622869401634353220344790419326516836146140706852577748364903349138246106379954647002557091131475669295997196484548199507335421499556985949139162639560622973283109342746186994609598854386966520638338999059


g = 2
y = 449703347709287328982446812318870158230369688625894307953604074502413258045265502496365998383562119915565080518077360839705004058211784369656486678307007348691991136610142919372779782779111507129101110674559235388392082113417306002050124215904803026894400155194275424834577942500150410440057660679460918645357376095613079720172148302097893734034788458122333816759162605888879531594217661921547293164281934920669935417080156833072528358511807757748554348615957977663784762124746554638152693469580761002437793837094101338408017407251986116589240523625340964025531357446706263871843489143068620501020284421781243879675292060268876353250854369189182926055204229002568224846436918153245720514450234433170717311083868591477186061896282790880850797471658321324127334704438430354844770131980049668516350774939625369909869906362174015628078258039638111064842324979997867746404806457329528690722757322373158670827203350590809390932986616805533168714686834174965211242863201076482127152571774960580915318022303418111346406295217571564155573765371519749325922145875128395909112254242027512400564855444101325427710643212690768272048881411988830011985059218048684311349415764441760364762942692722834850287985399559042457470942580456516395188637916303814055777357738894264037988945951468416861647204658893837753361851667573185920779272635885127149348845064478121843462789367112698673780005436144393573832498203659056909233757206537514290993810628872250841862059672570704733990716282248839

x=sympy.discrete_log(y,c1,g)
print(x)

a = sympy.Symbol('a')
p = sympy.solve(2019*a**2+2020*a**3+2021*a**4-x,a)[0]
print(p)
print(long_to_bytes(pow(c,dp,int(p))))
```

<img loading="lazy" width="1444" height="219" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-139.png" alt="" class="wp-image-4563" /> </figure> 

## 0x08 西湖论剑-密码人集合

nc连接访问

<pre class="wp-block-code"><code>------------------------------
论 *  *  | *  *  *  | *  *  一
*  *  *  | 要 *  一 | *  *  * 
*  一 西 | *  论 第 | *  我 * 
------------------------------
*  要 *  | *  一 *  | *  *  剑
*  *  *  | *  *  湖 | *  *  * 
*  *  *  | *  *  *  | *  湖 * 
------------------------------
*  *  一 | *  第 *  | *  *  * 
剑 *  *  | *  *  *  | *  *  * 
西 *  *  | 一 湖 *  | *  第 * 
------------------------------</code></pre>

可以发现是西湖论剑我要拿第一中的几个字构成的数独，用数字替换，得到

<pre class="wp-block-code"><code>------------------------------
6 *  *  | *  *  *  | *  *  9
*  *  *  | 2 *  9 | *  *  * 
*  9 4 | *  6 8 | *  1 * 
------------------------------
*  2 *  | *  9 *  | *  *  7
*  *  *  | *  *  5 | *  *  * 
*  *  *  | *  *  *  | *  5 * 
------------------------------
*  *  9 | *  8 *  | *  *  * 
7 *  *  | *  *  *  | *  *  * 
4 *  *  | 9 5 *  | *  8 * 
----------------------------</code></pre>

在线求解，去掉换行得到`612534879378219465594768213125893647836475921947126358259681734781342596463957182`，替换得到，`论我要湖拿西第剑一拿剑第要我一西论湖湖一西剑论第要我拿我要湖第一拿论西剑第拿论西剑湖一要我一西剑我要论拿湖第要湖一论第我剑拿西剑第我拿西要湖一论西论拿一湖剑我第要`<figure class="wp-block-image size-full">

<img loading="lazy" width="1444" height="575" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-140.png" alt="" class="wp-image-4565" /> </figure>

[1]: blob:http://81.70.81.64/f9b3f30c-0d27-4e6d-a5fb-f2c95fcac110
[2]: https://image-1303962289.cos.ap-beijing.myqcloud.com/image/20210119143922.png
