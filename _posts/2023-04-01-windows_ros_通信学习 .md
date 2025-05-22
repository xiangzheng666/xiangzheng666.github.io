---
categories: [windows_ros]
tags: [通信]
---

# 1.话题通信

![Snipaste_2021-12-21_22-10-09](https://github.com/xiangzheng666/picx-images-hosting/raw/master/Snipaste_2021-12-21_22-10-09.4joc29phcg.webp)

- 建立依赖

  > package.xml
  >
  > ​	<build_depend>message_generation</build_depend>
  >
  > ​	<exec_depend>message_runtime</exec_depend>
  >
  > cmakelist.txt
  >
  > ​	find_package( …… message_generation) 
  >
  > ​	catkin_package(CATKIN_DEPENDS geometry_msgs roscpp 
  >
  > ​	rospy std_msgs message_runtime) 
  >
  > ​	add_message_files(FILES Person.msg)
  >
  > ​	generate_messages(DEPENDENCIES std_msgs)

<exec_depend>message_runtime</exec_depend>

```
rostopic echo [topic] 查看topic上发布得到消息
```

```
rostopic list  列出当前已被订阅和发布的所有话题。
```

```
rostopic type [topic] 查看所发布话题的消息类型。
```

```
rostopic pub -1（一条消息后退出） [topic] [消息类型] [消息] 可以把数据发布到当前某个正在广播的话题上。
```

```
rostopic hz [topic] 报告数据发布的速率。
```



# 2.服务通信

![Snipaste_2021-12-21_22-11-51](https://github.com/xiangzheng666/picx-images-hosting/raw/master/Snipaste_2021-12-21_22-11-51.3d50to0kr5.webp)

> package.xml
>
> <build_depend>message_generation</build_depend> 
>
> <exec_depend>message_runtime</exec_depend> 
>
> 
>
> cmakelist.txt
>
>  find_package( …… message_generation) 
>
> catkin_package(CATKIN_DEPENDS geometry_msgs roscpp rospy std_msgs message_runtime)  
>
> add_service_files(FILES AddTwoInts.srv)

# 3 参数通信

![](http://www.autolabor.com.cn/book/ROSTutorials/assets/03ROS%E9%80%9A%E4%BF%A1%E6%9C%BA%E5%88%B603_%E5%8F%82%E6%95%B0%E6%9C%8D%E5%8A%A1%E5%99%A8.jpg)

参数服务器实现是最为简单的，该模型如下图所示,该模型中涉及到三个角色:

- ROS Master (管理者)
- Talker (参数设置者)
- Listener (参数调用者)

ROS Master 作为一个公共容器保存参数，Talker 可以向容器中设置参数，Listener 可以获取参数。

#### 1.Talker 设置参数

Talker 通过 RPC 向参数服务器发送参数(包括参数名与参数值)，ROS Master 将参数保存到参数列表中。

#### 2.Listener 获取参数

Listener 通过 RPC 向参数服务器发送参数查找请求，请求中包含要查找的参数名。

#### 3.ROS Master 向 Listener 发送参数值

ROS Master 根据步骤2请求提供的参数名查找参数值，并将查询结果通过 RPC 发送给 Listener。

------

参数可使用数据类型:

- 32-bit integers
- booleans
- strings
- doubles
- iso8601 dates
- lists
- base64-encoded binary data
- 字典

> 注意:参数服务器不是为高性能而设计的，因此最好用于存储静态的非二进制的简单数据

# Action通信方式

升级版的service

![](https://github.com/xiangzheng666/picx-images-hosting/raw/master/Snipaste_2021-12-22_23-44-16.2323ncilgg.webp)

