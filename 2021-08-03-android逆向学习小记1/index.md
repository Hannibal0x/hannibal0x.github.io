# Android逆向学习小记(1)

<div class="has-toc have-toc">
</div>

## 0x00 前言

 WhITECat安全团队开展了Android逆向学习的入门活动，正好对这块儿有些兴趣，趁此机会学习一下，顺便记录。

## 0x01 准备工作

Android逆向常用指令集

netstat -a 查看开启了哪些端口,常用netstat -an  
netstat -n 查看端口的网络连接情况，常用netstat -an  
netstat -o 显示网络与每个连接相关的所属进程 ID

taskkill /T 终止指定的进程和由它启用的子进程。  
taskkill /F 指定强制终止进程。  
taskkill /? 显示帮助消息。  
Windows 中杀死进程分两步：1 查询端口占用2.强行杀死进程  
例：#查询一下本地所有网络连接，提取包含 8080（已建立连接）的行  
netstat -ano | findstr "8080"  
taskkill /pid 4000 -t -f

常用ADB命令(用于电脑与手机或者模拟器交互)<figure class="wp-block-image size-full">

<img loading="lazy" width="732" height="425" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-28.png" alt="" class="wp-image-2128" /> </figure> 

在咸鱼上淘了个Nexus5，参考<a rel="noreferrer noopener" href="https://www.cnblogs.com/exmyth/p/4623180.html" target="_blank" rel="nofollow" >https://www.cnblogs.com/exmyth/p/4623180.html</a>刷root，然后配置 adb 调试，安装MT管理器。

雷电模拟器，该款模拟器的优势在于内存占用少，稳定，速度也比较快，当然最重要的是该模拟器在无需签名 app 也可以正常在模拟器上运行，同时已自动开启全局调试模式。模拟器自动开启了USB调试，只需要安装上MT管理器就完成环境搭建。

环境搭建需要配置好Java和SDK、NDK的环境变量。安装可视化的安卓应用逆向工具AndroidKiller，有Apk 反编译、Apk 打包、Apk签名，编码互转等功能。简化了逆向分析apk使用不同工具的繁琐工作。使用AndroKiller打开apk,修改smail代码，编译生成apk，安装。

## 0x02 APK文件结构

Android 应用是用Java 编程语言编写实现的，利用Android SDK 编译代码，并且把所有的数据和资源文件打包成APK(Application Package)文件，可以简单把apk视为一个压缩包。常见目录如下：<figure class="wp-block-image size-full">

<img loading="lazy" width="719" height="290" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-29.png" alt="" class="wp-image-2137" /> </figure> 

**assets目录**：存放需要打包到 APK的静态资源文件，例如图片资源文件、JSON 配置文件、渠道配置文件、二进制数据文件、HTML5 离线资源文件等。与res/raw 目录不同的是，assets 目录支持任意深度的子目录，同时该目录下面的文件不会生成资源ID。

**lib目录**：存放程序依赖的native 库文件，一般是用C/C++编写，这里的lib 库可能包含4 中不同类型，根据CPU 型号的不同，大体可以分为ARM，ARM-v7a，MIPS，X86，分别对应着ARM 架构，ARM-V7 架构，MIPS 架构和X86 架构。

**META-INF目录**：存放着应用程序的的签名和证书，该信息可以验证APK 的完整性。META-INF 目录中包含的文件有CERT.RSA(公钥、加密算法等信息)，CERT.SF(对摘要文件的签名文件)和MANIFEST.MF(摘要文件)。详情参考：<a href="https://blog.csdn.net/lostinai/article/details/54694564" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://blog.csdn.net/lostinai/article/details/54694564</a>

**res目录**：存放应用程序的资源，如图片资源，xml 配置资源。此文件夹下的所有文件都会映射到Android 工程中的.R 文件中，生成对应的资源ID，访问的时候直接使用资源ID，即R.ID.FILENAME，res 文件夹下可以包含多个文件夹；anim 是存放动画文件的；drawable 目录存放图形资源；layout 目录存放布局文件；values 目录存放一些特征值；colors.xml 存放color 的颜色值等。

**AndroidManifest.xml文件**：应用程序的配置文件，Android 应用的四大组件（Activity、Service、BroadcastReceiver 和 ContentProvider ）都在此配置和声明。

**classes.dex文件**：应用程序的可执行文件，Android 的所有java 代码都在这，通过反编译工具可以查看其代码。当文件中的方法数超过65535就会进行分包处理，若未超过则只有一个dex。

**resources.arsc文件**：资源索引表，资源配置文件，用来记录资源文件和资源ID 之间的映射关系，用来根据资源ID寻找资源。

Android应用Apk的安装有如下四种方式：

1.系统应用安装。没有安装界面，在开机时自动完成。  
2.网络下载应用安装。没有安装界面，在应用市场完成。  
3.ADB命令安装。没有安装界面，通过命令直接安装  
4.外部设备安装。有安装界面，通过SD卡等外部设备安装，由packageInstaller处理安装逻辑。<figure class="wp-block-image size-full">

<img loading="lazy" width="1508" height="795" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-31.png" alt="" class="wp-image-2146" /> </figure> 

## 0x03 修改apk图标实现二次打包

应用原始图标<figure class="wp-block-image size-full">

<img loading="lazy" width="117" height="136" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-32.png" alt="" class="wp-image-2156" /> </figure> 

将apk拖入AndroidKiller进行反编译，在AndroidManfest.xml配置文件中查看图片资源的名称。<figure class="wp-block-image size-full">

<img loading="lazy" width="1409" height="217" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-33.png" alt="" class="wp-image-2160" /> </figure> 

 ****META-INF目录下的MANIFEST.MF文件对apk 中所有文件和非文件进行摘要处理，因此在此文件中可以找到图标资源对应的路径。<figure class="wp-block-image size-full">

<img loading="lazy" width="887" height="357" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-34.png" alt="" class="wp-image-2163" /> </figure> 

到res目录下，替换相应的文件，再回编译该apk。在apk 中，每一个apk 都有一个唯一的包名。手机系统通过这个包名来检测是否属于同一个app,也就是包名是apk 的唯一标识。故需要删除之前安装的apk后再安装新apk。<figure class="wp-block-image size-full">

<img loading="lazy" width="136" height="147" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-35.png" alt="" class="wp-image-2165" /> </figure> 

## 0x04 修改apk包名实现分身

在AndroidManifest.xml 中的manifest 标签中的package 属性，这个属性后面的值就是 apk 的包名，这里是 package="com.miniclip.angerofstick2.yyh" ，修改package 的 属 性 值 （ 不 要 改 为 中 文 ） ， 这 里 改 为package="com.miniclip.angerofstick2.yyh.pro ”,然后还需要修改的是provider,即内容提供者，在 AndroidManifest.xml 中 搜 索 ” <provider” ， 修 改 provider 标 签 里 面 的android:authorities 这个属性的值，这里在原有的值后面全部加上1，然后点击保存。<figure class="wp-block-image size-full">

<img loading="lazy" width="464" height="23" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-36.png" alt="" class="wp-image-2169" /> </figure> 

回编译，安装，发现成功安装两个一样的app，并且可以正常运行。<figure class="wp-block-image size-full">

<img loading="lazy" width="405" height="161" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-37.png" alt="" class="wp-image-2170" /> </figure> 

修改apk名称方式有两种：

1、局搜索字符串"火柴人突击格斗"，替换所有"火柴人突击格斗"为"我的app"。建议此方法，效率更高，且不容易出错。

2、修改配置文件，直接固定apk 的名称。因为AndroidManifest.xml是 apk 的配置清单文件，所以可以直接修改这个文件进行篡改 apk 的名称。在AndroidManifest.xml 找 到 android:label ， 修 改 所 有 地 方 ， 这 里 改 成android:label="你的app",然后保存。<figure class="wp-block-image size-full">

<img loading="lazy" width="378" height="182" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-38.png" alt="" class="wp-image-2174" /> </figure> 

## 0x05 修改apk资源实现去广告

apk 的启动界面是在AndroidManifest.xml 配置声明的，他的配置声明位置如图所示：<figure class="wp-block-image size-full">

<img loading="lazy" width="1432" height="375" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-39.png" alt="" class="wp-image-2175" /> </figure> 

只需要修改apk 主界面的activity 为我们的初次打开界面即可去除开屏广告页面。在模拟器打开应用，使用adb命令查看是否正常开启。<figure class="wp-block-image size-full">

<img loading="lazy" width="263" height="72" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-40.png" alt="" class="wp-image-2177" /> </figure> 

使 用 命 令 `adb shell dumpsys activity | findstr"mFocusedActivity"`，查看当前界面的组件名为o`rg.cocos2dx.lua.AppActivity`。`dumpsys` 命令查询系统服务的运行状态 (对象的成员变量属性值)，命令格式：`dumpsys 服务名`。`dumpsys activity`，用于查询 AMS 服务相关信息。<figure class="wp-block-image size-full">

<img loading="lazy" width="1120" height="61" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-41.png" alt="" class="wp-image-2180" /> </figure> 

<pre class="wp-block-preformatted">&lt;action android:name="android.intent.action.MAIN"/&gt;
&lt;category android:name="android.intent.category.LAUNCHER"/&gt;</pre>

main 和launcher 属性结尾的是当前的入口界面。删除初始化启动页面，<category>标签里的`android.intent.category.DEFAULT`修改为`android.intent.category.LAUNCHER`<figure class="wp-block-image size-full">

<img loading="lazy" width="812" height="287" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-43.png" alt="" class="wp-image-2183" /> </figure> 

也可以直接删除整个activity，<category>标签里的`android.intent.category.DEFAULT`修改为`android.intent.category.LAUNCHER` <figure class="wp-block-image size-full">

<img loading="lazy" width="785" height="282" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-44.png" alt="" class="wp-image-2184" /> </figure> 

去除掉laserdraw的弹窗广告。将该apk 拖入AndroidKiller 中反编译，打开AndroidManifest.xml，找到修改`user-permission` 标签，删除掉部分关于网络权限配置声明。  
android.permission.INTERNET，访问网络连接，可能产生GPRS 流量  
android.permission.CHANGE\_WIFI\_STATE，Wifi 改变状态  
android.permission.ACCESS\_WIFI\_STATE，WiFi 状态  
android.permission.ACCESS\_NETWORK\_STATE，网络状态<figure class="wp-block-image size-full">

<img loading="lazy" width="1042" height="194" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-45.png" alt="" class="wp-image-2192" /> </figure>
