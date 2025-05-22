---
categories: [windows_ros]
tags: [ROS]
---
```python
# coding：<encoding name> ： # coding: utf-8

import rospy

from one.srv import test

import sys



if __name__ == "__main__":

  \# 2.初始化 ROS 节点

  rospy.init_node("AddInts_Client_p")

  \# 3.创建请求对象

  client = rospy.ServiceProxy("AddInts",test)

  client.wait_for_service()

  req = test()

  req.num1 = 1

  req.num2 = 2

  resp = client.call(req.num1,req.num2)

  rospy.loginfo("out:%d",resp.sum)
```

```python
# coding：<encoding name> ： # coding: utf-8
import rospy
from one.srv import test

def doReq(req):
    # 解析提交的数据
    sum = req.num1 + req.num2
    rospy.loginfo("get:num1 = %d, num2 = %d, sum = %d",req.num1, req.num2, sum)
    return sum


if __name__ == "__main__":

    rospy.init_node("addints_server_p")
    server = rospy.Service("AddInts",test,doReq)
    rospy.spin()
```



![](https://github.com/xiangzheng666/picx-images-hosting/raw/master/Snipaste_2021-12-22_22-10-25.2obr9nd1qw.webp)

![](https://github.com/xiangzheng666/picx-images-hosting/raw/master/Snipaste_2021-12-22_22-10-37.41yadoo3rt.webp)



#### 编译没有生成sitpackage中对应的srv文件等，删除build，devel重新catkin_make

