# Autodriving摸门槛笔记

<div class="has-toc have-toc">
</div>

## 0x00 前言

菜鸡从来没有接触过Autodriving，先简单接触一下。这个笔记只是了解浅显的知识，有个基本的认知。

视频学习来源：

<a href="https://www.bilibili.com/video/BV19A411T7Qb" data-type="URL" data-id="https://www.bilibili.com/video/BV19A411T7Qb" target="_blank" rel="noreferrer noopener" rel="nofollow" >自动驾驶技术_1_基本介绍</a>

<a href="https://www.bilibili.com/video/BV1pr4y1N7nw/?spm_id_from=333.788.recommend_more_video.-1" data-type="URL" data-id="https://www.bilibili.com/video/BV1pr4y1N7nw/?spm_id_from=333.788.recommend_more_video.-1" target="_blank" rel="noreferrer noopener" rel="nofollow" >自动驾驶技术_2_传感器及感知算法</a>

<a href="https://www.bilibili.com/video/BV1ao4y197vc/?spm_id_from=333.788.recommend_more_video.2" data-type="URL" data-id="https://www.bilibili.com/video/BV1ao4y197vc/?spm_id_from=333.788.recommend_more_video.2" target="_blank" rel="noreferrer noopener" rel="nofollow" >自动驾驶技术_3_规划及控制算法</a>

<a rel="noreferrer noopener" href="https://www.bilibili.com/video/BV1M4411g7g3?from=search&seid=18262137945301483497" data-type="URL" data-id="https://www.bilibili.com/video/BV1M4411g7g3?from=search&seid=18262137945301483497" target="_blank" rel="nofollow" >apollo无人驾驶</a>

<a href="https://www.bilibili.com/video/BV1854y1C7jd?from=search&seid=11685924019828740700" data-type="URL" data-id="https://www.bilibili.com/video/BV1854y1C7jd?from=search&seid=11685924019828740700" target="_blank" rel="noreferrer noopener" rel="nofollow" >首届百度安全自动驾驶CTF冠军战队成员分享参赛经验和解题过程</a>

## 0x01 基础知识

自动驾驶的分级从L0-L5，L0是无自动化，L1是指辅助驾驶，L2是指部分自动驾驶，L3是有条件的自动驾驶，L4是高度自动驾驶，L5是完全自动驾驶。<figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/Screenshot_20210801_000723_tv.danmaku.bili_.jpg" alt="" class="wp-image-2286" /></figure> 

自动驾驶的技术框架。<figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/Screenshot_20210801_001035_tv.danmaku.bili_.jpg" alt="" class="wp-image-2288" /></figure> 

传感器的类型和使用范围<figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/Screenshot_20210801_003126_tv.danmaku.bili_.jpg" alt="" class="wp-image-2291" /></figure> 

多个传感器的覆盖与标定。<figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/Screenshot_20210801_003410_tv.danmaku.bili_.jpg" alt="" class="wp-image-2293" /></figure> 

## 0x02 定位技术

<figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/Screenshot_20210801_003811_tv.danmaku.bili_.jpg" alt="" class="wp-image-2299" /></figure> 

PDF文件下载地址：<a href="https://www.researchgate.net/publication/321124951_Robust_and_Precise_Vehicle_Localization_based_on_Multi-sensor_Fusion_in_Diverse_City_Scenes" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.researchgate.net/publication/321124951_Robust_and_Precise_Vehicle_Localization_based_on_Multi-sensor_Fusion_in_Diverse_City_Scenes</a><figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/Screenshot_20210801_004355_tv.danmaku.bili_.jpg" alt="" class="wp-image-2305" /></figure> 

## 0x03 感知相关算法

<figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/Screenshot_20210801_003915_tv.danmaku.bili_.jpg" alt="" class="wp-image-2307" /> </figure> 

<a href="https://blog.csdn.net/Young_GY/article/details/75194914" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://blog.csdn.net/Young_GY/article/details/75194914</a>

<a href="https://blog.csdn.net/adamshan/category_9280008.html" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://blog.csdn.net/adamshan/category_9280008.html</a>

<a href="https://www.sohu.com/a/207740445_391994" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://www.sohu.com/a/207740445_391994</a><figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/Screenshot_20210801_004012_tv.danmaku.bili_.jpg" alt="" class="wp-image-2309" /> </figure> 

<a href="https://github.com/ApolloAuto/apollo/tree/master/docs" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://github.com/ApolloAuto/apollo/tree/master/docs</a><figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/Screenshot_20210801_004143_tv.danmaku.bili_.jpg" alt="" class="wp-image-2313" /></figure> 

<a href="https://blog.csdn.net/qq_39506912/article/details/118834054" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://blog.csdn.net/qq_39506912/article/details/118834054</a>

<a href="https://blog.csdn.net/mw_mustwin/article/details/53039338" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://blog.csdn.net/mw_mustwin/article/details/53039338</a><figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/Screenshot_20210801_004332_tv.danmaku.bili_.jpg" alt="" class="wp-image-2316" /></figure> 

<a href="https://blog.csdn.net/u010167269/article/details/52638771" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://blog.csdn.net/u010167269/article/details/52638771</a><figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/Screenshot_20210801_004401_tv.danmaku.bili_-1.jpg" alt="" class="wp-image-2318" /> </figure> 

<a href="https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python</a><figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/Screenshot_20210801_004454_tv.danmaku.bili_.jpg" alt="" class="wp-image-2321" /></figure> 

<a href="https://github.com/NikolasEnt/Extended-Kalman-Filter" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://github.com/NikolasEnt/Extended-Kalman-Filter</a>

<a href="https://blog.csdn.net/Young_GY/article/details/78468153" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://blog.csdn.net/Young_GY/article/details/78468153</a>

## 0x04 数据融合

<figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/Screenshot_20210801_004920_tv.danmaku.bili_.jpg" alt="" class="wp-image-2326" /></figure> 

## 0x05 预测和路径规划

<figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/Screenshot_20210801_005217_tv.danmaku.bili_.jpg" alt="" class="wp-image-2331" /></figure> 

<a rel="noreferrer noopener" href="http://web.mit.edu/16.412j/www/html/papers/original_dstar_icra94.pdf" target="_blank" data-type="URL" data-id="http://web.mit.edu/16.412j/www/html/papers/original_dstar_icra94.pdf" rel="nofollow" >http://web.mit.edu/16.412j/www/html/papers/original_dstar_icra94.pdf</a><figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/Screenshot_20210801_113236_tv.danmaku.bili_.jpg" alt="" class="wp-image-2337" /></figure> 

<a href="https://blog.csdn.net/hgdwdtt/article/details/82052577?spm=1001.2014.3001.5501" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://blog.csdn.net/hgdwdtt/article/details/82052577?spm=1001.2014.3001.5501</a>

<a href="https://blog.csdn.net/hgdwdtt/article/details/82080558" target="_blank" rel="noreferrer noopener" rel="nofollow" >https://blog.csdn.net/hgdwdtt/article/details/82080558</a><figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/Screenshot_20210801_113755_tv.danmaku.bili_.jpg" alt="" class="wp-image-2343" /></figure> 

## 0x06 车辆模型

<figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/Screenshot_20210801_114132_tv.danmaku.bili_.jpg" alt="" class="wp-image-2348" /></figure> 

## 0x07 安全问题

<figure class="wp-block-image size-full">

<img loading="lazy" width="1920" height="1080" src="https://cdn.jsdelivr.net/gh/Hannibal0x/img/2021/08/Screenshot_20210801_203214_tv.danmaku.bili_.jpg" alt="" class="wp-image-2352" /></figure>
