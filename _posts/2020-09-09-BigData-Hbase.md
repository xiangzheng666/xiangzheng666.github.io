---
categories: [BigData]
tags: [Pulsar]
---
# Hbase


HBase是一种分布式、可扩展、支持海量数据存储的NoSQL数据库。



+ 数据模型 

  -  **Name Space**：命名空间，类似于关系型数据库的DatabBase概念，每个命名空间下有多个表。HBase有两个自带的命名空间，分别是hbase和default，hbase中存放的是HBase内置的表，default表是用户默认使用的命名空间。 

  - **Region**：类似于关系型数据库的表概念。不同的是，HBase定义表时只需要声明列族即可，不需要声明具体的列。这意味着，往HBase写入数据时，字段可以动态、按需指定。因此，和关系型数据库相比，HBase能够轻松应对字段变更的场景。 

  - **Row：** HBase表中的每行数据都由一个**RowKey**和多个**Column**（列）组成，数据是按照RowKey的字典顺序存储的，并且查询数据时只能根据RowKey进行检索，所以RowKey的设计十分重要。 
  - **Column**：HBase中的每个列都由Column Family(列族)和Column Qualifier（列限定符）进行限定，例如info：name，info：age。建表时，只需指明列族，而列限定符无需预先定义。 
  - **Time** **Stamp**： 用于标识数据的不同版本（version），每条数据写入时，如果不指定时间戳，系统会自动为其加上该字段，其值为写入HBase的时间。 
  - **Cell** 由{rowkey, column Family：column Qualifier, time Stamp} 唯一确定的单元。cell中的数据是没有类型的，全部是字节数组形式存贮。 

+  架构 
   -  1.  **Region** **Server**  
          Region Server为 Region的管理者，其实现类为HRegionServer，主要作用如下:  
          对于数据的操作：get, put, delete  
          对于Region的操作：splitRegion、compactRegion。 
      2.  **Master**  
          Master是所有Region Server的管理者，其实现类为HMaster，主要作用如下：  
          对于表的操作：create, delete, alter  
          对于RegionServer的操作：分配regions到每个RegionServer，  
          监控每个RegionServer的状态，负载均衡和故障转移。 
      3.  **Zookeeper**  
          HBase通过Zookeeper来做Master的高可用、RegionServer的监控、元数据的入口以及集群配置的维护等工作。 
      4.  **HDFS**  
          HDFS为HBase提供最终的底层数据存储服务，同时为HBase提供高可用的支持。 
+  存储结构 
   - HRegionServer 
     * HRegion: 维护一段连续的行键范围，存储在一个或多个HDFS文件中 
       + store: 一个列族，存储该列族的数据 
         - mem store: 内存存储组件，用于存储最新的写入数据 
           * wal:由于数据要经MemStore排序后才能刷写到HFile，但把数据保存在内存中会有很高的概率导致数据丢失，为了解决这个问题，数据会先写在一个叫做Write-Ahead logfile的文件中，然后再写入MemStore中。所以在系统出现故障的时候，数据可以通过这个日志文件重建。
         - storeFile: 磁盘存储组件，用于存储已经flush到磁盘的数据 
           * HFile: StoreFile的具体实现，它是一种基于Hadoop的文件格式
     * HLog: HLog是HBase中的写前日志，用于记录每次写操作，以保证数据的可靠性。HLog中的数据会定期flush到磁盘中的HLog文件中，并且会定期清理已经过期的HLog文件。
+  zookeeper 
   -  /hbase：HBase在ZooKeeper中的根节点，所有HBase相关的节点都注册在该节点下。 
   -  /hbase/meta-region-server：该节点记录了hbase:meta表所在的RegionServer的地址信息。 
   -  /hbase/namespace：该节点记录了HBase中所有命名空间的信息，包括命名空间的名称和表的列表等。 
   -  /hbase/rs：该节点记录了HBase集群中所有RegionServer的信息，包括RegionServer的地址和状态信息等。 
   -  /hbase/table：该节点记录了HBase中所有表的信息，包括表名、列族、Region的分布信息等。 
   -  /hbase/backup：该节点用于HBase的备份和恢复操作，记录了备份和恢复相关的信息。 
   -  /hbase/quota：该节点记录了HBase中的配额信息，包括表的容量限制、读写限制等。 

除了以上节点，还有一些临时节点和锁节点，用于实现HBase集群中各个节点之间的协调和同步操作。这些节点的作用是管理和维护HBase集群的状态信息和元数据信息，以及协调各个节点之间的操作。通ZooKeeper，HBase集群中的各个节点可以实时获取、更新和同步状态信息，从而保证集群的可靠性和高可用性。 

+  写流程 
   1.  Client先访问zookeeper，获取hbase:meta表位于哪个Region Server。 
   2.  访问对应的Region Server，获取hbase:meta表，根据读请求的namespace:table/rowkey，查询出目标数据位于哪个Region Server中的哪个Region中。并将该table的region信息以及meta表的位置信息缓存在客户端的meta cache，方便下次访问。 
   3.  与目标Region Server进行通讯； 
   4.  将数据顺序写入（追加）到WAL； 
   5.  将数据写入对应的MemStore，数据会在MemStore进行排序； 
   6.  向客户端发送ack； 
   7.  等达到MemStore的刷写时机后，将数据刷写到HFile。 
+  读流程 
   1.  Client先访问zookeeper，获取hbase:meta表位于哪个Region Server。 
   2.  访问对应的Region Server，获取hbase:meta表，根据读请求的namespace:table/rowkey，查询出目标数	据位于哪个Region Server中的哪个Region中。并将该table的region信息以及meta表的位置信息缓存在客户端的meta cache，方便下次访问。 
   3.  与目标Region Server进行通讯； 
   4.  分别在Block Cache（读缓存），MemStore和Store File（HFile）中查询目标数据，并将查到的所有数据	进行合并。此处所有数据是指同一条数据的不同版本（time stamp）或者不同的类型（Put/Delete）。 
   5.  将从文件中查询到的数据块（Block，HFile数据存储单元，默认大小为64KB）缓存到Block Cache。 
   6.  将合并后的最终结果返回给客户端。 
+  MemStore Flush 
   1.  当某个memstroe的大小达到了**hbase.hregion.memstore.flush.size（默认值128M）**，其所在region的所有memstore都会刷写。当memstore的大小达到了hbase.hregion.memstore.flush.size（默认值128M）hbase.hregion.memstore.block.multiplier（默认值4）时，会阻止继续往该memstore写数据。 
   2.  当region server中memstore的总大小达到java_heapsize_hbase.regionserver.global.memstore.size（默认值0.4）_hbase.regionserver.global.memstore.size.upper.limit（默认值0.95），region会按照其所有memstore的大小顺序（由大到小）依次进行刷写。直到region server中所有memstore的总大小减小到hbase.regionserver.global.memstore.size.lower.limit以下。当region server中memstore的总大小达到ava_heapsize*hbase.regionserver.global.memstore.size（默认值0.4）时，会阻止继续往所有的memstore写数据。 
   3.  到达自动刷写的时间，也会触发memstore flush。自动刷新的时间间隔由该属性进行配置hbase.regionserver.optionalcacheflushinterval（默认1小时）。 

4)当WAL文件的数量超过**hbase.regionserver.max.logs**，region会按照时间顺序依次进行刷写，直到WAL文件数量减小到**hbase.regionserver.max.log**以下（该属性名已经废弃，现无需手动设置，最大值为32） 

+  StoreFile Compaction：memstore每次刷写都会生成一个新的HFile，且同一个字段的不同版本（timestamp）和不同类型（Put/Delete）有可能会分布在不同的HFile中，因此查询时需要遍历所有的HFile。为了减少HFile的个数，以及清理掉过期和删除的数据，会进行StoreFile Compaction。 
   - Minor Compaction会将临近的若干个较小的HFile合并成一个较大的HFile，但**不会**清理过期和删除的数据
   - Major Compaction会将一个Store下的所有的HFile合并成一个大HFile，并且**会**清理掉过期和删除的数据。
+  Region Split 
   -  随着数据的不断写入，Region会自动进行拆分  
      当1个region中的某个Store下所有StoreFile的总大小超过hbase.hregion.max.filesize，该Region就会进行拆分（0.94版本之前）。  
      当1个region中的某个Store下所有StoreFile的总大小超过Min(R^2 * "hbase.hregion.memstore.flush.size",hbase.hregion.max.filesize")，该Region就会进行拆分，其中R为当前Region Server中属于该Table的个数（0.94版本之后）。 

# Phoenix


Phoenix是HBase的开源SQL。可以使用标准JDBC API代替HBase客户端API来创建表，插入数据和查询HBase数据。



+  在HBase中创建的表，通过Phoenix是查看不到的。如果要在Phoenix中操作直接在HBase中创建的表，则需要在Phoenix中进行表的映射。映射方式有两种：视图映射和表映射。 
+  Phoenix二级索引 
   -  Global Index是默认的索引格式，全局索引适用于多读少写的业务场景,创建全局索引时，会在HBase中建立一张新表。也就是说索引数据和数据表是存放在不同的表中的，写数据的时候会消耗大量开销，因为索引表也要更新，而索引表是分布在不同的数据节点上的，跨节点的数据传输带来了较大的性能消耗。 
      * 实际上创建新表，row=索引+原始rowkey，value=0
      * 多级索引，row=索引1+索引1+原始rowkey，value=0
      * 单个索引1include（索引2，索引3）， 
        + row=索引1+原始rowkey，value=索引2，
        + row=索引1+原始rowkey，value=索引3，
   -  Local Index适用于写操作频繁的场景。  
      索引数据和数据表的数据是存放在同一张表中（且是同一个Region），避免了在写操作的时候往不同服务器的索引表中写索引带来的额外开销。查询的字段不是索引字段索引表也会被使用，这会带来查询速度的提升 
       * 在本表中插入新数据行 
         + key:索引+原始rowkey

HBase 和 Hive 都是在 Hadoop 生态系统中广泛使用的大数据存储和处理技术，它们可以相互集成，实现更强大的功能。

具体来说，Hive 可以通过 HBase 存储后端来实现对 HBase 中数据的查询和分析。Hive 默认使用 HDFS 作为其存储后端，但是通过将 Hive 表映射到 HBase 中的表，可以方便地在 Hive 中对 HBase 数据进行查询和分析。在这种情况下，Hive 可以利用 HBase 的快速查询特性，同时还可以使用 Hive 自带的 SQL 查询语言。

另外，HBase 也可以通过 Hive 来实现数据的加载和导入。Hive 提供了多种数据导入格式和方法，例如使用 Sqoop 或者直接从本地文件系统中加载数据。通过将数据加载到 Hive 中，可以方便地将数据导入到 HBase 中。