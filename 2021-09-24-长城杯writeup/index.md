# 长城杯writeup

<div class="has-toc have-toc">
</div>

## 0x00 签到

题目给出了一串16进制的字符串

<pre class="wp-block-code"><code>5a6d78685a3374585a57786a6232316c5833527658324e6f5957356e5932686c626d64695a544639</code></pre>

转ascii码，得到`ZmxhZ3tXZWxjb21lX3RvX2NoYW5nY2hlbmdiZTF9`，再base64解码下，得到`flag{Welcome_to_changchengbe1}`

## 0x01 baby_rsa

enc.py的源码如下

<pre class="wp-block-code"><code>#!/usr/bin/env python3

from Crypto.Util.number import *
from secret import flag, v1, v2, m1, m2


def enc_1(val):
    p, q = pow(v1, (m1+1))-pow((v1+1), m1), pow(v2, (m2+1))-pow((v2+1), m2)
    assert isPrime(p) and isPrime(q) and (
        p*q).bit_length() == 2048 and q &lt; p &lt; q &lt;&lt; 3
    return pow(val, 0x10001, p*q)


def enc_2(val):
    assert val.bit_length() &lt; 512
    while True:
        fac = &#91;getPrime(512) for i in range(3)]
        if isPrime(((fac&#91;0]+fac&#91;1]+fac&#91;2]) &lt;&lt; 1) - 1):
            n = fac&#91;0]*fac&#91;1]*fac&#91;2]*(((fac&#91;0]+fac&#91;1]+fac&#91;2]) &lt;&lt; 1) - 1)
            break
    c = pow(val, 0x10001, n)
    return (c, n, ((fac&#91;0]+fac&#91;1]+fac&#91;2]) &lt;&lt; 1) - 1)


if __name__ == "__main__":
    assert flag&#91;:5] == b'flag{'
    plain1 = bytes_to_long(flag&#91;:21])
    plain2 = bytes_to_long(flag&#91;21:])
    print(enc_1(plain1))
    print(enc_2(plain2))</code></pre>

enc_1的加密，参照大佬的<a href="https://blog.csdn.net/m0_49109277/article/details/120387581?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522163227754016780261984003%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=163227754016780261984003&biz_id=&utm_medium=distribute.pc_search_result.none-task-code-2~all~first_rank_ecpm_v1~rank_v31_ecpm-6-120387581-0.pc_search_result_control_group&utm_term=%E9%95%BF%E5%9F%8E%E6%9D%AF" data-type="URL" data-id="https://blog.csdn.net/m0_49109277/article/details/120387581?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522163227754016780261984003%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=163227754016780261984003&biz_id=&utm_medium=distribute.pc_search_result.none-task-code-2~all~first_rank_ecpm_v1~rank_v31_ecpm-6-120387581-0.pc_search_result_control_group&utm_term=%E9%95%BF%E5%9F%8E%E6%9D%AF" target="_blank" rel="noreferrer noopener" rel="nofollow" >wp</a>复现<figure class="wp-block-image size-full">

<img loading="lazy" width="245" height="73" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-181.png" alt="" class="wp-image-3870" /> </figure> 

`v1, v2, m1, m2`可爆，然后enc_2，m很小不需要这么多模数，只需要知道p就好了，然后记得v1确定之后框定一下m1的范围就很快可以爆破出来。脚本如下：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Crypto.Util.number import *
from gmpy2 import *
from math import log
import sys

c1 = 15808773921165746378224649554032774095198531782455904169552223303513940968292896814159288417499220739875833754573943607047855256739976161598599903932981169979509871591999964856806929597805904134099901826858367778386342376768508031554802249075072366710038889306268806744179086648684738023073458982906066972340414398928411147970593935244077925448732772473619783079328351522269170879807064111318871074291073581343039389561175391039766936376267875184581643335916049461784753341115227515163545709454746272514827000601853735356551495685229995637483506735448900656885365353434308639412035003119516693303377081576975540948311
c2 = (40625981017250262945230548450738951725566520252163410124565622126754739693681271649127104109038164852787767296403697462475459670540845822150397639923013223102912674748402427501588018866490878394678482061561521253365550029075565507988232729032055298992792712574569704846075514624824654127691743944112075703814043622599530496100713378696761879982542679917631570451072107893348792817321652593471794974227183476732980623835483991067080345184978482191342430627490398516912714451984152960348899589532751919272583098764118161056078536781341750142553197082925070730178092561314400518151019955104989790911460357848366016263083, 43001726046955078981344016981790445980199072066019323382068244142888931539602812318023095256474939697257802646150348546779647545152288158607555239302887689137645748628421247685225463346118081238718049701320726295435376733215681415774255258419418661466010403928591242961434178730846537471236142683517399109466429776377360118355173431016107543977241358064093102741819626163467139833352454094472229349598479358367203452452606833796483111892076343745958394932132199442718048720633556310467019222434693785423996656306612262714609076119634814783438111843773649519101169326072793596027594057988365133037041133566146897868269, 39796272592331896400626784951713239526857273168732133046667572399622660330587881579319314094557011554851873068389016629085963086136116425352535902598378739)
e = 0x10001

# enc_2
c2, n2, x = c2[0], c2[1], c2[2]
assert n2 % x == 0
n2 = x
p1 = 191
p2 = 193
p3 = 627383
p4 = 1720754738477317127758682285465031939891059835873975157555031327070111123628789833299433549669619325160679719355338187877758311485785197492710491
phi2 = (p1 - 1) * (p2 - 1) * (p3 - 1) * (p4 - 1)
d2 = invert(e, phi2)
m2 = pow(c2, d2, n2)
flag2 = long_to_bytes(m2)

# enc_1
lbound, ubound = 2 ** 1021, 2 ** 1027
for v1 in range(2, 1000000):
    for m1 in range(int(log(lbound, v1)), int(log(ubound, v1))):
        p = pow(v1, (m1 + 1)) - pow((v1 + 1), m1)
        if isPrime(p) and 1021 < p.bit_length() < 1027:
            phi1 = p - 1
            d1 = invert(e, phi1)
            m = pow(c1, d1, p)
            if long_to_bytes(m).startswith(b'flag'):
                flag1 = long_to_bytes(m)
                flag = flag1 + flag2
                print(flag)
                sys.exit(0)
```

<img loading="lazy" width="372" height="38" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-182.png" alt="" class="wp-image-3871" /> </figure> 

## 0x02 Just_cmp-re

直接丢到ida里面去分析，在主函数发现进行了flag的字符串比较。<figure class="wp-block-image size-full">

<img loading="lazy" width="612" height="303" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-170.png" alt="" class="wp-image-3854" /> </figure> 

对输入的字符进行右移3位相当于除8，也就是把字符串分为8个一组，对应和qword_201060的值做减法，可以得到主函数里显示的字符串。<figure class="wp-block-image size-full">

<img loading="lazy" width="468" height="270" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-171.png" alt="" class="wp-image-3855" /> </figure> 

数组元素的值如下：<figure class="wp-block-image size-full">

<img loading="lazy" width="884" height="31" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-172.png" alt="" class="wp-image-3856" /> </figure> 

编写脚本如下：

<pre class="wp-block-code"><code>#-*- coding:utf-8 -*-

enc = "flag{********************************}"
m = &#91;0x0A07370000000000,
     0x380B06060A080A37,
     0x3B0F0E38083B0A07,
     0x373B0709060B0A3A,
     0x0000000F38070F0D]

import binascii

flag = b''
for i in range(5):
    p = enc&#91;i*8:(i+1)*8]
    a = binascii.b2a_hex(p.encode('ascii')&#91;::-1])
    b = binascii.a2b_hex(hex(int(a,16) + m&#91;i])&#91;2:])&#91;::-1]
    flag += b
print (flag)</code></pre>

`flag{a14a424005b14e2b89ed45031ea791b9}`

## 0x03 java_url

首页源代码中有一条注释，初步推测此处的利用包含漏洞找flag文件。<figure class="wp-block-image size-full">

<img loading="lazy" width="630" height="80" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-173.png" alt="" class="wp-image-3858" /> </figure> 

先在download路径下发现<figure class="wp-block-image size-full">

<img loading="lazy" width="890" height="544" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-175.png" alt="" class="wp-image-3860" /> </figure> 

filename输入的字符串包含flag时，返回信息有变化。<figure class="wp-block-image size-full">

<img loading="lazy" width="87" height="26" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-176.png" alt="" class="wp-image-3861" /> </figure> 

`filename=../`确定存在文件包含漏洞，并且泄露tomcat的绝对路径`/usr/local/tomcat/webapps/ROOT/WEB-INF/`。<figure class="wp-block-image size-full">

<img loading="lazy" width="960" height="517" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-179.png" alt="" class="wp-image-3866" /> </figure> 

然后构造

<pre class="wp-block-code"><code>filename=../../../../../../../../../usr/local/tomcat/webapps/ROOT/WEB-INF/web.xml</code></pre>

下载到本地可以看到<figure class="wp-block-image size-full">

<img loading="lazy" width="1368" height="578" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-180.png" alt="" class="wp-image-3867" /> </figure> 

从而确定.class文件的路径`WEB-INF/classes/com/test2/aaa1`，接着构造

```
filename=../../../../../../../../../usr/local/tomcat/webapps/ROOT/WEB-INF/classes/com/test2/aaa1/testURL.class

filename=../../../../../../../../../usr/local/tomcat/webapps/ROOT/WEB-INF/classes/com/test2/aaa1/download.class
```

使用jd-gui-1.6.6.jar进行反编译分析class文件，发现download.class中的过滤flag。


<img loading="lazy" width="603" height="83" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-183.png" alt="" class="wp-image-3873" /> </figure> 

testURL.class中可以通过`/testURL?url=url:file:///flag`或者`/testURL?url=%00file:///flag`来进行绕过。<figure class="wp-block-image size-full">

<img loading="lazy" width="1019" height="201" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-184.png" alt="" class="wp-image-3874" /> </figure> 

## 0x04 你这flag保熟吗

打开文件发现有两张图和一个加密的rar压缩包。<figure class="wp-block-image size-full">

<img loading="lazy" width="413" height="161" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-185.png" alt="" class="wp-image-3877" /> </figure> 

丢到binwalk发现都有一个压缩包，foremost分离一下。<figure class="wp-block-image size-full">

<img loading="lazy" width="693" height="277" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-186.png" alt="" class="wp-image-3880" /> </figure> 

得到⼀个password.excel和⼀个hint，提示base64还给出了一个序列。<figure class="wp-block-image size-full">

<img loading="lazy" width="644" height="128" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-187.png" alt="" class="wp-image-3883" /> </figure> 

在表格中画出来，看了dalao的<a href="https://blog.csdn.net/qq_42880719/article/details/120381636" data-type="URL" data-id="https://blog.csdn.net/qq_42880719/article/details/120381636" target="_blank" rel="noreferrer noopener" rel="nofollow" >wp</a>才知道是个希尔伯特曲线。<figure class="wp-block-image size-full">

<img loading="lazy" width="336" height="407" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-188.png" alt="" class="wp-image-3885" /> </figure> 

套一下脚本

<pre class="wp-block-code"><code>from hilbertcurve.hilbertcurve import HilbertCurve
import xlrd
readbook = xlrd.open_workbook('password.xls')
sheet = readbook.sheet_by_index(0)
f = open('base64.txt','w+')
hilbert_curve = HilbertCurve(17, 2)
base64 = ''
for i in range(65536):
    &#91;j,k] = hilbert_curve.point_from_distance(i)
    base64 += sheet.cell(j,k).value
f.write(base64)</code></pre>

得到⼀⼤串base64和很多=，删除到只剩俩。循环解base64，最后得到`1f_y0u_h4ve_7he_fllllllag,_I_muSt_vvant_1t!`，解压文件发现类似brainfuck的代码。前面所有的.(点)都被出题人删了，而作用是输出指针指向的单元内容，所以前面那一长串都无法输出，值只能被保留在对应单元中。在<a href="https://fatiherikli.github.io/brainfuck-visualizer" target="_blank"  rel="nofollow" >https://fatiherikli.github.io/brainfuck-visualizer</a>，可以看到每个单元里面的信息，运行一段时间后，得到：<figure class="wp-block-image size-full">

<img loading="lazy" width="1018" height="784" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-190.png" alt="" class="wp-image-3888" /></figure> 

拼凑一下，得到：`117,111,122,116,123,83,114,82,121,118,105,103,95,88,102,105,101,118,95,49,72,95,52,95,101,101,48,109,119,118,105,117,102,33,95,120,102,105,101,118,125`

转为ascll，得到`uozt{SrRyvig_Xfiev_1H_4_ee0mwviuf!_xfiev}`<figure class="wp-block-image size-full">

<img loading="lazy" width="561" height="538" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-191.png" alt="" class="wp-image-3889" /> </figure> 

用atbash解密一下，得到`flag{HiIbert_Curve_1S_4_vv0nderfu!_curve}`

## 0x05 ez_python

题目内容：樱桃猫写了自己的第一个flask网站，你能帮他看看有什么问题吗？

打开首页，看看源代码。<figure class="wp-block-image size-full">

<img loading="lazy" width="240" height="21" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-177.png" alt="" class="wp-image-3864" /> </figure> 

传入pic参数后，页面的返回图片会变化。<figure class="wp-block-image size-full">

<img loading="lazy" width="334" height="322" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-178.png" alt="" class="wp-image-3865" /> </figure>
