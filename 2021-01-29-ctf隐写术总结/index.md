# CTF隐写术入门总结

<p class="has-large-font-size">
  0x00 前言
</p>

CTF中隐写术是一个非常有趣的部分，通常属于MISC的范围，有些题目需要和密码学等知识的结合，一直想整理出文字。套路一般固定，难度较低，但同时也极易形成思维定式，一旦遇上新颖的题型，没有足够的知识量和脑洞，可能就要吃瘪了。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="844" height="415" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/8343187-0eca908d6392480c.png" alt="" class="wp-image-386" /></figure>
</div>

  * **评价隐写术的标准核心标准**：隐蔽程度隐蔽程度越高，直接导致检测有效信息越困难
  * 其他标准：隐写算法的好坏、隐写手段的复杂度、提取信息的难易度

<div class="wp-block-image">
  <figure class="aligncenter size-large is-resized"><img loading="lazy" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/8343187-0eca908d6392480c-1.png" alt="" class="wp-image-389" width="503" height="358" /></figure>
</div>

在CTF中，隐写术的载体对象通常有文本、图像、音频、视频、压缩包等等，在一些情况下也不单一，下文也主要介绍上述种类。

<a href="https://www.cnblogs.com/13ck/p/4471146.html" data-type="URL" data-id="https://www.cnblogs.com/13ck/p/4471146.html" target="_blank" rel="noreferrer noopener" rel="nofollow" ><strong>各类文件的文件头标志</strong></a>

<p class="has-large-font-size">
  0x01 文本隐写
</p>

Doc文件的本质是一种zip压缩文件，docx中的x指的是xml。文件头是`50 4B`。

下面介绍几种常见的DOC隐藏方式。

  1. 白色背景下写白字，无法被肉眼识别出有隐藏的文字。
  2. 通过文字的**偏移（行移、字移）**和**颜色**等来传递信息，比如上偏移代表0，下偏移代表1，传达二进制信息。
  3. 利用空格、换行、回车、标点（句号和逗号或者中英文符号）等。
  4. 利用不同字体、简体繁体，调整间距拼凑（比如：‘仁’和‘m’）。
  5. 同义词替换、句法变换（比如：把字句和被字句）。
  6. 隐藏在xml等文件中，修改后缀为zip压缩文件，解压后搜索相关信息。
  7. Word隐藏图片，插入的图片方式分为**嵌入式**和**非嵌入式**。嵌入式随着文本的位置产生移动，即有回车后，图片下移。非嵌入图片保持原位置不动。
      1. **嵌入式**：单击“文件”标签，选择“选项”选项打开“Word选项”对话框。在对话框左侧的列表中选择“高 级”选项，在右侧的“显示文档内容”栏中勾选“显示图片框”复选框，单击“确定”按钮关闭对话框后，文档中的嵌入式图片将被隐藏，将只显示图片框的框线。
      2. **非嵌入式**：在“显示文档内容”栏中取消对“在屏幕上显示图形和文字”复选框的勾选。单击“确定”按钮关闭对话框后，文档中的非嵌入式图片将被隐藏。
  8. Word中选中要隐藏的字段，右击选择字体选项，在效果一栏中有隐藏选项，选中后即可隐藏。默认情况下隐藏文字是不会被打印出来的。如果想知道是否有隐藏文本，可在文件选项中单击“文件”-》选项-》显示，选择“隐藏文字”复选框，即可查看。在保存文件后选择文件-》检查-》检查文件，查看是否有隐藏文字。

PDF文件则可以利用PDF文件头添加额外信息，这个区域的信息会被Adobe Acrobat Reader阅读器忽略。利用工具wbStego4open会把插入数据中的每一个ASCII码转换为二进制形式，然后把每一个二进制数字再替换为十六进制的20或者09，20代表0，09代表1，嵌入到PDF文件中。

<p class="has-large-font-size">
  0x02 图片隐写
</p>

几乎8成的隐写题目都脱不开图片，而常见的图片格式有PNG、JPG/JPEG、BMP、GIF，下面分别介绍它们的结构。

**PNG的文件结构**

<a rel="noreferrer noopener" href="https://www.cnblogs.com/lidabo/p/3701197.html" data-type="URL" data-id="https://www.cnblogs.com/lidabo/p/3701197.html" target="_blank" rel="nofollow" >详细信息</a>

PNG无损压缩的位图格式，文件头`89 50 4E 47 0D 0A 1A 0A`，数据块（chunk）基本的构成：文件头数据块（IHDR）、调色板数据块（PLTE）、图像数据块（IDAT）、图像结束数据（IEND）。

我们重点关注IHDR。它包含有PNG文件中存储的图像数据的基本信息，并要作为第一个数据块出现在PNG数据流中，而且一个PNG数据流中只能有一个文件头数据块。 文件头数据块由13字节组成，它的格式如下表所示。

<div class="wp-block-image">
  <figure class="aligncenter size-large"><img loading="lazy" width="732" height="585" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/01/image.png" alt="" class="wp-image-423" /></figure>
</div>

**JPEG/JPG的文件结构**

JPEG/JPG为有损压缩，文件头为`FF D8 FF`。
