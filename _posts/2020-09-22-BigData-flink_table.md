---
categories: [BigData]
tags: [Table SQL]
---

# Table SQL


Table API是一套内嵌在Java和Scala语言中的查询API，它允许我们以非常直观的方式，组合来自一些关系运算符的查询（比如select、filter和join）。

Flink SQL，就是直接可以在代码中写SQL，来实现一些查询（Query）操作

**表**（Table）是由一个“标识符”来指定的，由3部分组成：Catalog名、数据库（database）名和对象名（表名）。如果没有指定目录或数据库，就使用当前的默认值。



## API

```plain
1.val tableEnv = ...     // 创建表的执行环境

2.// 创建一张表，用于读取数据
tableEnv.connect(...).createTemporaryTable("inputTable")
// 注册一张表，用于把计算结果输出
tableEnv.connect(...).createTemporaryTable("outputTable")

3.// 通过 Table API 查询算子，得到一张结果表
val result = tableEnv.from("inputTable").select(...)
// 通过 SQL查询语句，得到一张结果表
val sqlResult  = tableEnv.sqlQuery("SELECT ... FROM inputTable ...")

4.// 将结果表写入输出表中
result.insertInto("outputTable")
```

+  创建表环境 
   - val tableEnv = StreamTableEnvironment.create(env)
+  在Catalog中注册表 
   -  连接到文件系统（Csv格式） 

```plain
tableEnv
.connect( new FileSystem().path("sensor.txt"))  // 定义表数据来源，外部连接
  .withFormat(new OldCsv())    // 定义从外部系统读取数据之后的格式化方法
  .withSchema( new Schema()
    .field("id", DataTypes.STRING())
    .field("timestamp", DataTypes.BIGINT())
    .field("temperature", DataTypes.DOUBLE())
  )    // 定义表结构
  .createTemporaryTable("inputTable")
```

- 连接到Kafka 

```plain
tableEnv.connect(
  new Kafka()
    .version("0.11") // 定义kafka的版本
    .topic("sensor") // 定义主题
    .property("zookeeper.connect", "localhost:2181") 
    .property("bootstrap.servers", "localhost:9092")
)
  .withFormat(new Csv())
  .withSchema(new Schema()
  .field("id", DataTypes.STRING())
  .field("timestamp", DataTypes.BIGINT())
  .field("temperature", DataTypes.DOUBLE())
)
  .createTemporaryTable("kafkaInputTable")
```

- 链接jdbc   

```plain
val sinkDDL: String =
  """
    |create table dataTable (
    |  id varchar(20) not null,
    |  ts bigint,
    |  temperature double,
    |  pt AS PROCTIME()
    |) with (
    |  'connector.type' = 'filesystem',
    |  'connector.path' = 'file:///D:\\..\\sensor.txt',
    |  'format.type' = 'csv'
    |)
  """.stripMargin

tableEnv.sqlUpdate(sinkDDL) // 执行 DDL
aggResultSqlTable.insertInto("jdbcOutputTable")
```

 

+  表的查询 
   -  Table API:是一个新的 Table 
      *  val resultTable: Table = senorTable
         .select("id, temperature")
         .filter("id ='sensor_1'")

- SQL:SQL 查询的结果，是一个新的 Table 

```plain
tableEnv.sqlQuery("select id, temperature from inputTable where id ='sensor_1'")
```

+  输出表 
   -  表的输出，是通过将数据写入 TableSink 来实现的。TableSink 是一个通用接口，可以支持不同的文件格式、存储数据库和消息队列。具体实现，输出表最直接的方法，就是通过 Table.insertInto() 方法将一个 Table 写入注册过的 TableSink 中。 

| 输出模式                 | 代码                                                         |
| ------------------------ | ------------------------------------------------------------ |
| 追加模式（Append Mode）  | `tEnv.toAppendStream(resultTable, Row.class).print();`       |
| 撤回模式（Retract Mode） | `tEnv.toRetractStream(resultTable, Row.class).print();`      |
| 更新模式（Update Mode）  | `tEnv.toRetractStream(resultTable, Row.class, QueryConfigurations.ofBatchedRetractionWithMiniBatchSize(1000)).print();` |

- 输出到文件 

```plain
tableEnv.connect(
  new FileSystem().path("…\\resources\\out.txt")
) // 定义到文件系统的连接
  .withFormat(new Csv()) // 定义格式化方法，Csv格式
  .withSchema(new Schema()
  .field("id", DataTypes.STRING())
  .field("temp", DataTypes.DOUBLE())
) // 定义表结构
  .createTemporaryTable("outputTable") // 创建临时表

resultSqlTable.insertInto("outputTable"
```

- 输出到Kafka 

```plain
tableEnv.connect(
  new Kafka()
    .version("0.11")
    .topic("sinkTest")
    .property("zookeeper.connect", "localhost:2181")
    .property("bootstrap.servers", "localhost:9092")
)
  .withFormat( new Csv() )
  .withSchema( new Schema()
    .field("id", DataTypes.STRING())
    .field("temp", DataTypes.DOUBLE())
  )
  .createTemporaryTable("kafkaOutputTable")

resultTable.insertInto("kafkaOutputTable")
```

+ trait 

  -  DataStream 转换成表 
     * Table = tableEnv.fromDataStream(dataStream)
  -  表转换成DataStream 
     *  追加模式（Append Mode）: 用于表只会被插入（Insert）操作更改的场景。 
        +  DataStream[Row] = tableEnv.toAppendStream[Row](resultTable)
     *  撤回模式（Retract Mode）: 用于任何场景。有些类似于更新模式中Retract模式，它只有Insert和Delete两类操作。
        - DataStream[(Boolean, (String, Long))] = tableEnv.toRetractStream[(String, Long)](aggResultTable)

  -  数据类型与 Table schema的对应 
     *  DataStream 中的数据类型，与表的 Schema 之间的对应关系，是按照样例类中的字段名来对应的（name-based mapping），所以还可以用as做重命名 
     *  元组类型和原子类型，一般用位置对应会好一些；如果非要用名称对应，也是可以的：元组类型，默认的名称是 “_1”, “_2”；而原子类型，默认名称是 ”f0”。 
  -  创建临时视图（Temporary View） 
     -  tableEnv.createTemporaryView("sensorView", dataStream)
        tableEnv.createTemporaryView("sensorView", dataStream, 'id, 'temperature, 'timestamp as 'ts)
        tableEnv.createTemporaryView("sensorView", sensorTable)

  - Query的解释和执行 
    - val explaination: String = tableEnv.explain(resultTable)

## 流处理中的特殊概念


+  我们可以随着新数据的到来，不停地在之前的基础上更新结果。这样得到的表，在Flink Table API概念里，就叫做“**动态表**”（Dynamic Tables）。 
+  持续查询（Continuous Query） 
+  将动态表转换成流 
   - 仅追加（Append-only）流:仅通过插入（Insert）更改，来修改的动态表，可以直接转换为“仅追加”流。这个流中发出的数据，就是动态表中新增的每一行。
   - 撤回（Retract）流:Retract流是包含两类消息的流，添加（Add）消息和撤回（Retract）消息。
   - Upsert（更新插入）流:Upsert消息和delete消息
+  时间特性 

```plain
1.tableEnv.fromDataStream(dataStream, 'id, 'temperature, 'timestamp, 'pt.proctime、rowtime)
2.tableEnv.connect(
  new FileSystem().path("..\\sensor.txt"))
  .withFormat(new Csv())
  .withSchema(new Schema()
    .field("id", DataTypes.STRING())
    .field("timestamp", DataTypes.BIGINT())
    .field("temperature", DataTypes.DOUBLE())
    .field("pt", DataTypes.TIMESTAMP(3))
      .proctime()    // 指定 pt字段为处理时间
  ) // 定义表结构
  .createTemporaryTable("inputTable")
 
tableEnv.connect(
  new FileSystem().path("sensor.txt"))
  .withFormat(new Csv())
  .withSchema(new Schema()
    .field("id", DataTypes.STRING())
    .field("timestamp", DataTypes.BIGINT())
      .rowtime(
        new Rowtime()
          .timestampsFromField("timestamp")    // 从字段中提取时间戳
          .watermarksPeriodicBounded(1000)    // watermark延迟1秒
      )
    .field("temperature", DataTypes.DOUBLE())
  ) // 定义表结构
  .createTemporaryTable("inputTable")
```

 

+  窗口（Windows） 

```plain
tableapi：

groupBy('w, 'a)
1.滚动窗口（Tumbling windows）要用Tumble类来定义，另外还有三个方法：
    over：定义窗口长度
    on：用来分组（按时间间隔）或者排序（按行数）的时间字段
    as：别名，必须出现在后面的groupBy中
    
// Tumbling Event-time Window（事件时间字段rowtime）
.window(Tumble over 10.minutes on 'rowtime as 'w)
// Tumbling Processing-time Window（处理时间字段proctime）
.window(Tumble over 10.minutes on 'proctime as 'w)
// Tumbling Row-count Window (类似于计数窗口，按处理时间排序，10行一组)
.window(Tumble over 10.rows on 'proctime as 'w)

2.滑动窗口（Sliding windows）要用Slide类来定义，另外还有四个方法：
    over：定义窗口长度
    every：定义滑动步长
    on：用来分组（按时间间隔）或者排序（按行数）的时间字段
    as：别名，必须出现在后面的groupBy中
    
// Sliding Event-time Window
.window(Slide over 10.minutes every 5.minutes on 'rowtime as 'w)
// Sliding Processing-time window 
.window(Slide over 10.minutes every 5.minutes on 'proctime as 'w)
// Sliding Row-count window
.window(Slide over 10.rows every 5.rows on 'proctime as 'w)

3.会话窗口（Session windows）要用Session类来定义，另外还有三个方法：
    withGap：会话时间间隔
    on：用来分组（按时间间隔）或者排序（按行数）的时间字段
    as：别名，必须出现在后面的groupBy中
    
// Session Event-time Window
.window(Session withGap 10.minutes on 'rowtime as 'w)
// Session Processing-time Window 
.window(Session withGap 10.minutes on 'proctime as 'w)

4.Over Windows
    1） 无界的 over window
    // 无界的事件时间over window (时间字段 "rowtime")
    .window(Over partitionBy 'a orderBy 'rowtime preceding UNBOUNDED_RANGE as 'w)
    //无界的处理时间over window (时间字段"proctime")
    .window(Over partitionBy 'a orderBy 'proctime preceding UNBOUNDED_RANGE as 'w)
    // 无界的事件时间Row-count over window (时间字段 "rowtime")
    .window(Over partitionBy 'a orderBy 'rowtime preceding UNBOUNDED_ROW as 'w)
    //无界的处理时间Row-count over window (时间字段 "rowtime")
    .window(Over partitionBy 'a orderBy 'proctime preceding UNBOUNDED_ROW as 'w)

    2） 有界的over window
    // 有界的事件时间over window (时间字段 "rowtime"，之前1分钟)
    .window(Over partitionBy 'a orderBy 'rowtime preceding 1.minutes as 'w)
    // 有界的处理时间over window (时间字段 "rowtime"，之前1分钟)
    .window(Over partitionBy 'a orderBy 'proctime preceding 1.minutes as 'w)
    // 有界的事件时间Row-count over window (时间字段 "rowtime"，之前10行)
    .window(Over partitionBy 'a orderBy 'rowtime preceding 10.rows as 'w)
    // 有界的处理时间Row-count over window (时间字段 "rowtime"，之前10行)
    .window(Over partitionBy 'a orderBy 'proctime preceding 10.rows as 'w)
    
sql：
	Group BY
	1.TUMBLE(time_attr, interval)
		定义一个滚动窗口，第一个参数是时间字段，第二个参数是窗口长度。
    2.HOP(time_attr, interval, interval)
    	定义一个滑动窗口，第一个参数是时间字段，第二个参数是窗口滑动步长，第三个是窗口长度。
    3.SESSION(time_attr, interval)
    	定义一个会话窗口，第一个参数是时间字段，第二个参数是窗口间隔（Gap）。
    TUMBLE_START(time_attr, interval)
    TUMBLE_END(time_attr, interval)
    TUMBLE_ROWTIME(time_attr, interval)
    TUMBLE_PROCTIME(time_attr, interval)
    4.OVER
```

 

+  函数 

| 函数类型   | SQL                       | Table API                      |
| ---------- | ------------------------- | ------------------------------ |
| 比较函数   | value1 = value2           | ANY1 === ANY2                  |
|            | value1 > value2           | ANY1 > ANY2                    |
| 逻辑函数   | boolean1 OR boolean2      | BOOLEAN1                       |
|            | boolean IS FALSE          | BOOLEAN.isFalse                |
|            | NOT boolean               | !BOOLEAN                       |
| 算术函数   | numeric1 + numeric2       | NUMERIC1 + NUMERIC2            |
|            | POWER(numeric1, numeric2) | NUMERIC1.power(NUMERIC2)       |
| 字符串函数 | string1                   |                                |
|            | UPPER(string)             | STRING.upperCase()             |
|            | CHAR_LENGTH(string)       | STRING.charLength()            |
| 时间函数   | DATE string               | STRING.toDate                  |
|            | TIMESTAMP string          | STRING.toTimestamp             |
|            | CURRENT_TIME              | currentTime()                  |
|            | INTERVAL string range     | NUMERIC.days   NUMERIC.minutes |
| 聚合函数   | COUNT(*)                  | FIELD.count                    |
|            | SUM([ ALL                 | DISTINCT ] expression)         |
|            | RANK()                    | WINDOW.rank()                  |
|            | ROW_NUMBER()              | WINDOW.rowNumber()             |

-  用户自定义函数UDF 

```plain
tableEnv.registerFunction("hashCode", hashCode)

1.标量函数
可以将0、1或多个标量值，映射到新的标量值
class HashCode( factor: Int ) extends ScalarFunction {
  def eval( s: String ): Int = {
    s.hashCode * factor
  }
}
2.表函数joinLateral
可以将0、1或多个标量值作为输入可以返回任意数量的行作为输出
class Split(separator: String) extends TableFunction[(String, Int)]{
  def eval(str: String): Unit = {
    str.split(separator).foreach(
      word => collect((word, word.length))
    )
  }
}
3.聚合函数aggregate
首先，它需要一个累加器，用来保存聚合中间结果的数据结构（状态）。可以通过调用AggregateFunction的createAccumulator（）方法创建空累加器。
随后，对每个输入行调用函数的accumulate（）方法来更新累加器。
处理完所有行后，将调用函数的getValue（）方法来计算并返回最终结果。

class AvgTempAcc {
  var sum: Double = 0.0
  var count: Int = 0
}
class AvgTemp extends AggregateFunction[Double, AvgTempAcc] {
  override def getValue(accumulator: AvgTempAcc): Double =
    accumulator.sum / accumulator.count

  override def createAccumulator(): AvgTempAcc = new AvgTempAcc

  def accumulate(accumulator: AvgTempAcc, temp: Double): Unit ={
    accumulator.sum += temp
    accumulator.count += 1
  }
}
4.表聚合函数flatAggregate
把一个表中数据，聚合为具有多行和多列的结果表

class Top2TempAcc{
  var highestTemp: Double = Int.MinValue
  var secondHighestTemp: Double = Int.MinValue
}

class Top2Temp extends TableAggregateFunction[(Double, Int), Top2TempAcc]{
  
  override def createAccumulator(): Top2TempAcc = new Top2TempAcc

  def accumulate(acc: Top2TempAcc, temp: Double): Unit ={
    if( temp > acc.highestTemp ){
      acc.secondHighestTemp = acc.highestTemp
      acc.highestTemp = temp
    } else if( temp > acc.secondHighestTemp ){
      acc.secondHighestTemp = temp
    }
  }

  def emitValue(acc: Top2TempAcc, out: Collector[(Double, Int)]): Unit ={
    out.collect(acc.highestTemp, 1)
    out.collect(acc.secondHighestTemp, 2)
  }
}
```

 

