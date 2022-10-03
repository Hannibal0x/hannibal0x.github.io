# SXC 部分WriteUp



<div class="has-toc have-toc">
</div>

## 0x00 签到

点开视频即可。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="280" height="66" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-125.png" alt="" class="wp-image-1055" /></figure>
</div>

## 0x01 牛年大吉

右键点击属性。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="452" height="128" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-126.png" alt="" class="wp-image-1056" /></figure>
</div>

## 0x02 Flag不在这

010editor打开文件，搜索flag字符串。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-127.png" alt="" class="wp-image-1059" width="580" height="56" /></figure>
</div>

## 0x03 拼图

根据鬼刀找到原图，不会用工具，但图片数量不多，而且比较清晰，这里直接对照原图，简单拼一下。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="464" height="283" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-128.png" alt="" class="wp-image-1061" /></figure>
</div>

## 0x04 网络深处

拨号音.wav，想到DTMF，找工具解码得到`15975384265`，这个就是压缩包的密码，解压后把电话录音.wav导入Audacity分析，转频谱图发现如下信息：<figure class="wp-block-image size-large">

<img loading="lazy" width="748" height="180" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-129.png" alt="" class="wp-image-1067" /> </figure> 

百度可知tupper是自引用公式，也叫Tupper自我指涉公式，此公式的二维图像与公式本身外观一样，根据一个式子，在坐标图上显现出所要表达的东西。

```
from PIL import Image

k1=636806841748368750477720528895492611039728818913495104112781919263174040060359776171712496606031373211949881779178924464798852002228370294736546700438210687486178492208471812570216381077341015321904079977773352308159585335376746026882907466893864815887274158732965185737372992697108862362061582646638841733361046086053127284900532658885220569350253383469047741742686730128763680253048883638446528421760929131783980278391556912893405214464624884824555647881352300550360161429758833657243131238478311219915449171358359616665570429230738621272988581871

# Assign k1,k2, k3 to k to get desired image
k = k1
width = 106
height = 17
scale = 5

fname = "foo"
image  = Image.new("RGB", (width, height),(255, 255, 255))

for x in range (width):
    for y in range (height):
        if ((k+y)//17//2**(17*int(x)+int(y)%17))%2 > 0.5:
            # Image need to be flipped vertically - therefore y = height-y-1
            image.putpixel((x, height-y-1), (0,0,0))


#scale up image
image = image.resize((width*scale,height*scale))
image.save(fname+".png")
```

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-130.png" alt="" class="wp-image-1071" width="437" height="69" /></figure>
</div>

## 0x05 YLBNB

先wireshark分析，追踪tcp流，发现xor.py代码，里面有YLB字样，猜测有用。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="440" height="251" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-131.png" alt="" class="wp-image-1079" /></figure>
</div>

继续往下看，在`tcp.stream eq 17`时，用户POST了一个secret.cpython-38.pyc，同样带有YLB的字样。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-132.png" alt="" class="wp-image-1082" width="600" height="90" /></figure>
</div>

导出pyc，在<a href="https://tool.lu/pyc/" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://tool.lu/pyc/</a>反编译。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-133.png" alt="" class="wp-image-1087" width="469" height="88" /></figure>
</div>

用户POST了一个YLBSB.zip，提取出来，解压得到YLBSB.xor。<figure class="wp-block-image size-large">

<img loading="lazy" width="591" height="28" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-134.png" alt="" class="wp-image-1090" /> </figure> 

编写解密脚本。

<pre class="wp-block-code"><code>import base64
key = "YLBSB?YLBNB!"
file =open("YLBSB.docx", "wb")
enc =open("YLBSB.xor", "rb")

plain = enc.read().decode()
count = 0
d =''
for i in plain:
    a = chr(ord(i) ^ ord(key&#91;count % len(key)]))
    d = d + a
    count = count + 1
file.write(base64.b64decode(d))</code></pre>

发现Word文档存在异常。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="990" height="480" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-135.png" alt="" class="wp-image-1093" /></figure>
</div>

猜测文字白色，调颜色为黑色。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="250" height="37" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-136.png" alt="" class="wp-image-1095" /></figure>
</div>
