# 【i春秋】渗透测试入门 —— 真的很简单

<div class="has-toc have-toc">
</div>

## 0x00 前言

  * 题目链接：<a rel="noreferrer noopener" href="https://www.ichunqiu.com/battalion?t=2&r=54399" target="_blank" rel="nofollow" >https://www.ichunqiu.com/battalion?t=2&r=54399</a>
  * 实验环境
      * 操作机：`Windows XP`
  * 实验工具：
      * `net.exe`
      * `dedeCMS`
      * `中国菜刀`
  * 实验任务：
      * 本次实验要求获取www.test.ichunqiu网站的FLAG信息。
  * 实验试题:
      * 第1题：网站管理员密码是多少？
      * 第2题：网站后台目录名是什么？
      * 第3题：管理员桌面中flag文件信息是?

## 0x01 管理员密码

根据提示，访问url。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-9.png" alt="" class="wp-image-141" width="424" height="174" /></figure>
</div>

下载并打开dedecms.exe，输入目标url，一键爆账号密码，可以看到用户名和密码的20 位哈希值（织梦 CMS 的特性）成功出来了。

<blockquote class="wp-block-quote">
  <p>
    dedecms的20位md5加密算法是从32位md5中截取的20位，去掉前3位和最后1位，即可获得16位md5值，即可破解15位md5
  </p>
</blockquote>
<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-5.png" alt="" class="wp-image-126"  /></figure>
</div>


将密码的MD5加密值输入<a rel="noreferrer noopener" href="https://www.somd5.com/" target="_blank" rel="nofollow" >https://www.somd5.com/</a>，可以很快的得出密码是`only_system`

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-7.png" alt="" class="wp-image-132" width="374" height="159" /></figure>
</div>

## 0x02 后台目录名

采用御剑后台扫描工具进行目录扫描

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-11.png" alt="" class="wp-image-159" width="448" height="159" /></figure>
</div>

对其可能的结果一一进行验证，没有任何发现，采取其他扫描工具后也一无所获。查找资料发现**后台目录名具有较强的个性或随机性**,要转换思路，看看dedeCMS 是否存在后台地址信息泄露的漏洞。

`/data/admin/ver.txt`查看版本信息，无果。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-12.png" alt="" class="wp-image-161" width="316" height="66" /></figure>
</div>

尝试可能存在的爆出后台路径的MySQL报错信息`/data/mysql_error_trace.inc` 或者 `/data/mysqli_error_trace.inc`，成功得到后台目录名`lichunqiul`

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-13.png" alt="" class="wp-image-162"/></figure>
</div>


输入之前获取的用户名和密码，进入后台管理页面。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-15.png" alt="" class="wp-image-164" width="428" height="171" /></figure>
</div>

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-16.png" alt="" class="wp-image-165" width="526" height="345" /></figure>
</div>

## 0x03 flag文件

发现核心->附件管理->上传新文件可以传一句话木马。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-17.png" alt="" class="wp-image-167" width="541" height="303" /></figure>
</div>

在notepad++上写一句话木马。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-18.png" alt="" class="wp-image-170"/></figure>
</div>

在系统->系统设置->系统基本参数->附件设置进行修改并保存。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-19.png" alt="" class="wp-image-171" width="541" height="292" /></figure>
</div>

上传木马。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-20.png" alt="" class="wp-image-174" width="431" height="28" /></figure>
</div>

直接上中国菜刀WebShell,添加完成后，在新增的记录上点击右键，选择虚拟终端。在命令行中输入`whoami`，显示SYSTEM权限。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-21.png" alt="" class="wp-image-176" width="409" height="125" /></figure>
</div>

找到flag文件，`type`命令发现拒绝访问，用`cacls`命令查看访问控制列表，发现SYSTEM：N。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-22.png" alt="" class="wp-image-177" width="566" height="165" /></figure>
</div>

修改SYSTEM访问控制权限

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-25.png" alt="" class="wp-image-182" width="450" height="331" /><figcaption>CACLS命令使用方法</figcaption></figure>
</div>

再用`cacls`命令查看访问控制列表，发现SYSTEM：F。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="730" height="142" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-23.png" alt="" class="wp-image-180" /></figure>
</div>

再一次`type`文件得到`key{il2o3l}`。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="545" height="42" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/图片-24.png" alt="" class="wp-image-181" /></figure>
</div>
