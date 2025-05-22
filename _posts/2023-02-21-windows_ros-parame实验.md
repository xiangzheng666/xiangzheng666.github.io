---
categories: [windows_ros]
tags: [rospy]
---
```python
import rospy
if __name__ == "__main__":
    rospy.init_node("get_param_p")
    a=rospy.get_param('a',1000)
    rospy.loginfo("date_a:%d",a)
    b=rospy.get_param_cached('b')
    rospy.loginfo("cache_date_a:%d",a)
    names = rospy.get_param_names()
    for name in names:
        rospy.loginfo("name = %s",name)
    rospy.loginfo("-"*80)
    flag = rospy.has_param("p_int")
    rospy.loginfo("include p_int%d",flag)
    key = rospy.search_param("p_int")
    rospy.loginfo("seraach_key = %s",key)
    key = rospy.search_param("a")
    rospy.loginfo("serach_key_a = %s",key)
```

```python
if __name__ == "__main__":
    rospy.init_node("delete_param")

    try:
        rospy.delete_param("a")
    except Exception as e:
        rospy.loginfo("fail")
```

```python
import rospy

if __name__ == "__main__":
    rospy.init_node('set_param')
    rospy.set_param('a',100)
    rospy.set_param('b',"hello")
```

![](https://github.com/xiangzheng666/picx-images-hosting/raw/master/Snipaste_2021-12-22_22-43-43.5j4fffs8im.webp)



