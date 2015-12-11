#基于Python的新浪微博社交网络分析
>具体内容请看代码注释

##网络图
<img src="http://ww2.sinaimg.cn/large/680bc840jw1eyw2j1a8njj21kw0u60xh.jpg"/>

#时间图
<img src="http://ww1.sinaimg.cn/large/680bc840jw1eyw2lnu177j20mk0h0764.jpg"/>

##项目步骤
1. 爬取某个具体微博的转发数据；
2. 将爬下来的转发数据用图进行可视化

##基本模块
主要分了模拟登陆模块（weibo_login.py、post_encode.py）、解析网页模块（get_weibo.py）、绘制图像模块（network_graph.py、time_graph.py）

##文件说明
1. data.csv : 爬取下来的转发数据
2. weibo_login.py、post_encode.py : 模拟登陆模块
3. get_weibo.py ：解析网页模块
4. network_graph.py ： 绘制网络图
5. time_graph.py ： 绘制时间图
6. network_graph.png : 网络图
7. time_graph.png : 时间图

##参考博客
1. http://www.cnblogs.com/houkai/p/3488468.html
2. http://computational-thinking.farbox.com/blog/2014-08-03-study-osn-using-python#toc_6
