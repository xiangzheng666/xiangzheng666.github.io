---
categories: [BigData]
tags: [Zookeeper]
---
# Zookeeper


分布式应用程序的分布式协调服务



+  角色 
    - Leader：它负责 发起并维护与各 Follwer 及 Observer 间的心跳。所有的写操作必须要通过 Leader 完成再由 Leader 将写操作广播给其它服务器。一个 Zookeeper 集群同一时间只会有一个实际工作的 Leader。
    - Follower：它会响应 Leader 的心跳。Follower 可直接处理并返回客户端的读请求，同时会将写请求转发给 Leader 处理，并且负责在 Leader 处理写请求时对请求进行投票。一个 Zookeeper 集群可能同时存在多个 Follower。
    - Observer：角色与 Follower 类似，但是无投票权。目的是提高写性能
+  ZooKeeper 数据模型 
    -  ZooKeeper 提供的名称空间与标准文件系统的名称空间非常相似。名称是由斜杠 (/) 分隔的一系列路径元素。ZooKeeper 命名空间中的每个节点都由路径标识。 
    -  
    -  节点 
        * 持久(Persistent)：客户端和服务器端断开连接后，创建的节点不删除  
短暂(Ephemeral)：客户端和服务器端断开连接后，创建的节点自己删除
        * 每个 znode 节点在存储数据的同时，都会维护一个叫做 Stat 的数据结构
        * 
+  同步原理 
    - Leader 服务会为每一个 Follower 服务器分配一个单独的队列，然后将事务 Proposal 依次放入队列中，并根据 FIFO(先进先出) 的策略进行消息发送。Follower 服务在接收到 Proposal 后，会将其以事务日志的形式写入本地磁盘中，并在写入成功后反馈给 Leader 一个 Ack 响应。当 Leader 接收到超过半数 Follower 的 Ack 响应后，就会广播一个 Commit 消息给所有的 Follower 以通知其进行事务提 
        * Leader 等待 Server 连接；
        * Follower 连接 Leader，将最大的 zxid 发送给 Leader；
        * Leader 根据 Follower 的 zxid 确定同步点；
        * 完成同步后通知 follower 已经成为 uptodate 状态；
        * Follower 收到 uptodate 消息后，又可以重新接受 client 的请求进行服务了
+  监听原理： 
    - 首先要有一个maim线程：main线程中创建Zookeeper?客户端，这时就会创建两个线  
程，一个负责网络连愤通信(connet)，一个负责监听(listener).
    - 通过connect线程将注册的监听事件发送给Zookeeper.
    - 在Zookeeper的注册监听器列表中将注册的监听事件添加到列表中。
    - Zookeeper!监听到有数据或路径变化，就会将这个消息发送  
给listener线程。
    - listener线程内部调用了process(0方法。
+  常见的监听 
    - 监听节点数据的变化  
get path [watch]
    - 监听子节点增减的变化  
Is path [watch]
+  选举机制 
    -  半数机制：集群中半数以上机器存活，集群可用。所以Zookeeper适合安装奇数台服务器。 
    -  Zookeeper虽然在配置文件中并没有指定Master和Slave。但是，Zookeeper工作时，是有一个节点为Leader，其他则为Follower，Leader是通过内部的选举机制临时产生的。 
    -  5台服务启动选举 
        *  （1）服务器1启动，发起一次选举。服务器1投自己一票。此时服务器1票数一票，不够半数以上（3票），选举无法完成，服务器1状态保持为LOOKING； 
        *  （2）服务器2启动，再发起一次选举。服务器1和2分别投自己一票并交换选票信息：此时服务器1发现服务器2的ID比自己目前投票推举的（服务器1）大，更改选票为推举服务器2。此时服务器1票数0票，服务器2票数2票，没有半数以上结果，选举无法完成，服务器1，2状态保持LOOKING 
        *  （3）服务器3启动，发起一次选举。此时服务器1和2都会更改选票为服务器3。此次投票结果：服务器1为0票，服务器2为0票，服务器3为3票。此时服务器3的票数已经超过半数，服务器3当选Leader。服务器1，2更改状态为FOLLOWING，服务器3更改状态为LEADING； 
        *  （4）服务器4启动，发起一次选举。此时服务器1，2，3已经不是LOOKING状态，不会更改选票信息。交换选票信息结果：服务器3为3票，服务器4为1票。此时服务器4服从多数，更改选票信息为服务器3，并更改状态为FOLLOWING； 
        *  （5）服务器5启动，同4一样当小弟。 
+  写数据 
    - Client向ZooKeeper的Server1上写数据，发送一个写请求。
    - 如果Server1不是Leader,那么Server1会把接受到的请求进一步转发给Leader,因为每个ZooKee印et的Server里面有一个是Leader.。这个Leader会将写请求广播给各个Server,比如Server 13和Server2,各个Server会将该写请求加入待写队列，并向Leader发送成功信息。
    - 当Leaderl收到半数以上Server的成功信息，说明该写操作可以执行。Leader会向各个Server发送提交信息，各个Server收到信息后会落实队列里的写请求，此时写成功。
    - Server1会进一步通知Client数据写成功了，这时就认为整个写操作成功。

