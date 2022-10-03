# DASCTF Oct WriteUp



<div class="has-toc have-toc">
</div>

MISC大赛了属于是，麻了，出了个web就没咋做了，参考<a href="http://www.7yue.top/dasctf-oct-x-吉林工师-wp" target="_blank" rel="noreferrer noopener" rel="nofollow" >http://www.7yue.top/dasctf-oct-x-吉林工师-wp</a>学习复现下MISC吧。

## 0x00 魔法少女的迷音

可恶，魔法少女的信息被大魔王截断加密了，快救救她

打开压缩包，文件末尾写着

<pre class="wp-block-code"><code>nIhtnmTm+m0a+m0a0lA5LIA5LIA5LIA5LIA5LIA5LIA5LIA5LIA5L/CC
atom128</code></pre>

第一列atom128解密得到`passswowoowowddddddddddddddddddddddddddd`，播放音频，听着像是倒放，反向后发现在念数字。记录为：`151 55 97 51 49 53 54 48 98 153 153 51 150 50 48 99 57 97 52 57 50 102 97 153 54 48 49`

然后卡死在这里，方向错了，在想是不是啥截断解密，后来发现读的应该是`100 51 55 97 51 49 53 54 48 98 100 53 100 53 51 100 50 50 48 99 57 97 52 57 50 102 97 100 53 54 48 49`，10进制转ascii得到`d37a31560bd5d53d220c9a492fad5601`

## 0x01 WELCOME DASCTFxJlenu

<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-193.png" alt="" class="wp-image-4304" width="470" height="232" /> </figure> 

一直卡在这儿，后来发现这并不是从web页面入手的。。。。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-194.png" alt="" class="wp-image-4305" width="692" height="168" /> </figure> 

nc连接了随便填个数，怀疑是python2的input漏洞，参考<a rel="noreferrer noopener" href="https://blog.csdn.net/weixin_43921239/article/details/108569794" target="_blank" rel="nofollow" >https://blog.csdn.net/weixin_43921239/article/details/108569794</a>，输入`__import__('os').system('cat /flag.txt')`<figure class="wp-block-image size-full">

<img loading="lazy" width="963" height="255" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-195.png" alt="" class="wp-image-4306" /> </figure> 

## 0x02 迷路的魔法少女

魔法少女迷失在了代码空间 请寻找她现在在哪

<pre class="wp-block-code"><code>&lt;?php
highlight_file('index.php');

extract($_GET);
error_reporting(0);
function String2Array($data)
{
    if($data == '') return array();
    @eval("\$array = $data;");
    return $array;
}


if(is_array($attrid) && is_array($attrvalue))
{
        $attrstr .= 'array(';
        $attrids = count($attrid);
        for($i=0; $i&lt;$attrids; $i++)
        {
            $attrstr .= '"'.intval($attrid&#91;$i]).'"=&gt;'.'"'.$attrvalue&#91;$i].'"';
            if($i &lt; $attrids-1)
            {
                $attrstr .= ',';
            }
        }
        $attrstr .= ');';
}

String2Array($attrstr); </code></pre>

extract函数将$_GET传入的变量组合成一个数组后，再拆解开来，根据源代码可知，需要创建attrid和attrvalue两个参数。String2Array字符串转数组的函数，容易造成命令执行漏洞。

构造payload：`attrid[]=1&attrvalue[]=2");phpinfo();//`，在phpinfo里面搜索flag找到对应字段，得到`flag{7c36c113-c4a3-4855-bd5b-adb7f0ed85f4}`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-138.png" alt="" class="wp-image-4214" width="722" height="208" /> </figure> 

## 0x03 不可以色色

some body touch my flag！

题目貌似在提示body标签，查看发现存在video.?的提示信息。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-182.png" alt="" class="wp-image-4282" width="315" height="86" /> </figure> 

应该存在一个video.?文件，尝试下文件后缀，得到压缩包。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-183.png" alt="" class="wp-image-4283" width="436" height="270" /> </figure> 

打不开文件，查看发现文件头有问题啊<figure class="wp-block-image size-full">

<img loading="lazy" width="1214" height="195" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-184.png" alt="" class="wp-image-4285" /> </figure> 

修改为正常的<figure class="wp-block-image size-full">

<img loading="lazy" width="1192" height="101" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-186.png" alt="" class="wp-image-4287" /> </figure> 

然后看到一段离谱的动画，里面有几帧闪现了奇怪的码，使用命令`ffmpeg -i C:\Users\38952\Desktop\video<code>\video`\video.mp4 example.%d.jpg</code><figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-187.png" alt="" class="wp-image-4289" width="553" height="407" /> </figure> 

得到了一些码图，看dalao的WP才知道是PDF417二维条码。<figure class="wp-block-image size-full">

<img loading="lazy" width="2598" height="264" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-188.png" alt="" class="wp-image-4291" /> </figure> 

拼接如下<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/Snipaste_2021-10-26_14-30-48.png" alt="" class="wp-image-4293" width="469" height="261" /> </figure> 

在<a href="https://products.aspose.app/barcode/zh-hans/recognize/pdf417#/recognized" target="_blank"  rel="nofollow" >https://products.aspose.app/barcode/zh-hans/recognize/pdf417#/recognized</a>扫描得到flag，`DASCTF{8e2d479e26b3093651293f9fa26e3404}`。

## 0x04 魔法秘文

”来尝试获取我的秘密吧“ 魔法少女说到

压缩包解开得到一张图。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-197.png" alt="" class="wp-image-4310" width="399" height="191" /> </figure> 

binwalk发现一个压缩包，分离出来。<figure class="wp-block-image size-full">

<img loading="lazy" width="1310" height="148" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-198.png" alt="" class="wp-image-4311" /> </figure> 

文件尾有存在可疑的url编码字符串。<figure class="wp-block-image size-full">

<img loading="lazy" width="1200" height="296" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-196.png" alt="" class="wp-image-4309" /> </figure> 

转换得到200个汉字，是按笔画排的，结合hint，密码由32个中文组成，这串汉字铁定有问题。

```
二十丁厂七卜人入八九几儿了力乃刀又三于干亏士工土才寸下大丈与万上小口巾山千乞川亿个勺久凡及夕丸么广亡门义之尸弓己已子卫也女飞刃习叉马乡丰王井开夫天无元专云扎艺木五支厅不太犬区历尤友匹车巨牙屯比互切瓦止少日中冈贝内水见午牛手毛气升长仁什片仆化仇币仍仅斤爪反介父从今凶分乏公仓月氏勿欠风丹匀乌凤勾文六方火为斗忆订计户认心尺引丑巴孔队办以允予劝双书幻玉刊示末未击打巧正扑扒功扔去甘世古节本术可丙左厉右石布龙
```

压缩包内容<figure class="wp-block-image size-full">

<img loading="lazy" width="219" height="78" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-199.png" alt="" class="wp-image-4312" /> </figure> 

修改后缀为ttf，安装字体，然后在word里面输入上述汉字。会发现有的字歪了。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-200.png" alt="" class="wp-image-4313" width="503" height="240" /> </figure> 

挑出来是`丁厂八九几刀于干工上小个门之马王云木尤切少牛分六方丑玉古节可石布`，解压后得到flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="1592" height="98" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-201.png" alt="" class="wp-image-4316" /> </figure> 

## 0x05 闯入魔塔的魔法少女

魔法少女只身进入魔塔只为打败大魔王并获得flag

用FFDec打开分析，直接在P-Code中搜索flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="1551" height="59" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-203.png" alt="" class="wp-image-4322" /> </figure> 

## 0x06 giveyourflag

过来白嫖

把文件放入010里面查看，发现是压缩包套娃。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/10/图片-192.png" alt="" class="wp-image-4302" width="578" height="292" /> </figure> 

这里用脚本处理一下

<pre class="wp-block-code"><code>from os import system
import zipfile

zipname = "flag1"
f = zipfile.ZipFile(zipname, 'r')


while 1:
	try:
		name = f.namelist()&#91;0]
		print (name)
		f.extractall()
		system('rm -rf '+ str(zipname))
		f = zipfile.ZipFile(name, 'r')
		zipname = name
	except:
		break</code></pre>

最后得到flag文件，内容为：`R0RWRldJezdnZ3FnbGwzanl1a2RuY3N0aTlpY3BjM2ZlYjB2NW9wfQ==`，解base64得到`GDVFWI{7ggqgll3jyukdncsti9icpc3feb0v5op}`，凯撒密码解密得到`DASCTF{7ddndii3gvrhakzpqf9fzmz3cby0s5lm}`

## 0x07 英语不好的魔法少女

这个魔法少女的英语就是逊啦

把图片丢到010中，发现tpWj数据块有stego_text.txt<figure class="wp-block-image size-full">

<img loading="lazy" width="1338" height="726" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-35.png" alt="" class="wp-image-4377" /> </figure> 

在<a rel="noreferrer noopener" href="https://masterqian.github.io/picdir/" target="_blank" rel="nofollow" >https://masterqian.github.io/picdir/</a>进行提取图片文件夹中的文件，得到一堆单词<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-36.png" alt="" class="wp-image-4379" width="91" height="277" /> </figure> 

在<a rel="noreferrer noopener" href="http://330k.github.io/misc_tools/unicode_steganography.html" target="_blank" rel="nofollow" >http://330k.github.io/misc_tools/unicode_steganography.html</a>零宽字节解密得到`yjPW8RIz0og8HX3o6BcwTmveeyyEDiCurJNTwPJeY/PMyOhHXYVKPLln6isBRyL0`<figure class="wp-block-image size-full">

<img loading="lazy" width="3283" height="1362" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-37.png" alt="" class="wp-image-4380" /> </figure> 

用word对单词进行检查，发现存在拼写错误<figure class="wp-block-image size-full">

<img loading="lazy" width="2157" height="641" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-38.png" alt="" class="wp-image-4381" /> </figure> 

可以手动检查，也可以用脚本跑，最后得到的结果如下：

<pre class="wp-block-code"><code>accuratm
extfnt
biks
equivalens
openev
sendinx
foumula
fecused
journsy
threht
oparational
handbnok
sguthwest</code></pre>

错误的字母为：`mfsvxueshang`

然后将零宽字节解密得到的数据作为密文，单词错误字母作为key，求解AES，得到最终的flag。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-39.png" alt="" class="wp-image-4382" width="516" height="354" /> </figure> 

## 0x08 虚幻3

wdb！我真的好好喜欢你啊，为了你，我要出虚幻3！

这题据说跟网鼎杯里的虚幻系列类似，需要对提取最低位像素，转化黑白，然后grb顺序组合在一起，为一个汉信码。

这里直接贴下大佬的脚本

<pre class="wp-block-code"><code>from PIL import Image
pic = Image.open('cipher.bmp')
a, b = pic.size
r1 = &#91;]  # 储存r、g、b通道
g1 = &#91;]
b1 = &#91;]
r2 = &#91;]  # 一行一行临时储存
g2 = &#91;]
b2 = &#91;]
for y in range(b):
    for x in range(a):
        r2.append(pic.getpixel((x, y))&#91;0] % 2)
        g2.append(pic.getpixel((x, y))&#91;1] % 2)
        b2.append(pic.getpixel((x, y))&#91;2] % 2)
    r1.append(r2)
    g1.append(g2)
    b1.append(b2)
    r2 = &#91;]
    g2 = &#91;]
    b2 = &#91;]
pic_1 = Image.new('L', (a, b*3), 255)
for y in range(0, len(r1)*3, 3):
    for x in range(len(r1&#91;0])):
        pic_1.putpixel((x, y), g1&#91;y//3]&#91;x] * 255)
        pic_1.putpixel((x, y+1), r1&#91;y//3]&#91;x] * 255)
        pic_1.putpixel((x, y+2), b1&#91;y//3]&#91;x] * 255)
pic_1.show()
pic_1.save('flag.bmp')</code></pre>

最后得到<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-33.png" alt="" class="wp-image-4374" width="285" height="285" /> </figure> 

这里补上汉信码的定位符即可扫描出flag。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-34.png" alt="" class="wp-image-4375" width="309" height="311" /> </figure> 

## 0x09 阴游大师

人人都知道Fz是音游椰椰

用Malody打开，发现最右侧有多出来的数据。<figure class="wp-block-image size-full">

<img loading="lazy" width="1103" height="615" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-43.png" alt="" class="wp-image-4390" /> </figure> 

用010查看是zip格式的，重命名下，再解压，得到三个文件。<figure class="wp-block-image size-full">

<img loading="lazy" width="296" height="136" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-40.png" alt="" class="wp-image-4384" /> </figure> 

mc的内容如下：<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-42.png" alt="" class="wp-image-4387" width="127" height="486" /> </figure> 

猜测column为9时，存在异常数据，写脚本解出所有的column

<pre class="wp-block-code"><code>import json
fp = open('1634029079.mc', 'r')
data = fp.read()
json1 = json.loads(data)
note = json1&#91;'note']
for i in note:
    print(i&#91;'column'], end='')</code></pre>

发现所有异常数据都在0000-00000000这个区间内<figure class="wp-block-image size-full">

<img loading="lazy" width="2795" height="52" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-44.png" alt="" class="wp-image-4392" /> </figure> 

提取出数据，转十进制<figure class="wp-block-image size-full">

<img loading="lazy" width="2023" height="350" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-45.png" alt="" class="wp-image-4393" /> </figure> 

发现011不对，应该是101

## 0x0A 魔法信息

大魔王截获了魔法少女的信息，oh no

追踪tcp流，发现一个zip数据包。<figure class="wp-block-image size-full">

<img loading="lazy" width="2642" height="497" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-31.png" alt="" class="wp-image-4370" /> </figure> 

然后导出数据包，发现压缩包存在问题，但用7z能够把pdf文件提取出来，同时，pdf文件也存在数据问题。用010edittor打开pdf模板进行分析，发现flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="1584" height="887" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-32.png" alt="" class="wp-image-4371" /> </figure> 

## 0x0B 彁彁

请在做题前阅读： 当暴露在特定光影图案或闪光光亮下时，有极小部分人群会引发癲痫。这种情形可能是由于某些未查出的癫病症状引起，即使该人员并没有患癫痫病史也有可能造成此类病症。如果您的家人或任何家庭成员曾有过类似症状，请在进行游戏前咨询您的医生或医师。

视频很花，看到20几秒时，好像有二维码闪过，用ffmpeg分离出所有的帧。<figure class="wp-block-image size-full">

<img loading="lazy" width="761" height="428" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-93.png" alt="" class="wp-image-4473" /></figure> 

简单拼接得到<figure class="wp-block-image size-full">

<img loading="lazy" width="373" height="369" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-96.png" alt="" class="wp-image-4476" /> </figure> 

导入，识别<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-97.png" alt="" class="wp-image-4477" /></figure> 

可以得到关键词snowywar、git等等，搜索得到<a rel="noreferrer noopener" target="_blank" href="https://gitee.com/snowywar/gege" rel="nofollow" >https://gitee.com/snowywar/gege</a>

将4444.png拉下来分析，发现一个网址<figure class="wp-block-image size-full">

<img loading="lazy" width="1724" height="282" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-98.png" alt="" class="wp-image-4479" /> </figure> 

日语死的维基百科<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-99.png" alt="" class="wp-image-4480" width="840" height="439" /> </figure> 

twitter.jpg里面藏有文件，导出压缩包，发现存在密码，用`死`解密<figure class="wp-block-image size-full">

<img loading="lazy" width="2260" height="284" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-100.png" alt="" class="wp-image-4481" /> </figure> 

最终得到`=6270yFdE0<?@H0=@G60562C=J0v60v6`,ROT47得到flag<figure class="wp-block-image size-full">

<img loading="lazy" width="1659" height="274" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-101.png" alt="" class="wp-image-4482" /> </figure> 

## 0x0C 卡比卡比卡比

卡比！

解压得到两个文件。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-102.png" alt="" class="wp-image-4484" width="252" height="158" /> </figure> 

`volatility -f 1.raw imageinfo #查看系统版本`<figure class="wp-block-image size-full">

<img loading="lazy" width="2266" height="553" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-103.png" alt="" class="wp-image-4485" /> </figure> 

`volatility -f 1.raw --profile=Win7SP1x64 pslist # 列出进程`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/Snipaste_2021-11-18_19-49-03.png" alt="" class="wp-image-4486" width="586" height="527" /> </figure> 

使用`pstree`，可以识别出被隐藏的进程，发现最后存在cmd进程和ie进程。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/Snipaste_2021-11-18_19-49-03-1.png" alt="" class="wp-image-4487" width="578" height="538" /> </figure> 

使用`iehistory`，看看历史记录，发现搜索记录和key.png文件<figure class="wp-block-image size-full">

<img loading="lazy" width="3453" height="1269" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/Snipaste_2021-11-18_19-49-03-2.png" alt="" class="wp-image-4489" /> </figure> 

搜索的内容如下：<figure class="wp-block-image size-full">

<img loading="lazy" width="1674" height="330" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-105.png" alt="" class="wp-image-4491" /></figure> 

先使用`filescan`找到key.png文件，`volatility -f 1.raw --profile=Win7SP1x64 filescan | grep key.png`<figure class="wp-block-image size-full">

<img loading="lazy" width="1879" height="107" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-106.png" alt="" class="wp-image-4492" /> </figure> 

再通过`dumpfiles`提取，`volatility -f 1.raw --profile=Win7SP1x64 dumpfiles -Q 0x000000003e5e94c0 -D ./`<figure class="wp-block-image size-full">

<img loading="lazy" width="1864" height="102" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-107.png" alt="" class="wp-image-4493" /> </figure> 

key.png实际上是text文本，内容是`我记得我存了一个非常棒的视频，但怎么找不到了，会不会在默认文件夹下。`

视频的默认文件夹是Video，尝试搜索一下Video，发现可疑的文件，dump出来的内容为`xzkbyyds!`。<figure class="wp-block-image size-full">

<img loading="lazy" width="2602" height="424" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-108.png" alt="" class="wp-image-4495" /> </figure> 

查看cmd命令使用情况，`volatility -f 1.raw  --profile=Win7SP1x64 cmdscan`，发现异常输入<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-109.png" alt="" class="wp-image-4499" width="551" height="277" /> </figure> 

5201314可能是之前搜索的前缀，这里再次filescan一下，找到异常文件，dump出来。<figure class="wp-block-image size-full">

<img loading="lazy" width="1873" height="216" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-111.png" alt="" class="wp-image-4501" width="464" height="350" /></figure> 

下一步需要使用`mimikatz`获取windows的账号及明文密码，这里一直没有安装好，用PTF也可以找到密码`MahouShoujoYyds`。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-112.png" alt="" class="wp-image-4502" width="531" height="241" /> </figure> 

解压后的文件如下

<pre class="wp-block-code"><code>import struct
key = 'xxxxxxxxx'
fp = open('!@#$importance', 'rb')
fs = open('!@#$unimportance', 'wb')
data = fp.read()
for i in range(0, len(data)):
    result = struct.pack('B', data&#91;i] ^ ord(*key&#91;i % len(key)]))
    fs.write(result)
fp.close()
fs.close()</code></pre>

回想起最初的文件之一名字是!@#$unimportance，用之前的key来逆一下

<pre class="wp-block-code"><code>import struct
key = 'xzkbyyds!'
fp = open('!@#$importance', 'wb')
fs = open('!@#$unimportance', 'rb')
data = fs.read()
for i in range(0, len(data)):
    result = struct.pack('B', data&#91;i] ^ ord(*key&#91;i % len(key)]))
    fp.write(result)
fp.close()
fs.close()</code></pre>

拖到kali里面发现是图片<figure class="wp-block-image size-full">

<img loading="lazy" width="319" height="233" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-113.png" alt="" class="wp-image-4504" /> </figure> 

进一步确认是gif<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-114.png" alt="" class="wp-image-4505" width="656" height="50" /> </figure> 

这里注意一个细节，kali中显示的是119x103，实际的像素是119x119，我们用010editor打开，发现高度不对，6、7字节为宽， 8、9字节为高，且为小端序储存方式，修改6为7。<figure class="wp-block-image size-full">

<img loading="lazy" width="1216" height="100" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-115.png" alt="" class="wp-image-4506" /> </figure> 

用NamoGif打开，发现flag。<figure class="wp-block-image size-full">

<img loading="lazy" width="2346" height="495" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-116.png" alt="" class="wp-image-4509" /> </figure> 

## 0x0D Twinkle Twinkle Starry Night

Twinkle twinkle little star, get your flag somewhere far.

nc连接后得到一大串base64

```
ICAgICArICAgICArICAgICAgICArICAqICAgICAgKyogICAgICAgICsgICogICAgICsqICAgICAgICArICAqICAgICAgICsqICAgICAgICArICAqICAgICAgKyoKICAgICAgICArICAqICAgICAgKyogICAgICsgICAgICAgICsgICogICAgICArKiAgICAgICAgKyAgKiAgICAgKyogICAgICAgICsgICogICAgICArKiAgICAgICAKICsgICogICAgICAgKyogICAgICAgICsgICogICAgICArKiAgICAgKyAgICAgICAgKyAgKiAgICAgICsqICAgICAgICArICAqICAgICAgKyogICAgICAgICsgICoKICAgICArKiAgICAgICAgKyAgKiAgICAgKyogICAgICAgICsgICogICAgICsqICAgICArICAgICAgICArICAqICAgICAgKyogICAgICAgICsgICogICAgICsqICAKICAgICAgKyAgKiAgICAgICArKiAgICAgICAgKyAgKiAgICAgICsqICAgICAgICArICAqICAgICArKiAgICAgLiAgICAgLiAgICAgLiArICAgLiAgICAgKyAgICAKICAgICsgICogICAgICArKiAgICAgICAgKyAgKiAgICAgICsqICAgICAgICArICAqICAgICAgKyogICAgICAgICsgICogICAgICAgKyogICAgICAgICsgICogICAKICArKiArIC4gICAgICsgICAgICAgICsgICogICAgICArKiAgICAgICAgKyAgKiAgICAgICArKiAgICAgICAgKyAgKiAgICAgICArKiAgICAgICAgKyAgKiAgICAKICAgKyogKyAgICAgLiAgICAgKyAgICAgICAgKyAgKiAgICAgICArKiAgICAgICAgKyAgKiAgICAgKyogICAgICAgICsgICogICAgICsqICAgICAgICArICAqICAKICAgICArKiAgICAgKyAgICAgICAgKyAgKiAgICAgICsqICAgICAgICArICAqICAgICArKiAgICAgICAgKyAgKiAgICAgICsqICAgICAgICArICAqICAgICAgICsKKiAgICAgICAgKyAgKiAgICAgICArKiAgICAgKyAgICAgICAgKyAgKiAgICAgICArKiAgICAgICAgKyAgKiAgICAgKyogICAgICAgICsgICogICAgICArKiAgICAKICAgICsgICogICAgICsqICAgICAuICAgICAuICsgICAgICAgLiAgICAgKyAgICAgICAgKyAgKiAgICAgICsqICAgICAgICArICAqICAgICAgICsqICAgICAgICAKKyAgKiAgICAgICArKiAgICAgICAgKyAgKiAgICAgKyogKyAgICAgLiAgICAgKyAgICAgICAgKyAgKiAgICAgICsqICAgICAgICArICAqICAgICAgICsqICAgICAKICAgKyAgKiAgICAgKyogICAgICAgICsgICogICAgICsqICAgICArICAgICAgICArICAqICAgICAgKyogICAgICAgICsgICogICAgICAgKyogICAgICAgICsgICoKICAgICAgICsqICAgICAgICArICAqICAgICArKiAgICAgKyAgICAgICAgKyAgKiAgICAgICsqICAgICAgICArICAqICAgICAgICsqICAgICAgICArICAqICAgICAKICsqICAgICAgICArICAqICAgICAgKyogICAgICsgICAgICAgICsgICogICAgICAgKyogICAgICAgICsgICogICAgICsqICAgICAgICArICAqICAgICArKiAgICAKICAgICsgICogICAgICsqIC4gLiAuICsgICAuICAgICArICAgICAgICArICAqICAgICAgKyogICAgICAgICsgICogICAgICsqICAgICAgICArICAqICAgICAgICsKKiAgICAgICAgKyAgKiAgICAgKyogICAgICAgICsgICogICAgICsqICAgICArICAgICAgICArICAqICAgICAgICsqICAgICAgICArICAqICAgICArKiAgICAgICAKICsgICogICAgICsqICAgICAgICArICAqICAgICArKiAuICsgICAgIC4gICAgICsgICAgICAgICsgICogICAgICArKiAgICAgICAgKyAgKiAgICAgKyogICAgICAKICArICAqICAgICAgICsqICAgICAgICArICAqICAgICArKiAgICAgICAgKyAgKiAgICAgICArKiArICAgICAuICAgICArICAgICAgICArICAqICAgICAgKyogICAKICAgICArICAqICAgICArKiAgICAgICAgKyAgKiAgICAgICsqICAgICAgICArICAqICAgICAgICsqICAgICAgICArICAqICAgICAgICsqICAgICArICAgICAgICAKKyAgKiAgICAgICsqICAgICAgICArICAqICAgICArKiAgICAgICAgKyAgKiAgICAgICsqICAgICAgICArICAqICAgICAgICsqICAgICAgICArICAqICAgICAgKyoKICAgICArICAgICAgICArICAqICAgICAgKyogICAgICAgICsgICogICAgICAgKyogICAgICAgICsgICogICAgICAgKyogICAgICAgICsgICogICAgICArKiAgICAKICsgICAgICAgICsgICogICAgICArKiAgICAgICAgKyAgKiAgICAgICArKiAgICAgICAgKyAgKiAgICAgKyogICAgICAgICsgICogICAgICsqICAgICArICAgICAKICAgKyAgKiAgICAgICsqICAgICAgICArICAqICAgICAgICsqICAgICAgICArICAqICAgICAgKyogICAgICAgICsgICogICAgICArKiAgICAgICAuICAgICAgIC4KICAgICAgIC4gICAgICAgLiArIC4gICAgICsgICAgICAgICsgICogICAgICArKiAgICAgICAgKyAgKiAgICAgICArKiAgICAgICAgKyAgKiAgICAgKyogICAgICAKICArICAqICAgICArKiAgICAgKyAgICAgICAgKyAgKiAgICAgICsqICAgICAgICArICAqICAgICArKiAgICAgICAgKyAgKiAgICAgICArKiAgICAgICAgKyAgKiAKICAgICsqICAgICAgICArICAqICAgICAgICsqIC4gKyAgIC4gICAgICsgICAgICAgICsgICogICAgICArKiAgICAgICAgKyAgKiAgICAgKyogICAgICAgICsgICoKICAgICAgKyogICAgICAgICsgICogICAgICAgKyogICAgICAgICsgICogICAgICAgKyogKyAgICAgLiAgICAgKyAgICAgICAgKyAgKiAgICAgICsqICAgICAgICAKKyAgKiAgICAgKyogICAgICAgICsgICogICAgICAgKyogICAgICAgICsgICogICAgICsqICAgICAgICArICAqICAgICAgKyogICAgICsgICAgICAgICsgICogICAKICAgKyogICAgICAgICsgICogICAgICAgKyogICAgICAgICsgICogICAgICArKiAgICAgICAgKyAgKiAgICAgKyogICAuICsgICAuICAgICArKiArIC4gICAgICsKICAgICAgICArICAqICAgICAgICsqICAgICAgICArICAqICAgICArKiAgICAgICAgKyAgKiAgICAgKyogICAgICAgICsgICogICAgICArKiAqICsgICAgICAgLiAKICAgICsgICAgICAgICsgICogICAgICAgKyogICAgICAgICsgICogICAgICsqICAgICAgICArICAqICAgICAgKyogICAgICAgICsgICogICAgICsqKiArIC4gICAKICArICAgICAgICArICAqICAgICAgKyogICAgICAgICsgICogICAgICsqICAgICAgICArICAqICAgICAgICsqICAgICAgICArICAqICAgICArKiAgICAgICAgKyAKICogICAgICAgKyogICAgICsgICAgICAgICsgICogICAgICAgKyogICAgICAgICsgICogICAgICsqICAgICAgICArICAqICAgICArKiAgICAgICAgKyAgKiAgICAKICAgKyogICAgICsgICAgICAgICsgICogICAgICArKiAgICAgICAgKyAgKiAgICAgKyogICAgICAgICsgICogICAgICArKiAgICAgICAgKyAgKiAgICAgICArKiAKICAgICAgICsgICogICAgICArKiAuIC4gKyAgIC4gICAgICsgICAgICAgICsgICogICAgICArKiAgICAgICAgKyAgKiAgICAgKyogICAgICAgICsgICogICAgICAKKyogICAgICAgICsgICogICAgICAgKyogICAgICAgICsgICogICAgICAgKyogKyAgICAgICAuICAgICArICAgICAgICArICAqICAgICAgKyogICAgICAgICsgICoKICAgICAgICsqICAgICAgICArICAqICAgICArKiAgICAgICAgKyAgKiAgICAgICArKiAqICsgICAgICAgLiAgICAgKyAgICAgICAgKyAgKiAgICAgICsqICAgICAKICAgKyAgKiAgICAgKyogICAgICAgICsgICogICAgICArKiAgICAgICAgKyAgKiAgICAgICArKiAgICAgICAgKyAgKiAgICAgICsqICsgICAgICAgLiAgICAgKyAKICAgICAgICsgICogICAgICArKiAgICAgICAgKyAgKiAgICAgICArKiAgICAgICAgKyAgKiAgICAgICsqICAgICAgICArICAqICAgICArKiAqICsgLiAgICAgKyAKICAgICAgICsgICogICAgICArKiAgICAgICAgKyAgKiAgICAgKyogICAgICAgICsgICogICAgICAgKyogICAgICAgICsgICogICAgICsqICAgICAgICArICAqICAKICAgKyogKyAgIC4gICAgICsgICAgICAgICsgICogICAgICAgKyogICAgICAgICsgICogICAgICsqICAgICAgICArICAqICAgICArKiAgICAgICAgKyAgKiAgICAKICAgKyogKyAgICAgICAuICAgICArICAgICAgICArICAqICAgICAgKyogICAgICAgICsgICogICAgICAgKyogICAgICAgICsgICogICAgICAgKyogICAgICAgICsKICAqICAgICAgICsqICsgICAgIC4gICAgICsgICAgICAgICsgICogICAgICAgKyogICAgICAgICsgICogICAgICsqICAgICAgICArICAqICAgICArKiAgICAgICAKICsgICogICAgICsqICsgLiAgICAgKyAgICAgICAgKyAgKiAgICAgICsqICAgICAgICArICAqICAgICAgKyogICAgICAgICsgICogICAgICArKiAgICAgICAgKyAKICogICAgICAgKyogICAgICAgICsgICogICAgICAgKyogKyAgIC4gICAgICsgICAgICAgICsgICogICAgICArKiAgICAgICAgKyAgKiAgICAgKyogICAgICAgICsKICAqICAgICAgKyogKyAgICAgLg==
```

解码后发现为奇怪的字符串

<pre class="wp-block-code"><code>     +     +        +  *      +*        +  *     +*        +  *       +*        +  *      
+*        +  *     +** +       .     +        +  *       +*        +  *     +** + .     + 
       +  *      +*        +  *     +*        +  *      +*        +  *       +*        +  
*      +* +       .     +        +  *      +*        +  *     +*        +  *       +*     
   +  *      +*        +  *      +* +   .     +        +  *      +*        +  *     +*    
    +  *      +*        +  *       +*        +  *       +*     +        +  *       +*     
   +  *     +*        +  *      +*        +  *     +*     +        +  *      +*        +  
*       +*        +  *       +*        +  *       +*     +        +  *      +*        +  *
      +*        +  *      +*        +  *       +*        +  *     +*   .   .   . +     .  
   +        +  *       +*        +  *     +*        +  *     +*        +  *       +* +   .
     +        +  *      +*        +  *       +* * + .     +        +  *       +*        + 
 *     +*        +  *     +*        +  *     +* +   .     +        +  *      +*        +  
*       +*        +  *       +*        +  *     +*     +        +  *      +*        +  *  
     +*        +  *      +*        +  *      +*     . +   .     +        +  *       +*    
    +  *     +* * +     .     +        +  *       +*        +  *     +*        +  *     +*
        +  *     +* + .     +        +  *      +*        +  *       +*        +  *     +* 
       +  *     +** +   .     +        +  *       +** + .     +        +  *      +*       
 +  *       +*        +  *       +*        +  *      +* * + .     +        +  *      +*   
     +  *       +*        +  *     +*        +  *     +* + .     +        +  *      +*    
    +  *     +*        +  *      +*        +  *       +*        +  *      +*     +        
+  *      +*        +  *       +*        +  *       +*        +  *      +*     . +     .  
   +        +  *      +** +       .     +        +  *      +*        +  *     +*        + 
 *      +*        +  *       +*        +  *       +*     +        +  *      +*        +  *
       +*        +  *     +*        +  *     +*     +        +  *      +*        +  *     
+*        +  *       +*        +  *     +*        +  *       +* . . +   .     +        +  
*      +*        +  *       +*        +  *     +*        +  *     +*     +        +  *    
  +*        +  *     +*        +  *       +*        +  *     +*        +  *      +*     + 
       +  *      +*        +  *     +*        +  *       +*        +  *     +*        +  *
      +*     +        +  *      +*        +  *       +*        +  *      +*        +  *   
  +*       .       .       . +     .     +        +  *       +*        +  *     +*        
+  *      +*        +  *     +** +     .     +        +  *      +*        +  *     +*     
   +  *      +*        +  *       +*        +  *      +* +   .     +        +  *      +*  
      +  *      +*        +  *      +*        +  *       +* * + .     +        +  *      +
*        +  *     +*        +  *      +*        +  *       +*        +  *       +*     +  
      +  *      +*        +  *     +*        +  *       +*        +  *     +*        +  * 
      +*       . +   .     +        +  *      +*        +  *       +*        +  *     +*  
      +  *       +* * + .     +        +  *      +*        +  *       +*        +  *     +
*        +  *      +** +   .     +        +  *      +*        +  *       +*        +  *   
   +*        +  *     +* * + .     +        +  *      +*        +  *     +*        +  *   
    +*        +  *     +*        +  *     +* + .     +        +  *      +*        +  *    
  +*        +  *       +*        +  *      +* * +     .     +        +  *      +*        +
  *      +*        +  *      +*        +  *       +*        +  *       +*     +        +  
*       +*        +  *     +*        +  *     +*        +  *     +*     +        +  *     
 +*        +  *       +*        +  *       +*        +  *       +*     .     . +     .    
 +        +  *      +*        +  *     +*        +  *      +* + .</code></pre>

看了大佬的wp才知道是Starry语言<a href="https://blog.csdn.net/rednaxelafx/article/details/83363956" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://blog.csdn.net/rednaxelafx/article/details/83363956</a>

Starry语言的源码语法是

<pre class="wp-block-code"><code>dup      : " +"
swap     : "  +"
rotate   : "   +"
pop      : "    +"
push     : 5个或以上个空格，后面接一个"+"；空格数量减去5就是push的参数值

+        : "*"
-        : " *"
*        : "  *"
/        : "   *"
%        : "    *"

num_out  : "."
char_out : " ."

num_in   : ","
char_in  : " ,"

label    : 任意多个空格之后接一个"`"；空格的个数是该标签的标识符
jump     : 任意多个空格之后接一个"'"；空格的个数是跳转目标标签的标识符</code></pre>

改了下大佬的脚本

<pre class="wp-block-code"><code>import sys
fp = open('s.txt')
data = fp.read()
fs = open('f.txt', 'w')
sub = 0
for i in data:
    if i == '\n':
        continue
    elif i == ' ':
        sub += 1
    elif i == '+':
        if sub == 1:
            fs.write('dup\n')
            sub = 0
        elif sub == 2:
            fs.write('swap\n')
            sub = 0
        elif sub == 3:
            fs.write('rotate\n')
            sub = 0
        elif sub == 4:
            fs.write('pop\n')
            sub = 0
        else:
            fs.write('push  ' + str(sub-5) + '\n')
            sub = 0
    elif i == '*':
        if sub == 0:
            fs.write('+\n')
            sub = 0
        elif sub == 1:
            fs.write('-\n')
            sub = 0
        elif sub == 2:
            fs.write('*\n')
            sub = 0
        elif sub == 3:
            fs.write('/\n')
            sub = 0
        elif sub == 4:
            fs.write('%\n')
            sub = 0
        else:
            print('error!!!')
            sub = 0
            sys.exit()
    elif i == '.':
        if sub == 0:
            fs.write('num_out\n')
            sub = 0
        else:
            fs.write('char_out\n')
            sub = 0
    else:
        print('error!!!!')
        sys.exit()
fp.close()
fs.close()</code></pre>

得到结果<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-119.png" alt="" class="wp-image-4524" width="218" height="675" /> </figure> 

然后是对栈操作指令的脚本

<pre class="wp-block-code"><code>import sys
fp = open('f.txt', 'r')
data = &#91;]
for line in fp:
    line = line.strip('\n')
    if line&#91;:4] == 'push':
        data.append(int(line.split('  ')&#91;1]))
    elif line == '*':
        x = data&#91;-1]
        y = data&#91;-2]
        data = data&#91;:-2]
        data.append(x * y)
    elif line == '+':
        x = data&#91;-1]
        y = data&#91;-2]
        data = data&#91;:-2]
        data.append(x + y)
    elif line == '-':
        x = data&#91;-1]
        y = data&#91;-2]
        data = data&#91;:-2]
        if (x-y)&lt;0:
            data.append(y-x)
        else:
            data.append(x-y)
    elif line == 'dup':
        x = data&#91;-1]
        data.append(x)
    elif line == 'char_out':
        x = data&#91;-1]
        data = data&#91;:-1]
        print(str(x) + ' ', end='')
    else:
        print('error!!!')
        sys.exit()</code></pre>

得到`102 108 97 103 123 53 57 98 56 51 54 49 51 45 54 99 101 49 45 52 97 98 101 45 98 48 100 100 45 102 97 56 101 98 51 97 49 99 56 53 54 125 10`，转ascii码即可得到`flag{59b83613-6ce1-4abe-b0dd-fa8eb3a1c856}`。
