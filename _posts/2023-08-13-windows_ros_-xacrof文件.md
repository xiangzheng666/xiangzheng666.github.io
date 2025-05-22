---
categories: [windows_ros]
tags: [xacro]
---
# xacro文件

1. **使用**
   
   ```xml
   <!-- 根标签，必须声明 xmlns:xacro -->
   <robot name="my_base" xmlns:xacro="http://www.ros.org/wiki/xacro">
   ```
   
   先要转化成urdf：rosun xacro xacro xxx.xacro > xxx.urdf 在讲urdf文件读入param中
   
   或者直接
   
   ```xml
   <param name command="$(find xacro) xacro $find(pkg)/....xacro">进行xacro文件加载
   ```
   
2. **语法**    ***单位：米制***

   - ```xml
     1.属性
     	<xacro:property name="name" value="value"/>定义属性
   	$(name)调用属性
     	$(数学表达式)
     2.宏
     	<xacro:macro name params>
     		$(param)调用参数
     	</xacro:macro>      宏定义
     	<xacro:macro param=""../>   宏调用
     3.文件包含
     	<xacro:include filename="...">
     ```
     

3. ***与gazebo集成***

   - ```xml
     <依赖包: urdf、xacro、gazebo_ros、gazebo_ros_control、gazebo_plugins/>
     
     注意， 当 URDF 需要与 Gazebo 集成时，和 Rviz 有明显区别:
     
     1.必须使用 collision 标签，因为既然是仿真环境，那么必然涉及到碰撞检测，collision 提供碰撞检测的依据。
     
     2.必须使用 inertial 标签，此标签标注了当前机器人某个刚体部分的惯性矩阵，用于一些力学相关的仿真计算。
     
     3.颜色设置，也需要重新使用 gazebo 标签标注，因为之前的颜色设置为了方便调试包含透明度，仿真环境下没有此选项。
     ```


4. ***roslaunch文件加载***

   - ```xml
     <launch>
         <param name textfile/>
         <!-- 启动 gazebo -->
         <include file="$(find gazebo_ros)/launch/empty_world.launch" >
         	<arg name="world_name" value="$(find gazebo_urf)/worlds/csis.xml" />
         </include>
         <!-- 在 gazebo 中显示机器人模型 -->
         <node pkg="gazebo_ros" type="spawn_model" name="model" args="-urdf -model mycar -param name"  />
     </launch>
     ```

5. **inertial标签**

   - ```xml
     惯性矩阵的设置需要结合link的质量与外形参数动态生成，标准的球体、圆柱与立方体的惯性矩阵公式如下(已经封装为 xacro 实现):
     
     球体惯性矩阵
     <!-- Macro for inertia matrix -->
     <xacro:macro name="sphere_inertial_matrix" params="m r">
         <inertial>
             <mass value="${m}" />
             <inertia ixx="${2*m*r*r/5}" ixy="0" ixz="0"
                      iyy="${2*m*r*r/5}" iyz="0" 
                      izz="${2*m*r*r/5}" />
         </inertial>
     </xacro:macro>
     
     圆柱惯性矩阵
     <xacro:macro name="cylinder_inertial_matrix" params="m r h">
         <inertial>
             <mass value="${m}" />
             <inertia ixx="${m*(3*r*r+h*h)/12}" ixy = "0" ixz = "0"
                      iyy="${m*(3*r*r+h*h)/12}" iyz = "0"
                      izz="${m*r*r/2}" /> 
         </inertial>
     </xacro:macro>
     
     立方体惯性矩阵
      <xacro:macro name="Box_inertial_matrix" params="m l w h">
          <inertial>
              <mass value="${m}" />
              <inertia ixx="${m*(h*h + l*l)/12}" ixy = "0" ixz = "0"
                       iyy="${m*(w*w + l*l)/12}" iyz= "0"
                       izz="${m*(w*w + h*h)/12}" />
          </inertial>
     </xacro:macro>
     ```
     


