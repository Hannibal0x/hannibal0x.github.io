# 私密：个人学习笔记

<div class="has-toc have-toc">
</div>
## 0x00 攻击目标选择

<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-211.png" alt="" class="wp-image-4723" width="587" height="435" /> </figure> 

人

  * 个人基础信息
  * 员工通讯录
  * 社交账号：邮箱、手机、账号
  * 社交关系
  * 互联网泄露信息
  * 角色关系：客户、员工、供应商、合作方

信息资产

  * 域名/IP
  * 内外网拓扑结构
  * 端口
  * 使用软件
  * 使用网络设备
  * 关键系统：邮箱、OA、VPN、域控
  * 关联合作方资产

## 0x01 **如何寻找突破口？**

■工作人员的<span class="has-inline-color has-vivid-red-color">安全意识薄弱</span>永远是最致命的  
•弱口令、撞库、泄露账号、钓鱼、物理入侵

■已知漏洞未必无效，内网已成重灾区  
•积累漏洞利用库

■以小见大，稳步推进，主站无洞可从旁站入手  
• XSS、CSRF、SQLI、越权-＞获取管理员账号-＞上传、备份->后台getshell

■切勿急躁，发现源码-＞ 审计漏洞  
•文件扫描、GitHub

■未公开0day漏洞是超级武器，考虑得失比

## 0x02 **钓鱼攻击**

■ 口令钓鱼  
导引用户到URL与界面外观与真正网站几无二致的假冒网站输入个人数据。期算使用强式加密的SSL服务器认证，要侦测网站是否仿冒实际上仍很困难。（域名仿冒、中奖邮件）

■ 鱼叉式网络钓鱼  
私人化定制，伪装成目标的同事或亲友等身份，诱导目标点击链接或下载附件（word, vpn） 。或伪装成领导，要求员工进行XX操作。

■ 偷渡式下载(Drive-by download)  
授权但不了解后果的下载（例如，安装未知或伪造的可执行程序，ActiveX组件或Java applet）不知情的情况下进行的任何下载，通常是计算机病毒，间谍软件，恶意软件或犯罪软件。

■ 热点钓鱼（WIFI钓鱼）  
切断目标的网络，设置一个假的公开WIFI，目标一旦连入网络，所有数据和操作都会被掌控。

■ 搜索引擎钓鱼  
付费广告（购买近似域名、提升权重）。

■ 桌面钓鱼  
修改hosts并制作成自解压文件，捆绑其他软件，通过任意途径诱导用户安装。

■ 社会工程学  
伪造猎头身份，诱导目标员工下载word木马。根据个人信息，生成字典。

■ DNS欺骗  
破坏DNS记录，将目标网站的访客引至事先布好的欺诈网站（入侵路由器）。

■ 水坑攻击  
得知目标经常访问的网站后，攻击该网站，放置登录控件马。

■ 物理攻击  
水、电、网、空调维修人员冒充；假冒面试者，提供U盘进行打印。

## 0x03 后门隐藏

■ webshell的隐藏  
• 回调后门、代码混淆和加密、不死马、无文件webshell

■ 计划任务、启动项、注册表

■ 增加UID为0/权限为Administrator的账户

■ ssh key

■ alias后门——.bashrc /etc/profile alias命令进行重写操作

■ suid后门——<a rel="noreferrer noopener" href="https://zhuanlan.zhihu.com/p/97685460" target="_blank" rel="nofollow" >https://zhuanlan.zhihu.com/p/97685460</a>、<a href="http://wyb0.com/posts/2016/linux-suid-back-door/" target="_blank" rel="noreferrer noopener" rel="nofollow" >http://wyb0.com/posts/2016/linux-suid-back-door/</a>

■ ssh：软链接后门、ssh server wrapper

■ pam后门

■ mafix后门

■ Kbeast_rootkit后门

## 0x04 内网渗透-选择攻击目标

■ 优先攻击高权限账号，如管理员，目标系统负责人账号；

■ 优先攻击运维/安全人员账号和终端，这些人往往有服务器root账号，安全设备管理员账号，可以进一步深入控制；

■ 优先攻击集中管控设施，如域控，集中身份认证系统，终端管理系统，攻陷单系统即获得公司内大部分系统的权限；

■ 优先攻击基础设施，如DNS, DHCP,邮件系统，知识分享平台，oa系统，工单系统；这些系统有内置高权限账号，或可以帮助攻击者隐蔽痕迹。或Git/SVN等开发源代码管理服务器，通过代码审计发现应用0day漏洞。

**定制化恶意软件**

  * 远控功能
  * 敏感信息收集功能
  * 漏洞利用能力
  * 蠕虫特性
  * 目标业务实现
  * 免杀与流量加密

## 0x05 信息收集工具

■ 公司信息收集：<a rel="noreferrer noopener" href="https://www.tianyancha.com" data-type="URL" data-id="https://www.tianyancha.com" target="_blank" rel="nofollow" >天眼查</a>、<a rel="noreferrer noopener" href="https://aiqicha.baidu.com/" data-type="URL" data-id="https://aiqicha.baidu.com/" target="_blank" rel="nofollow" >爱企查</a>、GitHub、各大搜索引擎

■ 个人信息收集：Telegram、 QQ、微信、钉钉、支付宝、脉脉、Linkedin、贴吧

■ 端口扫描工具：NMap、ZMap、masscan、GGscan

■ 目录扫描工具：dirb、dirsearch、御剑、SourceLeakHacker、wwwscan、 weakfilescan

■ whois /备案查询：<a rel="noreferrer noopener" href="https://whois.chinaz.com/" data-type="URL" data-id="https://whois.chinaz.com/" target="_blank" rel="nofollow" >站长之家</a>、<a rel="noreferrer noopener" href="https://whois.aliyun.com/" data-type="URL" data-id="https://whois.aliyun.com/" target="_blank" rel="nofollow" >阿里云</a>、<a rel="noreferrer noopener" href="https://www.virustotal.com" data-type="URL" data-id="https://www.virustotal.com" target="_blank" rel="nofollow" >VirusTotal</a>、<a rel="noreferrer noopener" href="https://securitytrails.com/" data-type="URL" data-id="https://securitytrails.com/" target="_blank" rel="nofollow" >SecurityTrails</a>、<a rel="noreferrer noopener" href="http://icp.chinaz.com/" data-type="URL" data-id="http://icp.chinaz.com/" target="_blank" rel="nofollow" >备案查询</a>

■ 历史域名解析记录：<a rel="noreferrer noopener" href="https://viewdns.info/" data-type="URL" data-id="https://viewdns.info/" target="_blank" rel="nofollow" >ViewDNSInfo</a>、<a rel="noreferrer noopener" href="https://www.domaintools.com/" data-type="URL" data-id="https://www.domaintools.com/" target="_blank" rel="nofollow" >DomailTools</a>、<a rel="noreferrer noopener" href="https://dnsdumpster.com/" data-type="URL" data-id="https://dnsdumpster.com/" target="_blank" rel="nofollow" >dnsdumpster</a>、<a rel="noreferrer noopener" href="https://whoisrequest.com/" data-type="URL" data-id="https://whoisrequest.com/" target="_blank" rel="nofollow" >WhoISRequest</a>

■ C段收集工具：<a rel="noreferrer noopener" href="https://cn.bing.com/" data-type="URL" data-id="https://cn.bing.com/" target="_blank" rel="nofollow" >必应</a>

■ 子域名收集工具：Layer子域名挖掘机、subDomainsBrute、OneForAll、Sublist3r、<a rel="noreferrer noopener" href="https://dnsdumpster.com/" data-type="URL" data-id="https://dnsdumpster.com/" target="_blank" rel="nofollow" >DNSDumper</a>、IP反查域名、  
谷歌语法:site:baidu.com

■ 指纹识别：<a rel="noreferrer noopener" href="https://www.yunsee.cn" data-type="URL" data-id="https://www.yunsee.cn" target="_blank" rel="nofollow" >云悉</a>、<a rel="noreferrer noopener" href="https://fp.shuziguanxing.com/#/" data-type="URL" data-id="https://fp.shuziguanxing.com/#/" target="_blank" rel="nofollow" >Finger-P</a>、<a rel="noreferrer noopener" href="http://finger.tidesec.com/" data-type="URL" data-id="http://finger.tidesec.com/" target="_blank" rel="nofollow" >TiderFinger</a>、<a rel="noreferrer noopener" href="https://www.whatweb.net/" data-type="URL" data-id="https://www.whatweb.net/" target="_blank" rel="nofollow" >whatweb</a>

■ 多地ping工具(CDN )：<a rel="noreferrer noopener" href="http://ping.chinaz.com/" data-type="URL" data-id="http://ping.chinaz.com/" target="_blank" rel="nofollow" >站长之家</a>、<a rel="noreferrer noopener" href="https://ping.aizhan.com/" data-type="URL" data-id="https://ping.aizhan.com/" target="_blank" rel="nofollow" >爱站网</a>、<a rel="noreferrer noopener" href="http://itools.com/tool/just-ping" data-type="URL" data-id="http://itools.com/tool/just-ping" target="_blank" rel="nofollow" >just-ping</a>

## 0x06 绕过CDN查找真实IP

探测是否开启CDN （多地ping工具）

方法一：杳找二级域名（一般二级域名不会放CDN ）

方法二：nslookup法（大部分CDN只针对国内市场），nslookup http://xxx.cn 国外dns

方法三：ping法，ping http://xxx.com （有些CDN厂商基本只把 www.xxx.com cname到cdn主服务器上去www.xxx.co和http://xxx.com是两条独立的解析记录，一般只会把www.xxx.com 做 CDN ）

方法四：杳找历史域名解析记录（使用CDN前是真实IP ）

方法五：内部邮箱源（必须是目标自己的mailserver）

方法六：网站测试文件，phpinfo等

方法七：APP （抓包）

## 0x07 EXP、POC库，漏洞扫描框架

■ <a rel="noreferrer noopener" href="https://www.exploit-db.com/" data-type="URL" data-id="https://www.exploit-db.com/" target="_blank" rel="nofollow" >exploit-db</a>、<a rel="noreferrer noopener" href="http://wooyun.2xss.cc/" data-type="URL" data-id="http://wooyun.2xss.cc/" target="_blank" rel="nofollow" >乌云镜像库</a>、<a rel="noreferrer noopener" href="https://vulhub.org/" data-type="URL" data-id="https://vulhub.org/" target="_blank" rel="nofollow" >vulhub</a>

■ CMS-Hunter、onlinetools、Some-PoC-oR-ExP、exphub

■ struts-scan、wpscan、kunpeng、AWVS、appscan、nessus、xray

## 0x08 漏洞利用工具

■SQLMap、BrupSuite、NoSQLMap

■webshell : webshell、webshell-sample、WebShell、php-webshells

■webshell管理工具：菜刀（部分版本存在后门）、蚁剑（部分版本存在RCE漏洞 : 1、2）、冰蝎

■内网渗透神器：Metasploit-Framework、Cobalt Strike （可克隆网站、制作word宏病毒、发送邮件）

■ Proxy：ReGeorg、Earthworm、Termite、ProxyChains-ng、Proxifier、Venom、openvpn

■ 提权：windows-kernel-exploits、linux-kernel-exploits、LinEnum

■ 端口转发：Windows、 Linux

■ 手机短信接收平台：xx云短信、<a rel="noreferrer noopener" href="http://www.z-sms.com/" data-type="URL" data-id="http://www.z-sms.com/" target="_blank" rel="nofollow" >z-sms</a>、receive-sms-online

■ 在线临时匿名邮箱：<a href="https://yopmail.com/" data-type="URL" data-id="https://yopmail.com/" target="_blank" rel="noreferrer noopener" rel="nofollow" >yopmail</a>

■ 在线邮件伪造：<a href="https://emkei.cz/" data-type="URL" data-id="https://emkei.cz/" target="_blank" rel="noreferrer noopener" rel="nofollow" >EMKEI</a>、<a href="https://ihuan.me/mail" data-type="URL" data-id="https://ihuan.me/mail" target="_blank" rel="noreferrer noopener" rel="nofollow" >小幻邮箱系统</a>

■ 在线短链生成：<a href="http://tool.chinaz.com/tools/dwz.aspx?qq-pf-to=pcqq.group" data-type="URL" data-id="http://tool.chinaz.com/tools/dwz.aspx?qq-pf-to=pcqq.group" target="_blank" rel="noreferrer noopener" rel="nofollow" >站长之家</a>、短网址工具

■ 在线md5解密：<a href="https://www.cmd5.com/" data-type="URL" data-id="https://www.cmd5.com/" target="_blank" rel="noreferrer noopener" rel="nofollow" >cmd5</a>、<a href="https://www.zuwuwang.com/" data-type="URL" data-id="https://www.zuwuwang.com/" target="_blank" rel="noreferrer noopener" rel="nofollow" >zuwuwang</a>、<a rel="noreferrer noopener" href="https://www.somd5.com/" data-type="URL" data-id="https://www.somd5.com/" target="_blank" rel="nofollow" >somd5</a>、<a rel="noreferrer noopener" href="https://pmd5.com/" data-type="URL" data-id="https://pmd5.com/" target="_blank" rel="nofollow" >pmd5</a>、<a rel="noreferrer noopener" href="https://www.chamd5.org/" data-type="URL" data-id="https://www.chamd5.org/" target="_blank" rel="nofollow" >chamd5</a>、<a rel="noreferrer noopener" href="http://www.xmd5.org/" data-type="URL" data-id="http://www.xmd5.org/" target="_blank" rel="nofollow" >xmd5</a>、<a rel="noreferrer noopener" href="http://www.ttmd5.com/" data-type="URL" data-id="http://www.ttmd5.com/" target="_blank" rel="nofollow" >ttmd5</a>

## 0x09 数据安全：企业敏感信息泄露

**常见泄露源**

  * 网盘微盘（百度网盘）
  * 代码托管平台（github）
  * 文库平台
  * 微博、论坛等社交网站

**防范措施**

  * 禁止在互联网上发布公司内部信息

**常见泄露内容**

  * 企业组织架构
  * 员工通讯录
  * 供应商或合作方
  * 源码文件
  * 账号密码
  * 技术方案
  * 招投标文件
  * 项目合同
  * 网络拓扑
  * 内部系统手册

## 0x0A 弱口令

**什么是弱口令？**

  * 字符种类（数字、大小写、符号）不够、长度不够
  * 系统/设备默认（出厂）口令
  * 使用和个人或公司有关信息，例如生日、年份、公司名称：19800304、CHAITIN
  * 包含键盘上的连续按键：qwert、lqaz@wsz、! @#
  * 包含特殊含义字符串：520 、1314 、iloveyou
  * 其他常用字符串：root、abcl23 ! 、@123

使用一台双核PC+暴力破解软件进行本地破解需花费的时间

| 口令强度              | 6位长   | 8位长   |
| --------------------- | ------- | ------- |
| 纯粹由数字构成        | <1s     | 10s     |
| 小写或大写字母组成    | 30s     | 348mins |
| 大小写字母混合组成    | 33mins  | 62days  |
| 数字+ 大小写字母组成  | 90mins  | 253days |
| 数字+ 大小写+符号组成 | 22hours | 23years |

## 0x0B 常见端口和服务以及攻击手法（部分）

<figure class="wp-block-image size-full">

<img loading="lazy" width="843" height="962" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/11/图片-200.png" alt="" class="wp-image-4712" /> </figure> 

## 0x0C 设备部署

<figure class="wp-block-image size-full is-resized">

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/12/图片-1.png" alt="" class="wp-image-4730" /></figure> 

## 0x0D 社

<a href="https://www.iculture.cc/sg/pig=1034" target="_blank"  rel="nofollow" >https://www.iculture.cc/sg/pig=1034</a>

## 0x0E 加固

安全加固的三个方面：用户 文件 登录

`etc/login.defs`定义了`/etc/passwd`和`/etc/shadow`配套的用户限制，必须存在，没有时，某些时候并不会影响使用，但有些时候会产生意想不到的情况。

如果`/etc/passwd`和`/etc/shadow`与`/etc/login.`defs产生冲突，会以优先级更高的`/etc/passwd`和`/etc/shadow`为主。

使用命令`grep -Ev "^#|^$" /etc/login.defs`，查看文件内容

<pre class="wp-block-code"><code>MAIL_DIR        /var/mail 
PASS_MAX_DAYS	99999 #密码最大有效期 以天为单位 一般365天
PASS_MIN_DAYS	0 #两次修改密码最小间隔 以天为单位 
PASS_MIN_LEN    5 #密码最小长度 5 对root无效
PASS_WARN_AGE	7 #密码过期前n天开始提示
UID_MIN			 1000 #创建普通用户的时 如果不指定UID 就会从1000递增 centos6从500开始
UID_MAX			60000 #创建普通用户的最大ID 65534
SYS_UID_MIN			 201 #不指定UID时 创建系统的最小UID
SYS_UID_MAX			999 #不指定UID时 创建系统的最大UID
GID_MIN			 1000
GID_MAX			60000
SYS_GID_MIN			 201 
SYS_GID_MAX			999
CREATE_HOME yes #创建用户时 创建相应的家目录
UMASK		077 #用户的家目录的权限值 700
USERGROUPS_ENAB yes #删除用户时 如果用户组内没有其他用户时 是否删除用户组 
ENCRYPT_METHOD SHA512 #用户密码使用SHA512加密</code></pre>

修改后（通用型）

<pre class="wp-block-code"><code>PASS_MAX_DAYS	90 
PASS_MIN_LEN    12 </code></pre>

/etc/passwd的内容

<pre class="wp-block-code"><code>root : x : 0 : 0 : root : /root : /bin/bash
bin : x : 1 : 1 : bin : /bin : /sbin/nologin
用户名 : 用户密码 : 用户的UID : 用户的GID : 用户的注释 : 用户的主目录 : 用户的shell</code></pre>

由于/etc/passwd允许所有用户读取，容易导致用户的密码泄露，所以linux系统将用户相关的密码信息分离到/etc/shadow，只用root用户有读的权限。
