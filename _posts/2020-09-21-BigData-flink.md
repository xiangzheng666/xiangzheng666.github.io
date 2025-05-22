---
categories: [BigData]
tags: [Flink]
---

# Flink

+  Flink运行架构 

   *  作业管理器（JobManager）  
      每个应用程序都会被一个不同的JobManager所控制执行。JobManager会先接收到要执行的应用程序，向资源管理器（ResourceManager）请求执行任务必要的资源，也就是任务管理器（TaskManager）上的插槽（slot）。一旦它获取到了足够的资源，就会将执行图分发到真正运行它们的TaskManager上。 
   *  资源管理器（ResourceManager）  
      管理任务管理器（TaskManager）的插槽（slot），TaskManger插槽是Flink中定义的处理资源单元。 
   *  任务管理器（TaskManager）  
      每一个TaskManager都包含了一定数量的插槽（slots）。插槽的数量限制了TaskManager能够执行的任务数量。启动之后，TaskManager会向资源管理器注册它的插槽；收到资源管理器的指令后，TaskManager就会将一个或者多个插槽提供给JobManager调用 
   *  分发器（Dispatcher）  
      提供了REST接口。当一个应用被提交执行时，分发器就会启动并将应用移交给一个JobManager 

+  任务调度原理 

   * _**Client**_ 为提交 Job 的客户端，可以是运行在任何机器上（与 JobManager 环境连通即可）。提交 Job 后，Client 可以结束进程（Streaming的任务），也可以不结束并等待结果返回。
   * _**JobManager**_ 主要负责调度 Job 并协调 Task 做 checkpoint，职责上很像 Storm 的 Nimbus。从 Client 处接收到 Job 和 JAR 包等资源后，会生成优化后的执行计划，并以 Task 的单元调度到各个 TaskManager 去执行。
   * _**TaskManager（worker）**_在启动的时候就设置好了槽位数（Slot），每个 slot 能启动一个 Task，Task 为线程。从 JobManager 处接收需要部署的 Task，部署启动后，与自己的上游建立 Netty 连接，接收数据并处理。 
     + **Slots**  每个task slot表示TaskManager拥有资源的一个固定大小的子集。假如一个TaskManager有三个slot，那么它会将其管理的内存分成三份给各个slot。资源slot化意味着一个subtask将不需要跟来自其他job的subtask竞争被管理的内存，同一个JVM进程中的task将共享TCP连接（基于多路复用）和心跳消息-----_**Task Slot是静态的概念，是指TaskManager具有的并发执行能力**_，可以通过参数taskmanager.numberOfTaskSlots进行配置；而_**并行度parallelism是动态概念，即TaskManager运行程序时实际使用的并发能力**_

+  程序与数据流（DataFlow）  
   _**每一个dataflow以一个或多个sources开始以一个或多个sinks结束**_ 

    * _**Source**_  负责读取数据源
    * _**Transformation**_  利用各种算子进行处理加工
    * _**Sink**_  负责输出

+  执行图（ExecutionGraph）  
   StreamGraph -> JobGraph -> ExecutionGraph -> 物理执行图 

    *  _**StreamGraph**_：是根据用户通过 Stream API 编写的代码生成的最初的图。用来表示程序的拓扑结构。  
       _**JobGraph**_：StreamGraph经过优化后生成了 JobGraph，提交给 JobManager 的数据结构。主要的优化为，将多个符合条件的节点 chain 在一起作为一个节点，这样可以减少数据在节点之间流动所需要的序列化/反序列化/传输消耗。  
       _**ExecutionGraph**_：JobManager 根据 JobGraph 生成ExecutionGraph。ExecutionGraph是JobGraph的并行化版本，是调度层最核心的数据结构。  
       _**物理执行图**_：JobManager 根据 ExecutionGraph 对 Job 进行调度后，在各个TaskManager 上部署 Task 后形成的“图”，并不是一个具体的数据结构。 


   -  并行度 
      * _**One-to-one**_：stream(比如在source和map operator之间)维护着分区以及元素的顺序。那意味着map 算子的子任务看到的元素的个数以及顺序跟source 算子的子任务生产的元素的个数、顺序相同，map、fliter、flatMap等算子都是one-to-one的对应关系。类似于spark中的_**窄依赖**_
      * _**Redistributing**_：stream(map()跟keyBy/window之间或者keyBy/window跟sink之间)的分区会发生改变。每一个算子的子任务依据所选择的transformation发送数据到不同的目标任务。例如，keyBy() 基于hashCode重分区、broadcast和rebalance会随机重新分区，这些算子都会引起redistribute过程，而redistribute过程就类似于Spark中的shuffle过程。类似于spark中的_**宽依赖**_
   -  任务链  
      相同并行度的_**one to one操作**_，Flink这样相连的算子链接在一起形成一个task，原来的算子成为里面的一部分。将算子链接成task是非常有效的优化：它能减少线程之间的切换和基于缓存区的数据交换，在减少时延的同时提升吞吐量。链接的行为可以在编程API中进行指定。 

+  Flink 流处理API

   +  支持的数据类型 

      * 基础数据类型
      * Java和Scala元组（Tuples）
      * Scala样例类（case classes）
      * Java简单对象（POJOs）
      * 其它（Arrays, Lists, Maps, Enums, 等等）

   +  创建env： 

      * StreamExecutionEnvironment.getExecutionEnvironment
      * StreamExecutionEnvironment.createLocalEnvironment(1)
      * ExecutionEnvironment.createRemoteEnvironment("jobmanage-hostname", 6123,"YOURPATH//wordcount.jar")

   +  Source： 

      * 文件读取数据：env.readTextFile(YOUR_FILE_PATH)
      * kafka消息队列：env.addSource(newFlinkKafkaConsumer011[String]("sensor", new SimpleStringSchema(), properties))
      * 自定义Source:   env.addSource( new MySensorSource() )   -extends SourceFunction

   +  Transform: 

      *  import org.apache.flink.api.scala._ 

      *  map 

      *  flatMap 

      *  Filter 

      *  KeyBy 

      *  窗口聚合 

         + sum()
         + min()
         + max()
         + minBy()
         + maxBy()

      *  Reduce 

      *  Split 和 Select 

      *  Connect和 CoMap 

      *  Union 

      *  **Connect与Union区别**_  

         *  Union之前两个流的类型必须是一样，Connect可以不一样，在之后的coMap中再去调整成为一样的。Connect只能操作两个流，Union可以操作多个。 

      *  UDF函数 

         + MapFunction

         + FlatMapFunction

         + FilterFunction

         + ...

         + RichMapFunction

         + RichFlatMapFunction

         + RichFilterFunction

         + ...

   + 接口函数 
     - open()方法是rich function的初始化方法，当一个算子例如map或者filter被调用之前open()会被调用。
     - close()方法是生命周期中的最后一个调用的方法，做一些清理工作。
     - getRuntimeContext()方法提供了函数的RuntimeContext的一些信息，例如函数执行的并行度，任务的名字，以及state状态

      -  Sink 
         * stream.addSink(new MySink(xxxx))
         * _**new**_ FlinkKafkaProducer011[String](**"localhost:9092"**, _**"test"**_, _**new**_ SimpleStringSchema())
         * _**new**_ RedisSink[SensorReading](conf, _**new**_ MyRedisMapper)
         * ...

## Flink中的Window

+  -  window是一种切割无限数据为有限块进行处理 
   -  CountWindow：按照指定的数据条数生成一个Window，与时间无关。 
   -  TimeWindow：按照时间生成Window。 
      *  滚动窗口（Tumbling Windows）  
         将数据依据固定的窗口长度对数据进行切片。  
         特点：时间对齐，窗口长度固定，没有重叠。 
      *  滑动窗口（Sliding Windows）  
         滑动窗口是固定窗口的更广义的一种形式，滑动窗口由固定的窗口长度和滑动间隔组成。  
         特点：时间对齐，窗口长度固定，可以有重叠 
      *  会话窗口（Session Windows）  
         由一系列事件组合一个指定时间长度的timeout间隙组成，类似于web应用的session，也就是一段时间没有接收到新数据就会生成新的窗口。  
         特点：时间无对齐。 
   -  Window API 
      *  .timeWindow(Time.seconds(15)) 滚动窗口  countWindow(5) 
      *  .timeWindow(Time.seconds(15), Time.seconds(5)) 滑动窗口  countWindow(10,2) 
      *  window function 
         +  增量聚合函数（incremental aggregation functions）  
            每条数据到来就进行计算，保持一个简单的状态。典型的增量聚合函数有ReduceFunction, AggregateFunction。 
         +  全窗口函数（full window functions）  
            先把窗口所有数据收集起来，等到计算的时候会遍历所有数据。ProcessWindowFunction就是一个全窗口函数。 
         +  .trigger() —— 触发器  
            定义 window 什么时候关闭，触发计算并输出结果 
         +  .evitor() —— 移除器  
            定义移除某些数据的逻辑 
         +  .allowedLateness() —— 允许处理迟到的数据 
         +  .sideOutputLateData() —— 将迟到的数据放入侧输出流 
         +  .getSideOutput() —— 获取侧输出流 

## 时间语义与Wartermark

+  - Event Time：是事件创建的时间。它通常由事件中的时间戳描述，例如采集的日志数据中，每一条日志都会记录自己的生成时间，Flink通过时间戳分配器访问事件时间戳。
   - Ingestion Time：是数据进入Flink的时间。
   - Processing Time：是每一个执行基于时间操作的算子的本地系统时间，与机器相关，默认的时间属性就是Processing Time
   - Watermark:Watermark是用于处理乱序事件的
   - EventTime的引入 
     * env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime)
     * .assignTimestampsAndWatermarks(new MyAssigner()) 
       + AssignerWithPeriodicWatermarks 
         - 周期性的生成watermark 
           * 没有乱序:.assignAscendingTimestamps(e => e.timestamp)
           * 乱序:.assignTimestampsAndWatermarks(new SensorTimeAssigner) extends BoundedOutOfOrdernessTimestampExtractor
       + AssignerWithPunctuatedWatermarks 
         - 间断式地生成watermark。和周期性生成的方式不同，这种方式不是固定时间的，而是可以根据需要对每条数据进行筛选和处理
         - extends AssignerWithPunctuatedWatermarks
   - EvnetTime在window中的使用 
     * 滚动窗口（TumblingEventTimeWindows） 
       + textKeyStream.window(TumblingEventTimeWindows.**of**(Time.**seconds**(2)))
     * 滑动窗口（SlidingEventTimeWindows） 
       + textKeyStream.window(SlidingEventTimeWindows.**of**(Time.**seconds**(2),Time.**milliseconds**(500)))
     * 会话窗口（EventTimeSessionWindows） 
       + textKeyStream.window(EventTimeSessionWindows.**withGap**(Time.**milliseconds**(500)))
+  

## ProcessFunction API

+  -  

| API                           | 是否需要开窗 | 是否需要 keyBy |
| ----------------------------- | ------------ | -------------- |
| ProcessFunction               | 否           | 否             |
| KeyedProcessFunction          | 否           | **是**         |
| CoProcessFunction             | 否           | 否             |
| ProcessJoinFunction           | **是**       | **是**         |
| BroadcastProcessFunction      | 否           | 否             |
| KeyedBroadcastProcessFunction | 否           | **是**         |
| ProcessWindowFunction         | **是**       | **是**         |
| ProcessAllWindowFunction      | **是**       | 否             |


    -  
    -  TimerService 和 定时器（Timers） 
        * Context和OnTimerContext所持有的TimerService对象拥有以下方法:
        * currentProcessingTime(): Long 返回当前处理时间
        * currentWatermark(): Long 返回当前watermark的时间戳
        * registerProcessingTimeTimer(timestamp: Long): Unit 会注册当前key的processing time的定时器。当processing time到达定时时间时，触发timer。
        * registerEventTimeTimer(timestamp: Long): Unit 会注册当前key的event time 定时器。当水位线大于等于定时器注册的时间时，触发定时器执行回调函数。
        * deleteProcessingTimeTimer(timestamp: Long): Unit 删除之前注册处理时间定时器。如果没有这个时间戳的定时器，则不执行。
        * deleteEventTimeTimer(timestamp: Long): Unit 删除之前注册的事件时间定时器，如果没有此时间戳的定时器，则不执行。
    -  ProcessFunction 
    -  KeyedProcessFunction 
        * processElement(v: IN, ctx: Context, out: Collector[OUT]), 流中的每一个元素都会调用这个方法，调用结果将会放在Collector数据类型中输出。**Context**可以访问元素的时间戳，元素的key，以及**TimerService**时间服务。**Context**还可以将结果输出到别的流(side outputs)。
        * onTimer(timestamp: Long, ctx: OnTimerContext, out: Collector[OUT])是一个回调函数。当之前注册的定时器触发时调用。参数timestamp为定时器所设定的触发的时间戳。Collector为输出结果的集合
    -  CoProcessFunction 
    -  ProcessJoinFunction 
    -  BroadcastProcessFunction 
    -  KeyedBroadcastProcessFunction 
    -  ProcessWindowFunction 
    -  ProcessAllWindowFunction 
    -  

#### 侧输出流（SideOutput）

    -  
        * lazy val freezingAlarmOutput: OutputTag[String] =new OutputTag[String]("freezing-alarms")
        * ctx.output(freezingAlarmOutput, s"Freezing Alarm for")
        * .getSideOutput(new OutputTag[String]("freezing-alarms"))

+  

## 状态编程和容错机制

+  -  算子状态（operator state）  
      算子状态的作用范围限定为算子任务。这意味着由同一并行任务所处理的所有数据都可以访问到相同的状态，状态对于同一任务而言是共享的。算子状态不能由相同或不同算子的另一个任务访问。 
       *  列表状态（List state）  
          将状态表示为一组数据的列表。 
       *  联合列表状态（Union list state）  
          也将状态表示为数据的列表。它与常规列表状态的区别在于，在发生故障时，或者从保存点（savepoint）启动应用程序时如何恢复。 
       *  广播状态（Broadcast state）  
          如果一个算子有多项任务，而它的每项任务状态又都相同，那么这种特殊情况最适合应用广播状态。 
   -  键控状态（keyed state）  
      键控状态是根据输入数据流中定义的键（key）来维护和访问的。Flink为每个键值维护一个状态实例，并将具有相同键的所有数据，都分区到同一个算子任务中，这个任务会维护和处理这个key对应的状态 
       *  ValueState[T]保存单个的值，值的类型为T。 
          + get操作: ValueState.value()
          + set操作: ValueState.update(value: T)
       *  ListState[T]保存一个列表，列表里的元素的数据类型为T。基本操作如下： 
          + ListState.add(value: T)
          + ListState.addAll(values: java.util.List[T])
          + ListState.get()返回Iterable[T]
          + ListState.update(values: java.util.List[T])
       *  MapState[K, V]保存Key-Value对。 
          + MapState.get(key: K)
          + MapState.put(key: K, value: V)
          + MapState.contains(key: K)
          + MapState.remove(key: K)
       *  ReducingState[T] 
       *  AggregatingState[I, O] 
       *  一致性级别 
          +  at-most-once: 这其实是没有正确性保障的委婉说法——故障发生之后，计数结果可能丢失。同样的还有udp。 
          +  at-least-once: 这表示计数结果可能大于正确值，但绝不会小于正确值。也就是说，计数程序在发生故障后可能多算，但是绝不会少算。 
          +  exactly-once: 这指的是系统保证在发生故障后得到的计数结果与正确值一致。 
          +  端到端（end-to-end）状态一致性 
             -  内部保证 —— 依赖checkpoint 
             -  source 端 —— 需要外部源可重设数据的读取位置 
             -  sink 端 —— 需要保证从故障恢复时，数据不会重复写入外部系统 
                *  幂等写入  
                   所谓幂等操作，是说一个操作，可以重复执行很多次，但只导致一次结果更改，也就是说，后面再重复执行就不起作用了。 
                *  事务写入  
                   需要构建事务来写入外部系统，构建的事务对应着 checkpoint，等到 checkpoint 真正完成的时候，才把所有对应的结果写入 sink 系统中。 
                    + 预写日志（WAL）和两阶段提交（2PC）。DataStream API 提供了GenericWriteAheadSink模板类和TwoPhaseCommitSinkFunction 接口
          +  Flink的检查点算法 
             -  1.基于 Chandy-Lamport 算法进行分布式快照：  
                在 Flink 中，检查点是通过对任务进行快照来实现的。Flink 的基于 Chandy-Lamport 算法的分布式快照实现，会先从 JobManager 发出一个触发检查点的信号，然后从每个 TaskManager 开始进行快照的处理。每个 TaskManager 都会在接收到触发检查点的信号后，将当前任务的状态进行快照，包括所有的状态变量和缓存的数据。快照的过程是通过对数据流进行标记来实现的，标记会在数据流中不断传递，直到所有的状态变量和缓存数据都被标记。 
             -  2.基于异步快照的状态恢复：  
                在 Flink 中，状态恢复是通过将快照数据和状态更新日志组合起来来实现的。Flink 的异步快照实现，会将状态快照和状态更新日志存储到持久化存储中，例如 HDFS、S3 等。当任务发生故障或者需要恢复时，Flink 会读取最近的一个完整的检查点，然后将状态更新日志应用到检查点中，来实现状态的恢复。需要注意的是，Flink 的检查点算法是可配置的，用户可以根据不同的业务需求和系统环境来进行配置。例如，用户可以通过调整检查点的触发间隔和并行度来平衡数据一致性和系统性能。 
          +  状态后端(state backend) 
             -  MemoryStateBackend  
                内存级的状态后端，会将键控状态作为内存中的对象进行管理，将它们存储在TaskManager的JVM堆上；而将checkpoint存储在JobManager的内存中。 
             -  FsStateBackend  
                将checkpoint存到远程的持久化文件系统（FileSystem）上。而对于本地状态，跟MemoryStateBackend一样，也会存在TaskManager的JVM堆上。 
             -  RocksDBStateBackend  
                将所有状态序列化后，存入本地的RocksDB中存储。  
                注意：RocksDB的支持并不直接包含在flink中，需要引入依赖： 
          +  Flink+Kafka如何实现端到端的exactly-once语义 
             - 内部 —— 利用checkpoint机制，把状态存盘，发生故障的时候可以恢复，保证内部的状态一致性
             - source —— kafka consumer作为source，可以将偏移量保存下来，如果后续任务出现了故障，恢复的时候可以由连接器重置偏移量，重新消费数据，保证一致性
             - sink —— kafka producer作为sink，采用两阶段提交 sink，需要实现一个 TwoPhaseCommitSinkFunction
+  

## Flink CEP

+  -  复杂事件处理CEP:一个或多个由简单事件构成的事件流通过一定的规则匹配，然后输出用户想得到的数据，满足规则的复杂事件。 
   -  **Pattern API**  
      每个Pattern都应该包含几个步骤，或者叫做state。从一个state到另一个state，通常我们需要定义一些条件，例如下列的代码： 

```plain
val loginFailPattern = Pattern.begin[LoginEvent]("begin")
 .where(_.eventType.equals("fail"))
 .next("next")
 .where(_.eventType.equals("fail"))
 .within(Time.seconds(10)
```

 

    -  **Pattern 检测**  

通过一个input DataStream以及刚刚我们定义的Pattern，我们可以创建一个PatternStream： 

```plain
val input = ...
val pattern = ...

val patternStream = CEP.pattern(input, pattern)

val patternStream = CEP.pattern(loginEventStream.keyBy(_.userId), loginFailPattern)
```


一旦获得PatternStream，我们就可以通过select或flatSelect，从一个Map序列找到我们需要的警告信息 

    -  **select**  

select方法需要实现一个PatternSelectFunction，通过select方法来输出需要的警告。它接受一个Map对，包含string/event，其中key为state的名字，event则为真实的Event。 

```plain
val loginFailDataStream = patternStream
 .select((pattern: Map[String, Iterable[LoginEvent]]) => {
  val first = pattern.getOrElse("begin", **null**).iterator.next()
  val second = pattern.getOrElse("next", **null**).iterator.next()

  Warning(first.userId, first.eventTime, second.eventTime, "warning")
 })
```

 

    -  **flatSelect**  

通过实现PatternFlatSelectFunction，实现与select相似的功能。唯一的区别就是flatSelect方法可以返回多条记录，它通过一个Collector[OUT]类型的参数来将要输出的数据传递到下游。  
_**超时事件的处理**_  
通过within方法，我们的parttern规则将匹配的事件限定在一定的窗口范围内。当有超过窗口时间之后到达的event，我们可以通过在select或flatSelect中，实现PatternTimeoutFunction和PatternFlatTimeoutFunction来处理这种情况。 

```scala
val patternStream: PatternStream[Event] = CEP.pattern(input, pattern)

val outputTag = OutputTag[String]("side-output")

val result: SingleOutputStreamOperator[ComplexEvent] = patternStream.select(outputTag){
    (pattern: Map[String, Iterable[Event]], timestamp: Long) => TimeoutEvent()
} {
    pattern: Map[String, Iterable[Event]] => ComplexEvent()
}

val timeoutResult: DataStream<TimeoutEvent> = result.getSideOutput(outputTag)
```

 

