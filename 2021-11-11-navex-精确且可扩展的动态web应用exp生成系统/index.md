# NAVEX-精确且可扩展的动态Web应用EXP生成系统

<div class="has-toc have-toc">
</div>

## 0x00 前言

最近，要开始方班研讨厅了，在选题时，决定从SDN、指纹、EXP、拟态防御这四个里面挑选，最后结合自己正在做的自动化渗透测试系统和学长提到的EXP评分，把重点放在了EXP上面，而后在调研多家厂商的标准后，发现太工程化了，很难以研讨的方式讲述，在搜索相关资料时，看到了自动生成EXP的论文，在一番比较后，选择了18年发表在USENIX上的《NAVEX: Precise and scalable exploit generation for dynamic web applications》为题，这篇论文整体真的不错，但也存在一些小问题，比如7分76秒这种迷之错误，不过**_Distinguished Paper Award Winner_**的分量还是有的，整体的架构和算法都比较好理解，这里做个简单的学习笔记。

## 0x01 研究背景

首先为大家介绍两个概念，什么是动态web应用和EXP生成系统。

动态web应用和静态web应用的区别在哪儿？

动态web应用除了可以包含静态资源（例如，图像和 HTML 文件）外，还可以包含动态资源（例如，Servlet、JSP 文件、过滤器和相关联的元数据）。静态web应用则只能包含静态资源。

现代web应用多采取动态的架构，如下图所示，红色圈出的部分是静态架构中所没有的部分，插件会对web容器进行动态请求资源，容器返回动态响应给服务器，这个过程很好地体现出动态特性，即**根据用户交互和其他输入“动态”生成内容**。<figure class="wp-block-image size-full">

<img loading="lazy" width="1555" height="697" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片.png" alt="" class="wp-image-4329" /> </figure> 

下面给大家看两个动态web应用的例子，Wordpress博客和织梦的内容管理系统。<figure class="wp-block-image size-full">

<img loading="lazy" width="558" height="316" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-2.png" alt="" class="wp-image-4333" /></figure> 

但同时动态的特性也增加了web应用程序的**复杂性**，进行人工手动的代码审计的时间成本高，且可能存在审计不完整和效率低下的问题，即漏报和误报。

现在的一些现代web应用安全性的分析方法，如代码审计神器RIPS的核心技术——模拟PHP内置特性的静态代码精确分析技术、基于代码属性图的PHP分析技术、结合启发式的静态源码分析检测EAR漏洞、Web模板语言中使用类型限定符的上下文自动过滤等等，它们都存在同一个问题：**误报高，需要人工检查核验**。

OK,讲完了动态web应用，下面就介绍下EXP。

这里给出维基百科和metasploit官方的定义。

```
EXP ，全称Exploit ，为了利用漏洞而编写的攻击程序，即漏洞利用程序。

An exploit executes a sequence of commands that target a specific vulnerability found in a system or application to provide the attacker with access to the system.
```

简单说，EXP就是利用特定的漏洞执行一串代码获取权限。下面以线上购物为例，介绍EXP实例。漏洞存在于结算页面，用户需要先登录浏览页面，再跳转到购物车页面，在结算页面对id参数实现SQL注入，一个完整的EXP需要将这3个步骤串联起来，构造整个HTTP请求的路径。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-3.png" alt="" class="wp-image-4334" width="840" height="275" /> </figure> 

EXP自动生成和手动编写步骤有所区别，这里举一种自动生成的例子，它会对源代码进行分析，找出所有潜在的漏洞，自动构造恶意HTTP请求输入序列，进行尝试，最后恶意序列将应用程序的执行指向可疑的漏洞点。<figure class="wp-block-image size-full">

<img loading="lazy" width="2225" height="911" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-4.png" alt="" class="wp-image-4335" /> </figure> 

EXP自动生成大多使用静态分析方法，以**牺牲精度**来换取覆盖率； Web应用的内容(如表单、链接、JS代码)通常是动态生成的，代码在不同的层次上执行，**很难从静态角度进行建模**。

现在，就将自动生成动态web应用EXP的挑战做一个简单的汇总，扩展性的挑战来源于Web应用越来越复杂，漏洞的种类越来越繁多，动态特征的挑战是由于静态分析的局限，比如无法推断动态将会生成怎样的表单，最后是污点可达性的挑战，所谓污点可达性就是怎样找到一个完整的HTTP请求输入序列来指向漏洞点，模块之间的复杂依赖和无害处理的风险加大了分析的难度，这里的无害处理是指比如说过滤、强制转换等能够将恶意输入无害化的操作。<figure class="wp-block-image size-full">

<img loading="lazy" width="2177" height="422" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-5.png" alt="" class="wp-image-4336" /> </figure> 

怎样应对这些挑战呢？论文中就提出来NAVEX的方案，以静态分析为指导，辅助动态分析，简称，动静结合，这个策略有3大好处，适用于大型应用，有效降低复杂性，代码覆盖率高。<figure class="wp-block-image size-full">

<img loading="lazy" width="2259" height="596" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-6.png" alt="" class="wp-image-4337" /> </figure> 

## 0x02 **核心原理**

这里是它的架构图，可以简单看作两步走，先进行漏洞点识别，再生成具体EXP。<figure class="wp-block-image size-full">

<img loading="lazy" width="2406" height="563" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-7.png" alt="" class="wp-image-4338" /> </figure> 

信息的输入端需要动态web应用的源代码和预置的攻击字典，这个字典实际上就是针对多种漏洞的分析模板，NAVEX是实现了对6种漏洞进行分析，一个完整的字典由4部分构造，这里结合XSS的实例与大家讲解，XSS漏洞通常可以利用echo、print这些函数实现，所以我们将其定义为敏感操作，第2部分是字符替换等过滤函数，第3部分是遍历类型，这个会在后续展开讲解，第4部分就是XSS的攻击语句。<figure class="wp-block-image size-full">

<img loading="lazy" width="1770" height="649" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-8.png" alt="" class="wp-image-4339" /> </figure> 

将信息输入后，NAVEX系统会进行漏洞点的识别，识别又划分了三部分，图的构造和遍历，以及公式的构造，我会按照自顶向下的顺序展开，在构造图中NAVEX所采用的模型是基于代码属性图CPG的，什么是CPG?给大家介绍下概念。<figure class="wp-block-image size-full">

<img loading="lazy" width="2297" height="975" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-9.png" alt="" class="wp-image-4340" /> </figure> 

首先，明确一个公式。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-10.png" alt="" class="wp-image-4341" width="577" height="115" /> </figure> 

它是由三种图构成的，我们以代码为例，先构造抽象语法树AST。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-11.png" alt="" class="wp-image-4343" width="276" height="241" /> </figure> 

可以看到代码中的操作数被关联为叶子节点，内部节点则代表运算符，这种图适合简单的代码分析，代码量过大时，生成的树会很复杂。<figure class="wp-block-image size-full">

<img loading="lazy" width="515" height="322" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-12.png" alt="" class="wp-image-4344" /> </figure> 

再构造控制流图CFG，可以看到图中控制语句的执行逻辑，便于我们理解整个程序的运行，但这种方式定位不了漏洞点。<figure class="wp-block-image size-full">

<img loading="lazy" width="200" height="319" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-13.png" alt="" class="wp-image-4345" /> </figure> 

最后构造程序依赖图PDG，可以看到清晰的依赖关系，比如x的定义语句对后面有x出现的语句都存在数据依赖，if判断语句和他对应的执行语句也存在着控制依赖的关系，先有因后有果。<figure class="wp-block-image size-full">

<img loading="lazy" width="333" height="223" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-14.png" alt="" class="wp-image-4346" /> </figure> 

CPG就是个缝合怪，将这三种图组合起来，融合AST的语法结构、CFG的执行路径、PDG的依赖关系的一种数据结构。<figure class="wp-block-image size-full">

<img loading="lazy" width="734" height="232" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-15.png" alt="" class="wp-image-4348" /> </figure> 

虽然CPG是一种强大的数据结构，但它只进行过程内分析，这里加入调用图CG，构造调用的函数节点到对应定义根节点的边，来实现过程间层次上的推理。最后使用过滤函数标签来解析语句的过滤状态，比如有没有强制转换，使用数据库约束标签收集表名、列名、数据类型和值约束(例如，NOT NULL)等信息 。

完成图的构造后，需要进行遍历来搜索脆弱路径，遍历依据不同的漏洞类型分为向前、向后，下面介绍漏洞的遍历算法。<figure class="wp-block-image size-full">

<img loading="lazy" width="3626" height="1518" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-16.png" alt="" class="wp-image-4349" /> </figure> 

向后的遍历算法，实际上是从可能漏洞点向后搜索到达源点的路径，先依据攻击字典查找可能的漏洞点，再对所有遍历的路径进行一个剪枝的操作，去除含有过滤函数等的路径，最终返回一组脆弱路径。正向遍历则反过来，从源点到可能漏洞点的路径搜索。

完成遍历后得到的脆弱路径，被定义为Fpath，加上构造图中的数据库约束Fdb和攻击字典中的攻击字符串Fattack，组成扩充公式，发送到求解器，构造EXP字符串。最后将漏洞点和EXP字符串用于下一部分，EXP的具体生成。<figure class="wp-block-image size-full">

<img loading="lazy" width="2480" height="930" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-17.png" alt="" class="wp-image-4350" /> </figure> 

生成具体EXP分为三部分，动态执行，构建导航图，最终生成EXP，之前的漏洞点识别是静态分析的部分，而NAVEX动静结合的创新点主要在动态的执行，下面为大家介绍通过爬虫来解决客户端约束条件。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-18.png" alt="" class="wp-image-4351" width="641" height="370" /> </figure> 

爬虫会对每个角色类型进行身份验证，比如线上购物的用户和管理员，这样能把代码覆盖率最大化，然后从种子url开始广度优先遍历，遍历过程中搜集3个对象，链接将会作为下一次的种子url，JS和表单会利用符号执行等方法提取他们的约束信息，用于构造HTTP请求。<figure class="wp-block-image size-full">

<img loading="lazy" width="2225" height="405" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-19.png" alt="" class="wp-image-4352" /> </figure> 

下面是一个例子，bookname的取值只有两种，得到F<sub>html</sub>的值是a或b的关系，JS代码中当edition小于0是将会返回false,得到的F<sub>js</sub>就必须大于0，F<sub>js</sub>和F<sub>html</sub>组成了F<sub>form</sub>，经过约束求解器会得到如下的HTTP请求。<figure class="wp-block-image size-full">

<img loading="lazy" width="2504" height="711" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-20.png" alt="" class="wp-image-4353" /> </figure> 

爬虫是解决客户端的约束，而服务端的约束又要怎样解决呢？

什么是服务端约束？大家可以看到在代码中对publisher的长度在后端进行了判断，在前端我们无法获取这个约束条件。<figure class="wp-block-image size-full">

<img loading="lazy" width="877" height="33" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-22.png" alt="" class="wp-image-4355" /> </figure> 

这里引入了跟踪引擎的概念，会不断提取服务端约束进行尝试，直达它状态改变或者执行敏感操作，我们就认为成功了，会将信息存储，作为节点。<figure class="wp-block-image size-full">

<img loading="lazy" width="1934" height="587" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-21.png" alt="" class="wp-image-4354" /> </figure> 

下面是一个同时满足客户端约束和服务端约束的例子。

<pre class="wp-block-code"><code>(bookname=="intro to CS by author1"∨bookname=="intro to Math by author2")∧
length(publisher)&lt;=35∧edition >0</code></pre>

导航图表示模块执行的可能序列，导航图是有向图_G= (N,E)_ ，节点表示HTTP请求，边表示节点之间的导航(类型是链接或表单) ，_e = (n<sub>i，</sub>n<sub>j</sub>)∈ E， n<sub>i</sub>_表示发出请求的页面。由下方表格中的4种属性构成，每个节点是一个HTTP请求，边是链接或表单，作为节点的导航连接。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-23.png" alt="" class="wp-image-4356" width="411" height="165" /> </figure> 

NAVXE的优点就是将漏洞EXP的构造问题转换为对图的简单搜索问题，以下面的导航图为例，他就将6个层层递进的http请求转换成了从index节点到漏洞点的搜索，最终组合的http加上漏洞点识别步骤中得到的EXP字符串，生成最终的EXP。<figure class="wp-block-image size-full">

<img loading="lazy" width="919" height="157" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-25.png" alt="" class="wp-image-4358" /></figure> 

## 0x03 实验结果

数据集选取标准：评估最流行应用的最新版本，并且要求是**复杂**且**大型**的PHP应用程序

数据集：26个真实PHP应用程序，代码库组合为320万多行源代码和2万多个PHP文件。

| **应用（版本）**   | **PHP****文件数量** | **PHP****源代码行数** |
| ------------------ | ------------------- | --------------------- |
| WordPress (4.7.4)  | 699                 | 181257                |
| MediaWiki (1.30.0) | 3680                | 537913                |
| Joomla (3.7.0)     | 2764                | 302701                |
| Drupal (8.3.2)     | 8626                | 585094                |
| ……                 | ……                  | ……                    |

  1. NAVEX总共生成了**204**个EXP
      * 其中195个是注入漏洞(SQLI和XSS) 
      * 9个是逻辑漏洞(EAR) 
  2. 降低了**87%**的误报
  3. 提高了**54%**的精度
  4. 能够深入到**6**个HTTP请求以拼接EXP
  5. 能够分析的漏洞类型达到**6**种
  6. 第一个可以自动发现并利用EAR漏洞的方案<figure class="wp-block-image size-full">

<img loading="lazy" width="562" height="265" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-29.png" alt="" class="wp-image-4363" width="607" height="285" /></figure> 

## 0x04 总结

<img loading="lazy"  src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-30.png" alt="" class="wp-image-4364" /> 
