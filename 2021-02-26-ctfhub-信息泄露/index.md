# CTFHub-信息泄露

<div class="has-toc have-toc">
</div>

## 0x00 前言

菜鸡记录汇总下信息泄露的学习过程。

## 0x01 目录遍历

在页面可以遍历到目录<figure class="wp-block-image size-large">

<img loading="lazy" width="208" height="139" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-42.png" alt="" class="wp-image-1687" /> </figure> 

一个个点开，最后发现<figure class="wp-block-image size-large">

<img loading="lazy" width="201" height="76" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-41.png" alt="" class="wp-image-1686" /> </figure> 

## 0x02 PHPINFO

<figure class="wp-block-image size-large">

<img loading="lazy" width="231" height="136" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-43.png" alt="" class="wp-image-1691" /> </figure> 

点击后搜索关键字<figure class="wp-block-image size-large">

<img loading="lazy" width="681" height="29" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-44.png" alt="" class="wp-image-1692" /> </figure> 

## 0x03 网站源码

题目：当开发人员在线上环境中对源代码进行了备份操作，并且将备份文件放在了 web 目录下，就会引起网站源码泄露。<figure class="wp-block-image size-large">

<img loading="lazy" width="473" height="639" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-45.png" alt="" class="wp-image-1694" /> </figure> 

使用DirBuster设置后缀和文件名<figure class="wp-block-image size-large">

<img loading="lazy" width="1013" height="515" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-47.png" alt="" class="wp-image-1696" /> </figure> 

发现存在www.zip文件<figure class="wp-block-image size-large">

<img loading="lazy" width="372" height="151" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-48.png" alt="" class="wp-image-1697" /> </figure> 

下载文件<figure class="wp-block-image size-large">

<img loading="lazy" width="535" height="380" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-46.png" alt="" class="wp-image-1695" /> </figure> 

解压后发现可疑文件，打开后没有flag<figure class="wp-block-image size-large">

<img loading="lazy" width="237" height="90" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-50.png" alt="" class="wp-image-1700" /> </figure> 

换种思路，网页上访问。<figure class="wp-block-image size-large">

<img loading="lazy" width="883" height="121" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-49.png" alt="" class="wp-image-1699" /> </figure> 

## 0x04 bak文件

题目：当开发人员在线上环境中对源代码进行了备份操作，并且将备份文件放在了 web 目录下，就会引起网站源码泄露。<figure class="wp-block-image size-large">

<img loading="lazy" width="308" height="46" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-51.png" alt="" class="wp-image-1703" /> </figure> 

根据提示访问index.php.bak<figure class="wp-block-image size-large">

<img loading="lazy" width="540" height="384" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-52.png" alt="" class="wp-image-1704" /> </figure> 

得到flag<figure class="wp-block-image size-large">

<img loading="lazy" width="432" height="344" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-53.png" alt="" class="wp-image-1705" /> </figure> 

## 0x05 vim缓存

题目：当开发人员在线上环境中使用 vim 编辑器，在使用过程中会留下 vim 编辑器缓存，当vim异常退出时，缓存会一直留在服务器上，引起网站源码泄露。

Vim 的交换文件 .filename.swp，默认交换文件在打开文件的时候就会产生交换文件，正常退出的时候才会删除。

Vim 的备份文件 filename~，默认关闭，需要通过设置 `set backup` 来开启，Unbuntu的Vim配置文件是 /etc/vim/vimrc，开启后，对文件进行修改后会保存修改之前的一个副本。<figure class="wp-block-image size-large">

<img loading="lazy" width="542" height="362" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-54.png" alt="" class="wp-image-1708" /> </figure> 

打开文件<figure class="wp-block-image size-large">

<img loading="lazy" width="1029" height="197" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-55.png" alt="" class="wp-image-1709" /> </figure> 

## 0x06 .DS_Store

题目：.DS\_Store 是 Mac OS 保存文件夹的自定义属性的隐藏文件。通过.DS\_Store可以知道这个目录里面所有文件的清单。

下载.DS_Store<figure class="wp-block-image size-large">

<img loading="lazy" width="540" height="355" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-56.png" alt="" class="wp-image-1711" /> </figure> 

发现提示有flag的文件<figure class="wp-block-image size-large">

<img loading="lazy" width="700" height="86" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-57.png" alt="" class="wp-image-1713" /> </figure> 

## 0x07 Log

题目：当前大量开发人员使用git进行版本控制，对站点自动部署。如果配置不当,可能会将.git文件夹直接部署到线上环境。这就引起了git泄露漏洞。<figure class="wp-block-image size-large">

<img loading="lazy" width="807" height="151" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-58.png" alt="" class="wp-image-1715" /> </figure> 

使用<a rel="noreferrer noopener" href="https://github.com/maurosoria/dirsearch" data-type="URL" data-id="https://github.com/maurosoria/dirsearch" target="_blank" rel="nofollow" >dirsearch</a>工具进行目录扫描，执行`dirsearch.py -u http://challenge-6ef911625ae64cdf.sandbox.ctfhub.com:10800/ -e *`，注意url包含冒号，无法创建文件，可以通过-o指定outputfile文件的路径，或者修改在`default.conf`的`[reports] autosave-report = False`。<figure class="wp-block-image size-large">

<img loading="lazy" width="1269" height="333" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-59.png" alt="" class="wp-image-1717" /> </figure> 

使用GitHack进行文件恢复<figure class="wp-block-image size-large">

<img loading="lazy" width="1134" height="481" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-60.png" alt="" class="wp-image-1718" /> </figure> 

进入dist目录中的刚恢复的文件内打开git，题目提示log，联想到`git log`，查看历史提交记录。发现有个add flag的版本。<figure class="wp-block-image size-large">

<img loading="lazy" width="720" height="350" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-61.png" alt="" class="wp-image-1719" /> </figure> 

使用`git reset  [HEAD]` ，回退版本<figure class="wp-block-image size-large">

<img loading="lazy" width="532" height="65" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-62.png" alt="" class="wp-image-1720" /> </figure> 

发现dist文件夹中多出了可疑文件，打开得到flag。<figure class="wp-block-image size-large">

<img loading="lazy" width="339" height="226" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-63.png" alt="" class="wp-image-1721" /> </figure> 

## 0x08 Stash

题目：同上

使用dirsearch扫描，再重复用GitHack来clone源码。<figure class="wp-block-image size-large">

<img loading="lazy" width="1143" height="548" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-64.png" alt="" class="wp-image-1724" /> </figure> 

使用`git stash show`显示做了哪些改动，或者`git stash list`查看stash了哪些存储<figure class="wp-block-image size-large">

<img loading="lazy" width="422" height="99" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-65.png" alt="" class="wp-image-1728" /> </figure> 

刚好只有一个文件改动过，使用`git stash show -p` :，显示第一个存储的改动，成功得到flag。如果想显示其他存存储，命令：`git stash show stash@{$num} -p` ，比如第二个：`git stash show&nbsp;stash@{1}&nbsp;-p`<figure class="wp-block-image size-large">

<img loading="lazy" width="305" height="181" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-66.png" alt="" class="wp-image-1729" /> </figure> 

另一种解法：执行 `git stash pop` 发现从 git 栈中弹出来一个包含flag的文件。

第三种解法：使用`cat .git/refs/stash`打开stash文件，然后执行`git diff`比较工作区和暂存区<figure class="wp-block-image size-large">

<img loading="lazy" width="492" height="261" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-67.png" alt="" class="wp-image-1733" /> </figure> 

## 0x09 Index

题目：同上

clone源码，ls发现可疑文件，查看得到flag<figure class="wp-block-image size-large">

<img loading="lazy" width="445" height="155" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-68.png" alt="" class="wp-image-1736" /> </figure> 

## 0x0A SVN泄露

题目：当开发人员使用 SVN 进行版本控制，对站点自动部署。如果配置不当,可能会将.svn文件夹直接部署到线上环境。这就引起了 SVN 泄露漏洞。<figure class="wp-block-image size-large">

<img loading="lazy" width="436" height="159" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-69.png" alt="" class="wp-image-1739" /> </figure> 

在管理员使用SVN管理本地代码，并在发布代码时没有使用到处功能，直接使用了`全选+复制+粘贴`这种操作的话，就会将自动生成的 .svn 隐藏文件同时上传，而此文件中会有源码信息以及文件目录。

使用dirmap扫描隐藏文件<figure class="wp-block-image size-large">

<img loading="lazy" width="1205" height="459" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-71.png" alt="" class="wp-image-1745" /> </figure> 

发现存在了 .svn 文件，手动访问`.svn/entries`和`.svn/wc.db`均能成功下载<figure class="wp-block-image size-large">

<img loading="lazy" width="540" height="356" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-70.png" alt="" class="wp-image-1741" /> </figure> 

可以使用svn-extractor下载文件，但output不支持冒号，在源代码中加入`replace(":", "")`后才能正常运行。<figure class="wp-block-image size-large">

<img loading="lazy" width="1278" height="258" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-72.png" alt="" class="wp-image-1747" /> </figure> 

也可以直接使用svnExploit<figure class="wp-block-image size-large">

<img loading="lazy" width="1684" height="805" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-73.png" alt="" class="wp-image-1748" /> </figure> 

使用 Navicat Premium 打开 wc.db 文件，储存的为某一版本的文件目录，REPOSITORY表里存储了svn的项目路径，在NODES 表发现可疑文件，`local_relpath`是原始文件名。<figure class="wp-block-image size-large">

<img loading="lazy" width="443" height="104" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-74.png" alt="" class="wp-image-1749" /> </figure> 

checksum栏里的$sha1$后面的那串数字的前两位对应pristine文件夹里的00~ff文件名，index.html对应的是bf。<figure class="wp-block-image size-large">

<img loading="lazy" width="610" height="99" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-75.png" alt="" class="wp-image-1756" /> </figure> 

再通过PRISTINE表中的checksum，推断出flag文件的名称为75。<figure class="wp-block-image size-large">

<img loading="lazy" width="436" height="145" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-76.png" alt="" class="wp-image-1757" /> </figure> 

但url直接访问无法获取txt，通过dvcs-ripper获取 .svn 文件来得到文件的源码备份信息，从而查看此txt文件的内容。<figure class="wp-block-image size-large">

<img loading="lazy" width="965" height="79" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-77.png" alt="" class="wp-image-1760" /> </figure> 

查看隐藏文件<figure class="wp-block-image size-large">

<img loading="lazy" width="538" height="278" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-78.png" alt="" class="wp-image-1761" /> </figure> 

pristine文件夹下会储存旧版本的备份信息，故进行访问查看<figure class="wp-block-image size-large">

<img loading="lazy" width="523" height="181" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-79.png" alt="" class="wp-image-1762" /> </figure> 

发现目标文件夹<figure class="wp-block-image size-large">

<img loading="lazy" width="411" height="90" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-81.png" alt="" class="wp-image-1764" /> </figure> 

查看flag文件<figure class="wp-block-image size-large">

<img loading="lazy" width="849" height="112" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-82.png" alt="" class="wp-image-1765" /> </figure> 

## 0x0B HG泄露

题目：当开发人员使用 Mercurial 进行版本控制，对站点自动部署。如果配置不当,可能会将.hg 文件夹直接部署到线上环境。这就引起了 hg 泄露漏洞。<figure class="wp-block-image size-large">

<img loading="lazy" width="614" height="176" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-83.png" alt="" class="wp-image-1769" /> </figure> 

使用dvcs-ripper来获取.hg文件，执行`./rip-hg.pl -v -u http://challenge-be1484acebe78833.sandbox.ctfhub.com:10800/.hg/`执行过程中发现可疑文件<figure class="wp-block-image size-large">

<img loading="lazy" width="574" height="129" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-84.png" alt="" class="wp-image-1770" /> </figure> 

下载完成后cd到.hg文件夹，执行`grep -r flag *`<figure class="wp-block-image size-large">

<img loading="lazy" width="383" height="125" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-85.png" alt="" class="wp-image-1771" /> </figure> 

确认后url访问，get flag。
