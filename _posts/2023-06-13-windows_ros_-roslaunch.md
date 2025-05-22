---
categories: [windows_ros]
tags: [roslaunch]
---
# launch文件使用

1. **调用**     roslaunch 包名 xxx.launch    
   - **注意:**roslaunch 命令执行launch文件时，首先会判断是否启动了 roscore,如果启动了，则不再启动，否则，会自动调用 roscore 

2. **文件标签**

   1. ```xml
      <launch>
      <launch deprecated="弃用说明" >
      ```

   2. ```xml
      <node>
      <node pkg="belong to pkg" >
      <node pkg="pkg" type="name of node">
      <node pkg type args="args">
      <node pkg type args machine="chose runing machine">
      <node pkg type args machine respawn="true|false auto restart after shutdown">
      <node pkg type args machine respawn respawn_delay="N wait N second">
      <node pkg type args machine rospawn rospawn_delay required="true|whether necessary">
      <node pkg type args machine rospawn rospawn_delay required ns="namespace">
      <node pkg type args rospawn rospawn_delay machine required ns clear_params="true|false">
      <node pkg type args rospawn machine required ns clear_params output="log|screen">
      <node pkg type name="命名空间显示的名称" args required machine output>
      ```

   3. ```xml
      <include>
      <include file="$(find pkg)/xxx/xxx.launch" ns="namespace">
      ```

   4. ```xml
      <remap from="x" to="y">话题改名
      ```

   5. ```xml
      <param>参数服务器上设置参数
      <param name="name" value="value" type="str|int|double|bool|yaml" commad textfile/>
      ```

   6. ```xml
      <rosparam command="load|dump|delete" file="$(find pkg)/..yaml" param="参数名称" ns>
      ```

   7. ```xml
      <arg>函数参数
      <arg name="name" default="value" value="value" doc="description">
      使用arg：<......="$(arg name)">
      ```

      

```xml
<launch>
	<node pkg="turtlesim" type="turtlesim_node" output="screen"/>
    <node pkg="teleop_twist_keyboard" type="teleop_twist_keyboard">

</launch>
```

