# 2021年暑期夏令营笔记(day7-day8)

<div class="has-toc have-toc">
</div>
## 0x00 shellcode从0到1

<figure class="wp-block-image size-full">

<img loading="lazy" width="1252" height="471" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-37.png" alt="" class="wp-image-3632" /> </figure> 

Linux系统调用表

<a href="https://github.com/torvalds/linux/tree/master/arch/x86/entry/syscalls" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://github.com/torvalds/linux/tree/master/arch/x86/entry/syscalls</a>

<a href="https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md" target="_blank"  rel="nofollow" >https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md</a>

## 0x01 Windows平台下的shellcode利用

Windows下的Shellcode  
优势：使用起来非常灵活，且易变形  
劣势：开发困难  
难点：如何动态定位API函数地址

API HASH

<a href="https://neil-fox.github.io/Anti-analysis-using-api-hashing/" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://neil-fox.github.io/Anti-analysis-using-api-hashing/</a>

在常规编程中,只需引入其头文件,便可调用某API函数,编译器在编译过程中会将相关信息编译到PE文件中(这里的相关信息主要是指 MAGE\_IMPORT\_DESCRIPTORS结构体)。当程序执行时,操作系统会将PE文件映射到内存,这个映射过程包括调用 LoadLibrary加载相应的动态链接库,以及调用 GetProcAddress取所有AP函数在内存中的地址,像这样的dll加载方式,我们称为隐式链接。

ShellCode开源框架

<a href="https://github.com/mai1zhi2/ShellCodeFramework" target="_blank"  rel="nofollow" >https://github.com/mai1zhi2/ShellCodeFramework</a><figure class="wp-block-image size-full">

<img loading="lazy" width="560" height="509" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-39.png" alt="" class="wp-image-3638" /></figure> 

实操

<a href="https://uknowsec.cn/posts/notes/shellcode%E5%8A%A0%E8%BD%BD%E6%80%BB%E7%BB%93.html" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://uknowsec.cn/posts/notes/shellcode%E5%8A%A0%E8%BD%BD%E6%80%BB%E7%BB%93.html</a>

实战视角

<a href="https://blog.csdn.net/qq_35740100/article/details/116300959" data-type="URL" data-id="https://blog.csdn.net/qq_35740100/article/details/116300959" target="_blank" rel="noreferrer noopener" rel="nofollow" >msf生成弹出calc一段shellcode分析</a>

<a href="https://blog.csdn.net/lacoucou/article/details/107560280" data-type="URL" data-id="https://blog.csdn.net/lacoucou/article/details/107560280" target="_blank" rel="noreferrer noopener" rel="nofollow" >Metasploit & CobaltStrike 的shellcode分析</a><figure class="wp-block-image size-full">

<img loading="lazy" width="1076" height="432" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-40.png" alt="" class="wp-image-3640" /> </figure> 

在APT攻击中,有对现有 shellcode的利用,如<a rel="noreferrer noopener" href="https://www.freebuf.com/articles/system/280678.html" data-type="URL" data-id="https://www.freebuf.com/articles/system/280678.html" target="_blank" rel="nofollow" >海莲花组织利用CS的 shellcode进行攻击</a>，同时,某<a href="https://www.crowdstrike.com/blog/guloader-malware-analysis/" data-type="URL" data-id="https://www.crowdstrike.com/blog/guloader-malware-analysis/" target="_blank" rel="noreferrer noopener" rel="nofollow" >些APT组织也会开发一些特定的 shellcode</a>

推荐资料：

逆向工程核心原理  
Windows核心编程  
<a href="https://securitycafe.ro/?s=shellcode+development" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://securitycafe.ro/?s=shellcode+development</a>

## 0x02 加壳

原理： 原程序最开始运行的一段代码是原始入口点，加壳之后只要先把壳代码运行再跳转到入口点，原程序依然正常运行。而在壳代码中就可以对原程序进行加解密等操作。

目的：使反汇编和反编译变得尽可能复杂，“反”出来结果尽可能无意义，甚至根本就“反”不出来。

结果：静态反汇编的代码无意义，需要动态分析。

壳的分类：  
1.压缩壳  
2.加密壳  
3.虚拟机壳

加壳后的区别：

  * 入口点不同
  * 区段名会变
  * 区段大小会变

在32位系统下，操作系统给每一个应用程序都分配了4gb的存储空间（虚拟存储空间），仅仅是exe就不需要考虑这个问  
题，但是很多exe会加载动态链接库（.dll）

exe基址：<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-41.png" alt="" class="wp-image-3646" width="537" height="66" /> </figure> 

dll基址：<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-42.png" alt="" class="wp-image-3647" width="219" height="130" /> </figure> 

为什么是需要重定位：  
1、对与exe，exe首先会加载到内存，每个文件总是使用独立的虚拟内存空间，这就意味着exe文件就不需要考虑基址重定位的问题  
2、对于dll，在一个4gb虚拟内存里有多个dll，不能保证每次都加载到同样的位置，存在被其他dll占用的问题  
3、对于系统的dll，实际上不会发生重定位

**随机基址(alsr)**

恶意代码bypass alsr、bypass dep等等，windows vista之后才有的机制（原因：针对缓冲区溢出的保护机制，从NT6.0开  
始使用）

windows7上：程序重启就能随机基址，基址会变化  
windows10：重启的系统，基址会变化

开启条件：程序（vs中可以查看）+操作系统（windows7之后）

**exe程序开启alsr和没有开启有什么区别？（都能执行）**

1、区段数量不一样<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-44.png" alt="" class="wp-image-3651" width="588" height="457" /> </figure> 

2、文件头的characteristic中的重定位信息标志<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-45.png" alt="" class="wp-image-3652" width="702" height="569" /> </figure> 

3、可选头（option header）中的dllcharacteristic的dymaic_base标志<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-47.png" alt="" class="wp-image-3654" width="762" height="456" /> </figure> 

4、区段不一样<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-48.png" alt="" class="wp-image-3655" width="642" height="444" /> </figure> 

**如何去掉随机基址？**

修改两个字段：<figure class="wp-block-image size-full">

<img loading="lazy" width="1648" height="667" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-50.png" alt="" class="wp-image-3657" /> </figure> 

**汇编代码知识**<figure class="wp-block-image size-full">

<img loading="lazy" width="809" height="547" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-51.png" alt="" class="wp-image-3658" /> </figure> 

一个简单的壳：

  1. 添加区段
  2. 在区段中添加跳转到oep的汇编代码
  3. 修改原程序的oep为添加的区段中的代码的地址

一般情况下加壳的流程：

  1.  保存寄存器环境
  2. 加载一些必要的API
  3. 解密代码和数据
  4. 修复重定位
  5. 填充IAT
  6. 恢复寄存器环境

## 0x03 脱壳

**脱壳的方法**

  * 寻找原始OEP 
  * dump内存到文件
  * 修复文件

1、esp定律

有了ESP定律，可以方便我们脱掉大多数的压缩壳。

2、单步跟踪

利用OD的单条指令执行功能，从壳的入口一直执行到OEP，最终通过这个OEP将原程序dump出来。然当，在单步跟踪的时候需要跳过一些不能执行到的指令。

3、其他：<a href="https://www.52pojie.cn/thread-259984-1-1.html" target="_blank"  rel="nofollow" >https://www.52pojie.cn/thread-259984-1-1.html</a>

**脱壳相关工具**

  * OD：动态调试 
  * ImportRec：修复IAT 
  * PEID、exeinfo：查壳

**脱压缩壳**

  * Esp定律：
  * 步过保存寄存器的指令，在esp寄存器上下硬件断点，然后运行起来，单步几步找到oep 
  * 使用OD插件Ollydump或者OllydumpEx，转存
  * 使用ImportRec修复IAT 

**脱加密壳**

  * 解密IAT与脱壳分析
  * 脱壳脚本的编写

**脱反调试壳**

  1. 搭建异常触发环境
  2. 分析触发的异常
  3. 寻找原始OEP
  4. 寻找写入IAT和获取API地址的点
  5. 编写脚本修复IAT 
  6. 使用通用导入表修复工具修复IAT引用代码

**脱反虚拟机壳**

  1. 修改虚拟机配置
  2. 对偷取OEP的修复
  3. 对IAT调用的修复

**虚拟机保护壳-VMP**

虚拟机保护代码技术是将x86汇编指令转换为字节码指令，并且通过自己设计的解释器去执行字节码指令的一项技术，以达到保护原有指令不被轻易逆向和篡改

<a rel="noreferrer noopener" href="https://www.cnblogs.com/PhantomW/p/9334237.html" target="_blank" rel="nofollow" >手工脱壳之未知加密壳</a>

老师博客：<a rel="noreferrer noopener" href="https://www.yuque.com/hackdoors" target="_blank" rel="nofollow" >https://www.yuque.com/hackdoors</a>
