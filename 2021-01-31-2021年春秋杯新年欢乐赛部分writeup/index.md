# 2021年“春秋杯”新年欢乐赛部分WriteUp

<div class="has-toc have-toc">
</div>

## 0x00 签到题

万物皆有"FUN"，电脑扫"FUN"活动，提供大写的"FUN"字样，即可获取flag~

下载压缩包后，解压打开新年快乐.exe，发现获取摄像头权限在截图，根据提示。在纸上写下“FUN”，放到摄像头前，出现flag.txt，打开获取flag。`flag{ju5t_f0r_FUN}`

## 0x01 十二宫的挑衅

解压后发现图片。

<pre class="wp-block-code"><code>^#@$@#()/&gt;@?==%1(
!)&gt;(*+3&lt;#86@-7$^.
4&)8%#5&6!=%1#$-$
+5&?#!.03!%=@=101
0?(*~#??.+)%&.7^8
=1%^=$5$7@@8&gt;&*9
9@0185(+7)&lt;%3#@^4
&@@&lt;.)$3*#%%&lt;&lt;*++
.@.?=~**+!==65^@&</code></pre>

参考文章<a rel="noreferrer noopener" href="https://mp.weixin.qq.com/s/PG3tyhxEPuSjOo62g4iPDQ" target="_blank" rel="nofollow" >https://mp.weixin.qq.com/s/PG3tyhxEPuSjOo62g4iPDQ</a>发现**Z-340**的解密方法

首先将文本按上述步骤处理，得到如下结果。

<pre class="wp-block-code"><code>^&gt;%..@3*&
#(#0+@#+.
@*53)8@+@
$+&!%&gt;^&.
@36%&&4@?
#&lt;!=.*9@=
(#=@79@&lt;~
)8%=^=0.*
/611811)*
&gt;@#00%8$+
@-$1?*53!
?7-+(^(*=
=$$5*=+#=
=^4&~$7%6
%.&?#5)%5
1!)#?$&lt;&lt;^
()8!?7%&lt;@</code></pre>

文章里面提到了AZdecrypt解密工具，在<a rel="noreferrer noopener" href="https://drive.google.com/uc?id=1_lP82NAvj5-vzd8O33e5aggWViHd-THJ&export=download" target="_blank" rel="nofollow" >https://drive.google.com/uc?id=1_lP82NAvj5-vzd8O33e5aggWViHd-THJ&export=download</a>下载后使用。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="492" height="112" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-74.png" alt="" class="wp-image-372" /></figure>
</div>

成功得到`flag{WUUHUUTAKEOFF}`

## 0x02 puzzle

下载后一张松鼠图片和一个压缩包，解压后1125张低像素的松鼠图片碎片，题目也提到了拼图的好处，猜测是需要拼图的。初步观察发现图片藏有模糊的flag信息，肉眼识别难度较大。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="839" height="282" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-81.png" alt="" class="wp-image-441" /></figure>
</div>

目测flag{w9w45my5x8kk4e8gp9nqm6j2wad49}，但答案无法通过。

将个别图片放到<a rel="noreferrer noopener" href="https://zh.pixfix.com/" target="_blank" rel="nofollow" >https://zh.pixfix.com/</a>降噪处理，得到`flag{w9w45my6x8kk4e8gp9nqm6j2c154wad49}`

## 0x03 2019-nCoV

hint：1. 增加hint.txt下载 2.可用python统计次数最多的字符；

解压发现

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="127" height="86" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-52.png" alt="" class="wp-image-656" /></figure>
</div>


zip文件已加密，内部藏有信息。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="137" height="47" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-53.png" alt="" class="wp-image-658" /></figure>
</div>

使用 silenteye解码pass.wav，音频中的LSB（最低有效位）隐写，得到`priebeijoarkjpxmdkucxwdus`，尝试解密，错误。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-51.png" alt="" class="wp-image-655" width="502" height="344" /></figure>
</div>

打开hint.txt，内容如下：

```
NB2HI4B2F4XXO53XFZWWK4TSPFRGS3ZOMNXW2LTDNYXWE3DPM4XVGQKSKMWUG32WFUZC2Z3FNZXW22LDFVQW4YLMPFZWS4ZONB2G23AKNB2HI4DTHIXS653XO4XG4Y3CNEXG43DNFZXGS2BOM5XXML3POJTGM2LOMRSXELYKNB2HI4B2F4XXO53XFZWWK4TSPFRGS3ZOMNXW2LTDNYXWE3DPM4XWG33SN5XGC5TJOJ2XGLLJNZ2HE33EOVRXI2LPNYXGQ5DNNQFAUUDMMVQXGZJANZXXI2LDMUQFI2DFEBWGC4THMVZXIIDTORZHKY3UOVZGC3BAOBZG65DFNFXCAIAKORUGKIDQMFZXG53POJSCA2LTEB2GQZJAEBWWINJINF2CO4ZAM5SW4ZJAONSXC5LFNZRWKKJAMFXGIIDEN4QG433UEBWGK5BAORUGKIHCQCMFY3XCQCMSA2LOEBWWINJIFE======
```

解码base32得到

<pre class="wp-block-code"><code>http:&#47;&#47;www.merrybio.com.cn/blog/SARS-CoV-2-genomic-analysis.html
https://www.ncbi.nlm.nih.gov/orffinder/
http://www.merrybio.com.cn/blog/coronavirus-introduction.html

Please notice The largest structural protein
the password is the md5(it's gene sequence) and do not let the ‘\n’ in md5()</code></pre>

刺突蛋白（Spike Protein，S）是病毒最大的结构蛋白，猜测密码应该是它的序列的md5值，序列子范围为21536-25384，需要在第二个页面输入登录号`MN908947`搜寻，得到如下结果。

<pre class="wp-block-code"><code>MFLLTTKRTMFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDK
VFRSSVLHSTQDLFLPFFSNVTWFHAIHVSGTNGTKRFDNPVLPFNDGVY
FASTEKSNIIRGWIFGTTLDSKTQSLLIVNNATNVVIKVCEFQFCNDPFL
GVYYHKNNKSWMESEFRVYSSANNCTFEYVSQPFLMDLEGKQGNFKNLRE
FVFKNIDGYFKIYSKHTPINLVRDLPQGFSALEPLVDLPIGINITRFQTL
LALHRSYLTPGDSSSGWTAGAAAYYVGYLQPRTFLLKYNENGTITDAVDC
ALDPLSETKCTLKSFTVEKGIYQTSNFRVQPTESIVRFPNITNLCPFGEV
FNATRFASVYAWNRKRISNCVADYSVLYNSASFSTFKCYGVSPTKLNDLC
FTNVYADSFVIRGDEVRQIAPGQTGKIADYNYKLPDDFTGCVIAWNSNNL
DSKVGGNYNYLYRLFRKSNLKPFERDISTEIYQAGSTPCNGVEGFNCYFP
LQSYGFQPTNGVGYQPYRVVVLSFELLHAPATVCGPKKSTNLVKNKCVNF
NFNGLTGTGVLTESNKKFLPFQQFGRDIADTTDAVRDPQTLEILDITPCS
FGGVSVITPGTNTSNQVAVLYQDVNCTEVPVAIHADQLTPTWRVYSTGSN
VFQTRAGCLIGAEHVNNSYECDIPIGAGICASYQTQTNSPRRARSVASQS
IIAYTMSLGAENSVAYSNNSIAIPTNFTISVTTEILPVSMTKTSVDCTMY
ICGDSTECSNLLLQYGSFCTQLNRALTGIAVEQDKNTQEVFAQVKQIYKT
PPIKDFGGFNFSQILPDPSKPSKRSFIEDLLFNKVTLADAGFIKQYGDCL
GDIAARDLICAQKFNGLTVLPPLLTDEMIAQYTSALLAGTITSGWTFGAG
AALQIPFAMQMAYRFNGIGVTQNVLYENQKLIANQFNSAIGKIQDSLSST
ASALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEV
QIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVD
FCGKGYHLMSFPQSAPHGVVFLHVTYVPAQEKNFTTAPAICHDGKAHFPR
EGVFVSNGTHWFVTQRNFYEPQIITTDNTFVSGNCDVVIGIVNNTVYDPL
QPELDSFKEELDKYFKNHTSPDVDLGDISGINASVVNIQKEIDRLNEVAK
NLNESLIDLQELGKYEQYIKWPWYIWLGFIAGLIAIVMVTIMLCCMTSCC
SCLKGCCSCGSCCKFDEDDSEPVLKGVKLHYT</code></pre>

Md5加密得到`98eb1b1760bcc837934c8695a1cee923`，也解不开压缩包文件，怀疑可能是mp3加密，利用Mp3Stego解密。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="1074" height="253" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-63.png" alt="" class="wp-image-703" /></figure>
</div>

打开cov.mp3.txt，得到`2019-nCoV`。解压打开hint2，得到一串16进制代码

```
796f75206d7573742070617920617474656e74696f6e20746f204e2070726f7465696e202c486f7720646f20746861742067657420696e746f2074686520766972616c206361707369643f0a646f20796f75206b6e6f772073746567686964653f0a7468652070617373776f726420697320656e637279707420627920566967656ec3a87265204369706865720a74686520736372656374206b65792069732054686520746f702032302063686172616374657273207769746820746865206d6f7374206f6363757272656e6365732061726520636f756e7465642b434f4d424154
```

转ASCII码

```
you must pay attention to N protein ,How do that get into the viral capsid?&lt;br>do you know steghide?&lt;br>the password is encrypt by VigenÃ¨re Cipher&lt;br>the screct key is The top 20 characters with the most occurrences are counted+COMBAT
```

提示给到了N蛋白、steghide、维吉尼亚密码和词频统计Top20+`COMBAT`，先解密下图片。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="1080" height="66" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-64.png" alt="" class="wp-image-707" /></figure>
</div>

需要一个密码，应该和N蛋白的信息有关，N的序列范围为28274-29533，先统计解密了，但得不到结果，又在文章中看到病毒在进行装配时，N蛋白先和病毒RNA相互作用形成复合体形式，然后再结合M蛋白、E蛋白，最后被包装进入病毒衣壳内。这次加上M的序列范围为27202-27387，E的蛋白范围为26523-27191，得到：

<pre class="wp-block-code"><code>MSDNGPQNQRNAPRITFGGPSDSTGSNQNGERSGARSKQRRPQGLPNNTA
SWFTALTQHGKEDLKFPRGQGVPINTNSSPDDQIGYYRRATRRIRGGDGK
MKDLSPRWYFYYLGTGPEAGLPYGANKDGIIWVATEGALNTPKDHIGTRN
PANNAAIVLQLPQGTTLPKGFYAEGSRGGSQASSRSSSRSRNSSRNSTPG
SSRGTSPARMAGNGGDAALALLLLDRLNQLESKMSGKGQQQQGQTVTKKS
AAEASKKPRQKRTATKAYNVTQAFGRRGPEQTQGNFGDQELIRQGTDYKH
WPQIAQFAPSASAFFGMSRIGMEVTPSGTWLTYTGAIKLDDKDPNFKDQV
ILLNKHIDAYKTFPPTEPKKDKKKKADETQALPQRQKKQQTVTLLPAADL
DDFSKQLQQSMSSADSTQA

MFHLVDFQVTIAEILLIIMRTFKVSIWNLDYIINLIIKNLSKSLTENKYS
QLDEEQPMEID

MADSNGTITVEELKKLLEQWNLVIGFLFLTWICLLQFAYANRNRFLYIIK
LIFLWLLWPVTLACFVLAAVYRINWITGGIAIAMACLVGLMWLSYFIASF
RLFARTRSMWSFNPETNILLNVPLHGTILTRPLLESELVIGAVILRGHLR
IAGHHLGRCDIKDLPKEITVATSRTLSYYKLGASQRVAGDSGFAAYSRYR
IGNYKLNTDHSSSSDNIALLVQ</code></pre>

进行统计，得到Top20，注意到有一样频率的字，序列共有16种可能。<figure class="wp-block-image size-large">

<img loading="lazy" width="1348" height="612" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-68.png" alt="" class="wp-image-717" /> </figure> 

经过尝试，`LGASTRIQKNDPFEVYMWHC`为最终序列，加上`COMBAT`，构成密钥，对`priebeijoarkjpxmdkucxwdus`进行解密，得到`eliminatenovelcoronavirts`。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-70.png" alt="" class="wp-image-721" width="404" height="363" /></figure>
</div>

终于拿到了`flag{we_will_over_come_SARS-COV}`，累死了，跟套娃一样。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-71.png" alt="" class="wp-image-722" width="310" height="74" /></figure>
</div>
