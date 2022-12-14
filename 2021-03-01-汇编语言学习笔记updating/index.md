# 《汇编语言》学习笔记(updating)

<div class="has-toc have-toc">
</div>

## oxoo 前言

在绿盟测试赛题时遇到Reverse就头大，于是购入了王爽老师的第四版《汇编语言》，从零开始学习。

## 0x01 基础知识

汇编语言有以下3类指令组成。

（1）汇编指令：机器码的助记符，有对应的机器码，汇编语言的核心。

（2）伪指令：没有对应的机器码，由编译器执行，计算机并不执行。

（3）其他符号：如+、-、*、/等，由编译器识别，没有对应的机器码。

CPU想要进行数据的读写，必须和外部器件进行下面3类信息交互。

（1）存储单元的地址（地址信息）\----到哪儿去？

（2）器件的选择，读或写的命令（控制信息）\----怎么去？

（3）读或写的数据（数据信息）\----谁去？

内存地址空间的大小受CPU地址总线宽度的限制

## 0x02 寄存器

AX、BX、CX、DX这4个寄存器通常用来存放一般性的数据，被称为通用寄存器。AX的低8位（0-7位）构成了AL寄存器，高八位（8-15位）构成了AH寄存器。

在进行数据传送或运算时，要注意指令的两个操作对象的位数应当是一致的。

物理地址=段地址x16+偏移地址

段地址x16有一个更为常用的说法，左移4位

CS为代码段寄存器，IP为指令指针寄存器。

8086CPU的工作流程可以简要描述如下：

（1）从CS:IP指向的内存单元读取指令，读取的指令进入指令缓冲器。

（2）IP=IP+所读指令的长度，从而指向下一条指令。

（3）执行指令。转到步骤（1），重复这个过程。

“jmp 段地址:偏移地址”指令的功能：用指令中给出的段地址修改CS，偏移地址修改IP。

“jmp 某一合法寄存器”指令的功能：用寄存器中的值修改IP。

## 0x03 寄存器（内存访问）

任何两个地址连续的内存单元，N号单元和N+1号单元，可以将它们看成两个内存单元，也可看成一个地址为N的字单元中的高位字节单元和低位字节单元。

"[...]"表示一个内存单元，"[...]"中的0表示内存单元的偏移地址。

如果将10000H-1FFFFH，这段空间当作栈段，初始状态栈是空的，此时，SS=1000H，SP=?

如果将10000H-1FFFFH这段空间当作栈段，SS=1000H，栈空间为64KB，栈最底的字单元地址为1000:FFFE。任意时刻，SS:SP指向栈顶单元，当栈中只有一个元素的时候，SS=1000H，SP=FFFEH。栈为空，就相当于栈中唯一的元素出栈， 出栈后，SP=SP+2。

SP原来为FFFEH,加2后SP=0，所以，当栈为空的时候，SS=1000H， SP=0。

换一个角度看，任意时刻，SS:SP 指向栈顶元素，当栈为空的时候，栈中没有元素，也就不存在栈项元素，所以SS:SP只能指向栈的最底部单元下面的单元，该单元的地址栈最底部的字单元的地址+2。栈最底部字单元的地址为1000:FFFE，所以栈空时，SP=0000H。

下载winXP，DEBUG使用的是十六进制。

详细使用可参考：<a href="https://www.cnblogs.com/tiger2soft/p/5094917.html" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.cnblogs.com/tiger2soft/p/5094917.html</a>

## 0x04 第一个程序

段名 segment

段名 ends

segment和ends是成对使用的伪指令，功能是定义一个段，segment说明一个段的开始，ends说明一个段的结束。

end是一个汇编程序的结束标记，不同于ends。

assume的含义是“假设”，将特定用途的段和相关的段寄存器关联起来。

安装masm来对程序进行编程、编译、连接、跟踪。

## 0x05 [BX]和loop指令

loop指令的格式是：loop标号，CPU执行loop指令时，要执行两步操作，1、(cx)=(cx)-1；2、判断cx中的值，不为零则转至标号处执行程序，如果为零则向下执行。

在汇编源程序中，数据不能以字母开头。

## 0x06 包含多个段的程序

“dw”的含义是定义字型数据。dw即“define word”。

在单任务系统中，可执行文件中的程序执行过程如下。

（1）由其他的程序（Debug、command或其他程序）将可执行文件中的程序加载入内存

（2）设置CS:IP指向程序的第一条要执行的指令（即程序的入口），从而使程序得以运行。

（3）程序运行结束后，返回到加载者。

“assume cs:code,ds:data,ss:stack"将cs、ds和ss分别和code、data、stack段相连。

## 0x07 更灵活的定位内存地址的方法

用'.....'的方式指明数据是以字符的形式给出的，编译器将它们转化为相对应的ASCII码。

[bx+idata]表示一个内存单元，它的偏移地址为(bx)+idata

si和di是8086CPU中和bx功能相近的寄存器，si和di不能分成两个8位寄存器来使用。

寻址方式

（1）[idata]用一个常量来表示地址，用于直接定位一个内存单元。

（2）[bx]用一个变量来表示内存地址，可用于间接定位一个内存单元。

（3）[bx+idata]用一个变量和常量表示地址，可在一个起始地址的基础上用变量间接定位一个内存单元。

（4）[bx+si]用两个变量表示地址。

（5）[bx+si+idata]用两个变量和一个常量表示地址。

一般来说，在需要暂存数据的时候，我们都应该使用栈。

## 0x08 数据处理的两个基本问题

reg的集合包括：ax、bx、cx、dx、ah、al、bh、bl、ch、cl、dh、dl、sp、bp、si、di；

sreg的集合包括：ds、ss、cs、es。

在8086CPU中，只有bx、si、di和dp可以用在"[....]"中来进行内存单元寻址。

在[...]中，这4个寄存器可以单个出现，或只能以4种组合出现：bx和si、bx和di、bp和si、bp和di。

只要在[...]中使用寄存器bp，而指令中没有显性地给出段地址，段地址就默认在ss中。

div做除法时的注意事项:

(1)除数:有8位和16位两种，在一个reg或内存单元中。

(2)被除数:默认放在AX或DX和AX中，如果除数为8位，被除数则为16位，默认在AX中存放;如果除数为16位，被除数则为32位，在DX和AX中存放，DX存放高16位，AX存放低16位。

(3) 结果:如果除数为8位，则AL存储除法操作的商，AH存储除法操作的余数;如果除数为16位，则AX存储除法操作的商，DX存储除法操作的余数。

dup的使用格式如下：

db 重复次数 dup （重复的字节型数据）

dw 重复次数 dup （重复的字型数据）

dd 重复次数 dup （重复的双字型数据）

## 0x09 转移指令的原理

短转移IP的修改范围为-128-127

近转移IP的修改范围为-32768-32767

操作符offset在汇编语言中是由编译器处理的符号，它的功能是取得标号的偏移地址。

jmp short 标号（转到标号处执行指令），实现段内的短转移，功能为(IP)=(IP)+8位位移。

CPU在执行jmp指令的时候并不需要转移的目的地址。

jmp near ptr 标号，实现的是段内近转移，功能为(IP)=(IP)+16位位移。

"jmp far ptr 标号"实现的是段间转移，又称远转移。

"jcxz 标号"的功能相当于：if((cx)==0) jmp short 标号;

## 0x0A CALL和RET指令

ret指令用栈中的数据，修好IP的内容，从而实现近转移。

retf指令用栈中的数据，修好CS和IP的内容，从而实现远转移。

CPU执行call指令时，进行两步操作：

（1）将当前的IP或CS和IP压入栈中；

（2）转移。

call 标号（将当前的IP压栈后，转到标号处执行指令）

CPU执行此种格式call指令时，进行两步操作：

（1）(sp)=(sp)-2

((ss)*16+(sp))=(IP)

（2）(IP)=(IP)+16位位移

call far ptr 标号，实现的是段间转移。

CPU执行此种格式call指令时，进行两步操作：

（1）(sp)=(sp)-2

((ss)*16+(sp))=(CS)

(sp)=(sp)-2

((ss)*16+(sp))=(IP)

（2）(CS)=标号所在段的段地址

(IP)=标号所在段中的偏移地址

使用mul做乘法的时候，注意以下两点：

（1）两个相乘的数：两个相乘的数，要么都是8位，要么都是16位。如果是8位，一个默认放在AL中，另一个放在8位reg或内存字节单元中；如果是16位，一个默认放在AX中，另一个放在16位reg或内存字节单元中；

（2）结果：如果是8位乘法，结果默认放在AX中；如果是16位乘法，结果高位默认放在DX中，低位在AX中。

## 0x0B 标志寄存器

<figure class="wp-block-image is-resized">

<img loading="lazy" src="https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=3179392297,1084784159&fm=26&gp=0.jpg" alt="" width="602" height="121" title="点击查看源网页" /> </figure> <figure class="wp-block-image size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/03/图片-1.png" alt="" class="wp-image-1579" width="636" height="327" /></figure> 

CF和OF的区别：CF是对无符号数运算有意义的标志位，而OF是对有符号数运算有意义的标志位。

adc是带进位的加法指令，利用了CF上记录的进位值。

指令格式：adc 操作对象1 操作对象2

功能：操作对象1=操作对象1+操作对象2+CF

如果CF的值是被sub指令设置的，那么它的含义就是借位值；如果是被add指令设置的，那么它的含义就是进位值。

sbb是带借位的减法指令，利用了CF上记录的借位值。

指令格式：sbb 操作对象1 操作对象2

功能：操作对象1=操作对象1-操作对象2-CF

cmp是比较指令，cmp的功能相当于减法指令，只是不保存结果。cmp指令执行后，将对标志寄存器产生影响。其他相关指令通过识别这些被影响的标志寄存器位来得知比较结果。

DF在串处理指令中，控制每次操作后si、di的增减。

df=0 每次操作后si、di递增；df=1 每次操作后si、di递减。
