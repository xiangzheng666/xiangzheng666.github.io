---
categories: [BigData]
tags: [Kafka]
---
# Kafka


Kafka是一个分布式的基于发布/订阅模式的**消息队列，**主要应用于大数据实时处理领域



+ Kafka基础架构 

  - **（1）Producer ：**消息生产者，就是向kafka broker发消息的客户端；
  - **（2）Consumer ：**消息消费者，向kafka broker取消息的客户端；
  - **（3）Consumer Group （CG）：**消费者组，由多个consumer组成。消费者组内每个消费者负责消费不同分区的数据，一个分区只能由一个消费者消费；消费者组之间互不影响。所有的消费者都属于某个消费者组，即消费者组是逻辑上的一个订阅者。
  - **（4）Broker ：**一台kafka服务器就是一个broker。一个集群由多个broker组成。一个broker可以容纳多个topic。
  - **（5）Topic ：**可以理解为一个队列，生产者和消费者面向的都是一个topic；
  - **（6）Partition：**为了实现扩展性，一个非常大的topic可以分布到多个broker（即服务器）上，**一个topic可以分为多个partition**，每个partition是一个有序的队列；
  - **（7）Replica：**副本，为保证集群中的某个节点发生故障时，该节点上的partition数据不丢失，且kafka仍然能够继续工作，kafka提供了副本机制，一个topic的每个分区都有若干个副本，一个**leader**和若干个**follower**。
  - **（8）leader：**每个分区多个副本的“主”，生产者发送数据的对象，以及消费者消费数据的对象都是leader。
  - **（9）follower：**每个分区多个副本中的“从”，实时从leader中同步数据，保持和leader数据的同步。leader发生故障时，某个follower会成为新的leader。

+ Kafka存储 

  - topic 
    * partition:top-idnex 
      + log: 
        - segment:offset开始命名 
          * .log:data
          * .index:索引信息index:offset
        - segment
    * partition

+ Kafka生产者 

  - 分区策略 
    * **方便在集群中扩展**+**可以提高并发**
    * 数据分区的原则 
      + producer发送的数据封装成一个ProducerRecord对象
      + （1）指明 partition 的情况下，直接将指明的值直接作为 partiton 值；
      + （2）没有指明 partition 值但有 key 的情况下，将 key 的 hash 值与 topic 的 partition 数进行取余得到 partition 值；
      + （3）既没有 partition 值又没有 key 值的情况下，第一次调用时随机生成一个整数（后面每次调用在这个整数上自增），将这个值与 topic 可用的 partition 总数取余得到 partition 值，也就是常说的 round-robin 算法。
  - At Least Once + 幂等性 = Exactly Once 
    * Kafka的幂等性实现其实就是将原来下游需要做的去重放在了数据上游开启幂等性的
    * Producer在初始化的时候会被分配一个PID，发往同一Partition的消息会附带Sequence Number。而Broker端会对<PID, Partition, SeqNumber>做缓存，当具有相同主键的消息提交时，Broker只会持久化一条。
    * 当生产者挂了后，PID重启就会变化，同时不同的Partition也具有不同主键，所以幂等性无法保证跨分区跨会话的Exactly Once。
    * 为了实现跨分区跨会话的事务，需要引入一个全局唯一的Transaction ID，并将Producer获得的PID和Transaction ID绑定。这样当Producer重启后就可以通过正在进行的Transaction ID获得原来的PID。

+ broke数据可靠性保证 

  - partition向producer发送ack,否则重新发送数据 

  - **ack应答机制** 

    * 0：producer不等待broker的ack，这一操作提供了一个最低的延迟，broker一接收到还没有写入磁盘就已经返回，当broker故障时有可能**丢失数据**；
    * 1：producer等待broker的ack，partition的leader落盘成功后返回ack，如果在follower同步成功之前leader故障，那么将会**丢失数据**；
    * -1（all）：producer等待broker的ack，partition的leader和follower全部落盘成功后才返回ack。但是如果在follower同步完成后，broker发送ack之前，leader发生故障，那么会造成**数据重复**。

  - 副本数据同步 

    * | 半数以上完成同步，就发送ack | 延迟低                                             | 选举新的leader时，容忍n台节点的故障，需要2n+1个副本 |
      | --------------------------- | -------------------------------------------------- | --------------------------------------------------- |
      | **全部完成同步，才发送ack** | 选举新的leader时，容忍n台节点的故障，需要n+1个副本 | 延迟高                                              |

  - 同样为了容忍n台节点的故障，第一种方案需要2n+1个副本，而第二种方案只需要n+1个副本，而Kafka的每个分区都有大量的数据，第一种方案会造成大量数据的冗余。 

  *  虽然第二种方案的网络延迟会比较高，但网络延迟对Kafka的影响较小。 

-  故障处理 
   -  ISR ：Leader维护了一个动态的in-sync replica set (ISR)，意为和leader保持同步的follower集合。当ISR中的follower完成数据的同步之后，leader就会给producer发送ack。如果follower长时间未向leader同步数据，则该follower将被踢出ISR，该时间阈值由**replica.lag.time.max.ms**参数设定。Leader发生故障之后，就会从ISR中选举新的leader。
   -  LEO:每个副本的最后一个offset 
   -  HW:所有副本中最小的LEO 
   -  HW之前的数据才对Consumer可见 
   -  1.follower故障  follower发生故障后会被临时踢出ISR，待该follower恢复后，follower会读取本地磁盘记录的上次的HW，并将log文件高于HW的部分截取掉，从HW开始向leader进行同步。等该**follower的LEO大于等于该Partition的HW**，即follower追上leader之后，就可以重新加入ISR了。 
   -  2.leader故障  leader发生故障之后，会从ISR中选出一个新的leader，之后，为保证多个副本之间的数据一致性，其余的follower会先将各自的log文件高于HW的部分截掉，然后从新的leader同步数据。 注意：这只能保证副本之间的数据一致性，并不能保证数据不丢失或者不重复 

+  kafka消费者 
   - pull模式拉取，而不是broker的push，会适配消费者的消费能力
   - pull模式不足之处是，如果kafka没有数据，消费者可能会陷入循环中，一直返回空数据。针对这一点，Kafka的消费者在消费数据时会传入一个时长参数timeout，如果当前没有数据可供消费，consumer会等待一段时间之后再返回，这段时长即为timeout。
   - 分区分配 
     * roundrobin：将每个消费者轮流负责一组分区，即将所有分区平均分配给所有消费者，并保证每个消费者负责的分区数量尽可能相等。
     * Range分配策略（Range Assignor）：将每个消费者负责一组连续的分区，即对于所有分区，按照分区的起始位移排序，将排序后的所有分区均匀地分配给每个消费者。
     * Sticky分配策略（Sticky Assignor）：结合了Range和Round-robin两种分配策略的优点，保证在消费者组中增加或删除消费者时，尽可能地减少分区的重新分配。Sticky分配策略会首先使用Range分配策略将分区均匀地分配给消费者，然后再使用Round-robin分配策略将多余的分区分配给消费者。
   - 每个消费者会维护该消息的offset
+  高效传输数据 
   -  **1）顺序写磁盘**  
      Kafka的producer生产数据，要写入到log文件中，写的过程是一直追加到文件末端，为顺序写。官网有数据表明，同样的磁盘，顺序写能到到600M/s，而随机写只有100k/s。这与磁盘的机械机构有关，顺序写之所以快，是因为其省去了大量磁头寻址的时间。 
   -  **2）应用Pagecache**  
      Kafka数据持久化是直接持久化到Pagecache中，这样会产生以下几个好处：  
      I/O Scheduler 会将连续的小块写组装成大块的物理写从而提高性能  
      I/O Scheduler 会尝试将一些写操作重新按顺序排好，从而减少磁盘头的移动时间  
      充分利用所有空闲内存（非 JVM 内存）。如果使用应用层 Cache（即 JVM 堆内存），会增加 GC 负担  
      读操作可直接在 Page Cache 内进行。如果消费和生产速度相当，甚至不需要通过物理磁盘（直接通过 Page Cache）交换数据  
      如果进程重启，JVM 内的 Cache 会失效，但 Page Cache 仍然可用 
   -  **3）零复制技术** 
+  Controller 
   - Kafka集群中有一个broker会被选举为Controller，负责管理集群broker的上下线，所有topic的分区副本分配和leader选举等工作。
+  Kafka事务 
   - Producer事务：多个发送组成事务 
     * 回滚：设置topic不可见
   - consumer事务： 
     * Segment File生命周期问题，broker端无法保证多个pull的事务性
+  kafka消息发送 
   - **异步发送** 
     * **RecordAccumulator** 
       + 临时保存消息
     * **main线程** 
       + main线程将消息封装发送给RecordAccumulator
     * **Sender线程** 
       + Sender线程不断从RecordAccumulator中拉取消息发送到Kafka broker
   - 同步发送
+  kafka的consumer的offset维护 
   - Consumer消费数据时的可靠性是很容易保证的，因为数据在Kafka中是持久化的，故不用担心数据丢失问题。由于consumer在消费过程中可能会出现断电宕机等故障，consumer恢复后，需要从故障前的位置的继续消费，所以consumer需要实时记录自己消费到了哪个offset，以便故障恢复后继续消费。所以offset的维护是Consumer消费数据是必须考虑的问题。
   - 自动提交offset
   - 手动提交offset 
     * commitSync（同步提交） 
       + 会自动失败重试，一直到提交成功
     * commitAsync（异步提交）
   - 都有可能会造成数据的漏消费或者重复消费

