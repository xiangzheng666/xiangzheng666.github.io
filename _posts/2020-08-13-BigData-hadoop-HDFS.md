---
categories: [BigData]
tags: [hadoop,HDFS]
---
# Hadoop-HDFS


HDFS的使用场景：适合一次写入，多次读出的场景，且不支持文件的修改。适合用来做数据分析，并不适合用来做网盘应用



+  shell 

```plain
上传
hadoop fs -moveFromLocal
hadoop fs -copyFromLocal/hadoop fs -put
hadoop fs -appendToFile
下载
hadoop fs -get 
hadoop fs -getmerge 
常用
hadoop fs -ls/-mkdir -p/-cat/-chmod/-chown/-rm/-rmdir..
文件副本数量
hadoop fs -setrep
```

 

+  HDFS的写数据流 

```plain
1.客户端向NameNode请求上传文件，NameNode检查目标文件是否已存在，父目录是否存在。
2.NameNode返回是否可以上传
3.客户端请求第一个 Block上传到哪几个DataNode服务器上。
4.NameNode返回3个DataNode节点，分别为dn1、dn2、dn3。
5.客户端通过FSDataOutputStream模块请求dn1上传数据，dn1收到请求会继续调用dn2，然后dn2调用dn3，将这个通信管道建立完成。
6.dn1、dn2、dn3逐级应答客户端。
7.客户端开始往dn1上传第一个Block（先从磁盘读取数据放到一个本地内存缓存），以Packet为单位，dn1收到一个Packet就会传给dn2，dn2传给dn3；dn1每传一个packet会放入一个应答队列等待应答。
8.当一个Block传输完成之后，客户端再次请求NameNode上传第二个Block的服务器。（重复执行3-7步）。
----
网络拓扑-节点距离计算：两个节点到达最近的共同祖先的距离总和
----
上传数据副本位置
1.Client所处的节点上，如果客户端在集群外，随机选一个。
2.第二个副本和第一个副本位于相同机架，随机节点。
3.第三个副本位于不同机架，随机节点。
```

 

+  HDFS的读数据流 

```plain
1.客户端通过Distributed FileSystem向NameNode请求下载文件，NameNode通过查询元数据，找到文件块所在的DataNode地址。
2.挑选一台DataNode（就近原则，然后随机）服务器，请求读取数据。
3.DataNode开始传输数据给客户端（从磁盘里面读取数据输入流，以Packet为单位来做校验）。
4.客户端以Packet为单位接收，先在本地缓存，然后写入目标文件。
```

 

+  NameNode和SecondaryNameNode 

```plain
FsImage：产生在磁盘中备份元数据的 hdfs oiv -p 文件类型 -i镜像文件 -o 转换后文件输出路径
Edits:修改内存中的元数据并追加到Edits中 hdfs oev -p 文件类型 -i编辑日志 -o 转换后文件输出路径
2NN：
1）第一阶段：NameNode启动
（1）第一次启动NameNode格式化后，创建Fsimage和Edits文件。如果不是第一次启动，直接加载编辑日志和镜像文件到内存。
（2）客户端对元数据进行增删改的请求。
（3）NameNode记录操作日志，更新滚动日志。
（4）NameNode在内存中对元数据进行增删改。
2）第二阶段：Secondary NameNode工作
（1）Secondary NameNode询问NameNode是否需要CheckPoint。直接带回NameNode是否检查结果。
（2）Secondary NameNode请求执行CheckPoint。
（3）NameNode滚动正在写的Edits日志。
（4）将滚动前的编辑日志和镜像文件拷贝到Secondary NameNode。
（5）Secondary NameNode加载编辑日志和镜像文件到内存，并合并。
（6）生成新的镜像文件fsimage.chkpoint。
（7）拷贝fsimage.chkpoint到NameNode。
（8）NameNode将fsimage.chkpoint重新命名成fsimage。
```

 

+  安全模式 

```plain
l、NameNode启动
NameNode启动时，首先将镜像文件(Fsimage)载入内存，并执行编辑日志(Edits)中的各项操作。一
旦在内存中成功建立文件系统元数据的映像，则创建一个新的Fsimage文件和一个空的编辑日志。此时，
NameNode开始监听DataNodei请求。这个过程期间，NameNode-一直运行在安全模式，即NameNode的文件系
统对于客户端来说是只读的。
2、DataNode启动
系统中的数据块的位置并不是由NameNode维护的，而是以块列表的形式存储在DataNode中。在系统的
正常操作期间，NameNode会在内存中保留所有块位置的映射信息。在安全模式下，各个DataNode会向
NameNode发送最新的块列表信息，NameNode了解到足够多的块位置信息之后，即可高效运行文件系统。
3、安全模式退出判断
如果满足“最小副本条件”，NameNode会在30秒钟之后就退出安全模式。所谓的最小副本条件指的是在
整个文件系统中99.9%的块满足最小副本级别(默认值：dfs.replication.mi=1)。在启动一个刚刚格式化的
HDFS集群时，因为系统中还没有任何块，所以NameNode不会进入安全模式。
```

 

+  DataNode工作机制 

```plain
（1）一个数据块在DataNode上以文件形式存储在磁盘上，包括两个文件，一个是数据本身，一个是元数据包括数据块的长度，块数据的校验和，以及时间戳。
（2）DataNode启动后向NameNode注册，通过后，周期性（1小时）的向NameNode上报所有的块信息。
（3）心跳是每3秒一次，心跳返回结果带有NameNode给该DataNode的命令如复制块数据到另一台机器，或删除某个数据块。如果超过10分钟没有收到某个DataNode的心跳，则认为该节点不可用。
（4）集群运行中可以安全加入和退出一些机器。

----数据完整性
（1）当DataNode读取Block的时候，它会计算CheckSum。
（2）如果计算后的CheckSum，与Block创建时值不一样，说明Block已经损坏。
（3）Client读取其他DataNode上的Block。
（4）DataNode在其文件创建后周期验证CheckSum。

----节点操作
服役新数据节点 
1.hdfs --daemon start datanode
2.yarn-daemon.sh start nodemanager
3.start-balancer.sh
退役旧数据节点
1.vi dfs.hosts
2.hdfs-site.xml配置文件中增加dfs.hosts属性/hdfs-site.xml配置文件中增加dfs.hosts.exclude属性
3.hdfs dfsadmin -refreshNodes
4.yarn rmadmin -refreshNodes
Datanode多目录配置
<property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///${hadoop.tmp.dir}/dfs/data1,
        file:///${hadoop.tmp.dir}/dfs/data2</value>
</property>
```

 

