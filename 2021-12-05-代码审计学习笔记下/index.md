# 代码审计学习笔记（下）

<div class="has-toc have-toc">
</div>

## 0x00 二次漏洞审计

**什么是二次漏洞？**

需要先构造好利用代码写入网站保存，在第二次或多次请求后调用攻击代码触发或者修改配置触发的漏洞。

**审计技巧**

依然可以通过关键词定位，但精度不够，比如可以根据数据库字段、数据表名等去代码中搜索。二次漏洞的逻辑性强，通读有助于挖洞。业务越复杂越容易存在二次漏洞，可以重点关注购物车、订单、引用数据、文章编辑、草稿等。SQL注入和XSS较为常见。

## 0x01 代码审计小技巧

**1.钻GPC等转义的空子**

  * 不受GPC保护的`$_SERVER`变量。在PHP5之后用`$_SERVER`取到的header字段不受GPC影响，`$_FILES`变量也不受GPC保护。
  * 编码转换问题。如宽字节注入。

**2.神奇的字符串**

  * 字符处理函数报错信息泄露

页面的报错信息通常能泄露文件绝对路径、代码、变量以及函数等信息。`error_reporting`函数中有几个选项来配置显示错误的等级，列表如下：

<pre class="wp-block-code"><code>E_WARNING #常用，代表显示错误信息
E_PARSE
E_NOTICE #常用，代表显示基础提示信息
E_CORE_ERROR
E_CORE_WARNING
E_COMPILE_ERROR
E_COMPILE_WARNING
E_USER_ERROR
E_USER_WARNING
E_USER_NOTICE
E_STRICT
E_RECOVERABLE_ERROR
E_ALL #常用，代表显示所有问题</code></pre>

大多数错误提示都会显示文件路径。大多数程序会使用`trim`函数对用户名等值去掉两边的空格，这时候如果我们传入的用户名参数时一个数组，程序就会报错。

  * 字符串截断
      * %00截断。需要GPC关闭以及不被`addslashes`函数过滤，PHP5.3后全面修复。
      * iconv函数字符编码转换截断。iconv用于字符编码转换，如UTF-8到GBK。而字符集的编码转换存在一定的差异性，编码时不能成功转换，iconv遇到无法处理的字符串时会停止处理后续字符串。作者fuzz测试UTF-8到GBK的转码，发现chr(128)-chr(255)之间都可以截断字符串。

**3.php://输入输出流**

使用最多的封装器是`php://input`，`php://output`，`php://filter`。

`php://input`可以访问请求原始数据的只读流，即可以直接读取到POST上没有经过解析的原始数据，而无法获取“multipart/from-data”方式提交的数据。

`php://output`是一个只写的数据流，将刘书记输出。

`php://filter`是一个文件操作协议，可以对磁盘中的文件进行读写操作，效果类似`readfile`等。

**4.PHP代码解析标签**

PHP存在多种解析标签，最标准的是`<?php?>`，除此之外，还有：

  * 脚本标签。`<script language="php">....<script>`
  * 短标签。`<?...?>`，使用短标签前需要在php.ini中设置short\_open\_tag=on，默认开启。
  * asp标签。`<%...%>`，在PHP3.0.4版后可用，需要在php.ini中设置asp_tags=on，默认关闭。

**5.fuzz漏洞发现**

**6.不严谨的正则表达式**

  * 没有使用^和$限定匹配开始位置。
  * 特殊字符未转义。

**7.十余种MYSQL报错注入**

可参考<a href="http://81.70.81.64/%e5%ae%89%e5%85%a8%e7%89%9bsql%e6%b3%a8%e5%85%a5%e5%ad%a6%e4%b9%a0%e7%ac%94%e8%ae%b0/#0x02-%E6%8A%A5%E9%94%99%E6%B3%A8%E5%85%A5" target="_blank" rel="noreferrer noopener">http://81.70.81.64/%e5%ae%89%e5%85%a8%e7%89%9bsql%e6%b3%a8%e5%85%a5%e5%ad%a6%e4%b9%a0%e7%ac%94%e8%ae%b0/#0x02-%E6%8A%A5%E9%94%99%E6%B3%A8%E5%85%A5</a>

**8.Windows FindFirstFile利用**

目前大多数程序都会对上传的文件名加入时间戳等字符再进行MD5，然后下载文件的时候通过保存在数据库里的文件ID读取文件路径，一样也实现了文件下载，这样我们就无法直接得到我们上传的webshell文件路径，但是当在Windows下时，我们只需要知道文件所在目录，然后利用Windows的特性就可以访问到文件，这是因为Windows在搜索文件的时候使用了FindFirstFile这一个winapi函数，该函数到一个文件夹(包含子文件夹)去搜索指定文件。

利用方法很简单，我们只要将文件名不可知部分之后的字符用"<"或者">"代替即可，不过要注意一点是，只使用一个"<"或者">"则只能代表一个字符，如果文件名是12345或者更长，这时候请求"1<"或者"1>"都是访问不到文件的，需要"1<<"才能访问到，代表继续往下搜索，有点像Windows的短文件名，这样我们还可以通过这个方式来爆破目录文件了。

目前所有PHP版本都可用，PHP并没有在语言层面禁止使用>、<这些特殊字符，这一特性存在很多函数之中。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/12/5958785-743d736d7ad1b75c.png" alt="" class="wp-image-4765" width="813" height="391" /> </figure> 

**9.PHP可变变量**

PHP可变变量指的是一个变量的变量名可用动态地设置和利用。在PHP中，单引号代表纯字符串，而双引号则是会解析中间的变量，所以当使用双引号时会存在代码执行漏洞。

实例代码：`<?php $a="${@phpinfo()}";?>`

“@”符号必须存在，不然无法执行，其他写法：

<pre class="wp-block-code"><code>花括号内第一个字符为空格
$a="${ phpinfo()}";

花括号内第一个字符为TAB
$a="${ phpinfo()}";

花括号内第一个字符为注释符
$a="${/**/phpinfo()}";

花括号内第一个字符为回车换行符
$a="${
phpinfo()}";

花括号内第一个字符为加号
$a="${+phpinfo()}";


花括号内第一个字符为减号
$a="${-phpinfo()}";


花括号内第一个字符为感叹号
$a="${!phpinfo()}";

除此之外还有~、\等</code></pre>

## 0x02 参数的安全过滤

**第三方过滤函数与类**

**内置过滤函数**

  * SQL注入过滤函数。`addslashes`、`mysql_escape_string`、`mysql_real_escape_string`，它们的作用都是通过添加反斜杠来转义字符，前两种直接在敏感字符串前加，可能存在宽字节注入绕过的问题，最后一种会考虑当前连接数据库的字符集编码，安全性更好。
  * XSS过滤函数。`htmlspeacialchars`将字符串中的特殊字符转换成HTML实体编码，`strip_tags`用来去掉HTML及PHP标记。
  * 命令执行过滤函数。`escapeshellcmd`在Windows下过滤方式则是在特殊字符前面加了^，Linux下加\。`escapeshellarg`则是给所有参数加上一对双引号，强制转换为字符串。

## 0x03 使用安全的加密算法

MD5是目前使用最多的密码存储加密算法。

## 0x04 业务功能安全设计

**验证码**

  * 不刷新直接绕过
  * 暴力破解
  * 机器识别。非实时生成的验证码，把全部验证码文件报错，构建图片MD5库，利用时直接匹配服务器端返回的图片MD5即可。动态生成的验证码需要进行图片文字识别或者语言识别。
  * 打码平台，如<a href="http://www.damatu1.com/" data-type="URL" data-id="http://www.damatu1.com/" target="_blank" rel="noreferrer noopener" rel="nofollow" >打码兔</a>。

验证码资源滥用，如短信轰炸。

**用户登录**

  * 撞库漏洞。
  * API登录。

**用户注册**

安全设计思路

  * 设计验证码
  * 采集用户机器唯一识别码，拦截短时间内多次注册。
  * 根据账号格式自学习识别垃圾账号。
  * 防止SQL注入漏洞与XSS漏洞

**文件管理**

  * 禁止写入脚本可在服务端执行的文件
  * 限制文件管理功能操作的目录
  * 限制文件管理功能访问权限
  * 禁止上传特殊字符文件名的文件

## 0x05 应用安全体系

  * 用户密码安全策略
  * 前后台用户分表
  * 后台地址隐藏
  * 密码加密存储方式
  * 登录限制
  * API站库分离
  * 慎用第三方服务
  * 严格的权限控制
  * 敏感操作多因素验证
  * 应用自身的安全中心

<a href="https://code.google.com/archive/p/pasc2at/wikis/SimplifiedChinese.wiki" data-type="URL" data-id="https://code.google.com/archive/p/pasc2at/wikis/SimplifiedChinese.wiki" target="_blank" rel="noreferrer noopener" rel="nofollow" >高级PHP应用程序漏洞审核技术</a>


