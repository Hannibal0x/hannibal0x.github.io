# Android逆向学习小记(2)



## 0x00 前言 {#toc-head-1}

 继续对Android逆向进行学习，学习JAVA、Android、Dalvik的基本知识。

## 0x01 JAVA {#toc-head-2}

Java的关键字如下：<figure class="wp-block-image size-full">

<img loading="lazy" width="887" height="393" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-51.png" alt="" class="wp-image-2364" /></figure> 

继承可以使用 extends 这个关键字来实现继承，而且所有的类都是继承于java.lang.Object，当一个类没有继承的关键字，则默认继承 object（这个类在java.lang 包中，所以不需要 import）祖先类。

使用 implements 关键字可以变相的使java具有多继承的特性，使用范围为类继承接口的情况，可以同时继承多个接口（接口跟接口之间采用逗号分隔）。

以通过super关键字来实现对父类成员的访问，用来引用当前对象的父类。this关键字指向自己的引用。

final 关键字声明类可以把类定义为不能继承的，即最终类；或者用于修饰方法，该方法不能被子类重写。<figure class="wp-block-image size-full">

<img loading="lazy" width="861" height="195" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-52.png" alt="" class="wp-image-2366" /> </figure> 

多态是同一个行为具有多个不同表现形式或形态的能力。多态就是同一个接口，使用不同的实例而执行不同操作。现实生活中，同一个方法具体实现也会不同。例如，同样是调用人“吃饭”的方法，中国人用筷子吃饭，英国人用刀叉吃饭，印度人用手吃饭。


多态是方法的多态，不是属性的多态(多态与属性无关)。  
多态的存在要有3个必要条件：继承，方法重写，父类引用指向子类对象。  
父类引用指向子类对象后，用该父类引用调用子类重写的方法，此时多态就出现了。

容器：更强大、更灵活、容量随时可扩。容器的接口层次结构图如图所示：<figure class="wp-block-image size-full">

<img loading="lazy" width="791" height="423" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-53.png" alt="" class="wp-image-2369" /> </figure> 

Java 容器类类库的用途是保存对象，可以将其分为2 个概念：  
Collection，独立元素的序列，这些元素都服从一条或多条规则。List、Set 都是Collection 的一种，List 必须按照顺序保存元素，而Set 不能有重复元素。  
Map，Map 是键值对类型，允许用户通过键来查找对象。Hash 表允许我们使用另一个对象来查找某个对象。

Collection接口  
1）List 的特点及实现类  
List 是有序、可重复的容器。List 中每个元素都有索引标记。可以根据元素的索引标记访问元素，从而精确控制这些元素。List 允许加入重复的元素。更准确的来说，List 通常允许满足 e1.equals(e2) 的元素重复加入容器。List 接口常用的实现类有 3 个：ArrayList、LinkedList 和Vector。  
2）ArrayList  
ArrayList 底层是用数组实现的存储。ArrayList 是长度可变数组，元素以线性方式连续存储，内部允许存放重复元素。允许对元素进行随机的快速访问，但是向 ArrayList 中插入和删除元素的速度较慢。ArrayList 是非线程安全的。数组进行扩容时，会将老数组中的元素重新拷贝一份到新的数组中，每次数组容量的增长大约是其原容量的1.5 倍。  
特点：查询效率高，增删效率低，线程不安全。  
3）LinkedList  
LinkedLis 底层用双向链表实现的存储，内部采用双向循环链表实现，插入和删除元素的速度较快，随机访问的速度较慢，LinkedList 也是非线程安全的。  
特点：查询效率低，增删效率高，线程不安全  
4）Vector  
Vector 底层是用数组实现的List，相关的方法都加了同步检查，所以Vector 线程安全,效率低。  
特点：线程安全,效率低。

Set 接口继承Collection 接口，Set 容器的特点上面也提及过，无序不可重复。Set 的常见实现类有HashSet、TreeSet 等，一般使用HashSet。

Map 就是用来存储“键(key)-值(value) 对”的。 Map 类中存储的“键值对”通过键来标识，所以“键对象”不能重复。Map 在实际开发中使用非常广，特别是HashMap。put 进行添加值键对，containsKey 验证主要是否存在、containsValue 验证值是否存在、keySet 获取所有的键集合、values 获取所有值集合、entrySet 获取键值对。

## 0x02 Android

### Activity 

Activity（活动）是Android提供的四大组件之一，是进行Android开发必不可少的组件。

Activity是一个界面的载体，可以把它与html页面进行类比，html页面由各种各样的标签组成，而Activity则可以由各种控件组成。Activity是一个应用组件，用户可与其提供的屏幕进行交互，以执行拨打电话、聊天、发送电子邮件等操作。每个 Activity 都会获得一个用于绘制其用户界面的窗口。窗口通常会充满屏幕，但也可小于屏幕并浮动在其他窗口之上，因此每一个Activity都有一个生命周期。<figure class="wp-block-image size-full">

<img loading="lazy" width="806" height="724" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-54.png" alt="" class="wp-image-2375" /> </figure> 

创建Activity（活动）所要执行的方法：  
1）Create()这个方法已经看到过很多次了，每个活动中我们都重写了这个方法，它会在活动第一次被创建的时候调用。我们在这个方法中完成活动的初始化操作，比如说加载布局、绑定事件等。  
2）Start()这个方法在活动由不可见变为可见的时候调用，即Activity被显示到屏幕上的时候调用此方法。  
3）Resume()这个方法在活动准备好和用户进行交互的时候调用。此时的活动一定位于返回栈的栈顶，并且处于运行状态，即能够获得用户的焦点之前调用此方法。

Activity（活动）被销毁时所执行的方法：  
1）onPause()这个方法在系统准备去启动或者恢复另一个活动的时候调用。当第一个Activity 通过Intent 启动第二个Activity 的时候，将调用第一个Activity 的onPause()方法。然后调用第二个Activity的onCreate()，onStart()，onResume()方法，接着调用第一个 Activity 的 onStop()方法。如果第一个 Activity 重新获得焦点,则将调用onResume()方法；如果第一个Activity 进入用户不可见状态，那么将调用onStop()方法。  
2）onStop()这个方法在活动完全不可见的时候调用，即当第一个 Activity 被第二个Activity完全覆盖,或者被销毁的时候回调用此方法。它和 onPause()方法的主要区别在于，如果启动的新活动是一个对话框式的活动，那么 onPause()方法会得到执行，而onStop()方法并不会执行。  
3）onDestroy()这个方法在活动被销毁之前调用，之后活动的状态将变为销毁状态，或者是调用finish()方法结束Activity的时候调用此方法。可以在此方法中进行收尾工作，比如释放资源等。  
4）onRestart()这个方法在活动由停止状态变为运行状态之前调用，接着将调用 onStart()方法，也就是活动被重新启动了。

1. Activity（活动）的管理模式  
Android采用Task来管理多个Activity。当启动一个APP时,Android就会为之创建一个Task，然后每启动一个activity，则把当前的activity 压到栈顶。比如以此启动页面a->b>c，栈里面的结构如图所示  
c\-----栈顶  
b  
a\-----栈底  
按返回键的时候，从栈顶弹出页面依次为c->b->a


2.Activity的四种启动模式  
1）standard模式  
它是活动默认的启动模式，在不进行显示制定的情况下，所有活动都会自动使用这种启动模式。每次通过此模式来启动activity时，Android总会为目标activity启动一个新的实例。A 跳到了A1 ，A1 又跳到了 A2，但在我们返回点击 BACK 按钮的时候，要一个一个按才会退出程序，这就是standard模式的特点。  
2）singleTop模式  
看完标准模式觉得不太友好，再次使用还需要重新建立活动，而singleTop模式很好的解决了这个问题。就是启动活动的时候，它会去栈中查找一下，看有没有已经存在的活动，有的话就将其调到栈顶，没有就重新创建。  
3）singleTask模式  
使用这种加载模式的activity在同一个Task内只有一个实例，当系统采用此singleTask模式启动activity时，可分三种情况：  
a. 如果将要启动的activity 不存在，系统将会创建目标activity 实例，并将它加入到Task栈顶。  
b.如果将要启动的activity已经位于Task栈顶，此时与singleTop模式的行为相同。  
c. 如果将要启动的 activity 已经存在，但没有位于 Task 栈顶，系统将会把位于该activity上面的所有activity移出Task栈，从而使得目标activity转入栈顶。  
4）singleInstance模式  
使用singleInstance 模式就可实现程序间可以共享活动的实例，在这种模式下会有一个单独的返回栈来管理这个活动，不管是哪个应用程序来访问这个活动，都共用的同一个返回栈，也就解决了共享活动实例的问题。  
此加载模式下，无论从哪个Task中启动目标activity，只会创建一个目标activity实例，并会使用一个全新的Task栈来装载该activity实例。当系统采用singleInstance模式启动activity时，可以分为两种情况：  
a.如果将要启动的activity不存在，系统会先创建一个全新的Task、再创建目标activity的实例，并将它加入新的Task的栈顶。  
b. 如果将要启动的activity 已经存在，无论它位于哪个应用程序中，无论它位于哪个Task中，系统将会把该activity所在的Task转到前台，从而使用该activity显示出来。


Intent是对一个即将进行的操作的抽象，Intent的字面意识就是”意图”，Android应用程序中的三种其他应用程序基本组件——Activity, Service和Broadcast Receiver，都是使用称为intent的消息来”激活”的。如果是两个相邻activity之间的传值，使用Intent传值。


常见Activity之间的三种传递方式  
1）Extras，在intent中附加消息

<pre class="wp-block-code"><code>//传值

Intent intent = new Intent(this, XXXActivity.class);

intent.putExtra(key, value);

startActivity(intent);

//取值

getIntent()方法得到intent对象

Intent intent = getIntent();

//获取Intent中的数据：getXXXExtra()方法

intent.getIntExtra(key, value);--->int

intent.getStringExtra(key);--->String

显示方式：

吐司：Toast.makeText(this, "", Toast.LENGTH_SHORT).show();

打印:Log.i("TAG", "....");

显示在TextView控件上：

mTextView.setText();</code></pre>

2）Bundle传值

<pre class="wp-block-code"><code>//传值：

Intent对象

Intent intent = new Intent(.......);

创建Bundle对象,包裹数据

Bundle bundle = new Bundle();

bundle.putInt(key, value);

bundle.putString(...);

bundle.putBoolean(...);

......

将bundle挂载到Intent对象上

intent.putExtras(bundle);

跳转页面

startActivity(intent);

//取值

getIntent()得到intent对象

获取Bundle对象

intent.getExtras();--->Bundle bundle

bundle.getInt(key);

bundle.getString(key);

...........

显示：同上</code></pre>

3）通过对象方式传值

<pre class="wp-block-code"><code>//传值

Intent intent = new Intent(this, XXXActivity.class);

创建一个类实现序列化(Person为例)

部分代码：

public class Person implements Serializable{

 private static final long serialVersionUID = 1L;

 private String name;

 private List&lt;String> list;

 ....}

创建Person对象

Person person = new Person();

person.setName(...);

List&lt;String> list = new ArrayList&lt;>();

list.add(...);

person.setList(list);

在intent上设置序列化对象

intent.putExtra(key, person);

跳转

startActivity(intent);

//取值

获取intent对象

getIntent();-->Intent intent

获取序列化对象

intent.getSerializableExtra(key);-->Person person

显示在TextView上：

mTextView.setText(person.toString());</code></pre>

### Service

Service是是不能与用户交互的，不能自己启动的，运行在后台的程序。

Service基本上分为两种形式：启动状态和绑定状态。

启动状态 ：当应用组件（如 Activity）通过调用 startService() 启动服务时，服务即处于“启动”状态。一旦启动，服务即可在后台无限期运行，即使启动服务的组件已被销毁也不受影响，除非手动调用才能停止服务， 已启动的服务通常是执行单一操作，而且不会将结果返回给调用方。

绑定状态 ：当应用组件通过调用 bindService() 绑定到服务时，服务即处于“绑定”状态。绑定服务提供了一个客户端-服务器接口，允许组件与服务进行交互、发送请求、获取结果，甚至是利用进程间通信 (IPC) 跨进程执行这些操作。 仅当与另一个应用组件绑定时，绑定服务才会运行。 多个组件可以同时绑定到该服务，但全部取消绑定后，该服务即会被销毁。  
<figure class="wp-block-image size-full">

<img loading="lazy" width="505" height="689" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-56.png" alt="" class="wp-image-2390" /></figure> 

当我们第一次启动Service时，先后调 onCreate(),onStartCommand ()这两个方法，当停止Service 时，则执行onDestroy()方法，这里需要注意的是，如果 Service 已经启动了，当我们再次启动Service 时，不会再执行onCreate()方法，而是直接执行onStartCommand ()方法。

startService启动Service的生命周期  
执行 startService 时，Service 会经历 onCreate->onStartCommand 。当执行stopService 时，直接调用onDestroy 方法。调用者如果没有stopService，Service 会一直在后台运行，下次调用者再起来仍然可以stopService。

bindService启动Service的生命周期  
执行 bindService 时，Service 会经历 onCreate->onBind 。这个时候调用者和Service 绑定在一起。调用者调用unbindService 方法或者调用者Context 不存在了（如Activity 被finish 了），Service 就会调用onUnbind->onDestroy，这里所谓的绑定在一起就是说两者共存亡了。

### BroadcastReceiver

BroadcastReceiver 用来接收来自系统和应用中的广播。对接收到的广播进行选择处理，想要接收什么样的广播和内部定义的广播匹配，匹配则进行该做的处理操作，没有匹配则无操作，就比如在玩游戏的同时接收到短信事件，对此你要做什么操作，是想看短信内容还是不做什么处理继续玩游戏，这就是广播的用途。

广播的运行原理简图如下：<figure class="wp-block-image size-full">

<img loading="lazy" width="315" height="359" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-57.png" alt="" class="wp-image-2403" /> </figure> 

广播的生命周期十秒左右，如果在 onReceive() 内做超过十秒内的事情，就会报错。每次广播到来时 , 会重新创建 BroadcastReceiver 对象 , 并且调用 onReceive() 方法 , 执行完以后 , 该对象即被销毁 . 当 onReceive() 方法在 10 秒内没有执行完毕， Android会认为该程序无响应 . 所以在BroadcastReceiver 里不能做一些比较耗时的操作。所以一般遇到比较耗时的工作，应该发送intent 给service,由service 完成。

创建广播接收器也非常简单，我们只需要创建一个类继承自BroadCastReceiver 并实现onReceive()方法即可。 当广播到来的时候，onReceive()就会执行，具体的处理逻辑代码写在这个方法中就可以了。范例如下：

<pre class="wp-block-code"><code>package com.feichen.receiver;  

import android.content.BroadcastReceiver;  
import android.content.Context;  
import android.content.Intent;  
import android.util.Log;  

public class MyReceiver extends BroadcastReceiver {      
     private static final String TAG = "MyReceiver";       
     @Override  
     public void onReceive(Context context, Intent intent) {  
         String msg = intent.getStringExtra("msg");  
         Log.i(TAG, msg);  
     }   
} </code></pre>

注册广播的分类有两种，一种是在代码中注册，即动态注册，一种是在AndroidMainfest.xml 中注册，静态注册。

动态注册是在代码中动态指定广播地址并注册。通常是在Activity 或Service 注册一个广播。

<pre class="wp-block-code"><code>MyReceiver receiver = new MyReceiver();          
IntentFilter filter = new IntentFilter();  
filter.addAction("android.intent.action.MY_BROADCAST");            
registerReceiver(receiver, filter);</code></pre>

这种注册方式与静态注册相反，不是常驻型的，也就是说广播会跟随程序的生命周期。当注册完成之后，这个接收者就可以正常工作了。

静态注册是在AndroidManifest.xml 文件中配置的这里给MyReceiver 注册一个广播地址。

<pre class="wp-block-code"><code>&lt;receiver android:name=".MyReceiver">   
         &lt;intent-filter>  
               &lt;action android:name="android.intent.action.MY_BROADCAST"/>  
               &lt;category android:name="android.intent.category.DEFAULT" />  
         &lt;/intent-filter>  
&lt;/receiver> </code></pre>

配置了好之后，只要是 android.intent.action.MY_BROADCAST 这个地址的广播，MyReceiver 都能够接收到。注意，这种方式的注册是常驻型的，也就是说当应用关闭后，如果有广播信息传来，MyReceiver 也会被系统调用而自动运行。

### ContentProvider

ContentProvider 是内容提供者，就是另外一个应用想要访问此应用中私有的数据库，此应用中提供了一个中间对象来供其他应用访问，这个中间对象就是内容提供者。比较官方的理解为，ContentProvider 管理对结构化数据集的访问，它们封装数据，并提供用于定义数据安全性的机制，其他应用通过Context 的ContentResolver 对象作为客户端与ContentProvider 进行通信，访问操作数据。


Android 的数据存储方式总共有五种，分别是：Shared Preferences、网络存储、文件存储、外储存储、SQLite。

但我们知道一般这些存储都只在单独的一个应用程序之中达到一个数据的共享，有时我们需要操作其他应用程序的一些数据，例如操作系统里的通讯录，这时我们就可能通过ContentProvider 来满足我们的需求了。用一张图介绍下：<figure class="wp-block-image size-full">

<img loading="lazy" width="769" height="463" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-58.png" alt="" class="wp-image-2407" /> </figure> 

ContentProvider 常见的几个类  
1. ContentResolver  
在 ContentProvider的 使 用 过 程 中 ， 需 要 借 用 ContentResolver来 控 制ContentProvider所暴露处理的接口，作为代理来间接操作ContentProvider以获取数据。在 Context.java 的源码中如下抽象方法：

<pre class="wp-block-code"><code>/*Return a ContentResolver instance for your application's package.*/
public abstract ContentResolver getContentResolver();</code></pre>

能够在所有继承 Context 的类中通过 getContentResovler() 方法获取ContentResolver。

2. ContentObserver  
ContentObserver 内容观察者，用于观察Uri 引起ContentProvider 中数据变化和通知外界（即访问该数据访问者）。当ContentProvider 中的数据发生变化时，就会触发该ContentObserver 类。


3.URI  
Uri 是统一资源定位符，外界进程通过URI 来找到对应的ContentProvider 和其中的数据，再进行数据操作。ContentProvider 中的URI 有固定格式，如下图：<figure class="wp-block-image size-full">

<img loading="lazy" width="836" height="213" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-59.png" alt="" class="wp-image-2411" /> </figure> 

## 0x03 Dalvik

Dalvik 虚拟机是Android 程序的虚拟机，是Android 中Java 程序的运行基础。每一个Android应用在底层都会对应一个独立的Dalvik 虚拟机实例，其代码在虚拟机的解释下得以执行。

Dalvik 虚拟机（DVM）是基于寄存器的架构，运行的是Dalvik 字节码，Java 虚拟机(JVM)是基于栈的架构，运行的是java 字节码。JAVA 程序经过编译，生成JAVA字节码保存在class 文件中，JVM 通过解码class 文件中的内容来运行程序，而DVM运行的是Dalvik 字节码，所有的Dalvik 字节码由JAVA 字节码转换而来，并被打包到一个DEX 可执行文件中，DVM 通过解释DEX 文件来执行这些字节码。

ART 虚拟机也是一种在Android 操作系统上的运行环境，ART 能够把应用程序的字节码转换为机器码，是Android 所使用的一种新的虚拟机。Dalvik 与ART 区别在于，Dalvik 适用于Android 4.4 及其以下系统使用，而ART适用于Android 4.4 以上系统使用，并且在Android 5.0 及后续Android 版本中作为正式的运行库取代了以往的Dalvik 虚拟机。现在的运行环境基本都是基于 ART 虚拟机运行的。ART 运行时是和Dalvik 虚拟机一样，实现了一套完全兼容Java 虚拟机的接口，因此学习dalvik 虚拟机有助于我们更好的理解app 在我们手机系统上运行。

Dalvik 虚拟机解释执行的是dex 字节码，ART 虚拟机执行的是本地机器码（而这些本地机器码是从 dex 字节码转换而来）。一个简单转换过程如下：  
java–>java bytecode(.jar)–>dalvik bytecode(.dex)  
java–>java bytecode(.jar)–>dalvik bytecode(.dex)–>optimized androidruntime machine code(.odex)

ART 的优势在于采用的是AOT 编译，应用在第一次安装的时候，字节码就会预先编译成机器码存储在本地。而在Dalvik 下，应用每次运行的时候，字节码都需要通过即时编译器(JIT)转换为机器码再执行。在app 运行的时候，ART 比Dalvik 少了解释字节码的过程，所以app 的运行效率会有所提高，反馈给我们的效果就是卡顿更少，更加流畅。不过ART 需要应用程序在安装时，就把程序代码转换成机器语言，由于有了一个转码的过程，所以应用安装时间会增加。

Dalvik 虚拟机是基于寄存器架构的，其使用的寄存器都是 32 位的。对于64 位类型，使用相邻两个寄存器来表示。而寄存器的命名方式有两种，一种是v 命名法，一种是p 命名法。根据 Dalvik 虚拟机规定，方法参数使用最后面的寄存器。因此 v 命名法和p 命名法。用一张图表示如下，其中使用了M 个寄存器，有N 个参数。<figure class="wp-block-image size-full">

<img loading="lazy" width="684" height="315" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-60.png" alt="" class="wp-image-2415" /> </figure> 

Dalvik 字节码有两种类型，基本类型和引用类型，除了对象和数组以外，其他的所有Java 类型都是基本类型。基本类型都是使用单个字母来表示。数组类型使用 [ 表示。除数组以外的引用类型使用 L 加上全限定名表示。Dalvik 类型描述符如图所示：<figure class="wp-block-image size-full">

<img loading="lazy" width="636" height="540" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-61.png" alt="" class="wp-image-2416" /> </figure> 

Dalvik 字段描述格式如下：  
`类型;->字段名称：类型描述符`  
如：com.test.Test 类中的一个 String 类型的 name 字段，在 Dalvik 中就可表示为`Lcom/test/Test;->name:Ljava/lang/String`  
Dalvik 方法描述格式如下：  
`类型;->方法名(参数类型描述符)返回值类型描述符`  
如：com.test.Test 类中的 add() 方法有两个int 类型参数，返回值为int, 在Dalvik中可表示为`Lcom/test/Test;->add(II)`

Dalvik的指令格式如下：`基础字节码 名称后缀/字节码后缀 目的寄存器 源寄存器`  
例：`move-wide/from16 vAA,vBBBB`  
move 为基础字节码，即opcode  
wide 为名称后缀，标识指令操作的数据宽度为64 位  
from16 为字节码后缀，表示源为一个16 位的寄存器引用变量名称  
vAA 为目的寄存器,它始终在源的前面，取值范围为v0~v255  
vBBBB 为源寄存器，取值范围为v0~v65535

常见的十三种Dalvik操作指令介绍如下：

1）空操作指令  
空操作指令的助记符为nop。它的值为00,通常nop 指令被用来作对齐代码之用,无实际操作。

2）数据操作指令move  
`move vA, vB` 将vB.寄存器的值赋给vA 寄存器,源寄存器与目的寄存器都为4 位  
`move/from16 vAA,vBBB` 将vBBBB 寄存器的值赋给vAA 寄存器,源寄存器为16 位,目的寄存器为8 位  
`move-wide vA,vB` 为4 位的寄存器对赋值。源寄存器与目的寄存器都为4 位  
`move-object vA,vB` object 是对象。这里是为对象赋值。源寄存器与目的寄存器都为4 位  
`move-object/froml6 vAA,vBBB` 为对象赋值。源寄存器为16 位,目的寄存器为8 位  
`move-object/16 vAA,vBBBB` 为对象赋值。源寄存器与目的寄存器都为16 位  
`move-result vAA` 将上一个invoke 类型指令操作的单字非对象结果赋给vAA 寄存器  
`move-result-wide vAA` 将上一个invoke 类型指令操作的双字非对象结果赋给vAA 寄存器  
`move-result-object vAA` 将上一个invoke 类型指令操作的对象结果赋给vAA 寄存器  
`move-exception vAA` 将发生的异常 赋给vAA 寄存器 

move 指令有三种作用：  
第一种作用:进行赋值操作  
第二种作用:move-result 按收方法返回值操作  
第三种作用:处理异常的操作

3）返回指令<figure class="wp-block-image size-full">

<img loading="lazy" width="784" height="330" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-62.png" alt="" class="wp-image-2424" /> </figure> 

4）数据定义指令<figure class="wp-block-image size-full">

<img loading="lazy" width="674" height="419" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-64.png" alt="" class="wp-image-2426" /></figure> 

5）实例操作指令<figure class="wp-block-image size-full">

<img loading="lazy" width="758" height="393" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-65.png" alt="" class="wp-image-2427" /> </figure> 

6）数组操作指令<figure class="wp-block-image size-full">

<img loading="lazy" width="722" height="158" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-67.png" alt="" class="wp-image-2429" /></figure> 

7）异常指令  
`throw vAA` 抛出vAA寄存器中指定类型的异常

8）跳转指令<figure class="wp-block-image size-full">

<img loading="lazy" width="466" height="414" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-68.png" alt="" class="wp-image-2431" /> </figure> 

9）比较指令<figure class="wp-block-image size-full">

<img loading="lazy" width="574" height="197" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-70.png" alt="" class="wp-image-2433" /></figure> 

10）字段操作指令<figure class="wp-block-image size-full">

<img loading="lazy" width="292" height="61" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-71.png" alt="" class="wp-image-2434" /> </figure> 

11）方法调用指令<figure class="wp-block-image size-full">

<img loading="lazy" width="536" height="168" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-72.png" alt="" class="wp-image-2435" /> </figure> 

12）数据转换指令<figure class="wp-block-image size-full">

<img loading="lazy" width="708" height="223" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-73.png" alt="" class="wp-image-2436" /> </figure> 

13）数据运算指令<figure class="wp-block-image size-full">

<img loading="lazy" width="488" height="100" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/image-75.png" alt="" class="wp-image-2438" /> </figure>
