# HGAME 2022 week1(writeup)



## 0x00 Easy RSA {#0x00-easy-rsa}

描述  
这 RSA 不是有手就行？！  
(100分的题能拿125分，这不血赚)

```python
from math import gcd
from random import randint
from gmpy2 import next_prime
from Crypto.Util.number import getPrime
from secret import flag

def encrypt(c):
    p = getPrime(8)
    q = getPrime(8)
    e = randint(0, p * q)
    while gcd(e, (p - 1) * (q - 1)) != 1:
        e = int(next_prime(e))
    return e, p, q, pow(ord(c), e, p * q)

if __name__ == '__main__':
    print(list(map(encrypt, flag)))
    # [(12433, 149, 197, 104), (8147, 131, 167, 6633), (10687, 211, 197, 35594), (19681, 131, 211, 15710), (33577, 251, 211, 38798), (30241, 157, 251, 35973), (293, 211, 157, 31548), (26459, 179, 149, 4778), (27479, 149, 223, 32728), (9029, 223, 137, 20696), (4649, 149, 151, 13418), (11783, 223, 251, 14239), (13537, 179, 137, 11702), (3835, 167, 139, 20051), (30983, 149, 227, 23928), (17581, 157, 131, 5855), (35381, 223, 179, 37774), (2357, 151, 223, 1849), (22649, 211, 229, 7348), (1151, 179, 223, 17982), (8431, 251, 163, 30226), (38501, 193, 211, 30559), (14549, 211, 151, 21143), (24781, 239, 241, 45604), (8051, 179, 131, 7994), (863, 181, 131, 11493), (1117, 239, 157, 12579), (7561, 149, 199, 8960), (19813, 239, 229, 53463), (4943, 131, 157, 14606), (29077, 191, 181, 33446), (18583, 211, 163, 31800), (30643, 173, 191, 27293), (11617, 223, 251, 13448), (19051, 191, 151, 21676), (18367, 179, 157, 14139), (18861, 149, 191, 5139), (9581, 211, 193, 25595)]
```

根据题目我们知道列表里的每一个元组就能通过rsa解密出一个字符，然后把他们拼凑在一起就能得到flag，脚本如下：

<pre class="wp-block-code"><code>flag = ''
for i in range(len(res)):
	e = res&#91;i]&#91;0]
	p = res&#91;i]&#91;1]
	q = res&#91;i]&#91;2]
	c = res&#91;i]&#91;3]
	n = p*q
	phi = (p-1)*(q-1)
	d = gmpy2.invert(e,phi)
	flag += chr(pow(c,d,n))
print(flag)</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="395" height="40" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-173.png" alt="" class="wp-image-5073" /> </figure> 

## 0x01 饭卡的uno {#0x01-饭卡的uno}

描述  
饭卡今天第一天学iot 然后他的好朋友Actue让他先去学uno 然后悄悄给饭卡塞了一个固件

一开始被iot吓到了，后来发现解出来的人挺多的，用010打开文件，发现flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="910" height="141" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-174.png" alt="" class="wp-image-5074" /> </figure> 

## 0x02 Flag Checker {#0x02-flag-checker}

描述  
A Flag Checker,can you pass this check?

用jeb打开文件，分析代码，怀疑是rc4加密，`carol`是key，`mg6CITV6GEaFDTYnObFmENOAVjKcQmGncF90WhqvCFyhhsyqq1s=`是加密后的密文。<figure class="wp-block-image size-full">

<img loading="lazy" width="1213" height="187" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-175.png" alt="" class="wp-image-5075" /></figure> 

找个在线网站，解密rc4，得到flag。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-177.png" alt="" class="wp-image-5077" width="617" height="389" /> </figure> 

## 0x03 好康的流量 {#0x03-好康的流量}

描述  
总所周知 饭卡是个LSP并十分喜欢向其他人推销他的涩图 让我们去悄悄康康他发了什么

wireshark打开追踪流，发现一段很像图片的base64<figure class="wp-block-image size-full">

<img loading="lazy" width="896" height="511" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-182.png" alt="" class="wp-image-5082" /> </figure> 

放到cyberchef里面转一下<figure class="wp-block-image size-full">

<img loading="lazy" width="1528" height="771" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-183.png" alt="" class="wp-image-5083" /> </figure> 

另存图片后用stegsolve在Green plane 2得到一段条形码，用支付宝扫描得到`hgame{ez_1mg_`<figure class="wp-block-image size-full">

<img loading="lazy" width="1303" height="822" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-184.png" alt="" class="wp-image-5084" /> </figure> 

然后发现lsb隐写，后半段为`Steg4n0graphy}`<figure class="wp-block-image size-full">

<img loading="lazy" width="1082" height="841" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-185.png" alt="" class="wp-image-5085" /> </figure> 

## 0x04 群青(其实是幽灵东京） {#0x04-群青-其实是幽灵东京}

描述  
4CTU3从小就是Yoasobi的狂热粉丝 今天它给大家带来了一首它觉得很好听的老歌 它说你要用多感官去感觉

用au打开wav，发现`Yoasobi`<figure class="wp-block-image size-full">

<img loading="lazy" width="527" height="322" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-178.png" alt="" class="wp-image-5078" /> </figure> 

在详细信息里面，有暗示使用silenteye<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-179.png" alt="" class="wp-image-5079" width="428" height="567" /> </figure> 

解密得到一段url，浏览器输入把附件下载下来。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-180.png" alt="" class="wp-image-5080" width="662" height="526" /> </figure> 

得到S\_S\_T_V.wav看名字听声音就知道需要把sstv信号转成图片，手机上用robot36读取，得到一张二维码，扫描即可得到结果`hgame{1_c4n_5ee_the_wav}`。<figure class="wp-block-image size-full">

<img loading="lazy" width="320" height="240" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-181.png" alt="" class="wp-image-5081" /> </figure> 

## 0x05 蛛蛛...嘿嘿♥我的蛛蛛 {#0x05-蛛蛛-嘿嘿-我的蛛蛛}

描述  
蛛蛛...嘿嘿...我的蛛蛛...我的蛛蛛正在满地找头？？？

需要不断点击进入下一关，找到flag，感觉没多少关，可以手撕。<figure class="wp-block-image size-full">

<img loading="lazy" width="1351" height="692" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-186.png" alt="" class="wp-image-5088" /> </figure> 

过第100关后得到<figure class="wp-block-image size-full">

<img loading="lazy" width="1054" height="250" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-187.png" alt="" class="wp-image-5089" /> </figure> 

查看源代码，没有啥信息，想起题目说的头，联想到header，用插件打开发现flag。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-188.png" alt="" class="wp-image-5090" width="678" height="466" /> </figure> 

官方wp提供的爬虫脚本，这里微调一下

<pre class="wp-block-code"><code>import requests,regex

nextURL = base = 'http://hgame-spider.vidar.club/xxx'
while 1:
	keys = regex.findall('&lt;a href=\"(\S+)\">点我试试&lt;/a>',requests.get(nextURL).text)
	if len(keys) == 0:
		break
	nextURL = base + keys&#91;0]
print(nextURL)
print(requests.get(nextURL).headers)</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="1449" height="196" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-212.png" alt="" class="wp-image-5149" /> </figure> 

## 0x06 Tetris plus {#0x06-tetris-plus}

js小游戏，找到对应的js文件checking.js，发现可疑代码。<figure class="wp-block-image size-full">

<img loading="lazy" width="948" height="134" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-189.png" alt="" class="wp-image-5092" /> </figure> 

base64解密得到flag和一段乱码，明显不是真的flag。然后把后面一大段js代码输入控制台，得到flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="1893" height="408" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-190.png" alt="" class="wp-image-5093" /> </figure> 

## 0x07 这个压缩包有点麻烦 {#0x07-这个压缩包有点麻烦}

描述  
这个压缩包，它真的可以打开吗？

压缩包注释里面有Pure numeric passwords within 6 digits are not safe!，所以直接爆破即可解出下一层。

在ReadMe里面写有I don't know if it's a good idea to write down all the passwords.，还给出了password-note文件，包含压缩包的密码，所以可以用字典攻击进入下一层。<figure class="wp-block-image size-full">

<img loading="lazy" width="283" height="403" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-191.png" alt="" class="wp-image-5095" /> </figure> 

ReadMe的内容是If you don't like to spend time compressing files, just stores them.感觉没什么用，这里卡了很久，然后试试明文攻击，`bkcrack -C flag.zip -c README.txt -p README.txt`。<figure class="wp-block-image size-full">

<img loading="lazy" width="1100" height="227" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-192.png" alt="" class="wp-image-5098" /> </figure> 

得到key后，提取一下flag.jpg文件。<figure class="wp-block-image size-full">

<img loading="lazy" width="1429" height="109" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-194.png" alt="" class="wp-image-5101" width="294" height="197" /></figure> 

binwalk发现存在压缩包，提取出来。<figure class="wp-block-image size-full">

<img loading="lazy" width="1008" height="131" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-195.png" alt="" class="wp-image-5102" /> </figure> 

压缩包伪加密，解压得到真flag为`hgame{W0w!_y0U_Kn0w_z1p_3ncrYpt!}`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-196.png" alt="" class="wp-image-5103" width="457" height="48" /> </figure> 

## 0x08 Fujiwara Tofu Shop {#0x08-fujiwara-tofu-shop}

描述  
昨晚我输给一辆AE86。他用惯性漂移过弯，他的车很快，我只看到他有个豆腐店的招牌。<figure class="wp-block-image size-full">

<img loading="lazy" width="602" height="338" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-197.png" alt="" class="wp-image-5107" /> </figure> 

burp抓包，添加Referer字段<figure class="wp-block-image size-full">

<img loading="lazy" width="1800" height="581" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-198.png" alt="" class="wp-image-5108" /> </figure> 

通行证联想到User-Agent，修改后重发。<figure class="wp-block-image size-full">

<img loading="lazy" width="1797" height="565" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-199.png" alt="" class="wp-image-5109" /> </figure> 

明显修改cookie，响应包里面有flavor为草莓的字段，所以格式应该差不多。<figure class="wp-block-image size-full">

<img loading="lazy" width="1749" height="554" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-200.png" alt="" class="wp-image-5110" /> </figure> 

在响应包找到gasline，在请求包把值设为100。<figure class="wp-block-image size-full">

<img loading="lazy" width="1686" height="543" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-202.png" alt="" class="wp-image-5112" /> </figure> 

本地请求，尝试X-Forwarded-For发现有拦截，尝试X-Real-IP得到flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="1575" height="471" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-201.png" alt="" class="wp-image-5111" /> </figure> 

解法2：把X-Forworded-For的ip写两遍<figure class="wp-block-image size-full">

<img loading="lazy" width="1617" height="497" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-210.png" alt="" class="wp-image-5146" /> </figure> 

来自官方wp的笔记

IP 伪造和代理服务器有关，相关的请求头有X-Forworded-For,X-Real-IP,X-Client-IP等，至于那个请求头能成功伪造 IP，得参考具体的网络环境，编程语言，服务端框架和服务端配置。返回头里给出了后端框架：gin-gonic/gin，预期解法是让大家去查一查 gin 是怎样处理这些请求头的，不过好像没人去查www。(<a href="https://github.com/gin-gonic/gin/issues/1684" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://github.com/gin-gonic/gin/issues/1684</a>)

## 0x09 English Novel {#0x09-english-novel}

描述  
为了学好四六级，协会里某不知名的康师傅决定通过看英文小说来提高自己的英语水平。  
可不知道为什么，下载来的小说竟然都被打乱并加密了。  
他费尽千辛万苦重要找到了一部分小说的原文，你能帮帮他么？

我们能拿到部分明文和密文，但他们的顺序是打乱的，难搞。其实我们可以用大小排序，然后发现每个part最多是410字节，我们拿到的flag.enc的长度是45，所以可以先从短的找出对应，推理出key。

<pre class="wp-block-code"><code>m1 = '"Then we have won back what we had before," said Boxer.'
c1 = '"Nhoa ul mwmv bbd kfez wbzl dm ded epcnrk," uiii Zogaq.'

m2 = 'ge of wearing green ribbons on their tails on Sundays.'
c2 = 'wy ys ulyweex leusw txrbimk vv plequ qzirv yp Szabaho.'

m3 = 'to be more frightened of the pigs or of the human visitors.'
c3 = 'ji lr kvpj wialujswjf ef szr xecw wu le zkh jcmfa vrohxivp.'

m4 = 'arter of an hour and put an end to any chance of discussion.'
c4 = 'qltoe mm fj ygze owi ekt zf lvz xo dyv cndqmg ok bibytwmmle.'

m5 = 'apoleon himself, which was always served to him in the Crown Derby soup tureen.'
c5 = 'qjovrrl fnijvdk, kqnew wur nsewuw ahcsdd wr jqm vl cdd Wvlnr Knxqi puxa imjkgf.'</code></pre>

这里找到五段对应的明文和密文，然后分析算法。

<pre class="wp-block-code"><code>def decrypt(data, key):
    assert len(data) &lt;= len(key)
    result = ""
    for i in range(len(data)):
        if data&#91;i].isupper():
            result += chr((ord(data&#91;i]) - ord('A') + key&#91;i]) % 26 + ord('A'))
        elif data&#91;i].islower():
            result += chr((ord(data&#91;i]) - ord('a') + key&#91;i]) % 26 + ord('a'))
        else:
            result += data&#91;i]
    return result</code></pre>

可以通过爆破key[i]的值来与明文进行对比，从而得到key的值，同时，只有一段文字是不够的，因为中间有特殊符号和空格等，key会跳过这些，所以需要多段的key来组合。

<pre class="wp-block-code"><code>def getkey(c,m):
	key=&#91;]
	for i in range(len(c)):
		result=''
		l=&#91;]
		if c&#91;i].isupper():
			for j in range(0,256):
				result = chr((ord(c&#91;i]) - ord('A') + j) % 26 + ord('A'))
				if result==m&#91;i]:
					key.append(j)
					break
		elif c&#91;i].islower():
			for j in range(0,256):
				result = chr((ord(c&#91;i]) - ord('a') + j) % 26 + ord('a'))
				if result==m&#91;i]:
					key.append(j)
					break
		else:
			key.append(-1)
	return key</code></pre>
运行后得到

```
key1= [-1, 6, 0, 16, 13, -1, 2, 19, -1, 21, 4, 9, 9, -1, 21, 13, 10, -1, 17, 21, 24, 11, -1, 0, 6, 1, 8, -1, 19, 18, -1, 4, 22, 0, -1, 23, 15, 3, 1, 0, 20, -1, -1, -1, 24, 18, 0, 21, -1, 2, 0, 17, 4, 1, -1]
key2= [10, 6, -1, 16, 13, -1, 2, 19, 2, 21, 4, 9, 9, -1, 21, 13, 10, 12, 17, -1, 24, 11, 10, 0, 6, 1, 8, -1, 19, 18, -1, 4, 22, 0, 18, 23, -1, 3, 1, 0, 20, 23, -1, 16, 24, -1, 0, 21, 13, 2, 0, 17, 4, -1]
key3= [10, 6, -1, 16, 13, -1, 2, 19, 2, 21, -1, 9, 9, 8, 21, 13, 10, 12, 17, 21, 24, -1, 10, 0, -1, 1, 8, 13, -1, 18, 4, 4, 22, -1, 18, 23, -1, 3, 1, -1, 20, 23, 23, -1, 24, 18, 0, 21, 13, -1, 0, 17, 4, 1, 22, 6, 22, 3, -1]
key4= [10, 6, 0, 16, 13, -1, 2, 19, -1, 21, 4, -1, 9, 8, 21, 13, -1, 12, 17, 21, -1, 11, 10, 0, -1, 1, 8, -1, 19, 18, 4, -1, 22, 0, -1, 23, 15, 3, -1, 0, 20, 23, 23, 16, 24, -1, 0, 21, -1, 2, 0, 17, 4, 1, 22, 6, 22, 3, 9, -1]
key5= [10, 6, 0, 16, 13, 23, 2, -1, 2, 21, 4, 9, 9, 8, 21, -1, -1, 12, 17, 21, 24, 11, -1, 0, 6, 1, -1, 13, 19, 18, 4, 4, 22, -1, 18, 23, 15, 3, 1, 0, -1, 23, 23, -1, 24, 18, 0, -1, 13, 2, -1, 17, 4, 1, -1, 6, 22, 3, 9, 22, -1, 19, 17, 20, 11, 16, -1, 3, 20, 23, 15, -1, 11, 8, 8, 20, 24, 8, -1]
```

整理得到最后的key

```
key=[10,6,0,16,13,23,2,19,2,21,4,9,9,8,21,13,10,12,17,21,24,11,10,0,6,1,8,13,19,18,4,4,22,0,18,23,15,3,1,0,20,23,23,16,24,18,0,21,13,2,0,17,4,1]
```

使用加密方法得到flag<figure class="wp-block-image size-full">

<img loading="lazy" width="465" height="41" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-203.png" alt="" class="wp-image-5114" /> </figure> 

## 0x0A easy_auth {#0x0a-easy-auth}

描述  
尊贵的admin写了个todo帮助自己管理日常，但他好像没调试完就部署了....一个月后，当他再一次打开他的小网站，似乎忘记了密码...他的todo之前记录了很重要的东西，快帮帮他  
不要爆破！

首先在用户登录页面发现存在login.js文件，关键代码为匹配用户名密码，设置token。<figure class="wp-block-image size-full">

<img loading="lazy" width="1206" height="785" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-205.png" alt="" class="wp-image-5119" /> </figure> 

这里注册用户后登录，抓包，在响应包里获取到token。<figure class="wp-block-image size-full">

<img loading="lazy" width="1888" height="522" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-206.png" alt="" class="wp-image-5120" /> </figure> 

联想到jwt伪造，修改username，重发包。<figure class="wp-block-image size-full">

<img loading="lazy" width="1248" height="506" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-207.png" alt="" class="wp-image-5121" /> </figure> 

发送包，发现被拦截了有问题。<figure class="wp-block-image size-full">

<img loading="lazy" width="1835" height="419" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-208.png" alt="" class="wp-image-5122" /> </figure> 

这里卡了挺久的，后来又注册了一个用户进行实验，发现验证和id有关，猜测admin的id为1，继续伪造jwt，成功获取到flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="1862" height="538" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-209.png" alt="" class="wp-image-5123" /> </figure> 

## 0x0B Matryoshka(复现) {#0x0b-matryoshka-复现}

描述  
某天饭卡捡到了张奇怪的纸条。  
上面写满了奇奇怪怪的字符。  
纸条背面还写着奇怪的话：“Caesar：21; Vigenère:hgame”。  
你能看懂上面写了什么吗？

文件里面是盲文

```
⠨⠨⠤⠌⠤⠤⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠤⠤⠤⠤⠤⠌⠤⠤⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠤⠤⠤⠨⠨⠌⠨⠨⠨⠤⠤⠌⠤⠤⠨⠨⠤⠤⠌⠨⠤⠨⠨⠌⠨⠨⠨⠨⠤⠌⠤⠤⠨⠨⠤⠤⠌⠨⠨⠤⠤⠤⠌⠨⠨⠨⠨⠤⠌⠤⠤⠨⠨⠤⠤⠌⠨⠨⠤⠤⠤⠌⠤⠤⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠨⠤⠨⠤⠌⠤⠨⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠨⠨⠨⠤⠌⠨⠨⠨⠨⠤⠌⠤⠤⠨⠨⠤⠤⠌⠨⠨⠨⠨⠤⠌⠤⠤⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠤⠤⠤⠨⠨⠌⠨⠨⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠤⠤⠤⠨⠨⠌⠤⠤⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠨⠨⠨⠤⠌⠤⠨⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠤⠤⠤⠨⠨⠌⠨⠨⠨⠤⠤⠌⠤⠤⠨⠨⠤⠤⠌⠨⠤⠤⠤⠤⠌⠤⠤⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠤⠤⠨⠨⠨⠌⠨⠨⠨⠤⠤⠌⠤⠤⠨⠨⠤⠤⠌⠨⠨⠨⠤⠌⠨⠨⠨⠨⠤⠌⠤⠤⠨⠨⠤⠤⠌⠤⠨⠌⠨⠨⠨⠨⠤⠌⠤⠤⠨⠨⠤⠤⠌⠤⠤⠤⠤⠨⠌⠤⠤⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠤⠤⠨⠨⠨⠌⠨⠨⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠨⠨⠤⠌⠤⠨⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠨⠤⠨⠨⠌⠨⠨⠨⠨⠤⠌⠤⠤⠨⠨⠤⠤⠌⠨⠤⠤⠤⠤⠌⠤⠤⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠨⠌⠤⠨⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠤⠤⠤⠤⠨⠌⠨⠨⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠤⠤⠤⠨⠨⠌⠨⠨⠨⠤⠤⠌⠤⠤⠨⠨⠤⠤⠌⠨⠤⠤⠤⠤⠌⠤⠤⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠨⠨⠤⠌⠨⠨⠨⠨⠤⠌⠤⠤⠨⠨⠤⠤⠌⠨⠨⠨⠤⠌⠨⠨⠨⠨⠤⠌⠤⠤⠨⠨⠤⠤⠌⠨⠤⠤⠤⠤⠌⠨⠨⠨⠤⠤⠌⠤⠤⠨⠨⠤⠤⠌⠨⠤⠨⠤⠌⠨⠨⠨⠨⠤⠌⠤⠤⠨⠨⠤⠤⠌⠤⠤⠨⠨⠨⠌⠨⠨⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠤⠨⠨⠨⠨⠌⠨⠨⠨⠨⠤⠌⠤⠤⠨⠨⠤⠤⠌⠤⠤⠨⠨⠨⠌⠨⠨⠨⠨⠤⠌⠤⠤⠨⠨⠤⠤⠌⠤⠤⠤⠤⠤⠌⠤⠤⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠨⠌⠤⠨⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠨⠤⠤⠤⠤⠌⠨⠨⠨⠨⠤⠌⠤⠤⠨⠨⠤⠤⠌⠤⠨⠨⠨⠨⠌⠤⠤⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠤⠤⠤⠤⠤⠌⠨⠨⠨⠤⠤⠌⠤⠤⠨⠨⠤⠤⠌⠤⠤⠤⠨⠨⠌⠤⠤⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠨⠨⠤⠤⠤⠌⠨⠨⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠨⠨⠨⠨⠤⠌⠤⠤⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠨⠤⠨⠤⠌⠤⠨⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠤⠨⠨⠨⠨⠌⠨⠨⠨⠤⠤⠌⠤⠤⠨⠨⠤⠤⠌⠨⠤⠤⠤⠤⠌⠨⠨⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠨⠤⠤⠤⠤⠌⠨⠨⠨⠨⠤⠌⠤⠤⠨⠨⠤⠤⠌⠤⠤⠨⠨⠨⠌⠨⠨⠨⠤⠤⠌⠤⠤⠨⠨⠤⠤⠌⠤⠤⠨⠨⠨⠌⠤⠤⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠤⠨⠨⠨⠨⠌⠤⠨⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠨⠨⠨⠨⠤⠌⠤⠤⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠤⠤⠨⠨⠨⠌⠨⠨⠨⠤⠤⠌⠤⠤⠨⠨⠤⠤⠌⠨⠤⠨⠤⠌⠤⠨⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠨⠨⠤⠌⠨⠨⠨⠨⠤⠌⠤⠤⠨⠨⠤⠤⠌⠨⠌⠨⠨⠨⠨⠤⠌⠤⠤⠨⠨⠤⠤⠌⠨⠨⠨⠨⠤⠌⠤⠨⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠨⠨⠨⠨⠨⠌⠤⠨⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠨⠨⠨⠨⠤⠌⠨⠨⠨⠨⠤⠌⠤⠤⠨⠨⠤⠤⠌⠨⠨⠨⠨⠨⠌⠨⠨⠨⠤⠤⠌⠤⠤⠨⠨⠤⠤⠌⠤⠤⠤⠨⠨⠌⠤⠨⠨⠨⠨⠌⠤⠤⠨⠨⠤⠤⠌⠨⠨⠨⠨⠤⠌⠨⠨⠨⠨⠤⠌⠤⠤⠨⠨⠤⠤⠌⠨⠨⠨⠨⠤⠌⠤⠨⠨⠨⠨
```

转换一下，得到摩斯电码

```
..-/--.../--..--/-----/--.../--..--/---../...--/--..--/.-../....-/--..--/..---/....-/--..--/..---/--.../--..--/.-.-/-..../--..--/...-/....-/--..--/....-/--.../--..--/---../...../--..--/---../--.../--..--/...-/-..../--..--/---../...--/--..--/.----/--.../--..--/--.../...--/--..--/...-/....-/--..--/-./....-/--..--/----./--.../--..--/--.../...../--..--/..-/-..../--..--/.-../....-/--..--/.----/--.../--..--/./-..../--..--/----./...../--..--/---../...--/--..--/.----/--.../--..--/..-/....-/--..--/...-/....-/--..--/.----/...--/--..--/.-.-/....-/--..--/--.../...../--..--/-..../....-/--..--/--.../....-/--..--/-----/--.../--..--/./-..../--..--/.----/....-/--..--/-..../--.../--..--/-----/...--/--..--/---../--.../--..--/..---/...../--..--/....-/--.../--..--/.-.-/-..../--..--/-..../...--/--..--/.----/...../--..--/.----/....-/--..--/--.../...--/--..--/--.../--.../--..--/-..../-..../--..--/....-/--.../--..--/--.../...--/--..--/.-.-/-..../--..--/..-/....-/--..--/./....-/--..--/....-/-..../--..--/...../-..../--..--/....-/....-/--..--/...../...--/--..--/---../-..../--..--/....-/....-/--..--/....-/-....
```

解码得到

```
u7,07,83,l4,24,27,ā6,v4,47,85,87,v6,83,17,73,v4,n4,97,75,u6,l4,17,e6,95,83,17,u4,v4,13,ā4,75,64,74,07,e6,14,67,03,87,25,47,ā6,63,15,14,73,77,66,47,73,ā6,u4,e4,46,56,44,53,86,44
```

感觉这个解码很不对劲，尝试把摩斯电码reverse

```
....-/-..../--..--/-..../-..../--..--/....-/..---/--..--/--.../...../--..--/-..../-..../--..--/....-/...../--..--/....-/-..../--..--/-...././--..--/-..../-../--..--/....-/-.-./--..--/--.../...--/--..--/...--/-..../--..--/....-/....-/--..--/...--/...--/--..--/--.../...--/--..--/-..../----./--..--/...../----./--..--/--.../....-/--..--/....-/-.-./--..--/...--/-..../--..--/...../---../--..--/...--/..---/--..--/--.../-----/--..--/...--/....-/--..--/-..../----./--..--/....-/./--..--/...--/-----/--..--/-..../...--/--..--/-..../....-/--..--/...../...--/--..--/-..../-.-./--..--/--.../----./--..--/-..../-.../--..--/-..../-../--..--/...--/----./--..--/--.../..---/--..--/...../.----/--..--/....-/./--..--/...--/----./--..--/-..../..-./--..--/....-/-../--..--/...../...--/--..--/...--/.----/--..--/-..../.-/--..--/-..../-.../--..--/--.../...--/--..--/...--/----./--..--/--.../..---/--..--/....-/-.../--..--/...--/..---/--..--/...../..---/--..--/...--/-..../--..--/-..../-.../--..--/....-/-.-./--..--/...--/---../--..--/-..../---../--..--/-..../..-./--..--/--.../..---/--..--/...--/-----/--..--/...--/-..
```

得到

```
46,66,42,75,66,45,46,6E,6D,4C,73,36,44,33,73,69,59,74,4C,36,58,32,70,34,69,4E,30,63,64,53,6C,79,6B,6D,39,72,51,4E,39,6F,4D,53,31,6A,6B,73,39,72,4B,32,52,36,6B,4C,38,68,6F,72,30,3D
```

然后再转hex

<pre class="wp-block-code"><code>FfBufEFnmLs6D3siYtL6X2p4iN0cdSlykm9rQN9oMS1jks9rK2R6kL8hor0=</code></pre>

尝试base64无果，就卡在这里了。

学习wp知道，这里需要用维基利亚解密。

<pre class="wp-block-code"><code>YzBibXZnaHl6X3swUmF6X2d4eG0wdGhrem9fMG9iMG1fdm9rY2N6dF8hcn0=</code></pre>

然后得到

<pre class="wp-block-code"><code>c0bmvghyz_{0Raz_gxxm0thkzo_0ob0m_vokcczt_!r}</code></pre>

然后是栅栏密码（22）

<pre class="wp-block-code"><code>cbvhz{Rzgx0hz_o0_ocz_r0mgy_0a_xmtko0bmvkct!}</code></pre>

最后是凯撒密码（21）

<pre class="wp-block-code"><code>hgame{Welc0me_t0_the_w0rld_0f_crypt0graphy!}</code></pre>

## 0x0C Dancing Line(复现) {#0x0c-dancing-line-复现}

描述  
这条路弯弯曲曲的，到底通向哪里呢？

老实说，这题毫无头绪。<figure class="wp-block-image size-full">

<img loading="lazy" width="581" height="693" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-213.png" alt="" class="wp-image-5150" /> </figure> 

wp上说一个字符的 ASCII码有 8 位，图像中的每两个黑色色块间的路程也为 8 步。从左上角的色块出发，向右为 0，向下为 1，连起来就是对应字符的 ASCII 码。

<pre class="wp-block-code"><code>import numpy as np
from PIL import Image
# 判断下一步往哪走
def search(arr, x, y):
	if y+1&lt;arr.shape&#91;1] and (arr&#91;x, y+1, :] != 255).all():
		return x, y+1, 0
	elif x+1&lt;arr.shape&#91;0]:
		return x+1, y, 1
	else:
		return -1, -1, -1

if __name__ == "__main__":
	image = Image.open("Dancing Line.bmp")
	array = np.array(image)
	x = y = 0
	while True:
		asc = 0
		# 每八步拼接成一个字符的 ASCII 码
		for _ in range(8):
			x, y, v = search(array, x, y)
			if v&lt;0:
				exit()
			asc &lt;&lt;= 1
			asc |= v
		print(chr(asc), end = "")</code></pre>
