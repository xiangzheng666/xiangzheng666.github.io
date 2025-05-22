---
categories: [windows_ros]
tags: [ros]
---
# 1.概念

- 这是书上的
- ![](http://www.autolabor.com.cn/book/ROSTutorials/assets/%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F.jpg)

- ```
  WorkSpace --- 自定义的工作空间
  
      |--- build:编译空间，用于存放CMake和catkin的缓存信息、配置信息和其他中间文件。
  
      |--- devel:开发空间，用于存放编译后生成的目标文件，包括头文件、动态&静态链接库、可执行文件等。
  
      |--- src: 源码
  
          |-- package：功能包(ROS基本单元)包含多个节点、库与配置文件，包名所有字母小写，只能由字母、数字与下划线组成
  
              |-- CMakeLists.txt 配置编译规则，比如源文件、依赖项、目标文件
  
              |-- package.xml 包信息，比如:包名、版本、作者、依赖项...(以前版本是 manifest.xml)
  
              |-- scripts 存储python文件
  
              |-- src 存储C++源文件
  
              |-- include 头文件
  
              |-- msg 消息通信格式文件
  
              |-- srv 服务通信格式文件
  
              |-- action 动作格式文件
  
              |-- launch 可一次性运行多个节点 
  
              |-- config 配置信息
  
          |-- CMakeLists.txt: 编译的基本配置
  ```

- 理解的话就是work_space中可以包含多个package

- 注意devel的setup.bat激活当前功能包（package）

- 最注意package.xml（包含依赖关系）

  ```xml
  <?xml version="1.0"?>
  <!-- 格式: 以前是 1，推荐使用格式 2 -->
  <package format="2">
    <!-- 包名 -->
    <name>demo01_hello_vscode</name>
    <!-- 版本 -->
    <version>0.0.0</version>
    <!-- 描述信息 -->
    <description>The demo01_hello_vscode package</description>
  
   <!-- One maintainer tag required, multiple allowed, one person per tag -->
    <!-- Example:  -->
    <!-- <maintainer email="jane.doe@example.com">Jane Doe</maintainer> -->
    <!-- 维护人员 -->
    <maintainer email="xuzuo@todo.todo">xuzuo</maintainer>
  
    <!-- One license tag required, multiple allowed, one license per tag -->
    <!-- Commonly used license strings: -->
    <!--   BSD, MIT, Boost Software License, GPLv2, GPLv3, LGPLv2.1, LGPLv3 -->
    <!-- 许可证信息，ROS核心组件默认 BSD -->
    <license>TODO</license>
    <!-- 依赖的构建工具，这是必须的 -->
    <buildtool_depend>catkin</buildtool_depend>
  
    <!-- 指定构建此软件包所需的软件包 -->
    <build_depend>roscpp</build_depend>
    <build_depend>rospy</build_depend>
    <build_depend>std_msgs</build_depend>
  
    <!-- 指定根据这个包构建库所需要的包 -->
    <build_export_depend>roscpp</build_export_depend>
    <build_export_depend>rospy</build_export_depend>
    <build_export_depend>std_msgs</build_export_depend>
  
    <!-- 运行该程序包中的代码所需的程序包 -->  
    <exec_depend>roscpp</exec_depend>
    <exec_depend>rospy</exec_depend>
    <exec_depend>std_msgs</exec_depend>
  
  
    <!-- The export tag contains other, unspecified, tags -->
    <export>
      <!-- Other tools can request additional information be placed here -->
  
    </export>
  </package>
  ```

# 2.命令

- ```
  rospack find [package_name]
  ```

- ```
  roscd [package_name] 直接切换目录到某个软件包或者软件包集
  ```

- ```
  roscd log 进入存储ROS日志文件的目录
  ```

- ```
  rosls 直接按软件包的名称执行 ls 命令（而不必输入绝对路径）
  ```

## 创建catkin软件包

- ```
  首先 cd  .../catkin_ws/src
  ```

- ```
  catkin_create_pkg <package_name> [depend1] [depend2] [depend3]
  catkin_create_pkg <name>beginner_tutorials <依赖>std_msgs rospy roscpp
  ```

## 构建一个catkin工作区并生效配置文件

```
cd .../catkin_ws
catkin_make
.../catkin_ws/devel/setup.bash(激活)
```

## 软件包依赖关系

```
rospack depends1 <package_name>beginner_tutorials  （一级依赖）
rospack depends <package_name>beginner_tutorials  （所有依赖）
```

## 自定义软件包

 [package.xml](http://wiki.ros.org/catkin/package.xml) 配置：

- ```
  依赖管理
  <buildtool_depend>catkin</buildtool_depend>
  <build_depend>roscpp</build_depend>
  <build_depend>rospy</build_depend>
  <build_depend>std_msgs</build_depend>
  运行时依赖
  <exec_depend>roscpp</exec_depend>
  <exec_depend>rospy</exec_depend>
   <exec_depend>std_msgs</exec_depend>
  ```

## 使用catkin_make编译

```
catkin_make --source src路径
```

