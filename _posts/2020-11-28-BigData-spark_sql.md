---
categories: [BigData]
tags: [Spark SQL]
---
# Spark SQL


+  Spark SQL 通过提供基于事务的写入和批量写入来实现 Exactly-Once 语义。Spark SQL 通过使用 Catalyst 引擎和 Spark SQL 执行引擎来提供一致性和容错性。  
具体来说，Spark SQL 采用基于写入事务和批量写入的方法来实现 Exactly-Once 语义。在写入数据时，Spark SQL 会创建一个事务，对于每个批次的数据，都会在事务内部进行写入，并使用 Spark 的 WAL（Write Ahead Log）来记录事务的信息。如果发生故障，Spark SQL 可以通过 WAL 进行恢复，确保每个批次的数据只被写入一次。  
此外，Spark SQL 还提供了幂等性写入操作来避免重复写入，例如，在将数据写入数据库时，可以使用 INSERT IGNORE 或者 UPSERT 操作来保证数据只被写入一次。这些幂等性的写入操作可以确保即使在出现故障或者重试时也不会对数据造成重复写入的影响。 
+  DataFrame与RDD的主要区别在于，前者带有schema元信息，即DataFrame所表示的二维表数据集的每一列都带有名称和类型，Spark Core只能在stage层面进行简单、通用的流水线优化，+ Catalyst 优化器 
+  DSL 
    - df.select("name").show()
+  SQL 
    - df.createOrReplaceTempView("people")
    - spark.sql("SELECT * FROM people")
+  DataFrame 
    -  创建DataFrame 
        *  spark.read.  
csv  format  jdbc  json  load  option  options  orc  parquet  schema  table  text  textFile 
    -  RDD转换为DataFrame 
        *  import spark.implicits._ 
        *  手动确定转换 
            + peopleRDD.map{x=> val fields=x.split(",");(fields(0),fields(1).trim.toInt)}.toDF("name","age").show
        *  通过样例类反射转换 
            + peopleRDD.map{x=> var fields=x.split(",");People(fields(0),fields(1).toInt)}.toDF.show
        *  创建 
            +  

```plain
val rowRdd: RDD[Row] = rdd.map(x => Row(x._1, x._2))
val types = StructType(Array(StructField("name", StringType), StructField("age", IntegerType)))
val df: DataFrame = spark.createDataFrame(rowRdd, types)
```

 

    -  DataFrame转换为RDD 
        * df.rdd
+  DataSet：DataFrame=DataSet[Row] 
    - RDD转换为DataSet 
        * peopleRDD.map(line => {val fields = line.split(",");Person(fields(0),fields(1). toInt)}).toDS
    - DataSet转换为RDD 
        * DS.rdd
+  DataFrame转化为DataSet 
    - df.as[Person]
+  Dataset转为DataFrame 
    - ds.toDF
+  自定义函数 
    -  UDF  1 - 1 
        * spark.udf.register("addName",(x:String)=> "Name:"+x)
    -  UDAF  多行,返回一行 
        *  

```plain
class MyAverage extends UserDefinedAggregateFunction {
  // 给聚合函数定义输入的数据类型（Integer）
  def inputSchema: StructType = StructType(StructField("inputColumn", LongType) :: Nil)

  // 给聚合函数定义中间缓存区的数据类型
  def bufferSchema: StructType = {
    StructType(StructField("sum", LongType) :: StructField("count", LongType) :: Nil)
  }

  // 给聚合函数定义返回结果的数据类型（Double）
  def dataType: DataType = DoubleType

  // 基于初始化数据初始化聚合缓冲区
  def initialize(buffer: MutableAggregationBuffer): Unit = {
    buffer(0) = 0L
    buffer(1) = 0L
  }

  // 对于输入的每个数据进行聚合缓冲操作
  def update(buffer: MutableAggregationBuffer, input: Row): Unit = {
    if (!input.isNullAt(0)) {
      buffer(0) = buffer.getLong(0) + input.getLong(0)
      buffer(1) = buffer.getLong(1) + 1
    }
  }

  // 合并两个聚合缓冲区的数据
  def merge(buffer1: MutableAggregationBuffer, buffer2: Row): Unit = {
    buffer1(0) = buffer1.getLong(0) + buffer2.getLong(0)
    buffer1(1) = buffer1.getLong(1) + buffer2.getLong(1)
  }

  // 根据计算结果生成最终的结果
  def evaluate(buffer: Row): Any = {
    buffer.getLong(0).toDouble / buffer.getLong(1)
```

 

+  SparkSQL数据的加载与保存 
    - 加载数据 
        * spark.read.
        * spark.read.format("…")[.option("…")].save("…")
        * 在文件上直接运行SQL
    - 保存数据 
        * df.write.format("…")[.option("…")].save("…")
        * df.write.save
        * df.write.mode
+  默认数据源Parquet格式 
+  MySQL 
    -  

```plain
//方式1：通用的load方法读取
spark.read.format("jdbc")
    .option("url", "jdbc:mysql://hadoop202:3306/test")
    .option("driver", "com.mysql.jdbc.Driver")
    .option("user", "root")
    .option("password", "123456")
    .option("dbtable", "user")
    .load().show


//方式2:通用的load方法读取 参数另一种形式
spark.read.format("jdbc")
.options(Map("url"->"jdbc:mysql://hadoop202:3306/test?user=root&password=123456",
"dbtable"->"user","driver"->"com.mysql.jdbc.Driver")).load().show
```

 

+  Hive 
    -  

```plain
内嵌Hive直接使用
spark.sql("show tables").show
外部Hive
    hive-site.xml拷贝到spark的conf/目录下
    Mysql的驱动
    copy到Spark的jars/目录下
spark.sql("show tables").show
```

 

+  Spark SQL CLI 
    - bin/spark-sql 类似Hive窗口

