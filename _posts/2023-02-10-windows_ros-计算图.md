---
categories: [windows_ros]
tags: [计算图]
---
# 1.

计算图（Computation Graph）](http://wiki.ros.org/cn/ROS/Concepts#ROS.2Bi6F7l1b.2BXEJrIQ-)是一个由ROS进程组成的点对点网络，它们能够共同处理数据。ROS的基本计算图概念有节点（Nodes）、主节点（Master）、参数服务器（Parameter Server）、消息（Messages）、服务（Services）、话题（Topics）和袋（Bags），它们都以不同的方式向图（Graph）提供数据。

- [节点（Nodes）](http://wiki.ros.org/Nodes)：节点是一个可执行文件，它可以通过ROS来与其他节点进行通信。
- [消息（Messages）](http://wiki.ros.org/Messages)：订阅或发布话题时所使用的ROS数据类型。
- [话题（Topics）](http://wiki.ros.org/Topics)：节点可以将消息*发布*到话题，或通过*订阅*话题来接收消息。
- [主节点（Master）](http://wiki.ros.org/Master)：ROS的命名服务，例如帮助节点发现彼此。
- [rosout](http://wiki.ros.org/rosout)：在ROS中相当于`stdout/stderr（标准输出/标准错误）`。
- [roscore](http://wiki.ros.org/roscore)：主节点 + rosout + [参数服务器](http://wiki.ros.org/Parameter Server)（会在以后介绍）。

# 2.节点信息

```
rosnode list
rosnode info
rosrun [package_name] [node_name] __name:=my_turtle（自定义node名称）
rosnode ping [node_name]
```

# 3.rqt_graph

![ROS/Tutorials/UnderstandingTopics/rqt_graph_turtle_key.png](http://wiki.ros.org/ROS/Tutorials/UnderstandingTopics?action=AttachFile&do=get&target=rqt_graph_turtle_key.png)

如果把鼠标放在`/turtle1/command_velocity`上方，相应的ROS节点（这里是蓝色和绿色）和话题（这里是红色）就会高亮显示。可以看到，`turtlesim_node`和`turtle_teleop_key`节点正通过一个名为`/turtle1/command_velocity`的话题来相互通信。

![ROS/Tutorials/UnderstandingTopics/rqt_graph_turtle_key2.png](http://wiki.ros.org/ROS/Tutorials/UnderstandingTopics?action=AttachFile&do=get&target=rqt_graph_turtle_key2.png)