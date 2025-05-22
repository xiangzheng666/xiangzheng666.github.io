---
categories: [BigData]
tags: [hadoop,Yarn]
---
# hadoop-Yarn


1)ResourceManager(RM):处理客户端请求;监控NodeManager;启动或监控ApplicationMaster;资源的分配与调度
2)NodeManager(NM):营理单个节点上的资源;处理来自RM的命令;处里来ApplicationMaster的命令
3)ApplicationMaster(AM):负责数据的切分;为应用程序申请资源并分配给内部的任务;任务的监控与容错
4)Container:Container是YARN中的资原抽象，它封装了某个节点上的多维度资源，如内存、CPU等。


+  Yarn工作机制 

```plain
（1）MR程序提交到客户端所在的节点。
（2）YarnRunner向ResourceManager申请一个Application。
（3）RM将该应用程序的资源路径返回给YarnRunner。
（4）该程序将运行所需资源提交到HDFS上。
（5）程序资源提交完毕后，申请运行mrAppMaster。
（6）RM将用户的请求初始化成一个Task。
（7）其中一个NodeManager领取到Task任务。
（8）该NodeManager创建容器Container，并产生MRAppmaster。
（9）Container从HDFS上拷贝资源到本地。
（10）MRAppmaster向RM 申请运行MapTask资源。
（11）RM将运行MapTask任务分配给另外两个NodeManager，
	另两个NodeManager分别领取任务并创建容器。
（12）MR向两个接收到任务的NodeManager发送程序启动脚本，
	这两个NodeManager分别启动MapTask，MapTask对数据分区排序。
（13）MrAppMaster等待所有MapTask运行完毕后，向RM申请容器，运行ReduceTask。
（14）ReduceTask向MapTask获取相应分区的数据。
（15）程序运行完毕后，MR会向RM申请注销自己。
```

 

+  作业提交 

```plain
（1）作业提交
    第1步：Client调用job.waitForCompletion方法，向整个集群提交MapReduce作业。
    第2步：Client向RM申请一个作业id。
    第3步：RM给Client返回该job资源的提交路径和作业id。
    第4步：Client提交jar包、切片信息和配置文件到指定的资源提交路径。
    第5步：Client提交完资源后，向RM申请运行MrAppMaster。
（2）作业初始化
    第6步：当RM收到Client的请求后，将该job添加到容量调度器中。
    第7步：某一个空闲的NM领取到该Job。
    第8步：该NM创建Container，并产生MRAppmaster。
    第9步：下载Client提交的资源到本地。
（3）任务分配
    第10步：MrAppMaster向RM申请运行多个MapTask任务资源。
    第11步：RM将运行MapTask任务分配给另外两个NodeManager，
    	   另两个NodeManager分别领取任务并创建容器。
（4）任务运行
    第12步：MR向两个接收到任务的NodeManager发送程序启动脚本，
           这两个NodeManager分别启动MapTask，MapTask对数据分区排序。
    第13步：MrAppMaster等待所有MapTask运行完毕后，向RM申请容器，运行ReduceTask。
    第14步：ReduceTask向MapTask获取相应分区的数据。
    第15步：程序运行完毕后，MR会向RM申请注销自己。
（5）进度和状态更新
    YARN中的任务将其进度和状态(包括counter)返回给应用管理器, 
    客户端每秒(通过mapreduce.client.progressmonitor.pollinterval设置)
    向应用管理器请求进度更新, 展示给用户。
（6）作业完成
    除了向应用管理器请求作业进度外, 客户端每5秒都会通过调用waitForCompletion()
    来检查作业是否完成。时间间隔可以通过mapreduce.client.completion.pollinterval来设置。
    作业完成之后, 应用管理器和Container会清理工作状态。
    作业的信息会被作业历史服务器存储以备之后用户核查。
```

 

+  资源调度策略 

```plain
1．先进先出调度器（FIFO）
2．容量调度器（Capacity Scheduler）
	1、支持多个队列，每个队列可配置一定的资源量，每个队列采用FIF0调度策略。
	2、为了防止同一个用户的作业独占队列中的资源，该调度器会对同一用户提交的作业所占资源量进行限定。
	3、首先，计算每个队列中正在运行的任务数与其应该分得的计算资源之间的比值，
	   选择一个该比值最小的队列一一最闲的。
	4、其次，按照作业优先级和提交时间顺序，同时考虑用户资源量限制和内存限制对队列内任务排序。
3．公平调度器（Fair Scheduler）
	1.支持多队列多作业，每个队列可以单独配置
    2.同一队列的作业按照其优先级分享整个队列的资源，并发执行
    3.每个作业可以设置最小资源值，调度器会保证作业获得其以上的资源
```

 

+  优化性能 

```plain
1 数据输入
    (1)合并小文件：在执行R任务前将小文件进行合并，大量的小文件会
    产生大量的Map任务，增大Map任务装载次数，而任务的装载比较耗时，从而
    导致R运行较慢。
    (2)采用CombineTextInputFormat来作为输入，解决输入端大量小文件场景。
2 Map阶段
    (1)减少谥写(Spill)次数：通过调整io.sort.mb及sot.spil.percenta参数
    值，增大触发Spil的内存上限，减少Spil次数，从而减少磁盘O.
    (2)减少合并(Merge)次数：通过调整io.sort.factor参数，增大Merge的
    文件数目，减少Merge的次数，从而缩短MR处理时间。
    (3)在Map之后，不影响业务逻辑前提下，先进行Combines处理，减少I/O。
3 Reduce阶段
    (1)合理设置Map和Reduce数：两个都不能设置太少，也不能设置太多。
    太少，会导致Task等待，延长处理时间；太多，会导致Map、Rece任务间竞
    争资源，造成处理超时等错误。
    (2)设置Map、Reduce共存：调整slowstart.completedmaps参数，使Map运
    行到一定程度后，Reduce也开始运行，减少Reducel的等待时间。
    (3)规避使用Reduce:因为Reduce?在用于连接数据集的时候将会产生大量
    的网络消耗。
    （4） 合理设置Reducei端的Buffer:默认情况下，数据达到一个阈值的时候，
        Buffer中的数据就会写入磁盘，然后Reduce?会从磁盘中获得所有的数据。也就是
        说，Buffer和Reduce是没有直接关联的，中间多次写磁盘->读磁盘的过程，既然
        有这个弊端，那么就可以通过参数来配置，使得Bffr中的一部分数据可以直接
        输送到Reduce,从而减少IO开销：mapreduce.reduce.input.buffer.percent,默认为
        0.0。当值大于0的时候，会保留指定比例的内存读Bffr中的数据直接拿给
        Reduce使用。这样一来，设置Buffer需要内存，读取数据需要内存，Reduce计算
        也要内存，所以要根据作业的运行情况进行调整。
4 I0传输
    1)采用数据压缩的方式，减少网络IO的的时间。安装Snappy和LZO压缩编
    码器。
    2)使用Sequence File.二进制文件。
5数据倾斜问题
    1.数据倾斜现象
    	数据频率倾斜一某一个区域的数据量要远远大于其他区域。
    	数据大小倾斜一部分记录的大小远远大于平均值。
    2.减少数据倾斜的方法
        方法1：抽样和范围分区
            可以通过对原始数据进行抽样得到的结果集来预设分区边界值。
        方法2：自定义分区
            基于输出键的背景知识进行自定义分区。例如，如果Mp输出键的单词来源于一本
            书。且其中某几个专业词汇较多。那么就可以自定义分区将这这些专业词汇发送给固
            定的一部分Reduce?实例。而将其他的都发送给剩余的Reduce?实例。
        方法3:Combine
            使用Combine可以大量地减小数据倾酴斜。在可能的情况下，Combine的目的就是
            聚合并精简数据。
        方法4：采用Map Join,尽量避免Reduce Join.
```

 

