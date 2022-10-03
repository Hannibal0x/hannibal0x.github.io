# 业务安全学习笔记（实践篇）

## 0x00 账号安全案例总结

<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-161.png" alt="" class="wp-image-4665" width="532" height="291" /> </figure> 

**账号密码直接暴露在互联网上**

搜索语法

<pre class="wp-block-code"><code>邮件配置信息查询 site:Github.com smtp password;
数据库信息泄露 site:Github.com sa password;
svn信息泄露 site:Github.com svn;
数据库备份文件 site:Github.com inurl:sql</code></pre>

开源项目存在可解密信息，如base64加密的cookie。

**无限制登录任意账号**

攻击者可以利用漏洞绕过登录限制，或者利用已经认证的用户，通过修改身份ID登录任意账号。

**电子邮件账号泄露事件**

公开文件中包含邮件账号密码的敏感信息。

**中间人攻击**

SSL证书欺骗攻击，通过DNS劫持和局域网ARP欺骗甚至网关劫持等技术，将用户的访问重定向到攻击者的设备上，让用户机器与攻击者机器建立HTTPS连接（使用伪造的CA证书），而攻击者机器再跟Web服务端连接。

SSL劫持，是指将页面中的HTTPS超链接全部替换成HTTP版本，让用户始终以明文的形式进行通信。

**撞库攻击**

撞库是黑客公告收集互联网已泄露的用户和密码信息，生成对应的字典表，尝试批量登录其他网站后，得到一系列可以登录的用户名和密码组合。

## 0x01 密码找回安全案例总结

<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-162.png" alt="" class="wp-image-4667" width="632" height="582" /> </figure> 

**密码找回凭证可被暴力破解**

**密码找回凭证直接返回客户端**

有些信息系统在密码找回功能的设计上存在漏洞，可能会将用于用户自证明身份的信息的密码找回凭证以各种各样的方式返回到客户端。 

**密码重置链接存在弱Token**

有些信息系统的密码找回功能会在服务端生成一个随机Token并发送到用户邮箱作为密码找回凭证。但一旦这个Token的生成方式被破解，攻击者就可以伪造该Token作为凭证重置其他用户密码。

**密码重置凭证与用户账号关联不严**

有些信息系统在密码找回功能的校验逻辑上存在缺陷，只校验了密码重置凭证是否在数据库中存在，但未严格校验该重置凭证和用户账号之间的绑定关系。

**重新绑定用户手机或邮箱**

有些信息系统在绑定用户手机或者邮箱的功能上存在越权访问漏洞。攻击者可以利用该漏洞越权绑定其他用户的手机或者邮箱后，再通过正常的密码找回途径重置他人的密码。

**服务端验证逻辑缺陷**

有些信息系统的服务端验证逻辑上存在漏洞，攻击者可以通过删除数据包中的某些参数、修改邮件发送地址或者跳过选择找回方式和身份验证的步骤，直接进入重置密码页面成功重置其他人的密码。

**修改返回包绕过验证**

有些信息系统在密码找回功能的设计上存在缺陷，攻击者只要抓取服务端的返回包并修改其中的部分参数即可跳过验证步骤，直接进入密码重置页面。

**注册覆盖**

**Session覆盖**

## 0x02 越权访问安全案例

<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-163.png" alt="" class="wp-image-4668" width="644" height="278" /> </figure>
