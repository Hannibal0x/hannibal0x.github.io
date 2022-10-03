# 攻防世界-mobile（新手篇2）

<div class="has-toc have-toc">
</div>
## 0x00 easyjava

<figure class="wp-block-image size-full">

<img loading="lazy" width="960" height="540" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-150.png" alt="" class="wp-image-5042" /> </figure> 

jeb打开，分析关键代码，首先我们知道flag{}内的内容通过v4和v5加密得出的v3，最后为`wigwrkaugala`，所以逆推出解密的步骤就能得到flag。分析参考：<a href="https://www.cnblogs.com/cainiao-chuanqi/p/13565030.html" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.cnblogs.com/cainiao-chuanqi/p/13565030.html</a><figure class="wp-block-image size-full">

<img loading="lazy" width="703" height="672" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-151.png" alt="" class="wp-image-5043" /> </figure> 

先分析v4，得到是c的数组左移2位，结果是`17 23 7 22 1 16 6 9 21 0 15 5 10 18 2 24 4 11 3 14 19 12 20 13 8 25`<figure class="wp-block-image size-full">

<img loading="lazy" width="710" height="279" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-152.png" alt="" class="wp-image-5044" /> </figure> 

再分析v5，得到c的数组左移3位，结果是`21 4 24 25 20 5 15 9 17 6 13 3 18 12 10 19 0 22 2 11 23 1 8 7 14 16`<figure class="wp-block-image size-full">

<img loading="lazy" width="708" height="272" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-153.png" alt="" class="wp-image-5045" /> </figure> 

b类的a函数，该函数首先获取传进来的字符在字符串b.b中的索引，然后得到在b类中定义的整形数组中与该索引相等的在数组中的索引，然后调用b类的a()函数，将b类中数组与字符串左移一位，然后返回该数组索引。<figure class="wp-block-image size-full">

<img loading="lazy" width="566" height="573" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-154.png" alt="" class="wp-image-5046" /></figure> 

a类中的a(int)函数，该函数首先获取与传进来的参数相等的数组中的值的索引，然后获取在字符串中索引为该数组索引的字符，最后返回该字符，当然，其中也调用a()函数，但是该函数要求等于25，所以形同虚设。<figure class="wp-block-image size-full">

<img loading="lazy" width="465" height="721" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-156.png" alt="" class="wp-image-5048" /> </figure> 

所以整理解密的脚本如下：

<pre class="wp-block-code"><code>cipherText = 'wigwrkaugala'

aArray = &#91;21,4,24,25,20,5,15,9,17,6,13,3,18,12,10,19,0,22,2,11,23,1,8,7,14,16]
aString = 'abcdefghijklmnopqrstuvwxyz'

bArray = &#91;17,23,7,22,1,16,6,9,21,0,15,5,10,18,2,24,4,11,3,14,19,12,20,13,8,25]
bString = 'abcdefghijklmnopqrstuvwxyz'

def changeBArrayandString():
	global bString
	global bArray
	chArray = bArray&#91;0]
	chString = bString&#91;0:1]
	for i in range(len(bArray) - 1):
		bArray&#91;i] = bArray&#91;i + 1]
	bArray&#91;len(bArray) - 1] = chArray
	bString = bString&#91;1:]
	bString += chString

def getBchar(ch):
	v2 = bArray&#91;ch]
	arg = bString&#91;v2]
	changeBArrayandString()
	return arg

def getAint(ch):
	global aString
	global aArray
	v1 = aString.index(ch)
	arg5 = aArray&#91;v1]
	return arg5
    
flag =''
for k in cipherText:
	v0 = getAint(k)
	flag += getBchar(v0)
print('flag{' + flag + '}')</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="303" height="35" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-157.png" alt="" class="wp-image-5050" /> </figure> 

## 0x01 RememberOther

压缩包解压后，得到一个word文档和apk，文档内容是`不懂安卓，所以就只是和安卓扯了扯边，，，Have fun~`，点开可以看到需要输入用户名和一个16位的注册码。<figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-158.png" alt="" class="wp-image-5054" /> </figure> 

jeb查看源代码，我们知道是经过checkSN函数的判断后，输出了一段字符，可能和flag有关，那么我们下一步就是要获取这个字符串，下面有三种方法。<figure class="wp-block-image size-full">

<img loading="lazy" width="2988" height="444" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-159.png" alt="" class="wp-image-5055" /> </figure> 

方法1：我们能够在程序里看到输出的字符串是在程序中调用的，那它很可能存在程序的某段代码中，搜索发现，字符串在strings.xml中。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-160.png" alt="" class="wp-image-5056" width="323" height="438" /> </figure> 

方法2：在分析checkSN函数时，惊奇地发现，在用户名和注册码都不填写的情况下会返回true。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-161.png" alt="" class="wp-image-5057" width="496" height="272" /> </figure> 

方法3：分析checkSN函数可知，它是将用户名进行md5处理后，取所有的奇数位置的数字组合，组成16位sn再与注册码进行比较。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-162.png" alt="" class="wp-image-5058" width="521" height="275" /> </figure> 

python脚本如下：

<pre class="wp-block-code"><code>import hashlib
m = hashlib.md5()
m.update(b'123')
x = m.hexdigest()
sn = ''
for i in range(len(x)):
	if i%2 == 0:
		sn += x&#91;i]
print (sn)</code></pre>

总之，最后得到`b3241668ecbeb19921fdac5ac1aafa69`，解密下md5，得到`YOU_KNOW_`，结合 word 中的提示，整理得到flag: `YOU_KNOW_ANDROID`

## 0x02 Ph0en1x-100 

上模拟器，app功能是提交flag验证的。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-163.png" alt="" class="wp-image-5059" width="588" height="330" /> </figure> 

上jeb分析代码，在主函数得到判断语句，接着往下分析。<figure class="wp-block-image size-full">

<img loading="lazy" width="2260" height="384" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-164.png" alt="" class="wp-image-5060" /> </figure> 

encrypt和getFlag是从phcm库中调用的，导出库后，用ida分析。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-165.png" alt="" class="wp-image-5062" width="398" height="244" /> </figure> 

encrypt函数，分析可知对字符串的每个字符的ascii值减一。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-167.png" alt="" class="wp-image-5064" width="700" height="155" /> </figure> 

对于getFlag函数，由于该函数没有输入只有输出，所以可以通过APKIDE修改smali源码，在本来显示 Failed的地方，让其执行getFlag方法，将执行结果存入v1寄存器。<figure class="wp-block-image size-full">

<img loading="lazy" width="2641" height="1608" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-170.png" alt="" class="wp-image-5067" /> </figure> 

反编译后运行，可以得到一串字符串``ek`fz@q2^x/t^fn0mF^6/^rb`qanqntfg^E`hq|``<figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-171.png" alt="" class="wp-image-5068" /> </figure> 

将字符串的ascii值移位得到flag

<pre class="wp-block-code"><code>flag = ''
for i in c:
    flag += chr(ord(i) + 1)
print(flag)</code></pre><figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-172.png" alt="" class="wp-image-5070" width="442" height="40" /> </figure> 

## 0x03 黑客精神

JEB进行反编译，发现在MainActivity点击按钮后就弹出弹框，而后跳转到RegActivity界面去，在该界面点击注册后，调用了so层函数saveSN。<figure class="wp-block-image size-full">

<img loading="lazy" width="2924" height="903" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片.png" alt="" class="wp-image-5207" /> </figure> 

跳转到saveSN函数所在的类MyApp，进一步分析代码。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-1.png" alt="" class="wp-image-5208" width="525" height="516" /> </figure> 

接着分析libmyjni.so文件，在JNI_OnLoad函数中注册了initSN、saveSN和work函数，代码如下<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-4.png" alt="" class="wp-image-5211" width="902" height="248" /> </figure> 

用IDA分析so文件发现在java层注册的native函数都是动态注册的，发现对应的函数`n1`、`n2`、`n3`。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-3.png" alt="" class="wp-image-5210" width="653" height="202" /> </figure> 

setValue函数的作用是设置com/gdufs/xman/MyApp类的静态字段m的值，输入的注册码通过一系列的计算后得到的值，initSN函数会判断/sdcard/reg.dat文件的内容是否为`"EoPAoY62@ElRD"`，如果得到的值正确，则输入的注册码即为flag。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-6.png" alt="" class="wp-image-5214" width="352" height="595" /> </figure> 

输入`"EoPAoY62@ElRD"`，通过模拟器进行查看。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-7.png" alt="" class="wp-image-5215" width="360" height="198" /> </figure> 

## 0x04 easy-dex

dex里面包含了所有app代码，利用反编译工具可以获取java源码。理解并修改dex文件，就能更好的apk破解和防破解。<figure class="wp-block-image">

![https://box.kancloud.cn/8208f0e93ba1fc2e20ae480e31865dca_636x585.png][1] </figure> 

dex应该是藏在了so中，先寻找android_main函数，Native Activity的入口函数。qmemcpy函数将加密后的dex文件加载进来了，可以发现加密后的dex文件首地址为0x7004(IDA使用F5后，要使用那一块内存空间地址直接是以&unk地址命名的)，长度为0x3ca10。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-11.png" alt="" class="wp-image-5221" width="480" height="265" /> </figure> 

直接在静态下执行dump脚本<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-12.png" alt="" class="wp-image-5222" width="446" height="286" /> </figure> 

<pre class="wp-block-code"><code>import idaapi

addr = 0x7004
size = 0x3ca10

with open('dump','wb') as f:
    f.write(get_bytes(addr,size))
    
print('&#91;+] dump end')</code></pre>

这里直接用大佬的python解密dex脚本

<pre class="wp-block-code"><code>import zlib

with open('dump','rb') as f:
    data1 = f.read()
    data = list(data1)
    count = 0
    
    while True:
        if count &lt;= 0x59:
            count_tmp = (int)(count / 10)
            if count % 10 == 9:
                size = 0x3ca10
                size_tmp = (int)(size / 10)
                xor = (count_tmp + 1) * size_tmp
                if (size_tmp * count_tmp) &lt; xor:
                    index = size_tmp * count_tmp
                    while size_tmp:
                        data&#91;index] = data&#91;index] ^ count
                        index = index + 1
                        size_tmp = size_tmp - 1
                if count == 89:
                    while xor &lt; size:
                        data&#91;xor] = data&#91;xor] ^ 0x59
                        xor = xor + 1
        else:
            break
        count = count + 1

filebytes = bytes(data)
with open('easy-dex.dex','wb') as f1:
    f1.write(zlib.decompress(filebytes))
print('&#91;+] decrypt end')</code></pre>

jeb分析解压后的dex文件，MainActivity.java有一个按钮监听事件，触发后调用了a.java里面的onClick函数，调用了MainActivity里面的a函数。<figure class="wp-block-image size-full">

<img loading="lazy" width="2169" height="159" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-13.png" alt="" class="wp-image-5224" /> </figure> 

编写脚本，求出密文`iE3y2hEF1izgbVUfGKWQrUCtgFQFop7iEkbmRwWdwsZ1HdQGcPxRVAkWzV/eDC9N`

```python
import base64

m = [-120, 77, -14, -38, 17, 5, -42, 44, -32, 109, 85, 0x1F, 24, -91, -112, -83, 0x40, -83, -128, 84, 5, -94, -98, -30, 18, 70, -26, 71, 5, -99, -62, -58, 0x75, 29, -44, 6, 0x70, -4, 81, 84, 9, 22, -51, 0x5F, -34, 12, 0x2F, 77]
res = []
for i in m:
    res.append(i & 0xff)
b = bytes(res)
print(base64.b64encode(b))
```

再根据a函数，得出明文+key = 密文。<figure class="wp-block-image size-full">

<img loading="lazy" width="2377" height="390" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-14.png" alt="" class="wp-image-5225" /> </figure> 

在string.xml资源文件中发现字符串`I have a male fish and a female fish.`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-15.png" alt="" class="wp-image-5226" width="487" height="204" /> </figure> 

怀疑是TwoFish加密，输入key值和加密文本，得到flag。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-16.png" alt="" class="wp-image-5228" width="540" height="391" /> </figure> 

## 0x05 你是谁<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-17.png" alt="" class="wp-image-5234" width="357" height="608" /> </figure> 

点击皇上的图片，听到语音“你是个好人，但是我们不适合。”，白色的圆可以被点击。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-18.png" alt="" class="wp-image-5236" width="719" height="101" /> </figure> 

在MainActivity中找到注释中存在`@Override // com.iflytek.cloud.InitListener`，搜索发现来源是科大讯飞的语音集成。在background类中发现编码，`20667 25105 26159 36924`的中文unicode编码为`傻我是逼`。<figure class="wp-block-image size-full">

<img loading="lazy" width="1921" height="247" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/03/图片-19.png" alt="" class="wp-image-5237" /> </figure> 

推理得出编码前的flag顺序应该是`25105 26159 20667 36924`。

[1]: https://box.kancloud.cn/8208f0e93ba1fc2e20ae480e31865dca_636x585.png
