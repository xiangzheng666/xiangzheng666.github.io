---
categories: [windows_ros]
tags: [Ros]
---
# Ros安装 #

- 采用官网roswiki步骤

- 离线安装

# Ros依赖安装 

使用choco安装二进制文件

下载源码进行编译，并把devel/setup.bat激活

- 编译源码，生成lib
- choco install ros-melodic-<name>一般没有
- 下载git源码注意branch
- lib not find
  - 文件占用中
  - 文件路径不可知
  - 环境变量
  - 未解决！！！！！!![](\pic\Snipaste_2021-12-20_16-17-53.jpg)

# Vscode ros环境

- 插件www.baidu.com
- https://blog.csdn.net/MSNH2012/article/details/100516277
-  如果此处不自动生成c_cpp_properties.json文件, 可手动生成, 按Ctrl + Shift + P,输入`c/c++: edit configurations(JSON)`, 即可. 
-  2, 点击"终端"–>“新建终端”,在终端中输入"catkin_make"，系统会自动在test文件夹下创建 “build”, "devel"文件夹和其他配置文件 
-  关于task文件
-  关于扩展说明
-  未解决！！！！！

# Ros的python环境问题

- python3
- python的自定义消息文件
- python can‘t import rospy   
  - 要在环境使用c:\opt\ros\melodic\x64\setup.bat激活
- python can‘t import msg
  - msg在该功能包的setup.bat中,需先激活在import

- 已经弄清

---

# 环境搭建到此为止

[参考书](http://www.autolabor.com.cn/book/ROSTutorials/chapter1/15-ben-zhang-xiao-jie/151-roswen-jian-xi-tong.html)





 