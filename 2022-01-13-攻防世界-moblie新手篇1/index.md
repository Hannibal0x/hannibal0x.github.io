# 攻防世界-moblie（新手篇1）

<div class="has-toc have-toc">
</div>

## 0x00 easyjni

JNI（Java Native Interface）即java本地接口，众所周知，android有四层结构，应用层与应用接口层是用Java写的，而C/C++核心库和linux内核层由C/C++写的，既然知道了这一点，那理解JNI就很简单了，Java和C/C++肯定是不能直接互相调用的，那么应用层肯定就不能直接调用底层的东西，比如从应用层直接用Java想调用底层C/C++开发的启动相机或NFC等肯定是不能直接实现的。

安装apk，是一个验证flag的程序。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-117.png" alt="" class="wp-image-4993" width="632" height="355" /> </figure> 

使用jeb查看反编译代码，在主函数找到check的判断语句。初始化一个a类locala，并把输入进去的String类型的字符串穿换成Byte[]类型组传入a类locala的a方法。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-118.png" alt="" class="wp-image-4995" width="697" height="112" /> </figure> 

程序开头加载了库，与传入的字符串进行ncheck，最后返回一个布尔型的值。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-121.png" alt="" class="wp-image-5000" width="500" height="512" /> </figure> 

猜测调用的a类是base64变码表，循环长度为3，数组长度为4，最后补“=”。<figure class="wp-block-image size-full">

<img loading="lazy" width="3012" height="1554" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-119.png" alt="" class="wp-image-4996" /> </figure> 

将so文件导入ida，搜索ncheck定位到关键函数<figure class="wp-block-image size-full">

<img loading="lazy" width="2282" height="1349" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-120.png" alt="" class="wp-image-4999" /> </figure> 

分析第一个循环，是将前16位与后16位交换位置。

<pre class="wp-block-code"><code>for ( i = 0; i != 16; ++i )
    {
      v7 = &v12&#91;i];
      v12&#91;i] = v5&#91;i + 16];
      v8 = v5&#91;i];
      v7&#91;16] = v8;
    }</code></pre>

分析第二个循环，是将字符两两交换位置。

<pre class="wp-block-code"><code>do
    {
      v10 = v9 &lt; 30;
      v13 = v12&#91;v9];
      v12&#91;v9] = v12&#91;v9 + 1];
      v12&#91;v9 + 1] = v13;
      v9 += 2;
    }
    while ( v10 );</code></pre>
编写脚本如下：

```python
import base64
c = "MbT3sQgX039i3g==AQOoMQFPskB1Bsc7"
tmp = ""
for i in range(len(c)//2):
	tmp += c[i*2+1] + c[i*2]
#两两交换
new_c = tmp[16:] + tmp[:16]
#前后交换
string1 = str.maketrans("i5jLW7S0GX6uf1cv3ny4q8es2Q+bdkYgKOIT/tAxUrFlVPzhmow9BHCMDpEaJRZN","ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")
strEnBase64 = new_c.translate(string1)

strFlag = base64.b64decode(strEnBase64)

print(strFlag)
```

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-122.png" alt="" class="wp-image-5002" width="443" height="52" />

maketrans和translate方法简介：

Python maketrans() 方法用于创建字符映射的转换表，translate() 方法根据参数table给出的表(包含 256 个字符)转换字符串的字符。

实例如下：

<pre class="wp-block-code"><code>intab = "aeiou"
outtab = "12345"
trantab = str.maketrans(intab, outtab)   # 制作翻译表

str = "this is string example....wow!!!"
print (str.translate(trantab))

结果：th3s 3s str3ng 2x1mpl2....w4w!!!</code></pre>

## 0x01 easy-apk

简单看下功能，也是一个验证flag的功能。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-123.png" alt="" class="wp-image-5004" width="659" height="370" /> </figure> 

上jeb，在主函数看到它的判断逻辑。<figure class="wp-block-image size-full">

<img loading="lazy" width="3012" height="1315" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-124.png" alt="" class="wp-image-5006" /> </figure> 

阅读后发现Base64New类是base64变码表<figure class="wp-block-image size-full">

<img loading="lazy" width="3016" height="1524" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-125.png" alt="" class="wp-image-5007" /> </figure> 

编写脚本如下:

<pre class="wp-block-code"><code>import base64

c = "5rFf7E2K6rqN7Hpiyush7E6S5fJg6rsi5NBf6NGT5rs="

changed = "vwxrstuopq34567ABCDEFGHIJyz012PQRSTKLMNOZabcdUVWXYefghijklmn89+/"

origin = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

s = str.maketrans(changed, origin)
s_EnBase64 = c.translate(s)
flag = base64.b64decode(s_EnBase64)

print(flag)</code></pre>

得到flag<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-126.png" alt="" class="wp-image-5008" width="311" height="33" /> </figure> 

## 0x02 app1

按照惯例查看功能<figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-127.png" alt="" class="wp-image-5010" /> </figure> 

jeb分析，在主函数发现验证的逻辑，可以发现flag的值其实就是v3的每个字符和v4异或拼凑的结果。<figure class="wp-block-image size-full">

<img loading="lazy" width="2518" height="1329" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-128.png" alt="" class="wp-image-5011" /> </figure> 

找到v3、v4的值，编写脚本。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-129.png" alt="" class="wp-image-5012" width="607" height="52" /> </figure> 

<pre class="wp-block-code"><code>v3 = "X&lt;cP&#91;?PHNB&lt;P?aj"
v4 = 15
flag = ""

for i in v3:
	x = ord(i)^v4
	flag += chr(x)

print(flag)</code></pre>

得到flag<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-130.png" alt="" class="wp-image-5013" width="344" height="35" /> </figure> 

## 0x03 app2

这次是个登录界面。<figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1031" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-131.png" alt="" class="wp-image-5014" /> </figure> 

jeb分析SecondActivity代码，ili是用户名，lil是密码，他们加密后等于需要等于`VEIzd/V2UPYNdn/bxH3Xig==`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-134.png" alt="" class="wp-image-5018" width="632" height="209" /> </figure> 

加密的函数来自so文件<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-136.png" alt="" class="wp-image-5020" width="577" height="453" /> </figure> 

将so文件导入ida，搜索doRawData定位到关键函数 ，发现一个key值和AES\_128\_ECB\_PKCS5Padding\_Encrypt的字样，应该是AES加密。<figure class="wp-block-image size-full">

<img loading="lazy" width="2040" height="917" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-132.png" alt="" class="wp-image-5016" /> </figure> 

文本解密后发现不正确，在XML里面发现FileDataActivity从来没有用过<figure class="wp-block-image size-full">

<img loading="lazy" width="2977" height="563" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-135.png" alt="" class="wp-image-5019" /> </figure> 

点击发现有一段字符串，且使用了Encrypto的解密函数。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-137.png" alt="" class="wp-image-5022" width="629" height="375" /> </figure> 

编写python脚本

<pre class="wp-block-code"><code>import base64
from Crypto.Cipher import AES

c = base64.b64decode("9YuQ2dk8CSaCe7DTAmaqAA==")  
key = b'thisisatestkey=='
aes = AES.new(key,AES.MODE_ECB)
flag = aes.decrypt(c)
print(flag)</code></pre><figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-133.png" alt="" class="wp-image-5017" width="360" height="39" /> </figure> 

## 0x04 app3

ab文件没见过，搜索发现<a rel="noreferrer noopener" href="https://blog.csdn.net/qq_33356474/article/details/92188491" target="_blank" rel="nofollow" >https://blog.csdn.net/qq_33356474/article/details/92188491</a>，使用`abe.jar unpack app3.ab app3.tar`得到文件夹，发现apk文件和Encryto.db。

jeb分析代码，在MainActivity中能看到一些信息，怀疑flag加密在数据库文件之中，最后调用了a函数。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-138.png" alt="" class="wp-image-5026" width="710" height="250" /> </figure> 

分析发现需要把`v1.a(v2 + v1.b(v2, v0.getAsString("password"))).substring(0, 7)`的值给捋清楚。<figure class="wp-block-image size-full">

<img loading="lazy" width="2128" height="489" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-139.png" alt="" class="wp-image-5028" /> </figure> 

结合下面图中的代码，分析`v2`的值是Stra1234，`v0.getAsString("password")`的值是123456，然后剩下的看代码是MD5和SHA-1的加密这里直接用它的代码，把v2，v0等值赋过去就好。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-142.png" alt="" class="wp-image-5031" width="750" height="431" /></figure> 

参考<a href="https://www.52pojie.cn/thread-1082706-1-1.html" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.52pojie.cn/thread-1082706-1-1.html</a>代码如下：

```java
import java.security.MessageDigest;
import java.util.*;

public class b {
    public b() {
        super();
    }

    public static void main(String[] args)
    {
        String varV2 = "Stra1234";
        String varV1B = a(varV2);
        String varKey = varV2 + varV1B + "yaphetshan";
        System.out.print("KEY = ");
        System.out.print(b(varKey).substring(0,7));
    }
    
    public static final String a(String arg9) {
        String v0_2;
        int v0 = 0;
        char[] v2 = new char[]{'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'};
        try {
            byte[] v1 = arg9.getBytes();
            MessageDigest v3 = MessageDigest.getInstance("MD5");
            v3.update(v1);
            byte[] v3_1 = v3.digest();
            int v4 = v3_1.length;
            char[] v5 = new char[v4 * 2];
            int v1_1 = 0;
            while(v0 < v4) {
                int v6 = v3_1[v0];
                int v7 = v1_1 + 1;
                v5[v1_1] = v2[v6 >>> 4 & 15];
                v1_1 = v7 + 1;
                v5[v7] = v2[v6 & 15];
                ++v0;
            }
    
            v0_2 = new String(v5);
        }
        catch(Exception v0_1) {
            v0_2 = null;
        }
    
        return v0_2;
    }
    
    public static final String b(String arg9) {
        String v0_2;
        int v0 = 0;
        char[] v2 = new char[]{'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'};
        try {
            byte[] v1 = arg9.getBytes();
            MessageDigest v3 = MessageDigest.getInstance("SHA-1");
            v3.update(v1);
            byte[] v3_1 = v3.digest();
            int v4 = v3_1.length;
            char[] v5 = new char[v4 * 2];
            int v1_1 = 0;
            while(v0 < v4) {
                int v6 = v3_1[v0];
                int v7 = v1_1 + 1;
                v5[v1_1] = v2[v6 >>> 4 & 15];
                v1_1 = v7 + 1;
                v5[v7] = v2[v6 & 15];
                ++v0;
            }
    
            v0_2 = new String(v5);
        }
        catch(Exception v0_1) {
            v0_2 = null;
        }
    
        return v0_2;
    }
}
```

编译运行得到`ae56f99`<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-143.png" alt="" class="wp-image-5032" width="374" height="91" /> </figure> 

解密文件，得到flag的base64值。<figure class="wp-block-image size-full">

<img loading="lazy" width="924" height="118" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-144.png" alt="" class="wp-image-5033" /> </figure> 

## 0x05 easy-so

放到模拟器，字符串验证。<figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-145.png" alt="" class="wp-image-5034" /> </figure> 

上jeb，找到关键代码，开始分析。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-146.png" alt="" class="wp-image-5035" width="830" height="148" /> </figure> 

CheckString在so文件里面，上ida分析。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-147.png" alt="" class="wp-image-5036" width="419" height="206" /> </figure> 

简单分析代码<figure class="wp-block-image size-full">

<img loading="lazy" width="2287" height="1430" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-148.png" alt="" class="wp-image-5037" /> </figure> 

第一部分代码逻辑如下：

<pre class="wp-block-code"><code>v3 = strlen(v11);//v3是v11的字符串长度
v4 = (char *)malloc(v3 + 1);//为v4请求v3+1长度的内存空间
memset(&v4&#91;v3], 0, v3 != -1);//将v4扩增一倍并后面扩增的部分初始化为0，v4=----0000
memcpy(v4, v11, v3);//将v11的内容复制到v4中
if ( strlen(v4) >= 2 )//若v4的长度大于等于2
{
  v5 = 0;
  do
  {
    v6 = v4&#91;v5];
    v4&#91;v5] = v4&#91;v5 + 16];
    v4&#91;v5++ + 16] = v6;
  }
  while ( v5 &lt; strlen(v4) >> 1 );//在v5小于v4长度的一半时，将v4的第v5个字符与第v5+16个字符交换位置
}


void *memset(void *str, int c, size_t n) 复制字符 c（一个无符号字符）到参数 str 所指向的字符串的前 n 个字符。
str -- 指向要填充的内存块。
c -- 要被设置的值。该值以 int 形式传递，但是函数在填充内存块时是使用该值的无符号字符形式。
n -- 要被设置为该值的字符数。

void *memcpy(void *str1, const void *str2, size_t n) 从存储区 str2 复制 n 个字节到存储区 str1。
str1 -- 指向用于存储复制内容的目标数组，类型强制转换为 void* 指针。
str2 -- 指向要复制的数据源，类型强制转换为 void* 指针。
n -- 要被复制的字节数。</code></pre>

第二段代码逻辑如下： 

<pre class="wp-block-code"><code>v7 = *v4;//指针v7指向v4
if ( *v4 )//如果v4存在
{
  *v4 = v4&#91;1];
  v4&#91;1] = v7;
  if ( strlen(v4) >= 3 )//v4的长度大于等于3
  {
    v8 = 2;
    do
    {
      v9 = v4&#91;v8];
      v4&#91;v8] = v4&#91;v8 + 1];
      v4&#91;v8 + 1] = v9;
      v8 += 2;
    }
    while ( v8 &lt; strlen(v4) );//两两交换
  }
}</code></pre>

最后的结果为f72c5a36569418a20907b55be5bf95ad，那么我们可以编程逆退回去。

<pre class="wp-block-code"><code>c = "f72c5a36569418a20907b55be5bf95ad"
tmp = ""
#两两交换
for i in range(len(c)//2):
	tmp += c&#91;i*2+1] + c&#91;i*2]
#前后交换
flag = tmp&#91;16:] + tmp&#91;:16]

print(flag)</code></pre><figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-149.png" alt="" class="wp-image-5039" width="484" height="50" /> </figure>
