# SPbCTF 2021 WriteUp



<div class="has-toc have-toc">
</div>

## 0x00 前言

国外的比赛题型很新颖，换句话说，也挺花里胡哨的，不过太菜了，只解出了easy的题目，555，摸鱼打一打。

## 0x01 CatStep

题目

```
Greeting human!

We want to play a game with you. The mission is simple: you need to guess our flag, that’s all. We use an algorithm to determine the similarity of strings.
```

需要在这个页面以POST的方式传递一个flag的值，然后系统会根据莱文斯坦距离来计算所提交的flag与真实flag的相似度。<figure class="wp-block-image size-full">

<img loading="lazy" width="1718" height="1781" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-68.png" alt="" class="wp-image-4024" /> </figure> 

bp抓包后，提交一个空值，提示flag至少要8位。<figure class="wp-block-image size-full">

<img loading="lazy" width="1480" height="756" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-69.png" alt="" class="wp-image-4025" /> </figure> 

再构造超长的确定flag的最大位数。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-70.png" alt="" class="wp-image-4026" width="748" height="415" /> </figure> 

为了判断flag长度的精确值，构造flag值为特殊字符，得到的length即为真实flag的长度。<figure class="wp-block-image size-full">

<img loading="lazy" width="1483" height="766" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-71.png" alt="" class="wp-image-4027" /> </figure> 

然后使用inturder模块来逐位爆破，字典定义为a-z、A-Z、一些特殊字符，每一位正确length的长度就会减一，而且必定是spbctf{.........}格式的 。经过几轮的爆破得到spbctf{asy_webfgzc}。这个显然不是最终的结果，它表明了flag包含这些字符且前后顺序是相同的，那就可以把position插入到{}里面，逐个慢慢爆破，最后得到正确的flag为`spbctf{easy_web_fuzzing_0t5AFzSG0Oc}`

## 0x02 BLT

题目

<pre class="wp-block-code"><code>Our company provides services for the development of the most modern software.

Can you check our landing page for vulnerabilities?

Here's our website: 164.90.201.196:8080/
And here's our infrastructure: blt.zip</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="3806" height="1858" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-72.png" alt="" class="wp-image-4028" /> </figure> 

扫描一下目录，发现有.git泄露，不过用GitHack下不下来东西。<figure class="wp-block-image size-full">

<img loading="lazy" width="1974" height="1813" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-73.png" alt="" class="wp-image-4029" /> </figure> 

在压缩包的dockerfile文件中发现一个可疑的操作。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-74.png" alt="" class="wp-image-4030" width="569" height="239" /> </figure> 

到这里就没思路了，后来，听大佬说是用一个新出的apache的CVE-2021-41773来打。这里抓包用poc访问下/etc/passwd

<pre class="wp-block-code"><code>ip/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="1740" height="936" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-76.png" alt="" class="wp-image-4039" /> </figure> 

可以！接着知道了flag的路径，直接访问它，得到`spbctf{th3_lat3st_d03s_n0t_m3an_s3cur3}`<figure class="wp-block-image size-full">

<img loading="lazy" width="1631" height="448" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-77.png" alt="" class="wp-image-4040" /> </figure> 

## 0x03 Cook Admin

头一次做OSINT的题目，还挺有意思的，题目如下

```
A website has appeared on the Internet that promises free cookies to everyone.

However, no matter how many times you visit it, you will not see any cookies.

Expose this gang that gives you empty promises.

You will need to find the following people (‘to find’ means to obtain the email address of each of the three persons).

    The administrator and owner of the fraudulent website
    The courier who published a sample set of cookie pictures
    The programmer who developed this website (he is a huge fan of birds and his email is on the website domain)

Website: freecookiesforeverybody.xyz/

Submit here the administrator’s email.
```

ok，先访问提供的域名看看，查看源码也并没有什么有用的信息。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-78.png" alt="" class="wp-image-4041" width="468" height="80" /> </figure> 

跳转后来到谷歌云盘，里面是一些曲奇的图片。这时突然想到，whois查询域名或许能够发现邮箱信息。访问<a rel="noreferrer noopener" href="https://who.is/" target="_blank" rel="nofollow" >https://who.is/</a>，输入域名，得到flag，`spbctf{helen.m.clifford@mail.ru}`。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-79.png" alt="" class="wp-image-4042" width="600" height="587" /> </figure>
