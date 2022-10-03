# 端点检测与响应系统的战术溯源分析

<div class="has-toc have-toc">
</div>

## 0x00 前言

原论文是2020年IEEE Symposium on Security and Privacy (SP)的一篇文章《Tactical provenance analysis for endpoint detection and response systems》。

之所以选择这篇作为研讨厅的题目，是因为组内在做自动化渗透测试的系统，然后各个模块之间采用了ATT&CK的各种技术手段，所有的技术是不等价的，在攻击的过程中也不能盲目追求覆盖率，需要选择简单、有效、擅长的方法，这样每个模块间如何组合一个攻击高效的工具链就是一个值得研究的问题，然后我就想到能不能采用一种评分的机制，对各类威胁进行一个排列，优先采取高评分的威胁展开攻击，于是找到了这一篇论文，它创新性地提出一种威胁评分的机制，我觉得值得借鉴学习。

## 0x01 ATT&CK介绍

ATT&CK是什么呢？这里给出了官方的定义，MITRE公司的对抗战术、技术和常识( Adversarial Tactics, Techniques, and Common Knowledge;ATT&CK)是一个精心策划的网络对手行为知识库和模型，反映了对手攻击生命周期的各个阶段以及他们已知的目标平台.

简单来说，它是一个**攻击行为知识库和模型**。

核心理念与要素是**TTP（Tactics, Techniques and Procedures；战术, 技术与过程）**，当前ATT&CK是V10版本，共有14种战术。

<blockquote class="wp-block-quote">
  <p>
    1. 侦查：收集信息以计划未来对手的行动，即有关目标组织的信息
  </p>

  <p>
    2. 资源准备：建立资源以支持作战，即建立指挥和控制基础设施
  </p>

  <p>
    3. 初始访问：尝试突破边界进入网络，包含常规入侵和社会工程学入侵。
  </p>

  <p>
    4. 执行：尝试运行恶意代码，运行远程访问工具
  </p>

  <p>
    5. 持久化：通过修改系统配置和策略，试图建立长期据点。
  </p>

  <p>
    6. 权限提升：通过利用漏洞提升访问权限，试图获得更高级别的权限
  </p>

  <p>
    7. 防御规避：使用受信任的进程来隐藏恶意软件，试图规避检测
  </p>

  <p>
    8. 凭据窃取：窃取用户名和密码等凭据，例如利用键盘记录
  </p>

  <p>
    9. 内部探测：探索内部环境中所有系统，试图弄清楚所在环境
  </p>

  <p>
    10.横向移动：内网横向移动，即使用合法凭证在多个系统中移动
  </p>

  <p>
    11.数据收集：收集目标中有价值的数据，例如访问云存储中的数据
  </p>

  <p>
    12.命令和控制：与受感染的系统通信以控制它们，即模仿正常的网络流量与受害网络通信以进行远程控制
  </p>

  <p>
    13.数据渗漏：窃取数据，例如通过隐蔽隧道转移数据到云账户
  </p>

  <p>
    14.影响：操纵、中断或破坏系统和数据，即使用勒索软件加密数据
  </p>
</blockquote>

其中一个技术会被用于实现多个战术，过程则是该技术在实际攻击中的具体实现。下图中列出了执行、持久化、权限提升三种战术，每一行是战术，每一列是技术，可以看到定时任务这个技术在不同的战术中出现了三次。这里也给出了一个进程实例，比如说Lokibot是一个信息窃取程序，它在第二阶段 DLL 使用“timeSetEvent”设置了一个计时器来安排它的下一次执行。<figure class="wp-block-image size-full">

<img loading="lazy" width="1897" height="633" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片.png" alt="" class="wp-image-4796" /> </figure> 

ATT&CK的抽象层级是位于中间的，Cyber Kill Chain和STRIDE威胁模型可以划分为高层次模型，可以用来表达和理解高层次的攻击者目标和防护系统风险。这些高层模型抽象层次高，自然难以表达具体的攻击行为和攻击行为关联的具体的数据、防护措施、配置资源等。例如，我们可将某一IOC或攻击行为对应到攻击链的“C&C”阶段，这提醒防御方需要采取必要的措施了，但采取怎样的措施，攻击链模型是难以表达的。而在ATT&CK中，该IOC可能对应到战术 “Command and Control”，同时采用的是“Multi-hop Proxy”的技术手段以达成战术目标，至此，我们可以进一步获取针对该技术手段的一些通用的防护措施。当然，中层次的ATT&CK所描述的仍然是TTP的抽象，具体到实例化的行为描述，仍然需要细粒度的划分。

漏洞库及漏洞利用模型划分为低层次概念。我们可以认为CAPEC、CWE属于这个抽象层次。CAPEC（Common Attack Pattern Enumeration and Classification）关注的是攻击者对网络空间脆弱性的利用，其核心概念是攻击模式Attack Pattern。从攻击机制的角度，CAPEC通过多个抽象层次对攻击进行分类和枚举。其目标是全面的归类针对已知的应用程序脆弱性的攻击行为。相对而言，ATT&CK的目标不是对不同攻击战术目标下技术的穷尽枚举，而是通过APT等攻击组织的可观测数据提取共性的战术意图和技术模式。战术意图是CAPEC枚举库难以表达的。从攻击检测的角度来看，只有明确攻击技术的战术意图，才能进一步推测攻击的关联上下文信息，以支持攻击威胁的评估和响应。此外，通过提供攻击组织（group）和软件（software）信息，ATT&CK还能够串联起威胁情报和事件检测数据，打通对威胁事件的理解链路。<figure class="wp-block-image size-full">

<img loading="lazy" width="298" height="301" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-1.png" alt="" class="wp-image-4797" /> </figure> 

ATT&CK适用的场景很多，很多安全企业都在投入研究，而MITRE官方推荐如下：

<blockquote class="wp-block-quote">
  <p>
    对手模拟：通过获取对手的入侵情报并模拟他们的入侵行为来评估自身的安全性。ATT&CK可用于创建入侵者模拟场景来测试和验证防御。
  </p>

  <p>
    红队建设：红队的实战参考手册，ATT&CK 可用于创建红队攻击知识框架，并组织入侵行为。
  </p>

  <p>
    行为分析开发：将可疑活动特征联系在一起以监控对手的活动。ATT&CK 可用于简化并提炼可疑恶意活动行为模式。
  </p>

  <p>
    威胁情报：ATT&CK 允许防御者评估他们是否能够防御特定的高级持续威胁 (APT) 和构建威胁参与者的常见行为模型。
  </p>

  <p>
    防御差距评估：确定企业的哪些部分缺乏防御或可见性。ATT&CK 可用于评估现有工具，或在购买之前测试新工具，以确定安全范围和优先投资。
  </p>

  <p>
    安全运营成熟度评估：与防御差距评估类似，ATT&CK 可用于验证安全运营中心 (SOC) 在检测、分析和响应漏洞方面的能力成熟度。
  </p>
</blockquote>

根据全球最具权威的IT研究与顾问咨询公司Gartner的调查，前10个顶级EDR工具都利用了ATT&CK知识库来检测对手的行为。那么下面就为大家介绍下什么是EDR。

## 0x02 EDR介绍

端点检测与响应（Endpoint Detection & Response，EDR），是一种持续监控和响应以减轻网络威胁的网络技术。

端点指的是用于访问组织数据和网络的任何连接设备，比如PC、服务器、移动设备。

EDR的工作流程如图<figure class="wp-block-image size-full">

<img loading="lazy" width="417" height="373" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-4.png" alt="" class="wp-image-4828" /></figure> 

EDR 能够兼容各类网络架构。EDR 能够广泛适应传统计算机网络、云计算、边缘计算等各类网络架构，能够适用于各种类型的端点，且不受网络和数据加密的影响。

EDR 辅助管理员智能化应对安全威胁。EDR 对安全威胁的发现、隔离、修复、补救、调查、分析和取证等一系列工作均可自动化完成，大大降低了发现和处置安全威胁的复杂度，能够辅助用户更加快速、智能地应对安全威胁。

EDR 具有精准识别攻击的先天优势。端点是攻防对抗的主战场，通过 EDR 在端点上实施防御能够更加全面地搜集安全数据，精准地识别安全威胁，准确判定安全攻击是否成功，准确还原安全事件发生过程。<figure class="wp-block-image size-full">

<img loading="lazy" width="888" height="208" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-5.png" alt="" class="wp-image-4829" /> </figure> 

EDR与传统安全产品被动检测、以管代防的思路不同他是一种主动的安全方法，EDR并不依赖已知攻击特征，而是主动采集数据，通过情报碰撞、威胁模型分析等方式综合研判，发现未知威胁。

并且EDR能够主动寻找攻击痕迹进行威胁溯源，通过全量信息关联，为发现高级威胁提供更有力的数据支撑。

EDR 完整覆盖端点安全防御全生命周期。事件发生前，实时主动采集端安全数据和针对性地进行安全加固；事件发生时，通过异常行为检测、智能沙箱分析等主动发现和阻止威胁；安全事件发生后，通过端点数据追踪溯源。

## 0x03 现存EDR的挑战和解决方案

<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-6.png" alt="" class="wp-image-4830" width="368" height="343" /> </figure> 

首先，误报多，EDR工具存在大量虚假情报，容易引发警报疲劳，淹没有效信息，使得分析困难；

其次，生成上下文困难，判断警报的准确性需要大量低级日志信息，任务繁琐，上下文生成需要大量的手动工作和时间，这可能会延迟调查和恢复。

而且即使分析人员成功生成了警报的上下文，也很难通过查看系统级事件来了解整个攻击活动的进展。

最后，EDR工具通常使用FIFO队列，根据供应商的保留策略，一般仅保留几天。由于日志占用巨大资源，通常在进行调查之前就被删除。

当前学术界针对这些挑战，提出了**数据溯源**的思想。将日志解析为溯源图。这样有两个好处，一是描述系统执行的整体性，二是促进对系统活动的因果分析。<figure class="wp-block-image size-full">

<img loading="lazy" width="2078" height="915" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-7.png" alt="" class="wp-image-4831" /> </figure> 

基于这一思想，本文就实现了RapSheet系统，基于溯源的解决EDR工具现存缺陷的最佳方案。

采用TPG战术溯源图，提供多阶段攻击的紧凑可视化，加速调查。

为了解决EDR的误报问题，提出了一种基于TPGs中各个威胁警报之间的时间顺序的威胁评分方法。

最后，之前笨重的系统日志保留相比，维护了一个最低限度的骨架图，可以提供现有和未来的威胁警报之间的可连接性。

## 0x04 系统架构

<figure class="wp-block-image size-full">

<img loading="lazy" width="2202" height="719" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-8.png" alt="" class="wp-image-4832" /> </figure> 

首先，RapSheet对系统日志进行规则匹配，以确定符合ATT&CK行为的事件。接下来，我们从日志中生成一个溯源图数据库。在图的生成过程中，我们对与前一步中的ATT&CK技术相匹配的事件边进行注释。一旦完成带有警报注释的溯源图的构建，我们首先确定初始感染点 (IIP) 顶点，即时间线中生成威胁警报的第一个顶点。使用前向追踪在顶点的后代中找到所有警报，移除无关的系统事件，就会得到一个战术溯源图 (TPG)，显示因果相关警报的排序方式。最后执行威胁评分。战术溯源分析和威胁分数评估是RapSheet在威胁分析方面的最大创新点，能够提升EDR威胁检测精确度，检测未知攻击行为。

下面我会按照从左到右的顺序，详细展开每一个步骤。<figure class="wp-block-image size-full">

<img loading="lazy" width="2118" height="572" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-9.png" alt="" class="wp-image-4833" /> </figure> 

EDR工具会将各个主机上的系统日志，收集汇总。不同的操作系统有不同的收集策略，但日志的内容是统一的，包括低级别的系统事件，比如进程启动和文件操作。它们反映了不同系统实体之间的因果关系。

比如：一个父进程创建一个子进程之间的因果关系是由捕获对sys_clone()的调用而产生的事件来表示的

在windows日志方面，本文引入了对ALPC消息的收集来作为补充。ALPC是Windows 组件用于进程间通信的机制，许多攻击部分表现为使用 ALPC 消息启动的系统活动。如果缺少这些因果关系可能会断开溯源的链路，破坏取证调查。

日志收集后会进入规则匹配来发出警报。下面给出了一个简化的规则样例，可以看到如果匹配到连接的动作和3389的目的端口，就会生成一个T1076,远程桌面协议的警报。在右图中我们可以看到mstsc这个进程的连接操作时匹配到规则的，这时就会生成警报。<figure class="wp-block-image size-full">

<img loading="lazy" width="2194" height="342" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-10.png" alt="" class="wp-image-4834" /> </figure> 

之后，我们会将日志和警报传入RapSheet，生成溯源图数据库。

每个主机上的系统日志都被解析为一个称为溯源图的图结构。这里给出了一个溯源图的数据模型。

RapSheet生成的溯源图类似于之前在溯源图上的工作，其中添加了一些新的内容来推理ATT&CK策略。<figure class="wp-block-image size-full">

<img loading="lazy" width="1051" height="314" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-11.png" alt="" class="wp-image-4835" /> </figure> 

包含两种类型的顶点：进程顶点类型和对象顶点类型，其中包括文件、注册表等。

连接这些顶点的边被标记为一个事件类型，描述了它们之间的关系连接的实体和事件发生的时间戳。

此外，进程顶点标有开始和终止时间，这使我们可以在分析期间检查进程是否还活着。

我们还在溯源图数据库中实现了CPR (Causality Preserved Reduction ，因果关系保留减少)技术，合并了两个具有相同操作的顶点之间的边，并且只保留一个带有最新时间戳的边。

例如，大多数操作系统和许多 EDR 会为单个文件操作生成多个系统级事件。RapSheet 这些事件聚合到起源图中的单个边中。 可以有效减少溯源图的大小，同时仍然保持因果分析的正确性。

然后，我们进入关键环节，战术溯源分析。经过上一步我们得到一系列触发的警报和主机溯源图。在图中找到所有初始感染点（IIP），我们将 IIP 定义为满足两个条件的顶点。**对应于生成一个警报事件的过程且向后跟踪，溯源图中不包含其他警报事件。**如果IIP顶点对应的过程是多阶段攻击的第一步，那么其余的攻击将被此过程及其后代生成的未来警报捕获，我们可以对相关警报进行分组。<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-12.png" alt="" class="wp-image-4838" width="635" height="279" /> </figure> 

IIP图定义：给定一个溯源图**G <V，E>**和警报事件_e_<sub>a</sub>发生于IIP节点_V_<sub>a</sub>上，该IIP图**G’<V’，E’>**是一个以_V_<sub>a</sub>为根的图，其中**e∈E’**，如果**e**与_e_<sub>a</sub>有因果关系，并且**e**是一个警报事件或一个引发警报事件的事件。

对于每个IIP顶点通过DFS返回所有前向跟踪的路径，返回溯源路径中的所有警报事件，进行修剪，在IIP图中只保留那些至少包含一个警告的路径。<figure class="wp-block-image size-full">

<img loading="lazy" width="1406" height="366" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-16.png" alt="" class="wp-image-4842" /></figure> 

序列边定义：两个警报之间存在序列边(_e_<sub>a</sub>, _e<sub>b</sub>_)，并且满足以下任一条件: 

  * _e_<sub>a</sub>和_e<sub>b</sub>_是同一台主机和同一溯源路径上的警报，且_e_<sub>a</sub>是_e<sub>b</sub>_前向的因果关系。
  * _e_<sub>a</sub>和_e<sub>b</sub>_是同一主机上的警报，且_e_<sub>a</sub>顶点的时间戳小于_e<sub>b</sub>_ 
  * _e_<sub>a</sub> 在一台主机上有一个传出的连接事件边，且_e<sub>b</sub>_有一个回应的接收事件边。

TPG定义：TPG可以定义为一对(V,E)，其中**V是一组威胁警报事件**，而**E是顶点之间的一组序列边**。<figure class="wp-block-image size-full">

<img loading="lazy" width="1698" height="349" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-17.png" alt="" class="wp-image-4843" /> </figure> 

TPG 对分析人员可视化多阶段 APT 活动很有用，因为它可视化显示了**攻击的时间顺序**和**因果相关阶段**，而不会陷入低级系统事件。

IIP图实例和TPG图实例如下。<figure class="wp-block-image size-full">

<img loading="lazy" width="1051" height="230" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-19.png" alt="" class="wp-image-4846" /></figure> 

RapSheet 的一个关键目标是对警报进行分组并为其分配一个威胁评分，该评分可用于对这些情境化警报进行分类。

由于某些警报可疑性更大，因此我们采用了一种评分机制，其中包含单个警报的风险评分，包括两个风险评估指标：“**攻击可能性**”和“**典型严重性**”。每一个都按照非常低（1分），低（2分），中（3分），高（4分），非常高（5分）的五类等级进行评分。

最终得分为<figure class="wp-block-image size-full">

<img loading="lazy" width="497" height="31" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-20.png" alt="" class="wp-image-4847" /> </figure> 

第一个指标反映了一个特定的攻击模式成功的可能性有多大，考虑到诸如攻击的前提条件、攻击者所需的资源以及应对的防御措施的有效性等因素。

第二个指标旨在掌握成功实施攻击的后果有多严重。

我们给予严重性分数比可能性分数更高的权重，因为我们要防御的是先进的对手。他们可以有效地执行那些由于难度或成本而被认为不太可能的技术。

下面具一个例子，ATT&CK中的钓鱼技术，对应CAPEC这个常用攻击类型的分类数据集的98，找到它的指标，即可计算警报分数。然而ATT&CK和CAPEC并不是完全匹配的，文章中其他技术的指标是结合EDR厂商自定义的。<figure class="wp-block-image size-full">

<img loading="lazy" width="1412" height="551" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-21.png" alt="" class="wp-image-4849" /> </figure> 

为了将单个警报得分组合为总体得分，选择**基于TPG的评分方案**，因为基于路径的方法无法捕获攻击的整个上下文。<figure class="wp-block-image size-full">

<img loading="lazy" width="1935" height="155" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-22.png" alt="" class="wp-image-4850" /> </figure> 

我们找到这些有序警报中最长的（不一定是连续的）子序列，它与MITRE的战术杀伤链的阶段顺序一致。<figure class="wp-block-image size-full">

<img loading="lazy" width="1205" height="30" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-23.png" alt="" class="wp-image-4851" /> </figure> 

然后，我们将这个子序列中各个警报的分数相乘，给TPG一个总分。如果有多个最长的子序列，我们选择产生最高总分的那个。<figure class="wp-block-image size-full">

<img loading="lazy" width="2116" height="382" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-24.png" alt="" class="wp-image-4852" /> </figure> 

系统日志支持 EDR 工具的两个关键功能：1) 基于警报关联的威胁警报分类和 2) 使用攻击活动可视化进行事后攻击调查。因此，EDR 工具需要将这些日志保留足够长的时间以提供这些功能。然而，在大型企业中，系统日志会迅速变得庞大，使得长期保留十分困难。如何有效地使用这个有限的内存来存储是很重要的课题。

这篇文章提出了一种新技术来降低日志的保真度，同时仍然提供两个关键的 EDR 功能。提出了以下两个规则来在任何时间点修剪出处图，同时保留基于 TPG 的警报相关性。<figure class="wp-block-image size-full">

<img loading="lazy" width="1397" height="365" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-26.png" alt="" class="wp-image-4855" /> </figure> 

规则1：删除对象顶点O，如果O的后向追踪图中没有警报事件，且没有直连到O的警报事件边；

规则2：删除进程顶点P，如果①P的后向追踪图中没有警报事件，②没有直连到P警报事件边，③P被终止。

在每个可配置的时间间隔后，RapSheet 运行图缩减并仅存储骨架图，从而保留当前和未来策略之间的可链接性。

## 0x04 实验评估

<figure class="wp-block-image size-full">

<img loading="lazy" width="1532" height="749" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-30.png" alt="" class="wp-image-4860" /></figure> 

## 0x05 总结

<figure class="wp-block-image size-full">

<img loading="lazy" width="1187" height="419" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2022/01/图片-34.png" alt="" class="wp-image-4864" /></figure>
