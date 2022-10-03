# 凌虚平台CTF训练营（加密解密+隐写+取证）

<div class="has-toc have-toc">
</div>

## 0x00 hash还原

开局一张图，看这加密方式感觉像是md5。将`0cc175b9c0f1b6a831c399e269772661`进行MD5解密，得到a，确认加密方法后，找到一个类似的WP，下面开始爆破。<figure class="wp-block-image size-large is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/image_1.png" alt="" class="wp-image-1108" width="580" height="114" /> </figure> 

脚本如下：

<pre class="wp-block-code"><code>from string import ascii_letters,digits
import hashlib
import itertools

flag= '7e76d39945'
d=ascii_letters+digits
dic=itertools.product(d,repeat=4)
for i in dic:
    res=hashlib.md5(''.join(i)).hexdigest()
    if res&#91;0:10]==flag:
        print i
        print res</code></pre>

## 0x01 大明湖

发现图片属性中有一串16进制的数字。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-137.png" alt="" class="wp-image-1114" width="431" height="53" /></figure>
</div>

解出压缩包的密码，打开key即可得到flag。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-138.png" alt="" class="wp-image-1116" width="547" height="268" /></figure>
</div>

## 0x02 画图

打开文件，发现一堆255的数值，结合题目画图，想到用像素点画图。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="643" height="217" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-139.png" alt="" class="wp-image-1118" /></figure>
</div>

导出数值，编写代码：

<pre class="wp-block-code"><code>from PIL import Image

x = 173
y = 173
      
im = Image.new("RGB",(x,y))#创建图片
file = open('t.txt') #打开rbg值文件

#通过一个个rgb点生成图片
for i in range(0,x):
  for j in range(0,y):
    line = file.readline()#获取一行
    rgb = line.split(" ")#分离rgb
    im.putpixel((i,j),(int(rgb&#91;2]),int(rgb&#91;3]),int(rgb&#91;4])))#rgb转化为像素
im.show()</code></pre>

## 0x03 回忆童年

binwalk发现图片内部有压缩包文件，foremost出来，在010下发现文件头异常。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="641" height="119" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-157.png" alt="" class="wp-image-1181" /></figure>
</div>

修改后缀，得到图片，tips说答案为动漫的名字。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-158.png" alt="" class="wp-image-1184" width="243" height="337" /></figure>
</div>

最后flag试了很久，龙珠、Dragonball，但万万忘记了拼音qilongzhu，根据图片是倒过来的，那么将答案也倒过来，uhzgnoliq。

## 0x04 损坏的二维码

可以看到上面两个定位符和右下方的点本该是正方形但变成了矩形。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="143" height="150" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-154.png" alt="" class="wp-image-1173" /></figure>
</div>

利用画图工具修改。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-159.png" alt="" class="wp-image-1188" width="170" height="171" /></figure>
</div>

## 0x05 细心的大象

在属性里面发现一段base64，解密得到`MSDS456ASD123zz`。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-155.png" alt="" class="wp-image-1176" width="265" height="320" /></figure>
</div>

binwalk发现图片内部有rar压缩包文件，foremost出来，用刚刚的密码解压，得到一张图片，更改高度后，拿到flag。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-156.png" alt="" class="wp-image-1179" width="211" height="189" /></figure>
</div>

## 0x06 被攻破的后台

access.log是Apache的日志文件，打开能够看到黑客使用 head方式进行了目录扫描。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="884" height="237" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-161.png" alt="" class="wp-image-1195" /></figure>
</div>

黑客发现了管理员后台页面，对 admin.php 进行暴力破解。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-162.png" alt="" class="wp-image-1198" width="580" height="18" /></figure>
</div>

如果爆破成功并且登录，那么会302跳转到后台，所以我们搜索 302 状态码。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="763" height="34" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-163.png" alt="" class="wp-image-1202" /></figure>
</div>

## 0x07 木册木兰

木册木兰指的应该就是栅栏密码，txt中密文为`fsf5lrdwacloggwqi11l`，在线解密。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="251" height="57" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-160.png" alt="" class="wp-image-1192" /></figure>
</div>

## 0x08 SSCTF签到题

首先得到一串base64编码`Z2dRQGdRMWZxaDBvaHRqcHRfc3d7Z2ZoZ3MjfQ==`，解密得到`ggQ@gQ1fqh0ohtjpt_sw{gfhgs#}`，猜测为栅栏密码，7栏时解得`ggqht{ggQht_gsQ10jsf#@fopwh}`，再经过凯撒密码解密，得到`ssctf{ssCtf_seC10ver#@rabit}`。

## 0x09 base\_not\_only_64

根据题目可知，是base家族的解密。

```
4B46445759534B51494E34444F5443464E42555555564A5A504A49464B564A4C4D495A5643364B534E4A344847574B444E5243413D3D3D3D
base16decode:
KFDWYSKQIN4DOTCFNBUUUVJZPJIFKVJLMIZVC6KSNJ4HGWKDNRCA====
base32decode:
QGlIPCx7LEhiJU9zPUU+b3QyRjxsYClD
base64decode:
@iH<,{,Hb%Os=E>ot2F<l`)C
base91decode:
flag{base_n0t_3asy}
```


## 0x0A 手机热点

题目中说明手机共享，通过协议分级统计可知，用到了蓝牙。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-164.png" alt="" class="wp-image-1214" width="633" height="300" /></figure>
</div>

搜索flag字符串，发现异常流量。<figure class="wp-block-image size-large">

<img loading="lazy" width="1056" height="502" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-167.png" alt="" class="wp-image-1218" /> </figure> 

导出分组字节流，解压得到gif。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="223" height="79" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-168.png" alt="" class="wp-image-1219" /></figure>
</div>

## 0x0B 百里挑一

搜索flag字符串，得到一半。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="755" height="78" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-169.png" alt="" class="wp-image-1224" /></figure>
</div>

追踪流，查找}，得到后一半。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-171.png" alt="" class="wp-image-1231" width="145" height="29" /></figure>
</div>

## 0x0C 冬马和纱

用010打开，搜索FFD9文件尾，发现大片空白区域，下端以FFFB的MP3格式开头，导出，能够正常播放，联想到属性里的单词，猜测是mp3加密。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-188.png" alt="" class="wp-image-1319" width="397" height="165" /></figure>
</div>

利用MP3stego来解密。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="797" height="242" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-189.png" alt="" class="wp-image-1321" /></figure>
</div>

## 0x0D ping?

发现icmp的Data字段是由26字母顺序重复组成的，且长度不同，和之前做过的第三届“百越杯”福建省高校网络空间安全大赛的题目很相似，数出长度，编写脚本。

<pre class="wp-block-code"><code>a=&#91;102,108,97,103,123,118,101,114,121,103,111,111,100,125]
flag= ''
for i in a:
	flag=flag+chr(i)
print(flag)</code></pre>

## 0x0E 快！快！快！

脚本如下：

```python
import hashlib

Q1=103766439849465588084625049495793857634556517064563488433148224524638105971161051763127718438062862548184814747601299494052813662851459740127499557785398714481909461631996020048315790167967699932967974484481209879664173009585231469785141628982021847883945871201430155071257803163523612863113967495969578605521
Q2=151010734276916939790591461278981486442548035032350797306496105136358723586953123484087860176438629843688462671681777513652947555325607414858514566053513243083627810686084890261120641161987614435114887565491866120507844566210561620503961205851409386041194326728437073995372322433035153519757017396063066469743
Q=168992529793593315757895995101430241994953638330919314800130536809801824971112039572562389449584350643924391984800978193707795909956472992631004290479273525116959461856227262232600089176950810729475058260332177626961286009876630340945093629959302803189668904123890991069113826241497783666995751391361028949651
c=pow(Q1,Q2,Q)
md5_c= hashlib.md5()
md5_c.update(hex(c))
print md5_c.hexdigest()
```

## 0x0F rsarsa

脚本如下：

```python
from Crypto.Util.number import *
p=9648423029010515676590551740010426534945737639235739800643989352039852507298491399561035009163427050370107570733633350911691280297777160200625281665378483
q=11874843837980297032092405848653656852760910154543380907650040190704283358909208578251063047732443992230647903887510065547947313543299303261986053486569407
e = 65537
c=83208298995174604174773590298203639360540024871256126892889661345742403314929861939100492666605647316646576486526217457006376842280869728581726746401583705899941768214138742259689334840735633553053887641847651173776251820293087212885670180367406807406765923638973161375817392737747832762751690104423869019034
d=inverse(e,(p-1)*(q-1))
n=p*q
m=pow(c,d,n)
print (m)
```


## 0x10 you\_raise\_me_up

分析代码得到各个参数之间的关系，`c=m<sup>byte_to_long(flag)</sup>mod n`。求解flag需要用到离散对数，`byte_to_long(flag)=log<sub>(m mod n)</sub>(c mod n)`，导入sympy库，求离散对数的函数（如`7<sup>3</sup><em>mod</em>15=41`）：`discrete_log(41,15,7)`

```python
from sympy.ntheory import discrete_log
from Crypto.Util.number import *

n =2**512
m=391190709124527428959489662565274039318305952172936859403855079581402770986890308469084735451207885386318986881041563704825943945069343345307381099559075
c=6665851394203214245856789450723658632520816791621796775909766895233000234023642878786025644953797995373211308485605397024123180085924117610802485972584499
flag = discrete_log(n,c,m)
print long_to_bytes(flag)
```
