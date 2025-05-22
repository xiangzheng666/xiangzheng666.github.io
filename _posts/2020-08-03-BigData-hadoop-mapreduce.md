---
categories: [BigData]
tags: [hadoop,Mapreduce]
---
# hadoop-Mapreduce

AppMaster:负责整个程序的过程调度及状态协调。  
MapTask:负责Map阶段的整个数据处理流程。  
ReduceTask:负责Reduce阶段的整个数据处理流程。

+  运行机制 

```plain
1.InputFormat数据输入
    MapTask的并行度：
        1)一个Job的Map阶段并行度由客户端在提交Job时的切片数决定
        2)每一个Splitt切片分配一个MapTask并行实例处理
        3)默认情况下，切片大小=BlockSize
        4)切片时不考虑数据集整体，而是逐个针对每一个文件单独切片
    FileInputFormat切片机制------不管文件多小，都会是一个单独的切片
    	(1)简单地按照文件的内容长度进行切片
        (2)切片大小，默认等于Bloc大小
        (3)切片时不考虑数据集整体，而是逐个针对每一个文件单独切片
        1.TextlnputFormat
            k:键是存储该行在整个文件中的起始字节偏移量，LongWritable类型。
            v:值是这行的内容，不包括任何行终止符（换行符和回车符），
        2.KeyValue TextInputFormat
        	被分隔符分割为k,v
      	3.NLinelnputFormat
      		代表每个ma即进程处理的nputSplit不再按Block块去划分，而是按
			NlineInputFormat指定的行数N来划分。即输入文件的总行数=切片数
    CombineTextInputFormat切片机制---------虚拟存储切片最大值设置
    	虚拟存储过程：4：8.2=4+2.1+2.1
    	（a）判断虚拟存储的文件大小是否大于setMaxInputSplitSize值，大于等于则单独形成一个切片。
        （b）如果不大于则跟下一个虚拟存储文件进行合并，共同形成一个切片。
        （c）测试举例：有4个小文件大小分别为1.7M、5.1M、3.4M以及6.8M这四个小文件，
            则虚拟存储之后形成6个文件块，大小分别为：
            1.7M，（2.55M、2.55M），3.4M以及（3.4M、3.4M）
            最终会形成3个切片，大小分别为：
            （1.7+2.55）M，（2.55+3.4）M，（3.4+3.4）M
    自定义InputFormat
   		1、自定义一个类继承FileInputFormat
            (l)重写isSplitable()方法，返false不可切割
            (2)重写createRecordReader(),创建自定义的RecordReader>对象，并初始化
        2、改写RecordReader,实现一次读取一个完整文件封装为KV
            (1)采用IO流一次读取一个文件输出到valuer中，因为设置了不可切片，
               最终把所有文件都封装到了vae中
            (2)获取文件路径信息+名称，并设置key
        3、设置Driver
            (1)设置输入的inputFormat
            	job.setInputFormatclass(WholeFileInputformat.class);
            (2)设置输出的outputFormat
            	job.setoutputFormatclass(SequenceFileOutputFormat.class);
2.Mapper机制
	（1）Read阶段：MapTask通过用户编写的RecordReader，
		从输入InputSplit中解析出一个个key/value。
	（2）Map阶段：该节点主要是将解析出的key/value交给用户编写map()函数处理，
		并产生一系列新的key/value。
	（3）Collect收集阶段：在用户编写map()函数中，当数据处理完成后，
        一般会调用OutputCollector.collect()输出结果。
        在该函数内部，它会将生成的key/value分区（调用Partitioner），
        并写入一个环形内存缓冲区中。
	（4）Spill阶段：即“溢写”，当环形缓冲区满后，
        MapReduce会将数据写到本地磁盘上，生成一个临时文件。
        需要注意的是，将数据写入本地磁盘之前，先要对数据进行一次本地排序，
        并在必要时对数据进行合并、压缩等操作。
        	1.步骤1：利用快速排序算法对缓存区内的数据进行排序，排序方式是，
        	先按照分区编号Partition进行排序，然后按照key进行排序。
        	这样，经过排序后，数据以分区为单位聚集在一起，且同一分区内所有数据按照key有序。
            2.步骤2：按照分区编号由小到大依次将每个分区中的数据
            写入任务工作目录下的临时文件output/spillN.out（N表示当前溢写次数）中。
            如果用户设置了Combiner，则写入文件之前，对每个分区中的数据进行一次聚集操作。
            3.步骤3：将分区数据的元信息写到内存索引数据结构SpillRecord中，
            其中每个分区的元信息包括在临时文件中的偏移量、
            压缩前数据大小和压缩后数据大小。如果当前内存索引大小超过1MB
            ，则将内存索引写到文件output/spillN.out.index中。
	（5）Combine阶段：当所有数据处理完后，
        MapTask会将所有临时文件合并成一个大文件，并保存到文件output/file.out中，
        同时生成相应的索引文件output/file.out.index。在进行文件合并过程中，
        MapTask以分区为单位进行合并。对于某个分区，它将采用多轮递归合并的方式。
        每轮合并io.sort.factor（默认10）个文件，并将产生的文件重新加入待合并列表中，
        对文件排序后，重复以上过程，直到最终得到一个大文件。
3.Shuffle机制
	mapper输出胡k,v
	重写Partitioner
        1.通过k将数据输出到那个分区
        2.通过k进行排序输出到分区
4.Combiner机制
    Combiner是在每一个MapTask所在的节点运行，
    Reducer是接收全局所有Mapperl的输出结果；
    作用于reduce一样，进行局部汇总，以减小网络传输量
    自定义一个Combiner继承Reducer，重写Reduce方法
5.GroupingComparator分组
	对Reduce阶段的数据根据某一个或几个字段进行分组
	使reduce可以多个输出，即每个分组进行reduce操作
	将compare方法覆盖bean的compareTo方法
	（1）自定义类继承WritableComparator
	（2）重写compare()方法
6.ReduceTask机制
	（1）Copy阶段：ReduceTask从各个MapTask上远程拷贝一片数据，
		并针对某一片数据，如果其大小超过一定阈值，则写到磁盘上，否则直接放到内存中。
	（2）Merge阶段：在远程拷贝数据的同时，ReduceTask启动了两个后台线程
		对内存和磁盘上的文件进行合并，以防止内存使用过多或磁盘上文件过多。
	（3）Sort阶段：按照MapReduce语义，用户编写reduce()函数
        输入数据是按key进行聚集的一组数据。
        为了将key相同的数据聚在一起，Hadoop采用了基于排序的策略。
        由于各个MapTask已经实现对自己的处理结果进行了局部排序，
        因此，ReduceTask只需对所有数据进行一次归并排序即可。
	（4）Reduce阶段：reduce()函数将计算结果写到HDFS上
7.OutputFormat数据输出机制
	1.文本输出TextOutputFormat
      默认的输出格式是TextOutputFormat,
      它把每条记录写为文本行。它的键和值可以是任意类型，
      因为TextOutputFormat调用toStringO方法把它们转换为字符串。
    2.SequenceFileOutputFormat
      将SequenceFileOutputFormat输出作为后续MapReduce任务的输入，这便是一种好的输出
      格式，因为它的格式紧凑，很容易被压缩。
    3.自定义OutputFormat
      根据用户需求，自定义实现输出。
      (1)自定义一个类继承FileOutputFormat。。
	  (2)改写RecordWriter,具体改写输出数据的方法write()。
```

+  join 

```plain
reduce Join数据倾斜，将计算大部分放到reduce上面
Map Join适用于一张表十分小、一张表很大的场景。
```

+  总结 

```plain
1.输入数据接口：InputFormat
    (1)默认使用的实现类是：TextInputFormat
    (2)TextInputFormat的功能逻辑是：一次读一行文本，然后将该行的起始
    偏移量作为key,行内容作为value返回。
    (3)Key Value TextInputFormat每一行均为一条记录，被分隔符分割为key,
    value。。默认分隔符是tab(t).
    (4)NlineInputFormat按照指定的行数N来划分切片。
    (S)Combine TextInputFormat可l以把多个小文件合并成一个切片处理，提高
    处理效率。
    (6)用户还可以自定义InputFormat.
2.逻辑处理接口：Mapper
	用户根据业务需求实现其中三个方法：map（）seup（）cleanup（）
3.Partitioner分区
    (1)有默认实现IashPartitioner,逻辑是根据key的哈希值和
    numReduces来返回一个分区号；
    key.hashCode(O&Integer.MAXVALUE%numReduces
    (2)如果业务上有特别的需求，可以自定义分区。
4.Comparable排序
    (1)当我们用自定义的对象作为ky来输出时，就必须要实现
    WritableComparable接口，重写其中的compareTo方法。
    (2)部分排序：对最终输出的每一个文件进行内部排序。
    (3)全排序：对所有数据进行排序，通常只有一个Reduce.
    (4)二次排序：排序的条件有两个。
5.Combiner合并
    Combiner合并可以提高程序执行效率，减少IO传输。但是使用时必须不能影
    响原有的业务处理结果。
6.Reduce端分组：GroupingComparator
    在Reducei端对key进行分组。应用于：在接收的key为bean对象时，想让一个或几个字
    段相同（全部字段比较不相同）的key进入到同一个reduce方法时，可以采用分组排序。
7.逻辑处理接口：Reducer
	用户根据业务需求实现其中三个方法：reduce（）setup（）cleanup(）
8.输出数据接口：OutputFormat
    (1)默认实现类是TextOutputFormat,功能逻辑是：将每一个KV对，向目标文
    本文件输出一行。
    (2)将SequenceFileOutputFormat输出作为后续MapReduce任务的输入，这便是
    一种好的输出格式，因为它的格式紧凑，很容易被压缩。
    (3)用户还可以自定义OutputFormat。
```

+  Hadoop数据压缩 

```plain
DEFLATE	直接使用	DEFLATE	不可切分	和文本处理一样，不需要修改
Gzip	直接使用	DEFLATE	不可切分	和文本处理一样，不需要修改
bzip2	直接使用	bzip2	可切分	 	 和文本处理一样，不需要修改
LZO	    需要安装	LZO	    可切分      需要建索引，还需要指定输入格式
Snappy	需要安装	Snappy	不可切分	和文本处理一样，不需要修改
```

 

