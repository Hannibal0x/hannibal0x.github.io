# 2021年暑期夏令营笔记(day4-day5)


## 0x00 day4

<figure class="wp-block-image size-full">

<img loading="lazy" width="918" height="155" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-78.png" alt="" class="wp-image-3007" /></figure> 

## 0x01 day5

存储内存布局：C语言中，整数类型int通常使用小端方式存储。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-185.png" alt="" class="wp-image-3059" /></figure> 

C语言中，单精度浮点类型float通常使用IEEE浮点标准转换后再以小端方式存储。<figure class="wp-block-image size-full">

<img loading="lazy" width="1188" height="518" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-10.png" alt="" class="wp-image-3558" /> </figure> 

C语言中，字符串中的字符按照从左到右的顺序，依次存储在一段连续的空间里，其中每一个字符占用一个字节，其内容为该字符在ASCII码表中对应的数值。在实际存储时，将自动在字符串尾部加了一个结束标志‘\0’（其ASCII码值为0）<figure class="wp-block-image size-full">

<img loading="lazy" width="1241" height="436" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/图片-187.png" alt="" class="wp-image-3061" /></figure> 

指针变量定义的一般形式为：类型名 * 指针变量名；

指针变量有两个有关的运算符：& 取地址运算符，* 指针运算符。

若有赋值语句p=&a;，则：

&\*p=p。&和\*运算符的优先级相同，结合方向为从右到左。&\*p等价于&(\*p)，\*p就是变量a，再执行&运算，得到&a，也就是p。因此&\*p=&(*p)=&a=p。

\*&a=a。\*&a等价于\*(&a)，&a即为p，再执行\*运算，得到\*p，也就是变量a。因此\*&a=\*(&a)=\*p=a。

可见，&和*运算符在一起，其作用最后抵消。

如果p的初值是&a[0]，那么：  
p+i和a+i都可以表示元素a[i]的地址，即它们都指向数组的第i个元素。a代表数组首地址，a+i也是地址，它的计算方法与p+i相同。\*(p+i) 和\*(a+i)都表示指针p+i或a+i所指向的数组元素a[i]的值。

由此可见，引用一个数组元素可以有两种方法：下标法，如a[i]，指针法，如*(p+i)。

但是二者使用时仍然有区别。因为作为指针变量的p可以实现自身值的改变，例如p++，使p的值自增。而数组名a是一个代表数组首地址的常量，它自身的值是不能改变的，即a++是不合法的。指向数组元素的指针变量可以自增或自减，大大方便了数组元素的操作。

指向函数的指针变量定义的一般形式为：类型名 （* 指针变量名）（参数列表）；

例如：int (\*p)( )、表示p是一个指向函数的指针变量，此函数的返回值为int型。注意，\*p两侧的括号不能省略。

指向函数的指针变量主要由两个用途：调用函数，将函数作为参数在函数间传递。

指针数组定义的形式为：类型名 *数组名[常量表达式]；

指针数组的主要用于管理同种类型的指针，其中最常用在处理若干个字符串(如二维字符数组)的操作。使用指针数组处理字符串时方便、简洁、效率高。

函数调用约定，是指当一个函数被调用时，函数的参数会被传递给被调用的函数和返回值会被返回给调用函数。函数的调用约定就是描述参数是怎么传递和由谁平衡堆栈的，当然还有返回值。<figure class="wp-block-image size-full">

<img loading="lazy" width="1001" height="254" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-12.png" alt="" class="wp-image-3571" /> </figure> 

cdecl\--->ret，被调用者直接返回，不用恢复栈平衡，由调用者负责。stdcall\--->ret 4/8...，被调用者负责栈平衡，弹出字节。

调用过程

  1. 根据函数调用约定传递参数
  2. 保存函数的返回地址
  3. 保存调用方栈底（EBP）
  4. 设定被调用方的栈位置
  5. 为局部变量申请栈空间
  6. 调试版本会将局部变量的初始值设置为0xCCCCCCCC
  7. 保存寄存器环境
  8. 执行函数体
  9. 恢复寄存器环境
 10. 释放局部变量空间
 11. 恢复调用方栈底位置
 12. 根据调用约定清理参数占用空间

（A）__cdecl, 取出返回地址，将程序流程设定到此处，由调用方的代码负责清理参数空间  
（B）其他调用约定, 取出返回地址, 清理参数空间后, 程序流程按返回地址回到调用方

main函数是程序的入口，并不是第一个运行的代码。

宏定义分为带参数的宏定义和不带参数的宏定义。

宏名的有效范围是从定义位置到文件结束。如果需要终止宏定义的作用域，可以用#undef命令。

对程序中用双引号扩起来的字符串内的字符，不进行宏的替换操作。<figure class="wp-block-image size-full">

<img loading="lazy" width="1194" height="573" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/09/图片-13.png" alt="" class="wp-image-3576" /> </figure> 

Windows SDK是微软每推出一个重要的 windows版本，一般都会同时推出一个SDK（Software Development Kit）。SDK包含了开发该windows版本所需的windows函数和常数定义、API函数说明文档、相关工具和示例。

API（Application Programming Interface），其实就是操作系统留给应用程序的一个调用接口，应用程序通过调用操作系统的 API 而使操作系统去执行应用程序的命令（动作）。早在 DOS 时代就有 API 的概念，只不过那个时候的 API是 以中断调用的形式（ INT 21h）提 供 的 ，在DOS下跑的应用程序都直接或间接的通过中断调用来使用操作系统功能，比如将 AH 置为 30h 后调用 INT 21h就可以得到 DOS 操作系统的版本号。而在 Windows 中，系统 API 是以函数调用的方式提供的。同样是取得操作系统的版本号 ，在 Windows 中你所要做的就是调用 GetVersionEx() 函 数 。可以这么说 ，DOS API 是基于汇编的 ， 而Windows API是基于高级语言的。

微软官方文档：<a href="https://docs.microsoft.com/zh-cn/windows/win32/api/" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://docs.microsoft.com/zh-cn/windows/win32/api/</a>

DLL ， 即 Dynamic Link Librar y （ 动 态 链 接 库 ） 。 在 Windows 环境下含有大量.dll格式的文件，这些文件就是动态链接库文件 ，其实也是一种可执行文件格式。跟.exe文件不同的是，.dll文件不能直接执行，通常由.exe在执行时装入，内含有一些资源以及可执行代码等 。其实Windows的三大模块就是以 DLL的形式提供的（ Kernel32.dll， User32.dll， GDI32.dll） ， 里面就含有了API函数的执行代码 。为了使用DLL中的API函数，必须要有API函数的声明（.h）和其导入库（.lib），导入库可以先这样理解，导入库是为了在DLL中找到API的入口点而使用的。

**动态调试工具OllyDbg**

反汇编窗口的列中，双击的效果：

<pre class="wp-block-code"><code>地址列：显示相对被点击地址的地址，再次双击返回到标准地址模式

Hex数据列：设置或取消无条件断点，对应的快捷键是F2

反汇编列：调用汇编器，可直接修改汇编代码

注释列：运行增加或编辑注释，对应快捷键是“；”键</code></pre>

调试中我们经常要用到的快捷键有这些：

<pre class="wp-block-code"><code>F2：设置或取消无条件断点

F4：运行到选定位置

F7：单步步入

F8：单步步过

F9：运行

CTRL+F9：执行到返回</code></pre>

**静态调试工具IDA**

IDA子窗口

<pre class="wp-block-code"><code>IDA View-A是反汇编窗口

HexView-A是十六进制格式显示的窗口

Impor ts是导入表（程序中调用到的外面的函数）

Functions是函数表（这个程序中的函数）

Structures是结构

Enums是枚举</code></pre>
