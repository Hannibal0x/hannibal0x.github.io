# 灰帽黑客（第五版）学习笔记–下一代模糊测试

<div class="has-toc have-toc">
</div>

## 0x00 前言

前两章内容比较浅显，都是些简单的概念，第三章开始知识点变得丰富，这里结合书本、代码以及其他资料，整理记录自己的笔记。

## 0x01 FUZZ

Fuzz（模糊测试）是一种通过提供非预期的输入并监视异常结果来发现软件安全漏洞的方法。

根据数据生成算法的不同，分类如下：

  * 数据变异，根据已知数据样本通过变异的方法生成新的测试用例。
  * 数据生成，根据已知协议或接口规范进行建模生成新的测试用例。
  * 遗传或进化，使用来自每个测试用例的反馈，以了解随着时间推移输入的格式。例如，通过测量每个测试用例的代码覆盖率，计算出测试用例的哪些属性可以锻炼给定的代码区域，并逐渐演化出一套覆盖大部分程序代码的测试用例。

## 0x02 Peach基本知识

Peach是一个优秀的开源Fuzz框架。

Fuzz流程图

<div class="wp-block-image">
  <figure class="aligncenter"><img src="http://blog.nsfocus.net/wp-content/uploads/2015/07/image002.png" alt="image002" class="wp-image-730" /></figure>
</div>


开始Fuzz需要创建一个名为Pit的文件，Pit文件是包含模糊测试会话全部配置信息的XML文档。包含的典型信息如下：

  * 通用配置--定义与Fuzz参数无关的配置，如python路径
  * DataModel--定义了将通过Peach规范化语言的模糊化数据结构
  * StateModel--定义了用来正确表示协议的状态机
  * Agent和Monitor--定义Peach分配Fuzz工作量以及检测目标软件故障/漏洞迹象的方式
  * Test配置--定义Peach创建每一个测试用例的方式以及运用何种模糊测试策略来修改数据

<div class="wp-block-image">
  <figure class="aligncenter"><img src="http://blog.nsfocus.net/wp-content/uploads/2015/07/image003.png" alt="image003" class="wp-image-731" /></figure>
</div>


具体详见：

<a href="http://blog.nsfocus.net/peach-fuzz/" target="_blank" rel="noreferrer noopener" rel="nofollow" >http://blog.nsfocus.net/peach-fuzz/</a>

<a href="https://www.secpulse.com/archives/119442.html" target="_blank"  rel="nofollow" >https://www.secpulse.com/archives/119442.html</a>

<a href="https://github.com/MozillaSecurity/peach" target="_blank"  rel="nofollow" >https://github.com/MozillaSecurity/peach</a>

## 0x03 崩溃追踪

常见方式：

  * 可用来重现崩溃的样本文件或数据记录。发现崩溃时，对于文件Fuzzer，用于测试的样本文件会被保存并做好标记以供审查。对于网络应用Fuzzer，可能记录并保存PCAP文件。
  * 应用程序的崩溃日志文件可通过多种方式收集。发现崩溃时，调试器会收集CPU上下文信息（例如寄存器的状态和栈内存），并同崩溃样本文件一起储存。
  * 许多自定义脚本可在程序崩溃时运行，从而收集特定类型的信息。实现这类脚本最简单的方法就是扩展调试器。

处理崩溃时，Peach使用WinDbg和!exploitable扩展收集崩溃相关的上下文信息并将崩溃归类。

崩溃日志主要由两部分组成：

  * 调试器收集的崩溃信息，包括加载模块名称、CPU寄存器信息和内存片段。
  * !exploitable报告包含崩溃及其疯了信息。这部分日志提供更多崩溃上下文信息，如异常码、栈帧信息和分类等，分类是对崩溃可利用性潜力的评估结论，包括：Exploitable、Probably Exploitable、Probably Not Exploitable、Unknown。

## 0x04 AFL

AFL将Fuzz提升到一个新水平，使用遗传算法达到最佳的代码覆盖范围。

工作流程如下：<figure class="wp-block-image">

![1.jpg][1] </figure> 

参考资料：

<a href="https://www.freebuf.com/articles/system/191543.html" target="_blank"  rel="nofollow" >https://www.freebuf.com/articles/system/191543.html</a>

<a href="https://bbs.pediy.com/thread-249912.htm" target="_blank"  rel="nofollow" >https://bbs.pediy.com/thread-249912.htm</a>

[1]: https://image.3001.net/images/20181207/1544168163_5c0a22e3eedce.jpg!small
