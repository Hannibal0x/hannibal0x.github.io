# 物联网协议CoAP学习（理论篇）

<div class="has-toc have-toc">
</div>

## 0x00 前言

最近在想毕业设计的选题，和老师讨论后，觉得可以在原来基于SDN架构的企业局域网流量监控和访问控制系统的基础之上再改进，老师提到《基于SDN的IoT设备细粒度访问控制研究与实现》的论文可以用来参考，来达到对请求动作的权限访问控制，经过一通学习，发现整个过程是通过物联网协议CoAP来判断的，遂开始了对CoAP的学习。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="896" height="219" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-192.png" alt="" class="wp-image-1344" /></figure>
</div>

## 0x01 啥叫CoAP?

CoAP（Constrained Application Protocol）是一种在物联网世界的类web协议，它的详细规范定义在 <a rel="noreferrer noopener" href="https://tools.ietf.org/html/rfc7252" data-type="URL" data-id="https://tools.ietf.org/html/rfc7252" target="_blank" rel="nofollow" >RFC 7252</a>。COAP名字翻译来就是“受限应用协议”，顾名思义，使用在资源受限的物联网设备上。物联网设备的ram，rom都通常非常小，运行TCP和HTTP是不可以接受的。CoAP是一个完整的二进制应用层协议，消息格式紧凑，默认运行在UDP上。

CoAP定义了4种消息类型：Confirmable, Non-confirmable, Acknowledgement, Reset，其中一些信息中包含的方式代码和响应码使得它们携带了请求和响应。我们可以把CoAP在逻辑上视作两层，CoAP的消息层用于处理UDP和异步性质的交互，请求和响应的交互则通过方式代码和响应码实现。然而，CoAP是一个单一协议，仅在CoAP头具有消息传递和请求/响应功能。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-193.png" alt="" class="wp-image-1353" width="350" height="233" /></figure>
</div>

## 0x02 CoAP协议消息类型

上文提到CoAP协议有4种消息类型，下面就进一步学习。

CON—— 需要被确认的请求，如果CON请求被发送，那么对方必须做出响应。这有点像TCP，对方必须给确认收到消息，用以可靠消息传输。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-194.png" alt="" class="wp-image-1360" width="325" height="158" /></figure>
</div>

NON—— 不需要被确认的请求，如果NON请求被发送，那么对方不必做出回应。这适用于消息会重复频繁的发送，丢包不影响正常操作。这个和UDP很像。用以不可靠消息传输。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-195.png" alt="" class="wp-image-1363" width="308" height="105" /></figure>
</div>

ACK —— 应答消息，对应的是CON消息的应答。

RST —— 复位消息，可靠传输时候接收的消息不认识或错误时，不能回ACK消息，必须回RST消息。

## 0x03 CoAP消息格式

CoAP基于压缩消息的交换，默认情况下通过UDP协议传输。 (例如每个 CoAP消息占用了一个UDP的数据包的数据段) 。CoAP消息以简单的二进制格式编码，以 4字节的固定大小作为首部，后面是一个可变长度的令牌值，长度可以在0到8字节之间。令牌值之后是一系列类型长度值（TLV）格式的零个或多个CoAP选项，可选地携带占用其余数据报的有效负载。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="671" height="258" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/02/图片-196.png" alt="" class="wp-image-1372" /></figure>
</div>

  * 消息头（HEAD）
      * Ver : 2bit， 版本信息，当前是必须写0x01。
      * T： 2bit， 消息类型，包括 CON, NON. ACK, RST这4种。
      * TKL: 4bit，token长度， 当前支持0~8B长度，其他长度保留将来扩展用。CoAP协议中具有两种功能相似的标识符，一种为Message ID(报文编号)，一种为Token(标识符)。其中每个报文均包含消息编号，但是标识符对于报文来说是非必须的。
      * Code：8bit，分成前3bit（0~7）和后5bit（0~31），前3bit代表类型。 0代表空消息或者请求码， 2开头代表响应码，取值如下：
          1. 0.00 Indicates an Empty message
          2. 0.01-0.31 Indicates a request.
          3. 1.00-1.31 Reserved
          4. 2.00-5.31 Indicates a response.
          5. 6.00-7.31 Reserved
      * Message ID：16bit， 代表消息MID，每个消息都有一个ID ，重发的消息MID不变
      * token（可选）标识符具体内容，通过TKL指定Token长度。 token值为0到8字节的序列。 ( 每条消息必须带有一个标记, 即使它的长度为零）。 每个请求都带有一个客户端生成的token, 服务器在任何结果响应中都必须对其进行回应。token类似消息ID，用以标记消息的唯一性。token还是消息安全性的一个设置，使用全8字节的随机数，使伪造的报文无法获得验证通过。
      * option（可选，0个或者多个）主要用于描述请求或者响应对应的各个属性，类似参数或者特征描述，比如是否用到代理服务器，目的主机的端口等。
      * payload（可选）实际携带数据内容， 若有， 前面加payload标识符“0xFF”，如果没有payload标识符，那么就代表这是一个0长度的payload。如果存在payload标识符但其后跟随的是0长度的payload，那么必须当作消息格式错误处理。

## 0x04 CoAP的请求码和响应码

  * 请求方法
      * 【0.01】GET方法——用于获得某资源
      * 【0.02】POST方法——用于创建某资源
      * 【0.03】PUT方法——用于更新某资源
      * 【0.04】DELETE方法——用于删除某资源
  * 响应码
  * Success 2.xx，这一类型的状态码，代表请求已成功被服务器接收、理解、并接受。
      * 2.01 Created
      * 2.02 Deleted
      * 2.03 Valid
      * 2.04 Changed
      * 2.05 Content
  * Client Error 4.xx，这类的状态码代表了客户端看起来可能发生了错误，妨碍了服务器的处理。
      * 4.00 Bad Request
      * 4.01 Unauthorized
      * 4.02 Bad Option
      * 4.03 Forbidden
      * 4.04 Not Found
      * 4.05 Method Not Allowed
      * 4.06 Not Acceptable
      * 4.12 Precondition Failed
      * 4.13 Request Entity Too Large
      * 4.15 Unsupported Content-Format
  * Server Error 5.xx，这类状态码代表了服务器在处理请求的过程中有错误或者异常状态发生，也有可能是服务器的软硬件资源无法完成对请求的处理。
      * 5.00 Internal Server Error
      * 5.01 Not Implemented
      * 5.02 Bad Gateway
      * 5.03 Service Unavailable

## 0x05 参考文章

  * <a href="https://tools.ietf.org/html/rfc7252" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://tools.ietf.org/html/rfc7252</a>
  * <a rel="noreferrer noopener" href="https://www.jianshu.com/p/7fec0916a0d3" target="_blank" rel="nofollow" >https://www.jianshu.com/p/7fec0916a0d3</a>
  * <a rel="noreferrer noopener" href="https://baijiahao.baidu.com/s?id=1609055547851599818&wfr=spider&for=pc" target="_blank" rel="nofollow" >https://baijiahao.baidu.com/s?id=1609055547851599818&wfr=spider&for=pc</a>
