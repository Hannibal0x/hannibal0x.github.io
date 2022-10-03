# 长安战疫(Misc+Crypto)赛题复现


## 0x00 前言

长安战疫的题目还挺友好的，但有的知识点当时没有联系到，赛后做个复现，总结学习一下。

## 0x01 no\_math\_no_cry

```
from Crypto.Util.number import*
from secret import flag

assert len(flag) <= 80
def sec_encry(m):
    cip = (m - (1<<500))**2 + 0x0338470
    return cip

if __name__ == "__main__":
    m = bytes_to_long(flag)
    c = sec_encry(m)
    print(c)

# 10715086071862673209484250490600018105614048117055336074437503883703510511248211671489145400471130049712947188505612184220711949974689275316345656079538583389095869818942817127245278601695124271626668045250476877726638182396614587807925457735428719972874944279172128411500209111406507112585996098530169
```

当时比赛时是直接推出`cip = gmpy2.iroot((c - 0x0338470),2)[0] + (1<<500)`，结果死活求不出flag，赛后才发现开平方后可能是负数，所以正确的脚本应该如下：

<pre class="wp-block-code"><code>def sec_decry(c):
    cip1 = (1&lt;&lt;500) - gmpy2.iroot((c - 0x0338470),2)&#91;0] 
    cip2 = (1&lt;&lt;500) + gmpy2.iroot((c - 0x0338470),2)&#91;0] 
    return cip1,cip2

if __name__ == "__main__":
    m1,m2 = sec_decry(c)
    flag1 = long_to_bytes(m1)
    flag2 = long_to_bytes(m2)
    print('flag1:',flag1,'\nflag2:',flag2)</code></pre><figure class="wp-block-image size-full">

<img loading="lazy" width="2276" height="170" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-69.png" alt="" class="wp-image-4916" /> </figure> 

## 0x02 无字天书

追踪http流，发现504b开头的数据，疑似zip包，把他导出来。<figure class="wp-block-image size-full">

<img loading="lazy" width="2656" height="1824" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-70.png" alt="" class="wp-image-4917" /> </figure> 

解压出来得到两个东西，都是空白的。<figure class="wp-block-image size-full">

<img loading="lazy" width="156" height="105" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-71.png" alt="" class="wp-image-4918" /> </figure> 

key.ws是whitespace编码，导入<a rel="noreferrer noopener" href="https://www.dcode.fr/whitespace-language" target="_blank" rel="nofollow" >https://www.dcode.fr/whitespace-language</a>，可以解出key值为`XiAnWillBeSafe`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-72.png" alt="" class="wp-image-4919" width="603" height="198" /> </figure> 

flag.txt是snow编码，利用工具`SNOW.exe -p "XiAnWillBeSafe" -C flag.txt`求解，特别注意密码要用双引号不能是单引号，最后得到`cazy{C4n_y0u_underSt4nd_th3_b0oK_With0ut_Str1ng}`<figure class="wp-block-image size-full">

<img loading="lazy" width="1160" height="75" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-94.png" alt="" class="wp-image-4954" /> </figure> 

## 0x03 Ez_Steg

压缩包提示Password is six number，爆破得出`220101`，然后得到emoji.txt和一个pyc文件，起初以为pyc文件是要反编译成py然后求出key，和emoji通过解密得到flag。后来看wp发现，pyc文件存在Pyc字节码隐写，找到魔改的<a href="https://github.com/AngelKitty/stegosaurus" target="_blank"  rel="nofollow" >https://github.com/c10udlnk/stegosaurus</a>后，执行`./stegosaurus -x steg.pyc`对pyc文件的隐藏文本进行提取，最后得到`St3g1sV3ryFuNny`。<figure class="wp-block-image size-full">

<img loading="lazy" width="1200" height="68" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-95.png" alt="" class="wp-image-4955" /> </figure> 

然后在<a rel="noreferrer noopener" href="https://aghorler.github.io/emoji-aes/" target="_blank" rel="nofollow" >https://aghorler.github.io/emoji-aes/</a>进行求解，得到`cazy{Em0j1s_AES_4nd_PyC_St3g_D0_yoU_l1ke}`

## 0x04 西安加油-gaps解法

因为图片都是规则的正方形，所以可以考虑使用imagick结合gaps，使用`magick montage *.png -tile 8x6 -geometry +0+0 flag.png`，得到一张初具轮廓的图。<figure class="wp-block-image size-full">

<img loading="lazy" width="639" height="479" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-96.png" alt="" class="wp-image-4956" /> </figure> 

看下单张的详细信息<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-98.png" alt="" class="wp-image-4959" width="157" height="111" /> </figure> 

执行`gaps --image=flag.png --generation=30 --population=300 --size=100`得出完整拼图。<figure class="wp-block-image size-full">

<img loading="lazy" width="1566" height="523" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-100.png" alt="" class="wp-image-4963" width="745" height="327" /></figure> 

## 0x05 math

```
pinvq:0x63367a2b947c21d5051144d2d40572e366e19e3539a3074a433a92161465543157854669134c03642a12d304d2d9036e6458fe4c850c772c19c4eb3f567902b3
qinvp:0x79388eb6c541fffefc9cfb083f3662655651502d81ccc00ecde17a75f316bc97a8d888286f21b1235bde1f35efe13f8b3edb739c8f28e6e6043cb29569aa0e7b
c:0x5a1e001edd22964dd501eac6071091027db7665e5355426e1fa0c6360accbc013c7a36da88797de1960a6e9f1cf9ad9b8fd837b76fea7e11eac30a898c7a8b6d8c8989db07c2d80b14487a167c0064442e1fb9fd657a519cac5651457d64223baa30d8b7689d22f5f3795659ba50fb808b1863b344d8a8753b60bb4188b5e386
e:0x10005
d:0xae285803302de933cfc181bd4b9ab2ae09d1991509cb165aa1650bef78a8b23548bb17175f10cddffcde1a1cf36417cc080a622a1f8c64deb6d16667851942375670c50c5a32796545784f0bbcfdf2c0629a3d4f8e1a8a683f2aa63971f8e126c2ef75e08f56d16e1ec492cf9d26e730eae4d1a3fecbbb5db81e74d5195f49f1
```


先整理一下已知量，e、d、c和 invert(p,q) 、invert(q,p)，设置invert(p,q) 、invert(q,p)分别为\_q和\_p。参考：<a rel="noreferrer noopener" href="https://scerush.github.io/2020/09/17/ctf-show-unusualrsa4/" target="_blank" rel="nofollow" >https://scerush.github.io/2020/09/17/ctf-show-unusualrsa4/</a>

<pre class="wp-block-code"><code>e*d=1+k*phi，由此可以暴力枚举k值来破解phi。

p*_q mod q ≡1,q*_p mod p ≡1

phi = (p - 1) * (q - 1) ≡ n - p - q+1

(_p * phi) mod p ≡ _p * (n - p - q + 1) mod p ≡ (_p - _p*q) mod p ≡ (_p - 1) mod p

(_p * phi + 1 - _p) ≡  0 mod p

设(_p * phi + 1 - _p)为X,p能被X整除</code></pre><figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-102.png" alt="" class="wp-image-4966" width="550" height="283" /> </figure> 

由 `_p * q ≡ 1 mod p` 可计算出 q ，最后得到m。

脚本如下：

<pre class="wp-block-code"><code>from gmpy2 import *
from Crypto.Util.number import *

_p = qinvp
poss_phi = &#91;]
for i in range(1,e):
	phi = e * d -1 
	if phi%i == 0:
		phi = phi//i
		dd = invert(e,phi)
		if dd == d:
			poss_phi.append(phi)

for phi in poss_phi:
	try:
		x = 1 + _p * phi - _p
		y1 = pow(5, phi, x) - 1
		y2 = pow(3, phi, x) - 1
		y3 = pow(2, phi, x) - 1
		p = gcd(gcd(y1, y2),y3)
		q = invert(_p, p)
		n = p * q
		m = pow(c, d, n)
		flag = long_to_bytes(m)
		if b'flag' in flag:
			print(flag)
	except:
		continue</code></pre><figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-103.png" alt="" class="wp-image-4968" width="493" height="39" /> </figure> 

## 0x06 ez_Encrypt

追踪流，在第10个流发现疑似base64的字符串，导出解码后得到一个压缩包。<figure class="wp-block-image size-full">

<img loading="lazy" width="2656" height="1826" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-104.png" alt="" class="wp-image-4970" /> </figure> 

发现是ThinkPHP6的源码<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-105.png" alt="" class="wp-image-4971" width="758" height="397" /> </figure> 

D盾扫描发现可疑文件。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-107.png" alt="" class="wp-image-4974" width="569" height="413" /> </figure> 

打开/app/contoller/Index.php发现存在php代码混淆。<figure class="wp-block-image size-full">

<img loading="lazy" width="3455" height="1874" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-106.png" alt="" class="wp-image-4972" /> </figure> 

将eval改成echo，在线运行，查看相应的结果。<figure class="wp-block-image size-full">

<img loading="lazy" width="2227" height="1710" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-108.png" alt="" class="wp-image-4977" /> </figure> 

得到结果后，将eval改成echo，再次运行。

```
$VCBZQW="goMTQheqiaUOubmYfRJSrkWNndEsPZGjAKpCVtBIHwDFxczXLlvyYTciUuPngpsyqboOlhjFIZNSwzmMHGvDxtkXVaWfdAJErRKLCBQeHJ9ApdxYGvVopN5BtXzZhBuupZfrcDf3jerjF2rizLYrcDf3tiMZGmjni09jHNjuR2s2SE9ZGNSQGvsTfojnhDGGpiB0NVhNO2hqsLzuVmZ0iEuXSvhOhDVCpBkKO210p1k6bvGpV2unOKSZzZ5Jzv1SPohrO1z4zEzqiDVGc1GUVv1As1SvUZ5sFEkTVZVMbVELGEjDbBfKV0uAzNmAzdzFhVkksNrpb1zOpEhpVKBvVDWZhvELsBGiGK09fgZ7jmk3bZu1VK0ZGmjni09jNKSzCghZUokHi0BbSB0qjvhXpZ9HFVMKc10qjvhXpZ9HFVMKcE07jdGhivzdFK0ZGmjni09jNKcKLF4ZGmjni09jNKmALF4ZGmjni09jNKf0LF4ZGmjni09jNKmALF4ZGmjni09jNKf0LiMZNNGMzwGsHFh2ssrwh0abcE0qjvhXpZ9HFVMryE0qjvhXpZ9HFVMKLF4ZzBEcG0zCNKWzCgh2ssrwh0abcV0qjvhXpZ9HFVMeSE07jv1EUVEvOK0ZGmjni09jNKzzCghZUokHi0BbciSzyehtz25fzVRqHFhZUokHi0BbcDjzCghZUokHi0BbcKGzCghZUokHi0BbcDBzCghZUokHi0BbcDGzCghZUokHi0BbcKWzCghZUokHi0BbcKjzCghZUokHi0BbcKVzCghZUokHi0BbcDGzCghZUokHi0BbcKWzy2V2ONATjmk3bZu1VeYgFZVpiVTrRdkNpDWkVEV0RBTeSLhshNrMsNrppBjONoBZhNhEGNaTOVGNGmjZV1TKV0zvSVjaPEVDFm55NZzAhvfepEjVcoris2rMSEUKhZ9VhVjJVv5MzVTAzEWghNuFOKjps1ZKNBzBbvhSVZVypVBNRJWpVNrNODWNh1VdbEhgVNUKVEuXPvVdsBBZVores21APNEEhZjBporMVBV4pvVVhBuyhJWkiKjNcBBLz29tPDYIFwZ0p1SqGdViFEGOF0SFcBVVPv5FcdSQFZGMbNjfNDjNU2zIsoa4bBzqiBzcU1j0sBVvsBjaiLESpNaKFZGMbNjfNDjNU2zIsoa4bBzqiBzcU1j0sBVvsBjaiLSthKEvsVGvh1B5p3SthoraOZupcBGJG2aFp3uqV25yV0rmULSthKEvsVGvh1B5p3WCs2M3fgZkyK8+HJ9ApdxYGvVopN5BtXzdGNStbs4rcDf3jerjF2rizLYrcDf3tiMZhBkQPmj0HNjuR2s2SE9ZGNSQGvsTfojnhDGGpiB0NVhNO2hqsLzuVmZ0iEuXSvhOhDVCpBkKO210p1k6bvGpV2unOKSZzZ5Jzv1SPohrGsVZVvmeSLzDbET2OKEFNvhaVZhVbmG0ON1TNNEObEEZcNrUsKWFzBEIbmaNV0GnsVs1pVjVpdSpFmGuso5FcVhdNo5ssi09fgZ7jv1qV2uiFJ0ZhBkQPmj0NKSzCghvNo94UwhbSB0qjmGpb3uXzEMKc10qjmGpb3uXzEMKcE07jEGGV2S4GJ0ZhBkQPmj0NKcKLF4ZhBkQPmj0NKmALF4ZhBkQPmj0NKf0LF4ZhBkQPmj0NKmALF4ZhBkQPmj0NKf0LiMZONGVzBzsHFhNNVzDPvhbcE0qjmGpb3uXzEMryE0qjmGpb3uXzEMKLF4ZVBBLO3uZNKWzCghNNVzDPvhbcV0qjmGpb3uXzEMeSE07jvBZz2rSsK0ZhBkQPmj0NKzzCghvNo94UwhbciSzyehabBzTs0YqHFhvNo94UwhbcDjzCghvNo94UwhbcKGzCghvNo94UwhbcDBzCghvNo94UwhbcDGzCghvNo94UwhbcKWzCghvNo94UwhbcKjzCghvNo94UwhbcKVzCghvNo94UwhbcDGzCghvNo94UwhbcKWzy2V2ONATjv1qV2uiFXYgFZzps1VqsDhGPDWkVNa4i2hIcihBbNunsZVpsvhEFBzFcsGus1uZzVkdcLBghBjNsiW0hoELGv1BVorrViSyPEENUZaZNmjks0zNpEzvGdjgc1f1s1zMRBZrio5GVsG4ODEFOVVEGvrFVLhJVmsrs2SdSVjNcBkKsZGMhEhINwkZcDm2V0GpcBSdRvBNNEO0s25tsvEdsDjhVvrJs25NV2jvVBSDVBjvO2aMU2cAyskgp3hfO1VtpvSLiDSNVmZriszvs09OREGFcsjdODWtp2jEcLBiVKVcsDSvU1BOhokpbZ55s1R1bm1nbdEsNEGjOVGNFEZeSNuZc3WKNortFoVqiwBiVZ5csZR1RVjVGEEyhLhfVshFiBfrUwEFNEGesijNs2SNiZGNcvrAVBV4cEjMVLBGc3WvO2a0R2VEFoahcdhaVoaypvhNUBkNVNh1GJW0FEjshBGVp2a3s2M4SNEIzmugbLWvsDEWcvjdNo9ghLhaVoayivhORdSicBkLsiW0bVGIiZrpbdWksBGMhETAVBWSVskyGEzTp1SfhiVZNEjhGmGNFs0rRdWGV1kyVEz4zvjnGv1LVBkmsKjpV1mAzv1Np05cNorphEcKVBEubsV5VsVpF1UKhDGibZkkOo14FESdGvuSbvS5s1uESNEEVBWiV2rvsDEZp1SfhiVZNEjhGmGNFs0rRdWGV1kyVEz4zvEmGv1LVBkmsKjpV1mAzv1Np05HNBzFhEceNBzhcdhaVoayivhVpdVsNEGhsorNNBGMbEESbmf2O3kjSVGEzduZh2rcsZVMOVUeSNrpcdh4NDjtFs1qhwEicEjtOVGNsEOAiBjSpBjqsKSZSojEzv1Np05cGEhXR1kMbEzhcdhaV2atiBUApJGipKBesiWNiVVdRdkSc1jkVBhjcEmeVBhZhET0VDj0U1GNhZkZbEGpsijtbVzNNZhicBkuiDjpNBGIiZrpbEkmsKjpV1mehBSVhmjyO2aTRVceNZ5Zc055NNkNSm1NRmrNc0s1V0VAsohvswjVhvunNVhESVsezmjNp0kesVGAi2E6FwuVNvu5OokNSvSaSJEBFmk1iBuTPNjnbmBVc3WKsKjpV1mAzJESh3uHNBzhysBnzvrZbsGKF0SDC1WkO3VthKE1VDjTVESJG2aNbvrONiSTp0aJsoupbEOeVDEhb0kdNBSVbBf0NLB3p2ELsDSghiEsF2kjRmrJsoupbEOeVDEhb0kdNBSVbBf0NLB3p2ELsDSghiEsimSFREkfGdSsVZ1AimSFpEkMVDjNcVEQFZzps1VqsDhGPLz3imSFREkfGdSsVZ1AF1SIRm93Hi0gtFZ7HK4=";eval('?>'.$arCiCL($VvUrBZ($DEomKk($VCBZQW,$LnpnvY*2),$DEomKk($VCBZQW,$LnpnvY,$LnpnvY),$DEomKk($VCBZQW,0,$LnpnvY))));
```

一直向下解码，最后发现`cazy{PHP_ji4m1_1s_s00000_3aSyyyyyyyyyyy}`。<figure class="wp-block-image size-full">

<img loading="lazy" width="2220" height="1742" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-109.png" alt="" class="wp-image-4979" /> </figure> 

## 0x07 LinearEquations

```python
from Crypto.Util.number import*
from secret import flag
assert flag[:5] == b'cazy{'
assert flag[-1:] == b'}'
flag = flag[5:-1]
assert(len(flag) == 24)

class my_LCG:
    def __init__(self, seed1 , seed2):
        self.state = [seed1,seed2]
        self.n = getPrime(64)
        while 1:
            self.a = bytes_to_long(flag[:8])
            self.b = bytes_to_long(flag[8:16])
            self.c = bytes_to_long(flag[16:])
            if self.a < self.n and self.b < self.n and self.c < self.n:
                break
    
    def next(self):
        new = (self.a * self.state[-1] + self.b * self.state[-2] + self.c) % self.n
        self.state.append( new )
        return new

def main():
    lcg = my_LCG(getRandomInteger(64),getRandomInteger(64))
    print("data = " + str([lcg.next() for _ in range(5)]))
    print("n = " + str(lcg.n))

if __name__ == "__main__":
    main() 

# data = [2626199569775466793, 8922951687182166500, 454458498974504742, 7289424376539417914, 8673638837300855396]
# n = 10104483468358610819
```

a、b、c是未知的，求解拼凑后能够得到flag。首先我们要弄清楚lcg.next()的算法过程。

```
data[0] = (a * seed2 + b * seed1 + c) mod n
data[1] = (a * data[0] + b * seed2 + c) mod n
data[2] = (a * data[1] + b * data[0] + c) mod n
data[3] = (a * data[2] + b * data[1] + c) mod n
data[4] = (a * data[3] + b * data[2] + c) mod n

设t[x] = (data[x + 1] - data[x] ) mod n
t[0] = (data[1] - data[0] ) mod n
t[1] = (data[2] - data[1] ) mod n
t[2] = (data[3] - data[2] ) mod n = [a * data[2] + b * data[1] + c - (a * data[1] + b * data[0] + c)] mod n = [ a * (data[2] - data[1]) + b * (data[1] - data[0])] mod n = (a * t[1] + b * t[0]) mod n
t[3] = (data[4] - data[3] ) mod n = (a * t[2] + b * t[1]) mod n

t[0]到t[3]都能够求解出来，可以根据他们的值联立方程组，求解a和b

先消去b，求解a
t[1] * t[2] = (a * t[1] * t[1] + b * t[0] * t[1]) mod n
t[0] * t[3] = (a * t[2] * t[0] + b * t[1] * t[0]) mod n
得到下式
(t[2] * t[1] - t[3] * t[0]) = [a * (t[1] * t[1] - t[2] * t[0])] mod n
而后求出b、c，解出flag
```

脚本如下

<pre class="wp-block-code"><code>t = &#91;]

for i in range(1,len(data)):
	tmp = data&#91;i] - data&#91;i - 1]	
	t.append(tmp)
    
a = (t&#91;2] * t&#91;1] - t&#91;3] * t&#91;0]) * gmpy2.invert(t&#91;1] ** 2 - t&#91;2] * t&#91;0],n) % n
b = (t&#91;2] - a * t&#91;1]) * gmpy2.invert(t&#91;0],n) % n
c = (data&#91;4] - a * data&#91;3] - b * data&#91;2]) % n

flag = b'cazy{' + long_to_bytes(a) + long_to_bytes(b) + long_to_bytes(c) + b'}'
print(flag)</code></pre>

得到flag<figure class="wp-block-image size-full">

<img loading="lazy" width="623" height="67" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-116.png" alt="" class="wp-image-4989" /> </figure> 

## 0x08 pipicc

用010打开bmp发现IHDR，但没有PNG头，修改文件。<figure class="wp-block-image size-full">

<img loading="lazy" width="1206" height="274" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-110.png" alt="" class="wp-image-4980" /> </figure> 

删去bmp头，另存为png<figure class="wp-block-image size-full">

<img loading="lazy" width="1185" height="153" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-111.png" alt="" class="wp-image-4981" /> </figure> 

得到图片<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-112.png" alt="" class="wp-image-4982" width="753" height="423" /> </figure> 

stegsolve提取蓝色低位数据，可以看到d9ff，ffd9是jpg文件尾的标识。<figure class="wp-block-image size-full">

<img loading="lazy" width="1440" height="1058" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-113.png" alt="" class="wp-image-4984" /> </figure> 

搜索`FF D8 FF`找到jpg的文件尾<figure class="wp-block-image size-full">

<img loading="lazy" width="1339" height="292" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-114.png" alt="" class="wp-image-4985" /> </figure> 

删去后续数据后，在<a rel="noreferrer noopener" href="https://www.sweetscape.com/010editor/repository/scripts/file_info.php?file=StringReverse.1sc&type=1&sort=" target="_blank" rel="nofollow" >https://www.sweetscape.com/010editor/repository/scripts/file_info.php?file=StringReverse.1sc&type=1&sort=</a>下载插件stringreverse.1sc逆转后保存为jpg文件。

得到flag<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-115.png" alt="" class="wp-image-4987" width="584" height="56" /> </figure>
