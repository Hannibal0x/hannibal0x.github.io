# 业务安全学习笔记（技术篇）



## 0x00 前言

阅读《Web攻防之业务安全实战指南》一书所做的学习笔记。

## 0x01 登录认证模块测试

<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-150.png" alt="" class="wp-image-4618" width="569" height="377" /> </figure> 

**暴力破解测试**

burp利用字典穷举

**本地加密传输测试**

测试客户端与服务器交互数据在网络传输过程中是否采用SSL，加密数据能否被破解。

使用Wireshark抓包，在捕获流中找到对应的请求数据包，分析内容。

**Session会话固定测试**

攻击者可利用客户端上未清空的Session标识，并诱骗用户利用攻击者生成的固定会话进行系统登录，从而导致用户会话认证被窃取。

在注销退出系统时，使用burp截取请求数据，对当前浏览器授权SessionID值进行记录，再次登录时进行比对校验，判断是否使用相同的SessionID值进行授权认证，若是，则存固定会话风险。

**Session会话注销测试**

攻击者能利用用户注销或退出时留存的Session认证会话属性标识，将从持续有效的认证会话中盗取用户权限。

用burp对已登录授权的页面进行请求数据的截取，保存数据包中的Session认证参数值，发送至Repeater模块，退出页面后，再次发送授权访问请求并查看系统是否对退出的用户授权Session解出授权。

**Session会话超时时间测试**

对系统会话授权认证时长来进行测试，并根据系统承载的业务需求来分析判断当前Session的生命周期是否过长。

用burp对已登录授权的页面进行请求数据的截取，保存数据包中的Session认证参数值，发送至Repeater模块，在此后的固定时间内（比如30min）不再使用该授权会话与服务器进行交互访问，然后在Repeater模块发送授权访问请求并查看系统返回结果是否存在授权后可查阅的特殊信息。

**Cookie仿冒测试**

攻击者通过尝试修改Cookie中的身份标识，从而达到仿冒其他用户身份的目的，并拥有相关用户的所有权限。

使用普通账户登录系统，burp抓包修改Cookie的认证标识值（比如 userid改为“admin”），查看提交后的信息，判断身份授权是否被修改。

**密文比对认证测试**

有些网站系统的流程是在前台浏览器的客户端对密码进行Hash加密后传输到服务器并与数据库加密值进行比较，如果加密值相同，则判定用户提交密码正确。该流程会泄露密码加密方式，导致出现安全隐患。

以使用MD5加密算法为例，burp抓包查看加密后的密文，通过对页面代码的分析得出Web系统登录口令加密处理的过程是由本地JS脚本完成的，方式为MD5，添加burp配置项“Payload Processing”，点击“ADD”，选择“Hash“和“MD5”，将所有明文密码进行数据处理转换后暴力破解登录测试并成功破解。

**登录失败信息测试**

系统会在页面显示用户登录失败的信息，如提交的账号不存在，系统提示“用户名不存在”，提交的账号存在，系统提示“口令错误”等间接提示消息，攻击者可以据此判断用户账号信息，进行针对性的暴力破解。

## 0x01 业务办理模块测试

<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-151.png" alt="" class="wp-image-4624" width="370" height="281" /> </figure> 

**订单篡改测试**

当开发者没有考虑登录后用户权限隔离的问题时，就好导致平行权限绕过漏洞。

攻击者注册一个普通账户，然后篡改、遍历订单ID，获得其他用户订单中的敏感隐私信息。

**手机号码篡改测试**

在登录后的某些功能点，开发者很容易忽略登录用户的权限问题。

攻击者登录后，通过抓包等方式发现请求中有手机号参数时，可以尝试修改测试是否存在越权漏洞。

**用户ID篡改测试**

攻击者通过篡改用户ID越权访问其他用户隐私信息。

**邮箱和用户篡改测试**

在发送邮件或站内消息时，篡改其中发件人参数，导致攻击者可以伪造发信人进行钓鱼攻击等操作。

**商品编号篡改**

攻击者提交订单时，抓包篡改商品编号，导致价格不对应但却交易成功。

**竞争条件测试**

攻击者通常利用多线程并发请求，在数据库中的余额字段更新之前，多次兑换积分或购买商品，从中获利。

## 0x02 业务授权访问模块

<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-152.png" alt="" class="wp-image-4627" width="493" height="128" /> </figure> 

**非授权访问测试**

非授权访问是指在每一通过验证授权的情况下，能够直接访问需要通过认证才能访问到的页面或文本信息。

将登录后的相关页面链接复制到其他浏览器火其他电脑上进行访问，观察能否访问成功。

**水平越权测试**

正常更改或查看A账户信息，抓包或更改账户身份ID，成功查看同权限其他账户业务信息。

**垂直越权测试**

登录普通账户A，抓包或直接更改账户A的身份为高权限的账户C，查看高权限的用户信息。

## 0x03 输入/输出模块测试

<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-153.png" alt="" class="wp-image-4630" width="514" height="225" /> </figure> 

## 0x04 回退模块测试

**回退测试**

很多Web业务在密码修改后或者订单付款成功或等业务模块，在返回上一步重新修改密码或者重新付款时存在设置密码或付款的功能，如果能返回上一步重复的操作，而且还能更改或者重置结果则存在业务回退漏洞。

## 0x05 验证码机制测试

<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-154.png" alt="" class="wp-image-4634" width="492" height="312" /> </figure> 

**验证码暴力破解测试**

如果没有对验证码的失效时间和尝试失败次数做限制，攻击者就可以通过尝试这个区间内所有的数字来进行暴力破解攻击。

**验证码重复使用测试**

在网站的登录或评论等页面，如果验证码认证成功后没有讲session及时清空，将会导致验证码首次认证成功之后可重复使用，

**验证码客户端回显测试**

当验证码在客户端生成而非服务端生成是，可借助浏览器工具查看交互的详细信息。

**验证码绕过测试**

通过修改前端提交服务器返回的数据，可以实现绕过验证码。

**验证码自动识别测试**

以图形验证码为例，识别流程为：图像二值化处理--》去干扰--》字符分割--》字符识别

攻击者首先多次刷新验证码，发现验证码字符的组成范围，在PKAV HTTP Fuzzer里面设置，通过第三方识别工具自动对验证码图像进行二值化、去干扰等处理，然后通过人工对比来完善识别的准确率，达到预期效果后，抓包后的请求数据包放至PKAV HTTP Fuzzer工具请求包内，设置验证码标志位，用户名和密码标志位，开始暴力破解，自动载入验证码。

## 0x06 业务数据安全测试

<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-155.png" alt="" class="wp-image-4639" width="549" height="325" /> </figure> 

**商品支付金额篡改测试**

针对订单生成的过程中存在商品支付金额校验不完整而产生的业务风险点。

**商品订购数量篡改测试**

针对商品订购过程中对异常交易数据处理缺乏风控机制而导致的相关业务逻辑漏洞，如将请求中的商品数量修改为任意非预期数额、负数等后进行提交。

**前端JS限制绕过测试**

在限制用户购买数量时，服务器仅在页面通过JS脚本限制，未在服务器端校验用户提交的数量，通过抓取客户端发送的请求包修改JS端生成处理的交易数据。

**请求重放测试**

针对电商平台订购兑换业务流程中对每笔交易请求的唯一性判断缺乏有效机制的业务逻辑问题，攻击者进行模拟正常业务流程的重放操作，可以实现“一次购买多次收货”等违背正常业务逻辑的结果。

**业务上限测试**

针对一些电商类应用程序在进行业务办理流程中，服务端没有对用户提交的查询范围、订单数量、金额等数据进行严格校验而引发的一些业务逻辑漏，通常表现为查询到超出预计的信息、订购或兑换超出预期范围的商品等。

## 0x07 业务流程乱序测试

**业务流程绕过测试**

针对业务处理流程是否正常，确保攻击者无法通过技术手段绕过某些重要流程步骤。

以某社交网站为例，经过测试发现订单生成后流程走至链接http://www.xxx.com/index.php?contoller=site&action=payok&out\_trade\_no=，只要提供对应的充值订单号就可以绕过支付环节，未经支付直接充值成功。

## 0x08 密码找回模块测试

<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-157.png" alt="" class="wp-image-4646" width="510" height="422" /> </figure> 

**验证码客户端回显测试**

找回密码测试中注意验证码是否会回显在响应中。

**验证码暴力破解测试**

验证码位数及复杂性较弱，也没有对验证码次数限制导致可被暴力枚举并修改任意密码。

**接口参数账号修改测试**

拦截前端请求，修改邮箱或手机号等参数将修改后的数据发送到服务器进行欺骗达到密码重置的目的。

例如某个找回密码发送给用户邮件中的接口URL如下：

http://www.xxx.com/repwd?account=abcabc@126.com&token=123

将account参数修改为我们需要的账号，如：

http://www.xxx.com/repwd?account=<span class="has-inline-color has-vivid-red-color">hannibal</span>@126.com&token=123

**Response状态值修改测试**

修改请求的响应结果来达到密码重置的目的

**Session覆盖测试**

在找回密码页面输入A手机号，验证通过进入重置密码页面，打开新标签，输入目标账号B手机号，发送验证码，服务端将当前Session会话设置为了B手机号，这时再刷新A手机号，就可以重置B的密码了。

**弱Token设计缺陷测试**

在找回密码功能中，很多网站会向用户邮件发送找回密码页面链接，链接通常会加入校验参数来确认链接的有效性，通过校验参数的值与数据库生成的值是否一直来判断当前找回密码的链接是否有效。

利用密码找回功能获得多个密码找回的凭证，观察链接中的密码找回凭证是否有规律可循，比如解码后发现Token值是Base64编码（用户邮箱+随机4位验证码）。

**密码找回流程绕过测试**

例如账号使用正常顺序流程找回密码成功，3个URL如下：

（1）GET /account/findPassword.html 输入用户账号页面

（2）GET /forgetpawd/findPassNext.do 验证身份页面

（3）GET / forgetpawd /emailValidateNext.do 设置新密码页面

在输入目标账号后进入第二步的页面，直接修改URL为第三步的URL，访问是否可以直接进入密码重置页面。

## 0x09 业务接口调用模块测试

<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-158.png" alt="" class="wp-image-4655" width="531" height="333" /> </figure> 

**接口调用重放测试**

业务经过重放后是否能多次生成有效的业务或数据结果。

**接口调用遍历测试** 

Web接口一般将常见的一些功能需求进行封装，通过传入不同的参数来获取数据或执行相应的功能。

使用burp的爬虫功能，从重点关注目录（一般为根目录）开始爬取，在HTTP history选项卡中选中要开始爬取的项，单击鼠标右键，选择“Spider from here”，爬取登录后的网站链接。爬取完毕后在Target-》Site map过滤筛选出带有uid参数的链接，查看对应的HTTP请求包中是否带有期望的信息（如：ip地址、历史记录等），挑选后进行遍历测试。

**接口调用参数篡改测试**

攻击者账号为A，目标用户账号为B，在攻击者对B进行找回密码操作时，服务器给账号A的邮箱或手机发送密码重置信息，攻击者进入验证码验证环节，单击“重新发送验证码”并拦截重新发送这个请求，将请求中接收验证码用户的邮箱或者手机号修改为自己的。如果接收到密码重置的信息，则漏洞存在。

**接口未授权访问/调用测试**

登录后使用burp的爬虫功能，从重点关注目录（一般为根目录）开始爬取，在HTTP history选项卡中选中要开始爬取的项，单击鼠标右键，选择“Spider from here”，爬取登录后的网站链接。爬取完毕后在Target-》Site map使用MIME type过滤功能筛选出相关的HTTP请求（重点关注json、script、xml、text MIME type），查看对应的响应中是否带有期望的敏感信息（如：ip地址、个人电话等），将完整的请求URL复杂到未登录的浏览器中，查看能否访问对应URL的内容。 

**Callback自定义测试**

在浏览器中存在同源策略，所谓同源值的是域名、协议、端口相同。当使用Ajax异步传输数据是，非同源域名之间会存在限制。其中一种解决方法是JSONP（JSON with Padding）,基本原理是利用了HTML里<script></script>元素标签，远程调用JSON文件来实现数据传输。JSONP技术中一般使用Callback（回调函数）参数来声明回调时所使用的函数名，由于没有使用白名单的方法进行限制，导致攻击者可以自定义Callback的内容，从而触发XSS等漏洞。

攻击者使用burp的爬虫功能， 从重点关注目录（一般为根目录）开始爬取，在HTTP history选项卡中选中要开始爬取的项，单击鼠标右键，选择“Spider from here”，爬取完毕后在Target-》Site map使用MIME type过滤功能筛选出带有Callback或者jsonp参数的链接，判断请求响应的Content-Type是否为text/html，如果是，发送到Repeater，查看callback参数是否存在过滤（首先不使用script等标签等避免waf的检测），去除无关参数，最后构造恶意的payload进行利用。

**WebService测试**

WebService是一种跨编程语言和跨操作系统的远程调用技术。XML+XSD、SOAP（Simple Object Access Protocol）和WSDL（Web Service Description Language）就是构成WebService 平台的三大技术，其中 XML+XSD 用来描述、表达要传输的数据；SOAP是用于交换XML编码信息的轻量级协议，一般以XML或者XSD作为载体，通过HTTP协议发送请求和接收结果，SOAP协议会在HTTP协议的基础上增加一些特定的HTTP消息；WSDL是一个基于XML的用于描述WebService及其函数，参数和返回值的语言。

简而言之，WebService就是一个应用程序向外暴露出一个能通过Web进行调用的API。

找到服务器的WebService链接，使用WVS（Web Vulnerability Scanner）的Web Service Editor功能导入各个接口函数，通过关键词（如Get、Exec）定位到相关的接口函数，通过HTTP Editor对每一个接口函数的输入参数进行测试（如SQL注入、文件上传等），如果出现预期效果，则存在漏洞。
