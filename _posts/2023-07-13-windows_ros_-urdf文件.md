---
categories: [windows_ros]
tags: [urdf]
---
# urdf文件

1. **使用**
   
- 在ns中设置一个参数<param name="name" textfile="$(find xx)/.../...urf">
   - 在rviz或者gazebo中加载
   
2. **语法**    ***单位：米制***

   - ```xml
     <robot name="robot_name">
     ```

   - ```xml
     1.<link "刚体部分"/>
     <robot name="a1">
         <link name="link_name">
             ....
         </link>
     </robot>
     
     <visual "外观"/>
     <robot>
         <link>
             <visual>
             	....
             </visual>
         </link>
     </robot>
     
     2.<geometry "形状"/>
     <robot>
     	<link>
         	<visual>
             	<geometry>
                     <box size="x y z"/>
                     <cylinder radius=1 length=2/>
                     <sphere radius=1/>
                     <mesh filename=""/>
                 </geometry>
             </visual>
         </link>
</robot>
     
     3.<origin "偏移量与倾斜弧度"/>
     <robot name>
         <link name>
             <visual>
             	<geometry>
                     ...
             	</geometry>
                 <origin xyz="x y z" rpy="x y z"/>
             </visual>
         </link>
     </robot>
     4.<metrial "材料属性(颜色)"/>
     <robot name>
         <link name>
             <visual>
             	<geometry>
                     ...
             	</geometry>
                 <origin/>
                 <metrial>
                 	<color rgba="r g b a"/>
                 </metrial>
             </visual>
         </link>
     </robot>   
     5.<collision "碰撞检测配置于visual类似"/>
     6.<inertial "惯性检测"/>
     <inertial>
         <origin xyz="0 0 0" />
         <mass value="6" "质量"/>
         <inertia ixx="1" ixy="0" ixz="0" iyy="1" iyz="0" izz="1" “惯性矩阵”/>
     </inertial>
     ```
     
   - ```xml
     1.<joint "关节"/>
     <joint name type="关节运动形式：continuous|revolute|prismatic|palner|..">
     </joint>
     2.<joint name type>
     	<parent link="name"/>
         <child link="name"/>
         <!-- 两个 link 的物理中心之间的偏移量 -->
             <origin xyz="0.2 0 0.075" rpy="0 0 0" />
             <axis xyz="0 0 1" />
     </joint>
     ```
   
     

