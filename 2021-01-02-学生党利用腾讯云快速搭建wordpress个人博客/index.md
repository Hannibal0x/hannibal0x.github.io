# 利用腾讯云快速搭建WordPress个人博客

<div class="has-toc have-toc">
</div>

## 1.购买云服务器

### 步骤1：注册腾讯云账号

登录<a href="https://cloud.tencent.com/" target="_blank"  rel="nofollow" >https://cloud.tencent.com/</a>，自行完成用户注册。

### 步骤2：完成学生资质认证

直接购买服务器有点儿小贵，学生党可以通过腾讯云的云+校园活动，完成学生认证，可获得3次以购买价优惠续费的资格。详情如下：

<a href="https://cloud.tencent.com/act/campus?utm_source=qcloud&utm_medium=head&utm_campaign=campus" target="_blank"  rel="nofollow" >https://cloud.tencent.com/act/campus?utm_source=qcloud&utm_medium=head&utm_campaign=campus</a>

### 步骤3：选购云服务器

在这里本人选购了云服务器 1核2G，每3个月27元，索性直接来了一年的份儿，也可依据自己的需要挑选，两个区，上海和北京，那个离你的常住地近就优先选择，如果差不多随意就好。

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/image-20210101154124206.png" alt="" class="wp-image-16" width="774" height="255" /></figure>
</div>

## 2.手动搭建 LNMP 环境

LNMP 环境是指在 Linux 系统下，由 Nginx + MySQL/MariaDB + PHP 组成的网站服务器架构。首先在腾讯云云服务器（CVM）上手动搭建 LNMP 环境，以CentOS 7.5为例。

### 步骤1：登录 Linux 实例

WebShell 为腾讯云推荐的登录方式。无论您的本地系统为 Windows，Linux 或者 Mac OS，只要实例购买了公网 IP，都可以通过 WebShell 登录。  
WebShell 优点如下：

  * 支持快捷键复制粘贴。
  * 支持鼠标滚屏。
  * 支持中文输入法。
  * 安全性高，每次登录需要输入密码或密钥。

单击控制台，实例的管理页面，选择需要登录的 Linux 云服务器，单击【登录】。如下图所示：

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/image-20210101150400340.png" alt="" class="wp-image-18" width="880" height="274" /></figure>
</div>

在弹出的【登录Linux实例】窗口，选择【标准登录方式】，单击【立即登录】。如下图所示：

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/image-20210101150741440.png" alt="" class="wp-image-22" width="556" height="306" /></figure>
</div>

在打开的 WebShell 登录页面，根据实际需求，选择【密码登录】或者【密钥登录】方式进行登录。如下图所示：

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/image-20210101151001070.png" alt="" class="wp-image-23" width="275" height="307" /></figure>
</div>

如果登录成功，WebShell 界面会出现 Socket connection established 提示。如下图所示：

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="878" height="92" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/image-20210101151137709.png" alt="" class="wp-image-24" /></figure>
</div>

参考链接：<a href="https://cloud.tencent.com/document/product/213/5436" target="_blank"  rel="nofollow" >https://cloud.tencent.com/document/product/213/5436</a>

### 步骤2：安装 Nginx

  1. \#### 执行以下命令，在 `/etc/yum.repos.d/` 下创建 `nginx.repo` 文件。

<pre class="wp-block-code"><code>   vi /etc/yum.repos.d/nginx.repo</code></pre>

<ol start="2">
  <li>
    #### 按 “<strong>i</strong>” 切换至编辑模式，写入以下内容。
  </li>
</ol>

<pre class="wp-block-code"><code>   &#91;nginx] 
   name = nginx repo 
   baseurl = https://nginx.org/packages/mainline/centos/7/$basearch/ 
   gpgcheck = 0 
   enabled = 1</code></pre>

按 “**Esc**”，输入 “**:wq**”，保存文件并返回。

<ol start="3">
  <li>
    #### 执行以下命令，安装 nginx。
  </li>
</ol>

<pre class="wp-block-code"><code>   yum install -y nginx</code></pre>

<ol start="4">
  <li>
    #### 执行以下命令，打开 <code>nginx.conf</code> 文件。
  </li>
</ol>

<pre class="wp-block-code"><code>   vim /etc/nginx/nginx.conf</code></pre>

<ol start="5">
  <li>
    #### 按 “<strong>i</strong>” 切换至编辑模式，编辑 <code>nginx.conf</code> 文件。在 <code>include /etc/nginx/conf.d/*conf;</code>上方添加 <code>server{...}</code> 配置内容。如下图所示：
  </li>
</ol>

<pre class="wp-block-code"><code>   server {
    listen       80;
    root   /usr/share/nginx/html;
    server_name  localhost;
    #charset koi8-r;
    #access_log  /var/log/nginx/log/host.access.log  main;
    #
    location / {
          index index.php index.html index.htm;
    }
    #error_page  404              /404.html;
    #redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
      root   /usr/share/nginx/html;
    }
    #pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    location ~ .php$ {
      fastcgi_pass   127.0.0.1:9000;
      fastcgi_index  index.php;
      fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
      include        fastcgi_params;
    }
   }</code></pre>

<div class="wp-block-image">
  <figure class="aligncenter"><img src="https://main.qcloudimg.com/raw/901a3957ccd992c2fb345287271c4bef.png" alt="img" /></figure>
</div>

按 “**Esc**”，输入 “**:wq**”，保存文件并返回。

<ol start="6">
  <li>
    #### 执行以下命令启动 Nginx。
  </li>
</ol>

<pre class="wp-block-code"><code>   systemctl start nginx</code></pre>

<ol start="7">
  <li>
    #### 执行以下命令，设置 Nginx 为开机自启动。
  </li>
</ol>

<pre class="wp-block-code"><code>   systemctl enable nginx </code></pre>

<ol start="8">
  <li>
    #### 在本地浏览器中访问以下地址，查看 Nginx 服务是否正常运行。
  </li>
</ol>

<pre class="wp-block-code"><code>   http://云服务器实例的公网 IP</code></pre>

显示如下，则说明 Nginx 安装配置成功。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="638" height="243" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/image-20210101152722502.png" alt="" class="wp-image-25" /></figure>
</div>

### 步骤3：安装数据库

  1. \#### 执行以下命令，在 `/etc/yum.repos.d/` 下创建 `MariaDB.repo` 文件。

<pre class="wp-block-code"><code>   vi /etc/yum.repos.d/MariaDB.repo</code></pre>

<ol start="2">
  <li>
    #### 按 “<strong>i</strong>” 切换至编辑模式，写入以下内容，添加 MariaDB 软件库，不同操作系统的 MariaDB 软件库不同。
  </li>
</ol>

<pre class="wp-block-code"><code>   &#91;mariadb]
   name = MariaDB
   baseurl = http://yum.mariadb.org/10.4/centos7-amd64
   gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB
   gpgcheck=1</code></pre>

按 “**Esc**”，输入 “**:wq**”，保存文件并返回。

<ol start="3">
  <li>
    #### 执行以下命令，安装 MariaDB。此步骤耗时较长，请关注安装进度，等待安装完毕。
  </li>
</ol>

<pre class="wp-block-code"><code>   yum -y install MariaDB-client MariaDB-server</code></pre>

<ol start="4">
  <li>
    #### 执行以下命令，启动 MariaDB 服务。
  </li>
</ol>

<pre class="wp-block-code"><code>   systemctl start mariadb</code></pre>

<ol start="5">
  <li>
    #### 执行以下命令，设置 MariaDB 为开机自启动。
  </li>
</ol>

<pre class="wp-block-code"><code>   systemctl enable mariadb</code></pre>

<ol start="6">
  <li>
    #### 执行以下命令，验证 MariaDB 是否安装成功。
  </li>
</ol>

<pre class="wp-block-code"><code>   mysql</code></pre>

显示结果如下，则成功安装。

<div class="wp-block-image">
  <figure class="aligncenter"><img src="https://main.qcloudimg.com/raw/bfe9a604457f6de09933206c21fde13b.png" alt="img" /></figure>
</div>

<ol start="7">
  <li>
    #### 执行以下命令，退出 MariaDB。
  </li>
</ol>

<pre class="wp-block-code"><code>   \q</code></pre>

### 步骤4：安装配置 PHP

  1. \#### 依次执行以下命令，更新 yum 中 PHP 的软件源。

<pre class="wp-block-code"><code>   rpm -Uvh https://mirrors.cloud.tencent.com/epel/epel-release-latest-7.noarch.rpm</code></pre>

<pre class="wp-block-code"><code>   rpm -Uvh https://mirror.webtatic.com/yum/el7/webtatic-release.rpm</code></pre>

<ol start="2">
  <li>
    #### 执行以下命令，安装 PHP 7.2 所需要的包。
  </li>
</ol>

<pre class="wp-block-code"><code>   yum -y install mod_php72w.x86_64 php72w-cli.x86_64 php72w-common.x86_64 php72w-mysqlnd php72w-fpm.x86_64</code></pre>

<ol start="3">
  <li>
    #### 执行以下命令，启动 PHP-FPM 服务。
  </li>
</ol>

<pre class="wp-block-code"><code>   systemctl start php-fpm</code></pre>

<ol start="4">
  <li>
    #### 执行以下命令，设置 PHP-FPM 服务为开机自启动。
  </li>
</ol>

<pre class="wp-block-code"><code>   systemctl enable php-fpm</code></pre>

### 步骤5：验证环境配置

当您完成环境配置后，可以通过以下验证 LNMP 环境是否搭建成功。

  1. \#### 执行以下命令，创建测试文件。

<pre class="wp-block-code"><code>   echo "&lt;?php phpinfo(); ?&gt;" &gt;&gt; /usr/share/nginx/html/index.php</code></pre>

<ol start="2">
  <li>
    #### 执行以下命令，重启 Nginx 服务。
  </li>
</ol>

<pre class="wp-block-code"><code>   systemctl restart nginx</code></pre>

<ol start="3">
  <li>
    #### 在本地浏览器中访问如下地址，查看环境配置是否成功。
  </li>
</ol>

<pre class="wp-block-code"><code>   http://云服务器实例的公网 IP</code></pre>

显示结果如下， 则说明环境配置成功。<figure class="wp-block-image size-large">

<img loading="lazy" width="1166" height="326" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/image-20210101173408616.png" alt="" class="wp-image-26" /> </figure> 

## 3.Windows 系统通过 FTP 上传文件到云服务器

### 步骤1：安装 vsftpd

  1. \#### 执行以下命令，安装 vsftpd。

<pre class="wp-block-code"><code>   yum install -y vsftpd</code></pre>

<ol start="2">
  <li>
    #### 执行以下命令，设置 vsftpd 开机自启动。
  </li>
</ol>

<pre class="wp-block-code"><code>   systemctl enable vsftpd</code></pre>

<ol start="3">
  <li>
    #### 执行以下命令，启动 FTP 服务。
  </li>
</ol>

<pre class="wp-block-code"><code>   systemctl start vsftpd</code></pre>

<ol start="4">
  <li>
    #### 执行以下命令，确认服务是否启动。
  </li>
</ol>

<pre class="wp-block-code"><code>   netstat -antup | grep ftp</code></pre>

显示结果如下，则说明 FTP 服务已成功启动。  
![img][1]  
此时，vsftpd 已默认开启匿名访问模式，无需通过用户名和密码即可登录 FTP 服务器。使用此方式登录 FTP 服务器的用户没有权修改或上传文件的权限。

### 步骤2：配置 vsftpd

  1. \#### 执行以下命令，为 FTP 服务创建一个 Linux 用户，本文以`ftpuser` 为例。

<pre class="wp-block-code"><code>   useradd ftpuser</code></pre>

<ol start="2">
  <li>
    #### 执行以下命令，设置 ftpuser 用户的密码。
  </li>
</ol>

<pre class="wp-block-code"><code>   passwd ftpuser</code></pre>

输入密码后请按 `Enter`确认设置，密码默认不显示。

<ol start="3">
  <li>
    #### 执行以下命令，创建 FTP 服务使用的文件目录，本文以<code>/var/ftp/test</code>为例。
  </li>
</ol>

<pre class="wp-block-code"><code>   mkdir /var/ftp/test</code></pre>

<ol start="4">
  <li>
    #### 执行以下命令，修改目录权限。
  </li>
</ol>

<pre class="wp-block-code"><code>   chown -R ftpuser:ftpuser /var/ftp/test</code></pre>

<ol start="5">
  <li>
    #### 执行以下命令，打开 <code>vsftpd.conf</code>文件。
  </li>
</ol>

<pre class="wp-block-code"><code>   vim /etc/vsftpd/vsftpd.conf</code></pre>

<ol start="6">
  <li>
    按 i 切换至编辑模式，根据实际需求选择 FTP 模式，修改配置文件 <code>vsftpd.conf</code> 修改以下配置参数，设置匿名用户和本地用户的登录权限，设置指定例外用户列表文件的路径，并开启监听 IPv4 sockets。
  </li>
</ol>

<pre class="wp-block-code"><code>   anonymous_enable=NO
   local_enable=YES
   chroot_local_user=YES
   chroot_list_enable=YES
   chroot_list_file=/etc/vsftpd/chroot_list
   listen=YES</code></pre>

在行首添加 `#`，注释 `listen_ipv6=YES`配置参数，关闭监听 IPv6 sockets。

<pre class="wp-block-code"><code>   #listen_ipv6=YES</code></pre>

添加以下配置参数，开启被动模式，设置本地用户登录后所在目录，以及云服务器建立数据传输可使用的端口范围值。

<pre class="wp-block-code"><code>   local_root=/var/ftp/test
   allow_writeable_chroot=YES
   pasv_enable=YES
   pasv_address=xxx.xx.xxx.xx #请修改为您的 Linux 云服务器公网 IP
   pasv_min_port=40000
   pasv_max_port=45000</code></pre>

按 **Esc** 后输入 **:wq** 保存后退出。

<ol start="7">
  <li>
    #### 执行以下命令，创建并编辑 <code>chroot_list</code>文件。
  </li>
</ol>

<pre class="wp-block-code"><code>   vim /etc/vsftpd/chroot_list</code></pre>

<ol start="8">
  <li>
    #### 执行以下命令，重启 FTP 服务。
  </li>
</ol>

<pre class="wp-block-code"><code>   systemctl restart vsftpd</code></pre>

### 步骤4：设置安全组

  1. 登录 云服务器控制台。在左侧导航栏，单击【安全组】，进入安全组管理页面。
  2. 在安全组管理页面，选择【地域】，找到需要设置规则的安全组。
  3. 在需要设置规则的安全组行中，单击操作列的【修改规则】。
  4. 在安全组规则页面，单击“入站规则”时参考如下配置，添加安全组规则。 方向 类型 来源 协议端口 策略 入方向 自定义 0.0.0.0/0 TCP:20-21 允许

### 步骤5：连接云服务器

  1. 在本地下载并安装开源软件 FileZilla，打开 FileZilla，在 FileZilla 窗口中，填写主机、用户名、密码和端口等信息，单击【快速连接】。如下图所示：![img][2] 配置信息说明：

  * 主机：云服务器的公网 IP。在 云服务器控制台 的实例管理页面可查看对应云服务器的公网 IP。
  * 用户名：搭建 FTP 服务 时设置的 FTP 用户的帐号。图中以 “ftpuser1” 为例。
  * 密码：搭建 FTP 服务 时设置的 FTP 用户帐号对应的密码。
  * 端口：FTP 监听端口，默认为21。

  1. 在左下方的“本地站点”窗口中，右键单击待上传的本地文件，选择【上传】，即可将文件上传到 Linux 云服务器。如下图所示：![img][3] 

## 4.手动搭建 WordPress 个人站点

### 步骤1：配置数据库

  1. \#### 执行以下命令，进入 `MariaDB`。

<pre class="wp-block-code"><code>   mysql</code></pre>

<ol start="2">
  <li>
    #### 执行以下命令，创建 <code>MariaDB</code> 数据库。例如 <code>wordpress</code>。
  </li>
</ol>

<pre class="wp-block-code"><code>   CREATE DATABASE wordpress;</code></pre>

<ol start="3">
  <li>
    #### 执行以下命令，创建一个新用户。例如<code>user</code>，登录密码为 <code>123456</code>。
  </li>
</ol>

<pre class="wp-block-code"><code>   CREATE USER 'user'@'localhost' IDENTIFIED BY '123456';</code></pre>

<ol start="4">
  <li>
    #### 执行以下命令，赋予用户对<code>wordpress</code>数据库的全部权限。
  </li>
</ol>

<pre class="wp-block-code"><code>   GRANT ALL PRIVILEGES ON wordpress.* TO 'user'@'localhost' IDENTIFIED BY '123456';</code></pre>

<ol start="5">
  <li>
    #### 执行以下命令，设置 <code>root</code> 帐户密码。
  </li>
</ol>

<pre class="wp-block-code"><code>   ALTER USER root@localhost IDENTIFIED VIA mysql_native_password USING PASSWORD('输入您的密码');</code></pre>

<ol start="6">
  <li>
    #### 执行以下命令，使所有配置生效。
  </li>
</ol>

<pre class="wp-block-code"><code>   FLUSH PRIVILEGES;</code></pre>

<ol start="7">
  <li>
    #### 执行以下命令，退出<code>MariaDB</code>。
  </li>
</ol>

<pre class="wp-block-code"><code>   \q</code></pre>

### 步骤2：安装和配置 WordPress

  1. \#### 执行以下命令，删除网站根目录下用于测试 PHP-Nginx 配置的`index.php`文件。

<pre class="wp-block-code"><code>   rm -rf /usr/share/nginx/html/index.php</code></pre>

<ol start="2">
  <li>
    从 WordPress 官方网站下载 WordPress 最新中文版本，并利用FileZilla上传文件到<code>/var/ftp/test</code>
  </li>
  <li>
    #### 执行以下命令，将安装包移入<code>/usr/share/nginx/html/</code>目录，解压 WordPress。
  </li>
</ol>

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="1072" height="423" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/image-20210101205326553.png" alt="" class="wp-image-29" /></figure>
</div>

<pre class="wp-block-code"><code>   cd /usr/share/nginx/html</code></pre>

<pre class="wp-block-code"><code>   cp /var/ftp/test/wordpress-5.6-zh_CN.tar.gz /usr/share/nginx/html/</code></pre>

<pre class="wp-block-code"><code>   tar zxvf wordpress-5.6-zh_CN.tar.gz</code></pre>

<ol start="4">
  <li>
    #### 依次执行以下命令，进入 WordPress 安装目录，将<code>wp-config-sample.php</code>文件复制到<code>wp-config.php</code>文件中，并将原先的示例配置文件保留作为备份。
  </li>
</ol>

<pre class="wp-block-code"><code>   cd /usr/share/nginx/html/wordpress</code></pre>

<pre class="wp-block-code"><code>   cp wp-config-sample.php wp-config.php</code></pre>

<ol start="5">
  <li>
    #### 执行以下命令，打开并编辑新创建的配置文件。
  </li>
</ol>

<pre class="wp-block-code"><code>   vim wp-config.php</code></pre>

<ol start="6">
  <li>
    #### 按 <strong>i</strong> 切换至编辑模式，找到文件中 MySQL 的部分，并将相关配置信息修改为 [配置 WordPress 数据库]中的内容。
  </li>
</ol>

<pre class="wp-block-code"><code>    // ** MySQL settings - You can get this info from your web host ** //
    /** The name of the database for WordPress */
    define('DB_NAME', 'wordpress');

    /** MySQL database username */
    define('DB_USER', 'user');
    
    /** MySQL database password */
    define('DB_PASSWORD', '123456');
    
    /** MySQL hostname */
    define('DB_HOST', 'localhost');</code></pre>

修改完成后，按 **Esc**，输入 **:wq**，保存文件返回。

<ol start="7">
  <li>
    #### 在浏览器地址栏输入<code>http://域名或云服务器实例的公网 IP/wordpress 文件夹</code>，例如：
  </li>
</ol>

<pre class="wp-block-code"><code>   http:&#47;&#47;192.xxx.xxx.xx/wordpress</code></pre>

转至 WordPress 安装页，开始配置 WordPress。<figure class="wp-block-image">

![配置WP1][4] </figure> 

<ol start="8">
  <li>
    解决wordpress更新提示无法创建目录问题 执行以下命令
  </li>
</ol>

<pre class="wp-block-code"><code>   vim /usr/share/nginx/html/wordpress/wp-config.php</code></pre>

按 **i** 切换至编辑模式，添加：

<pre class="wp-block-code"><code>   define("FS_METHOD","direct");</code></pre>

修改完成后，按 **Esc**，输入 **:wq**，保存文件返回。

<ol start="9">
  <li>
    #### 修改wordpress安装目录所属组及php的配置文件
  </li>
</ol>

<pre class="wp-block-code"><code>   chown -R username.username xxx/wordpress/ </code></pre>

<ol start="10">
  <li>
    修改php配置 执行以下命令 <code>vim /etc/php-fpm.d/www.conf</code> 按 <strong>i</strong> 切换至编辑模式，修改： <code>user = usrname group = username</code> 修改完成后，按 <strong>Esc</strong>，输入 <strong>:wq</strong>，保存文件返回。 重启php-fpm <code>systemctl restart php-fpm</code>
  </li>
</ol>

[1]: https://main.qcloudimg.com/raw/2a7abf80253a8469c9340878d89b452a.png
[2]: https://mc.qcloudimg.com/static/img/dc603f912adf94a33749155c69ddddd2/24.png
[3]: https://main.qcloudimg.com/raw/45cd8f030ca74145b11e6c64203cedf2.png
[4]: https://main.qcloudimg.com/raw/c79c35b3d75f763561d7024f46983611.png
