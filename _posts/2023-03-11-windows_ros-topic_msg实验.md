---
categories: [windows_ros]
tags: [rospy]
---

# 编写py

```python
\# coding：<encoding name> ： # coding: utf-8

import rospy

from hello.msg import Person

def doPerson(p):

  print("lisnten:name:%s, age:%d, height:%.2f\n",p.name, p.age, p.height)

  \#1.初始化节点

  rospy.init_node("listener_person_p")

  \#2.创建订阅者对象

  sub = rospy.Subscriber("chatter_person",Person,doPerson)

  rospy.spin() #4.循环
```

 

```python
\# coding：<encoding name> ： # coding: utf-8

  import rospy

  from hello.msg import Person
     \#1.初始化 ROS 节点

  rospy.init_node("talker_person_p")

  \#2.创建发布者对象

  pub = rospy.Publisher("chatter_person",Person,queue_size=10)

  \#3.组织消息

  p = Person()

  p.name = "liu yu"

  p.age = 18

  p.height = 0.75


  \#4.编写消息发布逻辑

  rate = rospy.Rate(1)

  while not rospy.is_shutdown():

​    print("publish:name:%s, age:%d, heigh:%.2f\n",p.name, p.age, p.height)

​    pub.publish(p)  #发布消息

​    rate.sleep()  #休眠  #  运行
```

# 运行

![Snipaste_2021-12-21_23-27-27](https://github.com/xiangzheng666/picx-images-hosting/raw/master/Snipaste_2021-12-21_23-27-27.26lpl2bo5v.webp)
![Snipaste_2021-12-21_23-27-15](https://github.com/xiangzheng666/picx-images-hosting/raw/master/Snipaste_2021-12-21_23-27-15.7i0m5rxqtu.webp)

# 编写roslaunch文件

```xml
<launch>
  <node pkg="hello" name="hello-publish" type="publish.py" output="screen"/>
  <node pkg="hello" name="hello_subscribe" type="subscribe.py" output="screen"/>

</launch>
```

![Snipaste_2021-12-21_23-29-38](https://github.com/xiangzheng666/picx-images-hosting/raw/master/Snipaste_2021-12-21_23-29-38.1ap85m1zpx.webp)

# 注意

- rosrun hello  ..py时要保证python文件不报错才可以

- rosrun package名可能与文件名不一样

  