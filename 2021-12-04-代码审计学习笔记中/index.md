# 代码审计学习笔记（中）

<div class="has-toc have-toc">
</div>

## 0x00 SQL注入漏洞

**普通注入**

最容易利用的SQL注入漏洞，比如直接通过注入union查询，分int型和string型，后者需要使用单或双引号闭合。

搜索关键字：`select from`，`mysql_connect`，`mysql_query`，`mysql_fectch_row`，`update`，`insert`，`delete`等。

**编码注入**

最常见的编码注入是MySQL宽字节已经urldecode/rawurldecode函数导致的。

解决宽字节注入的方法（前2种更推荐）：

  1. 在执行查询之前先执行SET NAME 'gbk'，设置character\_set\_client=binary。
  2. 使用pdo方式，在PHP5.3.6及一下版本需要设置setAttribute(PDO::ATTR\_EMULATE\_PREPARES,false);来禁用prepared statements的仿真效果。
  3. 使用mysql\_set\_charset('gbk')设置编码，然后使用mysql\_real\_escape_string()函数被参数过滤。

挖掘宽字节注入的方法：搜索关键字，`SET NAMES`，`character_set_client=gbk`，`mysql_set_charset('gbk')`

挖掘二次urldecode注入的方法：搜索关键字，`urldecode`，`rawurldecode`

**漏洞防范**

通常数据污染有两种方式，一种是被动接收参数，类似于GET、POST等；还有一种是主动获取参数，类似于读取远程页面或者文件内容等。

  * `gpc/runtime`魔术引号。它们只对单引号、双引号、反斜杠及空字符NULL进行过滤，对int型的注入没有多大作用。
  * 过滤类和函数。两种应用场景，程序入口统一过滤和SQL语句运行前过滤。`addslashes`函数的过滤范围与GPC一致。`mysql_[real_]escape_string`函数对【\x00】【\n】【\r】【\】【'】【"】【\x1a】进行过滤，但real接受的是一个连接句柄并根据当前字符集转义字符串（推荐使用）。`intval`等字符转换，将变量转化成int类型。
  * PDO prepare 预编译。通过预编译的方式来处理数据库查询。

## 0x01 XSS漏洞

挖掘XSS漏洞的关键在于寻找没有被过滤的参数，且这些参数传入到输出函数，常用的出处函数列表如下：`print`、`print_r`、`echo`、`printf`、`sprintf`、`die`、`var_dump`、`var_export`。

**漏洞防范**

  * 特殊字符HTML实体转码，列表如下：'、"、<>、\、:、&、#。
  * 标签事件属性黑白名单。

## 0x02 CSRF漏洞

漏洞存在有权限控制的地方。白盒审计时注意核心文件或功能点里是否存在验证token和referer相关的代码。

**漏洞防范**

防御CSRF漏洞的最主要问题是解决可信的问题。

  * 增加token/referer验证避免img标签请求的水坑攻击。
  * 增加验证码。用于敏感操作的页面。

## 0x03 文件操作漏洞

文件操作包括文件包含、文件读取、文件删除、文件修改以及文件上传。

**文件包含漏洞**

文件包含又分为本地文件包含和远程文件包含。这种漏洞大多出现在模块加载、模板加载以及cache调用的地方，比如传入的模块名参数。挖掘是可以先跟踪程序的运行流程，观察模块加载时包含的文件是否可控，另外就是直接搜索`include`、`require`、`include _once`、`require_once`这四个函数来晦朔观察是否存在可控变量。

**文件读取（下载）漏洞**

挖掘经验：一种是先黑盒看看个功能点对应的文件，再去读文件。另一种方式是去搜索`file_get_contents`、`highlight_file`、`fopen`、`readfile`、`fread`、`fgetss`、`fgets`、`parse_ini_file`、`show_source`、`file`函数。

**文件上传漏洞**

挖掘经验：最快的方法是搜索`move_uploaded_file`函数，再去看调用这个函数上传文件的代码存不存在未限制上传格式或者可以绕过，其中问题较多的是黑名单限制文件格式已经未更改文件名的方式，没有更改文件名的情况下，在Apache利用其向前寻找解析格式和IIS的分号解析bug都可以执行代码。

**文件删除漏洞**

挖掘经验：黑盒下测试能否删除某个文件，如果删除不了，再去从执行流程去追提交的文件名参数的传递过程。白盒下搜索有变量参数的`unlink`、`session_destory`。

**通用文件操作防御**

文件操作漏洞利用的共同点：

  1. 由越权引起可以操作未授权操作的文件
  2. 要操作更多文件需要跳转目录
  3. 大多都是直接在请求中传入文件名

防御手段：

  * 合理的权限管理
  * 尽量避免直接传入文件名
  * 避免目录跳转

**文件上传漏洞的防范**

文件上传漏洞利用的方式有两种：文件类型验证不严谨和写入文件不规范。

作者给出了两种防范方案：

  * 白名单方式过滤文件拓展名，使用in_array或者三等于符号来对比拓展名。
  * 保存上传的文件时重命名文件，文件名命名规则采用时间戳的拼接随机数的MD5值，md5(time()+rand(1,10000))。

## 0x04 代码执行漏洞

挖掘经验：载入缓存或者模板以及对变量处理不严格导致PHP语句通过`eval`或`assert`执行。`preg_replace`在对字符串处理时，如URL、HTML标签已经文章内容等过滤功能，可能存在漏洞。复杂程序中可能存在`call_user_func`和`call_user_func_array`动态调用的代码执行。还有一类非常常见的动态函数的代码执行，如：_$\_GET($\_POST["xx"])_，基于此的各种变形常被作为Web后门。

可能存在过滤不严的调用函数：`call_user_func`、`call_user_func_array`、`array_map`、`usort`、`uasort`、`uksort`、`array_filter`、`array_reduce`、`array_diff_uassoc`、`array_diff_ukey`、`array_udiff`、`array_udiff_assoc`、`array_udiff_uassoc`、`array_uintersect`、`array_uintersect_uassoc`、`array_walk`、`array_walk_recursive`、`xml_set_character_data_handler`、`xml_set_default_handler`、`xml_set_element_handler`、`xml_set_end_namespace_decl_handler`、`xml_set_external_entity_ref_handler`、`xml_set_notation_decl_handler`、`xml_set_processing_instruction_handler`、`xml_set_start_namespace_decl_handler`、`xml_set_unparsed_entity_decl_handler`、`stream_filter_register`、`set_error_handler`、`register_shutdown_function`、`register_tick_function`。

**漏洞防范**

采用参数白名单过滤，结合正则表达式进行限制。

## 0x05 命令执行漏洞

挖掘经验：直接搜索`system`、`exec`、`shell_exec`、`passthru`、`pcntl_exec`、`popen`、`proc_open`函数名。

**漏洞防范**

命令防注入函数：`escapeshellcmd`过滤整条命令，`escapeshellarg`过滤参数。

参数白名单。

## 0x06 变量覆盖漏洞

挖掘经验：由函数导致的变量覆盖比较容易发现，只要搜下参数带有变量的`extract`、`parse_str`，然后回溯变量是否可控。`import_request_variable`函数则相当于开启了全局变量的注册，寻找未被初始化且操作前没有赋值的变量作为参数提交即可，另外写在此函数之前的所有变量都可覆盖。双`$$`符号注册变量会导致变量覆盖，也可以通过搜索来挖掘。

**漏洞防范**

  * 使用原始变量。不进行变量注册，直接使用原生的$\_GET、$\_POST等数组变量进行操作，如果需要注册个别变量，可直接在代码中定义，然后再把请求中的值赋值给它。
  * 验证变量存在。加入注册变量前对变量是否存在的判断。

## 0x07 逻辑处理漏洞

挖掘经验：通读功能点源码，熟悉业务流程，关注程序是否可重复安装、修改密码处是否可越权修改其他用户密码、找回密码验证码是否可被暴力破解以及修改其他用户密码、Cookie验证是否可绕过。

**等于与存在判断绕过**

  * `in_array`，用于判断一个值是否在某一个数组列表里面，但是它比较前会做类型转换，可能将字符串转换为整型，绕过检查。
  * `is_numeric`，用于判断一个变量是否为数字，当传入的参数时hex时直接通过并返回true，而MYSQL是可以直接使用hex编码代替字符串明文的，虽然不能直接 注入SQL语句，但存在二次注入和XSS等漏洞隐患。
  * 双等于和三等于。双等于会在判断前对变量进行类型转换，而三等于则不会。

**账户体系中的越权漏洞**

**未exit或return引发的安全问题**

某些情况下，经过条件判断后忘记写return、die、exit等退出行为，导致程序继续执行。

**常见支付漏洞**

客户端修改单价、总价、数量，服务端未严格校验。

重复发包来利用时间差，以少量的钱多次购买。

**漏洞防范**

  * 深入熟悉业务逻辑
  * 注意多熟悉函数的功能和差异

## 0x08 会话认证漏洞

挖掘经验：观察程序的登录功能代码，寻找是否存在业务逻辑能够控制session值或者直接让密码验证的漏洞。另外需要关注程序验证是否为登录的代码，即是否直接验证cookie值是否为空，还是通过cookie值来作为当前用户。

**漏洞防范**

严格现在输入的异常字符以及避免使用客户端提交上来的内容去直接进行操作，应该把cookie同session结合使用，避免将敏感信息存入cookie。
