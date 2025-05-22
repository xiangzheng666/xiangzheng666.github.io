---
categories: [BigData]
tags: [Spark Streaming]
---
# Spark Streaming


+  Receiver 接收器会将数据存储在内存或磁盘中，然后将一定时间范围内接收到的数据组成一个数据块（batch），并将这个数据块交给 Spark Streaming 的输入流（InputDStream）。接着，输入流将这个数据块转化为一个 RDD，并将这个 RDD 作为输入数据流（DStream）的一部分 
+  ![](https://img-blog.csdnimg.cn/img_convert/14c13bc046b8e2e524030c4386324c7e.png) 
+  ![](https://img-blog.csdnimg.cn/img_convert/9ff1a8725c1a86868994ad34807345bd.png) 
+  背压机制:动态控制数据接收速率来适配集群数据处理能力 
+  DStreams:是随时间推移而收到的数据的序列。在内部，每个时间区间收到的数据都作为RDD存在，而DStreams是由这些RDD所组成的序列(因此得名“离散化”)。DStreams可以由来自数据源的输入数据流来创建, 也可以通过在其他的 DStreams上应用一些高阶操作来得到。 
+  DStream创建 
   -  自定义数据源 
      *  继承Receiver，并实现onStart、onStop方法来自定义数据源采集 

```plain
class MyReceiver(host: String, port: Int) extends Receiver[String](StorageLevel.MEMORY_ONLY) {
	//创建一个Socket
  private var socket: Socket = _

  //最初启动的时候，调用该方法，作用为：读数据并将数据发送给Spark
  override def onStart(): Unit = {
    new Thread("Socket Receiver") {
      setDaemon(true)
      override def run() { receive() }
    }.start()
  }

  //读数据并将数据发送给Spark
  def receive(): Unit = {
    try {
      socket = new Socket(host, port)
      //创建一个BufferedReader用于读取端口传来的数据
      val reader = new BufferedReader(
        new InputStreamReader(
          socket.getInputStream, StandardCharsets.UTF_8))
      //定义一个变量，用来接收端口传过来的数据
      var input: String = null

      //读取数据 循环发送数据给Spark 一般要想结束发送特定的数据 如："==END=="
      while ((input = reader.readLine())!=null) {
        store(input)
      }
    } catch {
      case e: ConnectException =>
        restart(s"Error connecting to $host:$port", e)
        return
    }
  }

  override def onStop(): Unit = {
    if(socket != null ){
      socket.close()
      socket = null
    }
  }
```

 

-  Kafka数据源 
   *  ReceiverAPI：Executor去接收数据-专门的Executor去接收数据，然后发送给其他的Executor做计算 
   *  DirectAPI：Executor来主动消费数据 
   *  RDD队列:ssc.queueStream(queueOfRDDs) 
   *  **0-8** **ReceiverAPI**: 
      + 专门的Executor读取数据，速度不统一
      + 跨机器传输数据，WAL
      + Executor读取数据通过多个线程的方式，想要增加并行度，则需要多个流union
      + offset存储在Zookeeper中
   *  **0-8 DirectAPI**: 
      + Executor读取数据并计算
      + 增加Executor个数来增加消费的并行度
      + offset存储 
        - CheckPoint(getActiveOrCreate方式创建StreamingContext)
        - 手动维护(有事务的存储系统)
        - 获取offset必须在第一个调用的算子中：offsetRanges = rdd.asInstanceOf[HasOffsetRanges].offsetRanges
   *  **0-10** **DirectAPI:** 
      + Executor读取数据并计算
      + 增加Executor个数来增加消费的并行度
      + offset存储 
        - a.__consumer_offsets系统主题中
        - 手动维护(有事务的存储系统)+

+ DStream转换 

  - Transformations 

    *  无状态转化 

       +  无状态转化操作就是把简单的RDD转化操作应用到每个批次上，也就是转化DStream中的每一个RDD 

       ```plain
       val wordAndCountDStream: DStream[(String, Int)] = lineDStream.transform(
       	rdd => {
               val words: RDD[String] = rdd.flatMap(_.split(" "))
               val wordAndOne: RDD[(String, Int)] = words.map((_, 1))
               val value: RDD[(String, Int)] = wordAndOne.reduceByKey(_ + _)
                 value
           }
       )
       ```

    *  有状态转化 

       +  UpdateStateByKey 
       +  val stateDS: DStream[(String, Int)] = mapDS.updateStateByKey(
              (seq: Seq[Int], state: Option[Int]) => {
              	Option(seq.sum + state.getOrElse(0))
              }
          )

    *  window滑动窗口 

       *  ```
          1)window(windowLength, slideInterval)
          基于对源DStream窗化的批次进行计算返回一个新的Dstream
          2)countByWindow(windowLength, slideInterval)
          返回一个滑动窗口计数流中的元素个数
          3)countByValueAndWindow()
          返回的DStream则包含窗口中每个值的个数
          4)reduceByWindow(func, windowLength, slideInterval)
           通过使用自定义函数整合滑动区间流元素来创建一个新的单元素流
          5)reduceByKeyAndWindow(func, windowLength, slideInterval, [numTasks])
          当在一个(K,V)对的DStream上调用此函数，会返回一个新(K,V)对的DStream，此处通过对滑动窗口中批次数据使用reduce函数来整合每个key的value值
          6)reduceByKeyAndWindow(func, invFunc, windowLength, slideInterval, [numTasks])
          ```

- Output Operations 

```plain
1)print()
在运行流程序的驱动结点上打印DStream中每一批次数据的最开始10个元素。这用于开发和调试。在Python API中，同样的操作叫print()。
2)saveAsTextFiles(prefix, [suffix])
以text文件形式存储这个DStream的内容。每一批次的存储文件名基于参数中的prefix和suffix。”prefix-Time_IN_MS[.suffix]”。
3)saveAsObjectFiles(prefix, [suffix])
以Java对象序列化的方式将Stream中的数据保存为 SequenceFiles . 每一批次的存储文件名基于参数中的为"prefix-TIME_IN_MS[.suffix]". Python中目前不可用。
4)saveAsHadoopFiles(prefix, [suffix])
将Stream中的数据保存为 Hadoop files. 每一批次的存储文件名基于参数中的为"prefix-TIME_IN_MS[.suffix]"。Python API 中目前不可用。
5)foreachRDD(func)
这是最通用的输出操作，即将函数 func 用于产生于 stream的每一个RDD。其中参数传入的函数func应该实现将每一个RDD中数据推送到外部系统，如将RDD存入文件或者通过网络将其写入数据库。
```

 

