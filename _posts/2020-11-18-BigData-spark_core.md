---
categories: [BigData]
tags: [Spark core]
---
# spark core


+  集群 
    - 驱动器节点（Driver Node）：驱动器节点是 Spark 应用程序的核心节点，它负责整个应用程序的流程控制和协调工作。驱动器节点通常是 Spark 应用程序的入口点，负责从输入源中读取数据，并将数据分发到集群中的工作节点上进行处理。同时，驱动器节点还负责将处理结果返回给客户端或输出到外部存储系统中。
    - 管理节点（Master Node）：管理节点是 Spark 集群的管理节点，它负责协调集群中的资源分配和任务调度等工作。管理节点通常是 Spark Standalone 模式下的 Master 节点、YARN 模式下的 ResourceManager 节点或 Mesos 模式下的 Mesos Master 节点。
    - 工作节点（Worker Node）：工作节点是 Spark 集群中的工作节点，它负责执行 Spark 应用程序中的任务。工作节点上运行着 Spark 的执行引擎，可以处理由驱动器节点分发过来的任务，并将处理结果返回给驱动器节点。
+  RDD:(Resilient Distributed Dataset).叫做弹性分布式数据集，是Spark中最基本的数据抽象。  
代码中是一个抽象类，它代表一个弹性的、不可变、可分区、里面的元素可并行计算的集合。 
+  RDD创建 
    - 1）从集合中创建RDD，Spark]主要提供了两种函数： 
        * sc.parallelize： 用于将一个已有的集合（例如Python中的列表或NumPy中的数组）转换为一个RDD
        * sc.makeRDD： 可以从一个已有的RDD、一个Hadoop文件、一个本地文件系统文件或一个外部数据源中创建RDD
        * 分区中元素是一个任意对象
    - 2）从外部存储系统的数据集创建 
        * sc.textFile("input")
        * 分区中元素是一行
    - 分区规则 
        * 默认分区cpu核心
        * 指定分区 
            + 0xdatalenth/split_num----1xdatalenth/split_num..
+  Transformation转换算子 
    - Value类型 
        * map() 对分区中的每一个元素进行map中的函数处理
        * mapPartitions()  会一次处理分区所以元素，输入一个迭代器
        * mapPartitionsWithIndex()  会一次处理分区，额外输出分区号
        * flatMap()   对分区中的每一个元素flat，在进行map中的函数处理
        * glom(): 分区聚合成数组
        * groupBy()分组进入不同分区，会shuffle落盘
        * filter()
        * sample()采样
        * distinct()去重 
            + `distinct()`方法会先使用`map()`方法将RDD中的每个元素映射为`(element, null)`的形式，然后使用`reduceBykey()`方法对元素进行哈希分区，将相同哈希值的元素划分到同一个分区内。在每个分区内，使用Scala自带的`distinct()`方法对元素进行去重，最后将所有分区中的元素按照分区顺序进行合并，得到一个去重后的RDD
        * coalesce()重新分区  (2, true) 变成2个区，shuffle
        * repartition()重新分区（执行Shuffle） 
            + coalesce重新分区，可以选择是否进行shuffle过程。由参数shuffle: Boolean = false/true决定。
            + repartition实际上是调用的coalesce，进行shuffle。源码如下：
            + coalesce一般为缩减分区，如果扩大分区，不使用shuffle是没有意义的，因为不落盘（打乱重组），增加不了分区
            + repartition扩大分区执行shuffle。
        * sortBy(f,true,numpartition)排序 对分区的每一个元素执行f,根据f的值对元素进行排序，默认正序 
            + 首先使用`zipWithIndex()`方法为RDD中的每个元素打上索引，然后使用`RangePartitioner`类对元素进行分区。分区后，每个分区内的元素使用快速排序算法进行排序。最后，将所有分区中的元素按照分区顺序进行合并，得到一个排序后的RDD。
        * pipe()调用脚本
    - 双Value 
        * union()并集
        * subtract ()差集
        * intersection()交集
        * zip()拉链  要求两个RDD中的分区数量和分区中的元素数量必须相同
    - Key-Value类型 
        * partitionBy()按照K重新分区
        * reduceByKey()按照K聚合V
        * groupByKey()按照K重新分组 迭代器 
            + reduceByKey：按照key进行聚合，在shuffle之前有combine（预聚合）操作，返回结果是RDD[k,v]。
            + groupByKey：按照key进行分组，直接进行shuffle。
            + 在不影响业务逻辑的前提下，优先选用reduceByKey。求和操作不影响业务逻辑，求平均值影响业务逻辑。
        * aggregateByKey()按照K处理分区内和分区间逻辑 
            + aggregateByKey(0)(math.max(_, _), _ + _)
            + aggregateByKey(初始值)(分区内,分区间)
        * foldByKey()分区内和分区间相同的aggregateByKey()
        * combineByKey()转换结构后分区内和分区间操作 
            + createCombiner:V=>C  
分组内的创建组合的函数。通俗点将就是对读进来的数据进行初始化，其把当前的值作为参数，可以对该值做一些转换操作，转换为我们想要的数据格式
            + mergeValue:(C,V)=>C  
该函数主要是分区内的合并函数，作用在每一个分区内部。其功能主要是将V合并到之前(createCombiner)的元素C上，注意，这里的C指的是上一函数转换之后的数据格式，而这里的V指的是原始数据格式（上一函数为转换之前的）
            + mergeCombiners:(C,C)=>R  
该函数主要是进行多分区合并，此时是将两个C合并为一个C,例如两个C:(lnt)进行相加之后得到一个R:(lnt)
        * sortByKey()按照K进行排序
        * mapValues()只对V进行操作
        * join()连接 将相同key对应的多个value关联在一起
        * cogroup() 类似全连接，但是在同一个RDD中对key聚合
+  Action行动算子 
    - reduce()聚合:先聚合分区内数据，再聚合分区间数据
    - collect()以数组的形式返回数据集
    - count()返回RDD中元素个数
    - take()返回由RDD前n个元素组成的数组
    - takeOrdered()返回该RDD排序后前n个元素组成的数组
    - aggregate()将每个分区里面的元素通过分区内逻辑和初始值进行聚合，然后用分区间逻辑  
和初始值(zeroValue)进行操作
    - fold()aggregate的简化操作，即，分区内逻辑和分区间逻辑相同
    - countByKey()统计每种key的个数
    - save相关算子 
        * saveAsTextFile(path)保存成Text文件,toString方法
        * saveAsSequenceFile(path) 保存成Sequencefile文件  只有kv类型RDD有该操作，单值的没有
        * saveAsObjectFile(path) 序列化成对象保存到文件
        * foreach(f)遍历RDD中每一个元素
+  RDD序列化 
    - 初始化工作是在Driver端进行的，而实际运行程序是在Executor端进行的，这就涉及到了跨进程通信，是需要序列化的
+  RDD依赖关系 
    - 窄依赖：窄依赖表示每一个父RDD的Partition最多被子RDD的一个Partition使用，窄依赖我们形象的比喻为独生子女
    - 宽依赖：同一个父RDD的Partition被多个子RDD的Partition依赖，会引起Shuffle，总结：宽依赖我们形象的比喻为超生
+  

#### job调度
+  
    - Spark集群 
        * 多个Spark应用：SparkContext 
            + 运行多个Job：执行一个行动算子，都会提交一个Job 
                - 多个Stage组成：宽依赖是划分Stage的依据 
                    * 一个宽依赖做一次阶段的划分
                    * 阶段的个数 =  宽依赖个数  + 1
                    * 多个Task组成 
                        + 每一个阶段最后一个RDD的分区数，就是当前阶段的Task个数
+  RDD持久化 
    - RDD Cache缓存 
        * JVM的堆内存：触发后面的action时，该RDD将会被缓存在计算节点的内存
        * Cache操作会增加血缘关系，不改变原有的血缘关系
        * rdd.cache()
        * 存储级别
        * 
+  RDD CheckPoint检查点 
    - sc.setCheckpointDir("./checkpoint1")
    - rdd.checkpoint()
    - 存储到HDFS集群 
        * System.setProperty("HADOOP_USER_NAME","name")
        * sc.setCheckpointDir("hdfs://hadoop102:9000/checkpoint")
+  CheckPoint与Cache  
1）Cache缓存只是将数据保存起来，不切断血缘依赖。Checkpoint检查点切断血缘依赖。  
2）Cache缓存的数据通常存储在磁盘、内存等地方，可靠性低。Checkpoint的数据通常存储在HDFS等容错、高可用的文件系统，可靠性高。  
3）建议对checkpoint()的RDD使用Cache缓存，这样checkpoint的job只需从Cache缓存中读取数据即可，否则需要再从头计算一次RDD。  
4）如果使用完了缓存，可以通过unpersist（）方法释放缓存 
+  分区 
    -  k-v 
    -  rdd.partitionBy() 
    -  Hash分区： 
        * 对于给定的key,计算其hashCode,并除以分区的个数取余，如果余数小于0，则用余数+分区的个数(否则加0)，最后返回的值就是这个ky所属的分区D。
        * 可能导致每个分区中数据量的不均匀
    -  Range分区 
        * 将一定范围内的数映射到某一个分区内，尽量保证每个分区中数据量均匀，而且分区与分区之间是有序的，一个分区中的元素肯定都是比另一个分区内的元素小或者大，但是分区内的元素是不能保证顺序的。简单的说就是将一定范围内的数映射到某一个分区内。
        * 将一定范围内的数映射到某一个分区内
    -  用户自定义分区 
        *  

```plain
class MyPartitioner(num: Int) extends Partitioner {
    override def numPartitions: Int = num
    override def getPartition(key: Any): Int = {
        if (key.isInstanceOf[Int]) {
            val keyInt: Int = key.asInstanceOf[Int]
            if (keyInt % 2 == 0)
                0
            else
                1
        }else{
            0
        }
    }
}
```

 

+  数据读取与保存 
    - Text文件 
        * 数据读取：sc.textFile(String)
        * 数据保存：saveAsTextFile(String)
    - Json文件 
        * 如果JSON文件中每一行就是一个JSON记录，那么可以通过将JSON文件当做文本文件来读取，然后利用相关的JSON库对每一条数据进行JSON解析
    - Sequence文件 
        * Hadoop用来存储二进制形式的key-value对而设计的一种平面文件(Flat File)。在SparkContext中，可以调用sequenceFile[keyClass, valueClass](path)。
        * sc.sequenceFile[Int,Int](%22output%22)
        * saveAsSequenceFile()
    - Object对象文件 
        * sc.objectFile[(Int)](%22output%22)
        * saveAsObjectFile("output")
    - HDFS
    - MySQL
+  累加器 
    -  分布式数据聚合：累加器提供了一种分布式数据聚合的机制，多个节点上执行的任务可以将其结果累加到同一个累加器变量中，从而实现数据的汇总和聚合。 
    -  共享只读变量：累加器变量会被多个任务同时读取，这使得在并行任务执行过程中保证了共享变量的可见性。 
    -  基于驱动器程序的任务跟踪：在Spark中，累加器的值是只写的，只能由累加器所在的驱动器程序更新。这个特点保证了对任务的监控和跟踪。 
    -  高效的实现方式：Spark的累加器变量设计为分布式的只写容器，可以高效存储和管理大量的累加器值。 
    -  系统累加器 
        * val sum1: LongAccumulator = sc.longAccumulator("sum1")
    -  自定义累加器 
        *  累加器的运行原理：Spark的累加器是一个只写的变量，由驱动程序初始化，同时在每个工作节点上有一份副本。当Spark任务执行时，每个节点上的任务都可以局部地更新本节点的累加器变量，最后将这些中间结果传回驱动程序，在驱动程序中对各个节点的计算结果进行全局聚合，得到最终的累加器值 
        *  

```plain
class MyAccumulator extends AccumulatorV2[String, mutable.Map[String, Long]] {

    // 定义输出数据集合
    var map = mutable.Map[String, Long]()

    // 是否为初始化状态，如果集合数据为空，即为初始化状态
    override def isZero: Boolean = map.isEmpty

    // 复制累加器
    override def copy(): AccumulatorV2[String, mutable.Map[String, Long]] = {
        new MyAccumulator()
    }

    // 重置累加器
    override def reset(): Unit = map.clear()

    // 增加数据
    override def add(v: String): Unit = {
        // 业务逻辑
        if (v.startsWith("H")) {
            map(v) = map.getOrElse(v, 0L) + 1L
        }
    }

    // 合并累加器
    override def merge(other: AccumulatorV2[String, mutable.Map[String, Long]]): Unit = {

        var map1 = map
        var map2 = other.value

        map = map1.foldLeft(map2)(
            (map,kv)=>{
                map(kv._1) = map.getOrElse(kv._1, 0L) + kv._2
                map
            }
        )
    }

    // 累加器的值，其实就是累加器的返回结果
    override def value: mutable.Map[String, Long] = map
}
```

 

    -  广播变量：分布式共享只读变量 
        *  广播变量的生成：在驱动器程序中通过调用SparkContext的broadcast()方法生成广播变量。广播变量可以是任意类型的变量，只要实现了Java Serializable接口即可。 
        *  广播变量的分发：在Spark任务开始之前，广播变量通过TCP socket发送到集群中的各个节点。广播变量只会被发送一次，并且在节点上仅仅保留一份拷贝保存。广播变量具有唯一的标识符，可以在任务执行过程中快速地获取到它的值。 
        *  广播变量的使用：在Spark任务执行过程中，广播变量会被多个任务共享，这些任务可以通过广播变量的标识符获取其值。广播变量的值只能被读取，无法进行写操作。 
        *  

```plain
val broadcastList: Broadcast[List[(String, Int)]] = sc.broadcast(list)
```

 

