# 安全牛反序列化学习笔记

<div class="has-toc have-toc">
</div>

## 0x00 反序列化的基本概念

序列化和反序列化的目的是使得程序间传输对象会更加方便。

内存数据是“稍纵即逝”的；——通常，程序执行结束，立即全部销毁。变量所存储的数据，就是内存数据；文件是“持久数据”；

序列化就是，将内存的变量数据，“保存”到文件中的持久数据的过程。简化就是：将内存变为文件。

反序列化就是，将序列化过存储到文件中的数据，恢复到程序代码的变量表示形式的过程。简化就是：将文件变为内存。

**相关函数**

serialize — 产生一个可存储的值的表示

**serialize**(mixed`$value`): string

**serialize()** 返回字符串，此字符串包含了表示 `value` 的字节流，可以存储于任何地方。

unserialize — 从已存储的表示中创建 PHP 的值

**unserialize**(string `$str`): mixed

**unserialize()** 对单一的已序列化的变量进行操作，将其转换回 PHP 的值。<figure class="wp-block-image size-full">

<img loading="lazy" width="738" height="607" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-200.png" alt="" class="wp-image-3097" /></figure> 

## 0x01 魔术方法

PHP中把以两个下划线__开头的方法称为魔术方法(Magic methods)<figure class="wp-block-image size-full">

<img loading="lazy" width="1238" height="331" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-201.png" alt="" class="wp-image-3100" /> </figure> 

__construct，构造函数，PHP 5 允行开发者在一个类中定义一个方法作为构造函数。具有构造函数的类会在每次创建新对象时先调用此方法，所以非常适合在使用对象之前做一些初始化工作。

\_\_toString，打印一个对象时，如果定义了\_\_toString()方法，就能在测试时，通过echo打印对象体，对象就会自动调用它所属类定义的toString方法，格式化输出这个对象所包含的数据。

__destruct，析构函数，PHP 5 引入了析构函数的概念，这类似于其它面向对象的语言，如C++。析构函数  
会在到某个对象的所有引用都被删除或者当对象被显式销毁时执行。

\_\_construct和\_\_destruct会在对象创建或者销毁时自动调用。

__sleep magic方法在一个对象被序列化的时候调用。

__wakeup magic方法在一个对象被反序列化的时候调用。

## 0x02 序列化注意点

\x00 + 类名+ \x00 + 变量名反序列化出来的是private变量,

\x00 + * + \x00 + 变量名反序列化出来的是protected变量

直接变量名反序列化出来的是public变量<figure class="wp-block-image size-full">

<img loading="lazy" width="1152" height="566" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-202.png" alt="" class="wp-image-3104" /> </figure> 

有时候+号会被识别为空格，需要通过url编码来绕过。

PHP Bug 72663

简单来说就是当序列化字符串中，如果表示对象属性个数的值大于真实的属性个数时就会跳过__wakeup的执行。

## 0x03 session序列化以及phar序列化

Php bug 71101

<a href="https://bugs.php.net/bug.php?id=71101" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://bugs.php.net/bug.php?id=71101</a>

PHP 内置了多种处理器用于存取$_SESSION 数据时会对数据进行序列化和反序列化，常用的有以下三种，对应三种不同的处理格式。<figure class="wp-block-image size-full">

<img loading="lazy" width="1153" height="175" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-203.png" alt="" class="wp-image-3108" /> </figure> 

PHP 提供了session.serialize_handler 配置选项，通过该选项可以设置序列化及反序列化时使用的处理器。  
session.serialize\_handler "php" PHP\_INI_ALL

如果PHP 在反序列化存储的$_SESSION 数据时的使用的处理器和序列化时使用的处理器不同，会导致数据无法正确反序列化，通过特殊的构造，甚至可以伪造任意数据。

范例

<pre class="wp-block-code"><code>当存储是php_serialize处理，然后调用时php去处理
如果这时候注入的数据是a=|O:4:"test":0:{}
那么session中的内容是a:1:{s:1:"a";s:16:"|O:4:"test":0:{}";}
根据解释,其中a:1:{s:1:"a";s:16:"在经过php解析后是被看成键名,
后面就是一个实例化test对象的注入</code></pre>

当配置选项session.auto_start＝Off，两个脚本注册Session会话时使用的序列化处理器不同，就会出现安全问题。

当配置选项session.auto\_start＝On，会自动注册Session 会话，因为该过程是发生在脚本代码执行前，所以在脚本中设定的包括序列化处理器在内的session 相关配选项的设置是不起作用的，因此一些需要在脚本中设置序列化处理器配置的程序会在session.auto\_start＝On 时，销毁自动生成的Session 会话，然后设置需要的序列化处理器，再调用session_start() 函数注册会话，这时如果脚本中设置的序列化处理器与php.ini 中设置的不同，就会出现安全问题。

**phar序列化**

在Blackhat2018，来自Secarma的安全研究员Sam Thomas讲述了一种攻击PHP应用的新方式，利用这种方法可以在不使用unserialize()函数的情况下触发PHP反序列化漏洞。漏洞触发点在使用phar://协议读取文件的时候，文件内容会被解析成phar对象，然后phar对象内的Meta data信息会被反序列化。<a href="https://blog.ripstech.com/2018/new-php-exploitation-
technique/" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://blog.ripstech.com/2018/new-php-exploitation-technique/</a>

可利用函数

<pre class="wp-block-code"><code>ìnclude()、  fopen()、  file_get_contents()、  file()

file_exists($_GET&#91;'file']);
md5_file($_GET&#91;'file']);
filemtime($_GET&#91;'file']);
filesize($_GET&#91;'file']);</code></pre>
