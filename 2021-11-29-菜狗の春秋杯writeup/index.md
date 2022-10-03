# 菜狗の春秋杯WriteUp

## 0x00 Vigenere

二战的鹰酱截获了敌军发送的密报，但是关于如何破解却无从下手。经过密码学专家分析，这是“不可破译的密码”。但那已经是上个世纪的事了，现在，我相信你肯定有办法。

题目明示维基利亚加密，文本如下：

```
cvnwvk lqae bw wzgy czxrxlm gnaoiiaafy. am ara xaufwiu qf fwg mlfckmnv tru aajtwxr pmsd afw rfe zms ehvv bzmn lpiebq yeeuiia. zq hsl qrvq keskw fn jqswtvtp wjpwkmvvuq afw lzoz feuarzksx lwoic qf unxhvdiluof litcjutq. amj usun jxwvijoh vbvvkluofl mekdgdw iiemldalbse bwetagk, imnqrkx ieoazewkmeo, tunskc jmugramc, tzqbtgzvrxzk afw wf wf. fhw miru zms ohr kpw fhakh gzale ag xym kqcggh eiluoftp zvvgslkmrt Aztwkrvb kqcmkmkg lqczgscwyk scbpca uamhxxzbaan, lai zvxaretxzwf eeunvzbq fratxytgz tjtmeqfs csft, rvv fhw litwfp pjbdv qf fhw "zyrv'sz cmi" qrvsseexrk whqrsmmfv szd etmebwzafvi twebelbxzwf af alk emliojd wvkmdilr wbqdxs uhqgmlutahr.tlmeeu pickgye qhy, kicq ygnv wtss:53d613xv-6g5t-4lv6-n3cw-8ug867t6n648
```

这里使用以前编写的小工具进行差分分析，能够推测出密钥<figure class="wp-block-image size-full">

<img loading="lazy" width="1954" height="312" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-160.png" alt="" class="wp-image-4660" /> </figure> 

可以看到文本信息也是能理解的内容，但因为原来的程序没有考虑特殊字符，如-和空格，分析的内容存在一些小误差，但用密钥在线解密就能够得到flag了。

## 0x01 helloshark

张三深知misc的魅力所在，于是他向大佬给他出了一道题，是一张图片。你能帮张三找出图片中的秘密吗？<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-174.png" alt="" class="wp-image-4680" width="674" height="299" /> </figure> 

解压，得到hint，压缩包密码在图片中。<figure class="wp-block-image size-full">

<img loading="lazy" width="234" height="81" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-173.png" alt="" class="wp-image-4679" /> </figure> 

LSB隐写查看到密码`@91902AF23C#276C2FC7EAC615739CC7C0`<figure class="wp-block-image size-full">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-175.png" alt="" class="wp-image-4682" /> </figure> 

解压分析流量，追踪tcp流发现端倪。<figure class="wp-block-image size-full">

<img loading="lazy" width="2318" height="1678" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-176.png" alt="" class="wp-image-4683" /> </figure> 

手动拼凑得到`flag{a40a418-fced-4b2d-9d76-fdc9053d69a1}`

## 0x02 secret-chart

NO one know chart better than me!<figure class="wp-block-image size-full">

<img loading="lazy" width="2756" height="362" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-164.png" alt="" class="wp-image-4670" /> </figure> 

解压得到压缩包，爆破得到密码`9527`<figure class="wp-block-image size-full">

<img loading="lazy" width="1588" height="806" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-165.png" alt="" class="wp-image-4671" /> </figure> 

打开表格，发现只有1和空白的数据，是24X24格式的。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-166.png" alt="" class="wp-image-4672" width="515" height="987" /> </figure> 

把所有数据拼凑在一起，新建格式规则，填充。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-169.png" alt="" class="wp-image-4675" width="187" height="182" /></figure> 

用中国编码扫描得到`zfua{B3s1o9in1Nw0halUnofuNc0HM1}`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-170.png" alt="" class="wp-image-4676" /> </figure> 

凯撒加密枚举得到flag<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-171.png" alt="" class="wp-image-4677" width="589" height="479" /> </figure>
