# 代码审计学习笔记（上）

<div class="has-toc have-toc">
</div>

## 0x00 前言

学习《代码审计 企业级Web代码安全架构》一书所做的笔记。

## 0x01 PHP核心配置详解

<a rel="noreferrer noopener" href="https://www.php.net/manual/zh/ini.list.php" data-type="URL" data-id="https://www.php.net/manual/zh/ini.list.php" target="_blank" rel="nofollow" >官方配置说明</a>

**PHP\_INI\_* 常量的定义**

| 常量               | 含义                                                                                                                                                                                     |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PHP_INI_USER`   | 可在用户PHP脚本或 <a href="https://www.php.net/manual/zh/configuration.changes.php#configuration.changes.windows" target="_blank"  rel="nofollow" >Windows 注册表</a>以及 <var>.user.ini</var> 中设定 |
| `PHP_INI_PERDIR` | 可在 <var>php.ini</var>，<var>.htaccess</var> 或 <var>httpd.conf</var> 中设定                                                                                                                 |
| `PHP_INI_SYSTEM` | 可在 <var>php.ini</var> 或 <var>httpd.conf</var> 中设定                                                                                                                                      |
| `PHP_INI_ALL`    | 可在任何地方设定                                                                                                                                                                               |
| php.ini only     | 可仅在php.ini中设置                                                                                                                                                                          |</figure> 

## 0x02 会影响PHP脚本安全的配置列表以及核心配置选项

**_1.register_globals（全局变量注册开关）_**

该选项在设置为on的情况下，会直接把用户GET、POST等方式提交上来的参数注册成全局变量并初始化值为参数对应的值，使得提交参数可以直接在脚本中使用。register\_globals在PHP版本小于等于4.2.3时设置为PHP\_INI_ALL，从PHP 5.3.0起被废弃，不推荐使用，在PHP 5.4.0中移除了该选项。

**_2.allow\_url\_include（是否运行包含远程文件）_**

在该配置为on的情况下，它可以直接包含远程文件，当存在include（$var）且$var可控的情况下，可以直接控制$var变量来执行PHP代码。allow\_url\_include在PHP 5.2.0后默认设置为off，配置范围是PHP\_INI\_ALL。与之类似的配置有allow\_url\_fopen，配置是否允许打开远程文件。

**_3.magic\_quotes\_gpc（魔术引号自动过滤）_**

magic\_quotes\_gpc只要被开启，在不存在编码或者其他特殊绕过的情况下，可以使得很多漏洞无法被利用。当该选项设置为on时，会自动在GET、POST、COOKIE变量中的单引号（'）、双引号（"）、反斜杠（\）及空字符（NULL）的前面加上反斜杠（\），但是在PHP 5中magic\_quotes\_gpc并不会过滤$\_SERVER变量，导致很多类似client-ip、referer一类的漏洞能够利用。在PHP 5.3之后的不推荐使用magic\_quotes_gpc，PHP 5.4之后干脆被取消。

**4.magic\_quotes\_runtime_（魔术引号自动过滤）_** 

它跟magic\_quotes\_gpc的区别是，处理的对象不一样，magic\_quotes\_runtime只对从数据库或者文件中获取的数据进行过滤。同样，magic\_quotes\_runtime在PHP 5.4之后也被取消，配置范围是PHP\_INI\_ALL。

有部分函数受它的影响，所以在某些情况下这个配置是可以绕过的，受影响的列表如下：

`get_meta_tags（）`、`file_get_contents（）`、`file（）`、`fgets（）`、`fwrite（）`、`fread（）`、`fputcsv（）`、`stream_socket_recvfrom（）`、`exec（）`、`system（）`、`passthru（）`、`stream_get_contents（）`、`bzread（）`、`gzfile（）`、`gzgets（）`、`gzwrite（）`、`gzread（）`、`exif_read_data（）`、`dba_insert（）`、`dba_replace（）`、`dba_fetch（）`、`ibase_fetch_row（）`、`ibase_fetch_assoc（）`、`ibase_fetch_object（）`、`mssql_fetch_row（）`、`mssql_fetch_object（）`、`mssql_fetch_array（）`、`mssql_fetch_assoc（）`、`mysqli_fetch_row（）`、`mysqli_fetch_array（）`、`mysqli_fetch_assoc（）`、`mysqli_fetch_object（）`、`pg_fetch_row（）`、`pg_fetch_assoc（）`、`pg_fetch_array（）`、`pg_fetch_object（）`、`pg_fetch_all（）`、`pg_select（）`、`sybase_fetch_object（）`、`sybase_fetch_array（）`、`sybase_fetch_assoc（）`、`SplFileObject：fgets（）`、SplFileObject：fgetcsv（）`、`SplFileObject：fwrite（）`

**5.magic\_quotes\_sybase_（魔术引号自动过滤）_** 

设置为on时，它会覆盖掉magic\_quotes\_gpc=on的配置。而它们之前的区别在于处理方式不同，magic\_quotes\_sybase仅仅是转义了空字符和把单引号（'）变成了双引号（''）。PHP 5.4 后移除。

**_6.safe_mode（安全模式）_**

这个配置会出现下面限制：

  * 所有文件操作函数（例如unlink（）、file（）和include（））等都会受到限制。
  * 通过函数popen（）、system（）以及exec（）等函数执行命令或程序会提示错误。

下面是启用safe_mode指令时受影响的函数、变量及配置指令的完整列表：

`apache_request_headers（）`、`ackticks（）`、`hdir（）`、`hgrp（）`、`chmode（）`、`chown（）`、`copy（）`、`dbase_open（）`、`dbmopen（）`、`dl（）`、`exec（）`、`filepro（）`、`filepro_retrieve（）`、`ilepro_rowcount（）`、`fopen（）`、`header（）`、`highlight_file（）`、`ifx_*`、`ingres_*`、`link（）`、`mail（）`、`max_execution_time（）`、`mkdir（）`、`move_uploaded_file（）`、`mysql_*`、`parse_ini_file（）`、`passthru（）`、`pg_lo_import（）`、`popen（）`、`posix_mkfifo（）`、`putenv（）`、`rename（）`、`zmdir（）`、`set_time_limit（）`、`shell_exec（）`、`show_source（）`、`symlink（）`、`system（）`、`touch（）`

**7_.open_basedir PHP可访问目录_**

open\_basedir指令用来限制PHP只能访问哪些目录，通常我们只需要设置Web文件目录即可，如果需要加载外部脚本，也需要把脚本所在目录路径加入到open\_basedir指令中，多个目录以分号（；）分割。

使用open\_basedir需要注意的一点是，指定的限制实际上是前缀，而不是目录名。例如，如果配置open\_basedir=/www/a，那么目录/www/a和/www/ab都是可以访问的。所以如果要将访问仅限制在指定的目录内，请用斜线结束路径名。例如设置成：open_basedir=/www/a/。

当open\_basedir配置目录后，执行脚本访问其他文件都需要验证文件路径，因此在执行效率上面也会有一定的影响。该指令的配置范围在PHP版本小于5.2.3时是PHP\_INI\_SYSTEM，在PHP版本大于等于5.2.3是PHP\_INI_ALL。

_**8.disable_functions（禁用函数）**_

使用disable\_functions指令来禁止一些敏感函数的使用。同时把dl（）函数也加到禁止列表，因为攻击者可以利用dl（）函数来加载自定义的PHP扩展以突破disable\_functions指令的限制。

**_9.display\_errors和error\_reporting错误显示_**

display\_errors表明是否显示PHP脚本内部错误的选项，在生产环境中设置display\_errors=on会带来一些安全隐患。error_reporting选项用来配置错误显示的级别，可使用数字也可使用内置常量配置。<figure class="wp-block-image size-full">

<img loading="lazy" width="1088" height="356" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/12/图片-2.png" alt="" class="wp-image-4745" /> </figure> 

## 0x03 常用指令以及对应的说明

<figure class="wp-block-image size-full">

<img loading="lazy" width="1088" height="724" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/12/图片-3.png" alt="" class="wp-image-4746" /> </figure> 

## 0x04 常见的代码审计思路

**敏感函数回溯参数过程**

目前使用最多。优点是只需搜索相应敏感关键字，即可快速挖掘想要的漏洞。缺点是没有全覆盖代码，定位漏洞利用点花费时间长，无法挖掘逻辑漏洞。

**通读全文代码**

首先看程序的大体代码结构，如主目录的文件，模块目录的文件等等，还有注意文件的名称、大小、创建时间。

目录结构，需要特别注意的文件：

  1. 函数集文件，通常包含functions或者common等关键字，这些文件包含一些公共的函数，提供统一调用。寻找技巧：打开index.php或者一些功能性文件。
  2. 配置文件，通常命名中包含config等关键字，配置文件包括Web程序运行必须的功能性配置选项以及数据库等配置信息。需要注意配置文件中参数值使用单引号还是双引号，如果是双引号则很可能存在代码执行漏洞。
  3. 安全过滤文件，通常命名中有filter、safe、check等关键字，主要是对参数进行过滤。
  4. index文件，程序的入口文件，可以了解整个程序的架构、运行的流程、包含到的文件。

通读全文代码的好处是可以更好地了解程序的架构以及业务逻辑，能够挖掘到更多、更高质量的逻辑漏洞。缺点是花费的时间多，复杂程序的分析困难。

**根据功能点定向审计**

  * 文件上传功能。最常见的漏洞是任意文件上传。还有SQL注入，因为一般程序员不会注意到对文件名进行过滤，但有需要把文件名存入数据库。
  * 文件管理功能。如果程序将文件名或文件路径直接在参数中传递，则很可能存在任意文件操作漏洞。还可能存在XSS，程序会在页面输出文件名，而通常会疏忽对文件名进行过滤。
  * 登录认证功能。目前大多认证方式是基于Cookie和Session的，可能存在任意用户登录漏洞，或者越权漏洞。
  * 找回密码功能。如果可以重置管理员密码，就能间接控制业务权限甚至服务器权限。最常见的是验证码爆破。
