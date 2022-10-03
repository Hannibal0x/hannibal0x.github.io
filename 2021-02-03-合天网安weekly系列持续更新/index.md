# 合天网安Weekly系列（1-8）


## 0x00 前言

好久没逛过合天了，进实验室van一van。

地址：<a href="https://www.hetianlab.com/cour.do?w=1&c=CCID2d51-5e95-4c58-8fc9-13b1659c1356" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.hetianlab.com/cour.do?w=1&c=CCID2d51-5e95-4c58-8fc9-13b1659c1356</a>

## 0x01 第一周 | 神奇的磁带

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5001
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}

输入IP地址，进入页面。<figure class="wp-block-image size-large">

<img loading="lazy" width="1525" height="828" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片.png" alt="" class="wp-image-460" /> </figure> 

在html底部发现一个`./Flag.txt`，输入url，点开解码Unicode后，出现：

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-1.png" alt="" class="wp-image-462" width="87" height="25" /></figure>
</div>

抓包发现cookie值是base64编码。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-2.png" alt="" class="wp-image-466" width="259" height="20" /></figure>
</div>

decoder解码后得到`q1234567890p..`，作为密码输入，出现弹窗。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-3.png" alt="" class="wp-image-470" width="265" height="172" /></figure>
</div>

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-4.png" alt="" class="wp-image-472" width="549" height="154" /></figure>
</div>

答案很明显是`tape`，又来了弹窗。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-5.png" alt="" class="wp-image-474" width="300" height="178" /></figure>
</div>

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-6.png" alt="" class="wp-image-476" width="426" height="173" /></figure>
</div>

输入`/Flag-Win.txt`，得到提示。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-7.png" alt="" class="wp-image-478" width="423" height="88" /></figure>
</div>

直接`btzhy`，弹窗又来了。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-8.png" alt="" class="wp-image-480" width="274" height="161" /></figure>
</div>

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-9.png" alt="" class="wp-image-482" width="459" height="182" /></figure>
</div>

好，给了个PHP的文件，感觉离flag又近了一步。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-10.png" alt="" class="wp-image-485" width="426" height="174" /></figure>
</div>

HTML里提示两位数，Intruder开始爆破10-99。在长度栏发现华点。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-11.png" alt="" class="wp-image-495" width="413" height="111" /></figure>
</div>

成功得到flag。`Flag{ctf_victory_SecBug}`

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-12.png" alt="" class="wp-image-498" width="307" height="162" /></figure>
</div>

## 0x02 第二周 | 就差一把钥匙

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5002
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}

打开后啥也妹有，html代码也没有任何信息。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-14.png" alt="" class="wp-image-503" width="234" height="39" /></figure>
</div>

使用Nikto扫描敏感目录，发现存在robots.txt。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-13.png" alt="" class="wp-image-502" width="692" height="222" /></figure>
</div>

发现隐藏目录。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-15.png" alt="" class="wp-image-508" width="189" height="52" /></figure>
</div>

进不去，更改`X-Forwarded-For：127.0.0.1`

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-16.png" alt="" class="wp-image-510" width="466" height="24" /></figure>
</div>

成功得到flag。`flag{hetianlab-weekctf}`

## 0x03 第三周 | 迷了路

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5003
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-18.png" alt="" class="wp-image-523" width="397" height="400" /></figure>
</div>

好的，开幕就是访问国外网站，猜测需要修改HTTP请求头的accept-language，抓个包尝试下。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="58" height="37" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-19.png" alt="" class="wp-image-525" /></figure>
</div>

多出了flag的部分信息，八个国家，应该尝试8次拼接就好。参考<a rel="noreferrer noopener" href="https://blog.csdn.net/u014549283/article/details/81742104" data-type="URL" data-id="https://blog.csdn.net/u014549283/article/details/81742104" target="_blank" rel="nofollow" >【WEB】语言代码缩写表大全（用于Accept-Language）</a>（日语应该是jp而不是ja）

成功得到`flag{Thisis_hetianlab@}`

## 0x04 第四周 | Check your source code

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5004
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}

根据题目信息，看看html源代码，发现source.txt。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="783" height="550" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-20.png" alt="" class="wp-image-534" /></figure>
</div>

从源代码可知，username需要输入admin，password不能为admin，需要设置一个名为check的cookie，难点在找到check的值。首先，根据ahash的值来推出secret为88。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-21.png" alt="" class="wp-image-541" width="129" height="198" /></figure>
</div>

构造`ODg=%61%64%6d%69%6e%31`，成功得到`flag{welcome_to_htlab}`。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="969" height="81" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-22.png" alt="" class="wp-image-544" /></figure>
</div>

## 0x05 第五周 | Easy upload

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5005
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}

题目已经明示了是文件上传类型的题目，看源码。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-23.png" alt="" class="wp-image-549" width="474" height="400" /></figure>
</div>

先随便传张图片。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="712" height="58" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-24.png" alt="" class="wp-image-551" /></figure>
</div>

抓包改filename为give\_me\_flag.php。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-26.png" alt="" class="wp-image-555" width="540" height="65" /></figure>
</div>

再插入givemeflag。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="434" height="99" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-27.png" alt="" class="wp-image-557" /></figure>
</div>

清清爽爽得到了`flag{hetian@lab_com}`。

## 0x06 第六周 | 套娃一样的上传

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5006
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}<figure class="wp-block-image size-large">

<img loading="lazy" width="680" height="526" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-28.png" alt="" class="wp-image-566" /> </figure> 

先传一张图片。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="1005" height="62" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-29.png" alt="" class="wp-image-568" /></figure>
</div>

需要修改文件类型，这里修改filename为1.php。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="755" height="95" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-30.png" alt="" class="wp-image-572" /></figure>
</div>

黑名单绕过，可以大小写绕过，例如Php、PhP或者利用黑名单中没有的，但是又能够被解析的后缀名，例如php、php3、php4、php5、php7、pht、phtml、phps。尝试phtml通过。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-31.png" alt="" class="wp-image-576" width="531" height="86" /></figure>
</div>

尝试把图片内容长度修改为17。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-32.png" alt="" class="wp-image-579" width="438" height="63" /></figure>
</div>

Get it。`flag{0000_0000_0000}`

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="265" height="53" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-33.png" alt="" class="wp-image-580" /></figure>
</div>

## 0x07 第七周 | 再见上传

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5007
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}

从题目得知，又是一道上传的题，老规矩，先传图片。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-34.png" alt="" class="wp-image-585" width="500" height="298" /></figure>
</div>

改filename，发现不管用了。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-35.png" alt="" class="wp-image-587" width="580" height="22" /></figure>
</div>

白名单校验，可以利用Apache的解析漏洞，Apache是从后面开始检查后缀，按最后一个合法后缀，在文件上传目录用%00截断，这里由于是POST方式，需要urldecode。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="328" height="55" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-36.png" alt="" class="wp-image-589" /></figure>
</div>

成功得到`flag{asdf_hetianlab_com}`。哪儿来的女朋友，我向往自由.jpg

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-37.png" alt="" class="wp-image-592" width="248" height="54" /></figure>
</div>

## 0x08 第八周 | 随意的上传

  * **背景说明**
      * 本实验无writeup，需要同学们发挥自己所学，拿下最终目标。
  * **实验环境**
      * 目标机：Centos7 IP地址：10.1.1.147:5008
      * 攻击机：Kali IP地址：随机分配
      * 要求：获取目标flag
      * 提示：flag格式为Flag{}
  * **提示**
      * 随意到不提供工具？你打开C盘的tools看看呢~

首先打开c盘的tools，发现三个文件。文件上传类型，一般与bp和菜刀有关，bp直接在桌面，没必要大费周章的提示，所以题目和菜刀有关，先写个一句话木马。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-38.png" alt="" class="wp-image-599" width="251" height="84" /></figure>
</div>

写了php木马但系统没有警告，看来题目的思路没错。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-39.png" alt="" class="wp-image-601" width="234" height="20" /></figure>
</div>

找到文件上传路径。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-40.png" alt="" class="wp-image-605" width="270" height="23" /></figure>
</div>

发现字符<?php被过滤。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-41.png" alt="" class="wp-image-607" width="380" height="206" /></figure>
</div>

用这一段代码来代替。

<pre class="wp-block-code"><code>&lt;script language="pHp"&gt;@eval($_POST&#91;'cmd'])&lt;/script&gt;</code></pre>

成功进入。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="1007" height="204" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-42.png" alt="" class="wp-image-612" /></figure>
</div>

找到flag.php，拿到`flag{0123_4567_8901}`

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-43.png" alt="" class="wp-image-615" width="171" height="44" /></figure>
</div>
