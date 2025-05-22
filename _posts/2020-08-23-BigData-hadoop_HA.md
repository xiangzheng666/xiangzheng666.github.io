---
categories: [BigData]
tags: [hadoop,HA]
---
# hadoop-HA


HDFS HA功能通过配置Active/Standby两个NameNodes实现在集群中对NameNode的热备来解决上述问题。



+  HDFS-HA 
    - CHANGE 
        * 元数据管理方式需要改变  
内存中各自保存一份元数据；  
Edits日志只有Active状态的NameNode节点可以做写操作；  
两个NameNode都可以读取Edits；  
共享的Edits放在一个共享存储中管理（qjournal和NFS两个主流实现）；
        * 需要一个状态管理功能模块  
实现了一个zkfailover，常驻在每一个namenode所在的节点，每一个zkfailover负责监控自己所在NameNode节点，利用zk进行状态标识，当需要进行状态切换时，由zkfailover来负责切换，切换时需要防止brain split现象的发生。
        * 必须保证两个NameNode之间能够ssh无密码登录
        * 隔离（Fence），即同一时刻仅仅有一个NameNode对外提供服务
    - 自动故障转移 
        * ZooKeeper和ZKFailoverController（ZKFC）
        * HA的自动故障转移依赖于ZooKeeper的以下功能： 
            + 故障检测  
集群中的每个NameNode在ZooKeeper中维护了一个持久会话，如果机器崩溃，ZooKeeper中的会话将终止，ZooKeeper通知另一个NameNode需要触发故障转移。
            + 现役NameNode选择  
ZooKeeper提供了一个简单的机制用于唯一的选择一个节点为active状态。如果目前现役NameNode崩溃，另一个节点可能从ZooKeeper获得特殊的排外锁以表明它应该成为现役NameNode。  
ZKFC是自动故障转移中的另一个新组件，是ZooKeeper的客户端，也监视和管理NameNode的状态。每个运行NameNode的主机也运行了一个ZKFC进程，ZKFC负责：
            + 健康监测  
ZKFC使用一个健康检查命令定期地ping与之在相同主机的NameNode，只要该NameNode及时地回复健康状态，ZKFC认为该节点是健康的。如果该节点崩溃，冻结或进入不健康状态，健康监测器标识该节点为非健康的。
            + ZooKeeper会话管理  
当本地NameNode是健康的，ZKFC保持一个在ZooKeeper中打开的会话。如果本地NameNode处于active状态，ZKFC也保持一个特殊的znode锁，该锁使用了ZooKeeper对短暂节点的支持，如果会话终止，锁节点将自动删除。
            + 基于ZooKeeper的选择  
如果本地NameNode是健康的，且ZKFC发现没有其它的节点当前持有znode锁，它将为自己获取该锁。如果成功，则它已经赢得了选择，并负责运行故障转移进程以使它的本地NameNode为Active。故障转移进程与前面描述的手动故障转移相似，首先如果必要保护之前的现役NameNode，然后本地NameNode转换为Active状态。
+  YARN-HA 
    - [http://hadoop.apache.org/docs/r3.1.3/hadoop-yarn/hadoop-yarn-site/ResourceManagerHA.html](bigdata_http:_hadoop.apache.org_docs_r2.7.2_hadoop-yarn_hadoop-yarn-site_resourcemanagerha)
    - 手动转换和故障转移  
当未启用自动故障转移时，管理员必须手动将其中一个 RM 转换为活动状态。要从一个 RM 故障转移到另一个，他们应该首先将 Active-RM 转换为 Standby，然后将 Standby-RM 转换为 Active。所有这些都可以使用“ yarn rmadmin ” CLI来完成。
    - 自动故障转移  
RM 可以选择嵌入基于 Zookeeper 的 ActiveStandbyElector 来决定哪个 RM 应该是活动的。当 Active 关闭或变得无响应时，另一个 RM 会自动选为 Active 然后接管。请注意，不需要像 HDFS 那样运行单独的 ZKFC 守护进程，因为嵌入在 RM 中的 ActiveStandbyElector 充当故障检测器和领导选举人，而不是单独的 ZKFC 守护进程。
    - RM 故障转移上的客户端、ApplicationMaster 和 NodeManager  
当有多个 RM 时，客户端和节点使用的配置（yarn-site.xml）应该列出所有 RM。客户端、ApplicationMasters (AM) 和 NodeManagers (NMs) 尝试以循环方式连接到 RM，直到它们命中活动 RM。如果 Active 出现故障，他们将恢复循环轮询，直到找到“新”Active。
+  HDFS Federation 
    - problem 
        * Namespace（命名空间）的限制  
由于NameNode在内存中存储所有的元数据（metadata），因此单个NameNode所能存储的对象（文件+块）数目受到NameNode所在JVM的heap size的限制。50G的heap能够存储20亿（200million）个对象，这20亿个对象支持4000个DataNode，12PB的存储（假设文件平均大小为40MB）。随着数据的飞速增长，存储的需求也随之增长。单个DataNode从4T增长到36T，集群的尺寸增长到8000个DataNode。存储的需求从12PB增长到大于100PB。
        * 隔离问题  
由于HDFS仅有一个NameNode，无法隔离各个程序，因此HDFS上的一个实验程序就很有可能影响整个HDFS上运行的程序。
        * 性能的瓶颈  
由于是单个NameNode的HDFS架构，因此整个HDFS文件系统的吞吐量受限于单个NameNode的吞吐量。
    - 多个名称节点/名称空间  
为了水平扩展名称服务，联邦使用多个独立的名称节点/名称空间。名称节点是联合的；Namenodes是独立的，不需要相互协调。Datanodes被所有Namenodes用作块的公共存储。每个 Datanode 都向集群中的所有 Namenode 注册。数据节点发送周期性心跳和块报告。它们还处理来自名称节点的命令。

