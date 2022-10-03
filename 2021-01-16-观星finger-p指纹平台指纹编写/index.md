# 观星Finger-P指纹平台指纹编写

<div class="has-toc have-toc">
</div>

## 0x00 前言

最近，数字观星和谷安联合主办了一个活动，奖品比较丰厚，还有甜品能帮上应届求职，不免有些心动，但原来从没有接触过指纹编写，就在文档和大佬指点下开始尝试了，如今也刚好达到了40条，顺便记录下心路历程。

<div class="wp-block-image">
  <figure class="aligncenter"><img loading="lazy" width="184" height="43" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-44.png" alt="" class="wp-image-256" /></figure>
</div>

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-40.png" alt="" class="wp-image-239" width="433" height="64" /></figure>
</div>

<a rel="noreferrer noopener" href="https://fp.shuziguanxing.com/#/" data-type="URL" data-id="https://fp.shuziguanxing.com/#/" target="_blank" rel="nofollow" >数字观星Finger-P指纹平台</a>

## 0x01 啥是指纹？

数字观星Finger-P指纹平台是基于Wappalyzer针对于web指纹识别的平台，在此文中指纹特指web指纹。Web指纹是web服务组件在开发时留下的对其类型及版本进行标识的**特殊信息**，包括web服务器指纹、web运用指纹以及前端框架指纹等。在web安全测试过程中，收集web指纹信息也是一个比较重要的步骤；在安全运营过程中，通过指纹识别识别资产的web信息，这样能更加了解整个资产存在哪些方面的威胁，然后对症检测修补，提升安全工作的效率。网络上开源的web指纹识别程序很多，如Wappalyzer，whatweb, wpscan, joomscan等等，也有<a rel="noreferrer noopener" href="https://www.yunsee.cn/" data-type="URL" data-id="https://www.yunsee.cn/" target="_blank" rel="nofollow" >云悉</a>等在线指纹平台。

这里简单展示火狐插件Wappalyzer对本网站的指纹信息检测。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-41.png" alt="" class="wp-image-241" width="321" height="398" /></figure>
</div>

观星Finger-P指纹平台接收指纹（网站默认首页能识别）的范围包括CMS应用指纹、WEB中间件指纹、首页能识别的应用指纹、国内外的其它web应用指纹等。

**指纹应用层级**

**应用层：**主要是各种web应用系统以及前端js框架等，比如dedecms、xxx应用系统、邮件系统等；  
**支撑层：**主要是语言、后端框架等，比如java、php、struts、spring等；  
**服务层：**主要是服务和应用，以及协议，包含openssh、apahce、tomcat、ssl、ntp、icmp等；  
**系统层：**主要指操作系统，包含Linux、unix、centos、Ubuntu、Windows等；  
**硬件层：**主要是硬件设备为主，包含路由器、交换机、防火墙、VPN、waf（现在不区分软waf）、以及物联网等设备；

基于Wappalyzer的指纹识别分类

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-42.png" alt="" class="wp-image-246" width="503" height="2091" /></figure>
</div>

**指纹识别的几种方式**

A、网页中发现关键字（比如CopyRight、电话号、应用名称等。）

B、特定文件的MD5（主要是静态文件、不一定要是MD5）

C、指定URL的关键字

D、指定URL的TAG模式

## 0x02 Wappalyzer的安装与使用

Wappalyzer是基于正则表达式来识别web应用，它的功能是识别单个url的指纹，其原理就是给指定URI发送HTTP请求，获取响应头与响应体并按指纹规则进行匹配。它也是一款浏览器插件，能识别出网站采用了那种web技术，能够检测出CMS和电子商务系统、留言板、javascript框架，主机面板，分析统计工具和其它的一些web系统。

（1）Wappalyzer的安装与使用需要基于<a rel="noreferrer noopener" href="https://nodejs.org/en/" data-type="URL" data-id="https://nodejs.org/en/" target="_blank" rel="nofollow" >Node.js</a>，需要注意的是官方的帮助文档中提及Nodejs V10/12 已经不支持采用TLS 1.0以前协议的HTTPS站点，建议使用V8版本来进行测试。

（2）通过Node.js安装wappalyzer 

<pre class="wp-block-code"><code>&lt;code>npm i wappalyzer</code>&lt;/code></pre>

（3）使用wappalyzer指纹识别

cmd打开命令行，使用`wappalyzer 目的网站`命令来进行指纹识别。

或者通过调用wappalyzer模块识别指纹信息`node ./node_modules/wappalyzer/cli.js 目的网站`

Wappalyze执行文件在`C:\Users\xx\AppData\Roaming\npm\`，Wappalyzer的包目录在`C:\Users\xx\AppData\Roaming\npm\node_modules\wappalyzer`，重点是apps.json(即为technologies.json），这个文件记录的是整个的指纹规则，json文件里面有两部分apps（technologies）与categories，写的指纹就是放在这里面进行识别网站的，categories是指纹的类型，这项可以不用管，只看apps（technologies）。

## 0x03 指纹规则

基于Wappalyzer的指纹规则说明

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-43.png" alt="" class="wp-image-252" width="499" height="914" /></figure>
</div>

**指纹编写样例**

<pre class="wp-block-code"><code>"Struts": {
 "cats": &#91; "18"],
 "html":"(href|action|src).*?=.*?(action|do)\\;confidence:50",
  "url": "/.*\\.do$|/.*\\.action$\\;confidence:40",
  "html": "Struts Problem Report",
  "website": "http://struts.apache.org/",
  "_fingerprint_note":"Apache Struts是一个用于开发Java EE网络应用程序的开放源代码网页应用程序架构。",
  "_fingerprint_test_url":"https://www.shuziguanxing.com/"
}</code></pre>

  1. 应用名称struts组件
  2. 分类18（web框架）
  3. 匹配html中是否存在action,do后缀，定义可信值50
  4. layer是指这个应用属于5层中的那一层，该应用属于数据支撑层
  5. 匹配URL中是否有do和action后缀，定义可信值40
  6. 匹配html中是否存在“Struts Problem Report”字符串
  7. website为应用官网地址
  8. \_fingerprint\_note是简单描述这个应用
  9. \_fingerprint\_test_url为指纹识别测试的URL

**默认不定义可信值则为100。总体可信值如果超过100，也只会返回100。**

**Wappalyzer测试的编写样例**

<pre class="wp-block-code"><code>{   "$schema":
"../schema.json",   
"apps":{                      
 "1C-Bitrix":{         
  "cats":&#91;  1  ],       
   "headers":{
      "Set-Cookie":"BITRIX_",            
      "X-Powered-CMS":"Bitrix Site Manager"  
   },         
    "html":"(?:&lt;link&#91;^&gt;]+components/bitrix(?:src|href)=\"/bitrix/(?:js|templates))",    
    "icon":"1C-Bitrix.png",  
    "implies":"PHP",   
    "script":"1c-bitrix",          
    "website":"http://www.1c-bitrix.ru"   },     },   
    "categories":{     "1":
      {  "name":"CMS",     "priority":1       },                       ......    
}}</code></pre>

**apps**

  1. 应用名1C-Bitrix
  2. 匹配Headers特征
  3. 匹配html
  4. 匹配icon
  5. 包含PHP的所有指纹信息
  6. 匹配Script
  7. website为应用官网地址

**categories**

  1. 编号
  2. 名称
  3. 优先级

上述样例中用到了一些<a rel="noreferrer noopener" href="https://www.runoob.com/regexp/regexp-tutorial.html" data-type="URL" data-id="https://www.runoob.com/regexp/regexp-tutorial.html" target="_blank" rel="nofollow" >正则表达式</a>，这在指纹编写过程中可以提升指纹的质量，比如将年份2021换成`\d{4}`。

## 0x04 实战编写

（1）**寻找要写web指纹的产品**

这里需要用到一些工具，<a rel="noreferrer noopener" href="https://shodan.io" data-type="URL" data-id="https://shodan.io" target="_blank" rel="nofollow" >Sodan</a>、<a rel="noreferrer noopener" href="https://fofa.so/" data-type="URL" data-id="https://fofa.so/" target="_blank" rel="nofollow" >Fofa</a>、<a rel="noreferrer noopener" href="https://www.zoomeye.org/" data-type="URL" data-id="https://www.zoomeye.org/" target="_blank" rel="nofollow" >ZoomEye</a>，可以通过类似<a href="https://www.oschina.net/project" target="_blank"  rel="nofollow" >h</a><a rel="noreferrer noopener" href="https://www.oschina.net/project" target="_blank" rel="nofollow" >ttps://www.oschina.net/project</a>或者<a rel="noreferrer noopener" href="https://www.cnvd.org.cn/flaw/typelist?typeId=29" target="_blank" rel="nofollow" >https://www.cnvd.org.cn/flaw/typelist?typeId=29</a>去批量获取产品名录；或者是批量获取web软件厂商名录再去空间测绘的站点批量收集厂商的产品名录；又或者直接范围较广的关键词在空间测绘引擎中搜索批量获取名单，诸如地名，应用类别名称等关键词。俗话说，万事开头难，这一步是整个指纹编写最难搞的一步。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-45.png" alt="" class="wp-image-269" width="679" height="158" /></figure>
</div>

（2）**寻找线上样例与排重**

可以直接到指纹库中查询进行大概率排重。也可以考虑在批量寻找产品的时候，在大方向上避开Finger-P指纹平台上已有的大块，这个需要对Finger-P指纹平台已有指纹的大块有所了解和自行分析。通过避开Finger-P指纹平台上已有的大块来简化排重这一个步骤。出现“此域名指纹不存在！”或者现有的指纹信息中没有对应产品。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-46.png" alt="" class="wp-image-271" width="197" height="33" /></figure>
</div>

（3）**观察该web应用**

按照我微不足道的经验来说，Web应用系列的产品中html是最容易看出来的，一般藏在`<title>`、`<p>`、`<div>`、`<meta>`等标签中。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="625" height="215" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-48.png" alt="" class="wp-image-275" /></figure>
</div>

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="683" height="220" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-49.png" alt="" class="wp-image-278" /></figure>
</div>

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="541" height="196" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-50.png" alt="" class="wp-image-279" /></figure>
</div>

其次是`cookie`和`script`。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="414" height="24" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-47.png" alt="" class="wp-image-274" /></figure>
</div>

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="895" height="371" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-51.png" alt="" class="wp-image-282" /></figure>
</div>

其他的按照指纹规则搜集。

（4）**依据以上特征**提交****指纹****到平台****

&nbsp;平台提供两种方式：表单提交和批量提交，初学者建议采用表单提交，熟练后批量提交很爽快。

首先看一下表单的页面。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-53.png" alt="" class="wp-image-288" width="616" height="505" /></figure>
</div>

<p class="has-black-color has-text-color">
  应用层级对应0x01的内容。
</p>

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-54.png" alt="" class="wp-image-289" width="182" height="197" /></figure>
</div>

识别方式默认是首页特征（即为HTML中的内容），对应指纹的识别方式。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="127" height="275" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-55.png" alt="" class="wp-image-290" /></figure>
</div>

指纹种类默认是Web Server（Web 服务），可根据需要多选或修改，一般默认就足够的。<figure class="wp-block-image size-large is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-52.png" alt="" class="wp-image-287" width="603" height="539" /> </figure> 

批量提交的指纹撰写方式可具体参考下列文档。

<a href="https://mp.weixin.qq.com/s?__biz=MzI0MDQ3ODc0NQ==&mid=2247485689&idx=1&sn=dca6780e11f2257576eec691a4e48637&chksm=e91b778fde6cfe9950d9f34512a19f7fb1e8b953ae1718f53c07b6d9a206c43867641f04e81c&mpshare=1&scene=23&srcid=0110AUTnW9wSYUwrd7X4EWkL&sharer_sharetime=1610246119985&sharer_shareid=c19b17eee72722da6822e38c152fcc26#r" data-type="URL" data-id="https://mp.weixin.qq.com/s?__biz=MzI0MDQ3ODc0NQ==&mid=2247485689&idx=1&sn=dca6780e11f2257576eec691a4e48637&chksm=e91b778fde6cfe9950d9f34512a19f7fb1e8b953ae1718f53c07b6d9a206c43867641f04e81c&mpshare=1&scene=23&srcid=0110AUTnW9wSYUwrd7X4EWkL&sharer_sharetime=1610246119985&sharer_shareid=c19b17eee72722da6822e38c152fcc26#r" target="_blank" rel="noreferrer noopener" rel="nofollow" >小雪 | 宜学以致用写指纹 忌不积硅步绘资产</a>

<a href="https://mp.weixin.qq.com/s?__biz=MzI0MDQ3ODc0NQ==&mid=2247484922&idx=1&sn=4e6def9ceace35d12442ec0b9d0b1273&chksm=e91b7a8cde6cf39adec741ba29ec61132177323991491ac1dd3788a7115e653ece8c7d5a95de&mpshare=1&scene=23&srcid=0110HaTCObO1sVJ6UauCAd1t&sharer_sharetime=1610246094500&sharer_shareid=c19b17eee72722da6822e38c152fcc26#rd" data-type="URL" data-id="https://mp.weixin.qq.com/s?__biz=MzI0MDQ3ODc0NQ==&mid=2247484922&idx=1&sn=4e6def9ceace35d12442ec0b9d0b1273&chksm=e91b7a8cde6cf39adec741ba29ec61132177323991491ac1dd3788a7115e653ece8c7d5a95de&mpshare=1&scene=23&srcid=0110HaTCObO1sVJ6UauCAd1t&sharer_sharetime=1610246094500&sharer_shareid=c19b17eee72722da6822e38c152fcc26#rd" target="_blank" rel="noreferrer noopener" rel="nofollow" >小雪 | 宜指纹学习以致用 忌只看少练基础功</a>

<a href="https://mp.weixin.qq.com/s?__biz=MzI0MDQ3ODc0NQ==&mid=2247486286&idx=1&sn=9888b0f3107243d97d724abacf7c7610&chksm=e91b7438de6cfd2e119a512de3f15832b12516b576c033143d41189dacd3f6b59223f4de9301&mpshare=1&scene=23&srcid=0108qb1EEzguW4bcDOT1L614&sharer_sharetime=1610342432710&sharer_shareid=c19b17eee72722da6822e38c152fcc26#rd" data-type="URL" data-id="https://mp.weixin.qq.com/s?__biz=MzI0MDQ3ODc0NQ==&mid=2247486286&idx=1&sn=9888b0f3107243d97d724abacf7c7610&chksm=e91b7438de6cfd2e119a512de3f15832b12516b576c033143d41189dacd3f6b59223f4de9301&mpshare=1&scene=23&srcid=0108qb1EEzguW4bcDOT1L614&sharer_sharetime=1610342432710&sharer_shareid=c19b17eee72722da6822e38c152fcc26#rd" target="_blank" rel="noreferrer noopener" rel="nofollow" >Finger-P指纹平台活动技术指南 : Web指纹编写与批量编写思想</a>

<a href="https://fp.shuziguanxing.com/#/fingerplatinfo" data-type="URL" data-id="https://fp.shuziguanxing.com/#/fingerplatinfo" target="_blank" rel="noreferrer noopener" rel="nofollow" >官方帮助文档</a>
