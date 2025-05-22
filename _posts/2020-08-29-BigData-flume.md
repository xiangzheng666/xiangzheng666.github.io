---
categories: [BigData]
tags: [Flume]
---
# Flume

Flume是Cloudera提供的一个高可用的，高可靠的，分布式的海量日志采集、聚合和传输的系统。Flume基于流式架构，灵活简单。

+  Agent  
   Agent是一个JVM进程，它以事件的形式将数据从源头送至目的。  
   Agent主要有3个部分组成，Source、Channel、Sink。 

+  Source  
   Source是负责接收数据到Flume Agent的组件。Source组件可以处理各种类型、各种格式的日志数据，包括avro、thrift、exec、jms、spooling directory、netcat、sequence generator、syslog、http、legacy。 

   远程主机收集 syslog 日志

   ```
   a1.sources.r1.type = syslogtcp
   a1.sources.r1.host = 192.168.1.10
   a1.sources.r1.port = 5140
   a1.sources.r1.channels = c1
   ```

   Spooling Directory Source 组件

   用于监控指定目录，并将新文件内容转发到 Flume 管道

   ```
   a1.sources.r1.type = spooldir
   a1.sources.r1.spoolDir = /path/to/your/directory
   a1.sources.r1.fileHeader = true
   a1.sources.r1.fileSuffix = .COMPLETED
   a1.sources.r1.channels = c1
   ```

   Avro Source

   使用 Avro 协议向 Flume 管道发送数据

   ```
   a1.sources.r1.type = avro
   a1.sources.r1.bind = 0.0.0.0
   a1.sources.r1.port = 41414
   a1.sources.r1.channels = c1
   ```

   HTTP Source

   用于 Web 客户端收集数据

   ```
   a1.sources.r1.type = http
   a1.sources.r1.bind = 0.0.0.0
   a1.sources.r1.port = 8080
   a1.sources.r1.handler = org.apache.flume.source.http.JSONHandler
   a1.sources.r1.channels = c1
   ```

   Exec Source

   执行外部命令或脚本，将其输出作为数据源

   ```
   a1.sources.r1.type = exec
   a1.sources.r1.command = tail -F /var/log/messages
   a1.sources.r1.channels = c1
   ```

   其他 Source 类型

   - Kafka Source
   - Netcat Source

+  Sink  Sink不断地轮询Channel中的事件且批量地移除它们，并将这些事件批量写入到存储或索引系统、或者被发送到另一个Flume Agent。  
   Sink组件目的地包括hdfs、logger、avro、thrift、ipc、file、HBase、solr、自定义。 

   - File Sink：将数据输出到本地文件系统中的文件。

    - HDFS Sink：将数据输出到Hadoop分布式文件系统（HDFS）中。

    - Kafka Sink：将数据输出到Kafka消息队列中。

    - Elasticsearch Sink：将数据输出到Elasticsearch搜索引擎中。

    - Logger Sink：将数据输出到日志文件中。

    - Avro Sink：将数据以Avro格式输出到本地文件系统或HDFS中。

+  Channel  
   Channel是位于Source和Sink之间的缓冲区。因此，Channel允许Source和Sink运作在不同的速率上。Channel是线程安全的，可以同时处理几个Source的写入操作和几个Sink的读取操作。  
   Flume自带两种Channel：Memory Channel和File Channel。  
   Memory Channel是内存中的队列。Memory Channel在不需要关心数据丢失的情景下适用。如果需要关心数据丢失，那么Memory Channel就不应该使用，因为程序死亡、机器宕机或者重启都会导致数据丢失。  
   File Channel将所有事件写到磁盘。因此在程序关闭或机器宕机的情况下不会丢失数据。 
+  Event  
   传输单元，Flume数据传输的基本单元，以Event的形式将数据从源头送至目的地。Event由Header和Body两部分组成，Header用来存放该event的一些属性，为K-V结构，Body用来存放该条数据，形式为字节数组。 
+  channel的 事务机制 
+  Put事务流程  
   1.doPut批数据先写入临时爱中区putlst  
   2.doComm it查channelp内存队列是香足够合并。  
   3.doRollbackchannelf内存队列空间不足，回数据 
+  Take事务  
   1.doTake将数据取到临时援中区☒akeL凵ist,并将数据发送到HDFS  
   2.docommit:如果数据全部发送成功，则清除荆临时爱中☒akeList  
   3.doRollback数据发送过程中如果出现异常，rollback将剂临时等中区t  
   4.akeLis中的据归还给channell内存队列。 
+  组件 
   -  ChannelSelector  
      ReplicatingSelector会将同一个Event发往所有的Channel，  
      Multiplexing会根据相应的原则，将不同的Event发往不同的Channel。 
   -  SinkProcessor  
      DefaultSinkProcessor对应的是单个的Sink，  
      LoadBalancingSinkProcessor可以实现负载均衡的功能，  
      FailoverSinkProcessor可以错误恢复的功能。 
+  拓扑结构 
   -  简单串联 
   -  复制和多路复用 
      * 数据丢失问题：在Flume的多路复用模式下，如果多个Sink共享同一个Channel，并且它们的处理速度不同，可能会出现事件丢失的问题。为了避免数据丢失，需要合理配置Channel的事务容量和Sink的处理能力，确保所有的Sink都能够正常工作。
      * a1.sources.r1.selector.type = replicating
   -  负载均衡和故障转移 
      *  a1.sinkgroups.g1.processor.type = failover  
         a1.sinkgroups.g1.processor.priority.k1 = 5  
         a1.sinkgroups.g1.processor.priority.k2 = 10  
         a1.sinkgroups.g1.processor.maxpenalty = 10000 
   -  聚合 
      * 端口
+  自定义Source 
   -  configure方法中读取Flume配置文件中定义的参数 
   -  process方法用于封装并发送事件到Channel 
   -  

```plain
public class MySource extends AbstractSource implements Configurable, PollableSource {

    //定义配置文件将来要读取的字段
    private Long delay;
    private String field;

    //初始化配置信息
    @Override
    public void configure(Context context) {
        delay = context.getLong("delay");
        field = context.getString("field", "Hello!");
    }

    @Override
    public Status process() throws EventDeliveryException {
        try {
            //创建事件头信息
            HashMap<String, String> hearderMap = new HashMap<>();
            //创建事件
            SimpleEvent event = new SimpleEvent();
            //循环封装事件
            for (int i = 0; i < 5; i++) {
                //给事件设置头信息
                event.setHeaders(hearderMap);
                //给事件设置内容
                event.setBody((field + i).getBytes());
                //将事件写入channel
                getChannelProcessor().processEvent(event);
                Thread.sleep(delay);
            }
        } catch (Exception e) {
            e.printStackTrace();
            return Status.BACKOFF;
        }
        return Status.READY;
    }
    @Override
    public long getBackOffSleepIncrement() {
        return 0;
    }
    @Override
    public long getMaxBackOffSleepInterval() {
        return 0;
    }
}
```

 

+  自定义Interceptor 
   -  initialize方法中读取Flume配置文件 
   -  在intercept方法中对事件进行处理。可以通过调用Event的getHeaders和getBody方法获取事件的头信息和内容，并对其进行处理 
   -  

```plain
public class CustomInterceptor implements Interceptor {
    @Override
    public void initialize() {
    }
    @Override
    public Event intercept(Event event) {
        byte[] body = event.getBody();
        if (body[0] < 'z' && body[0] > 'a') {
            event.getHeaders().put("type", "letter");
        } else if (body[0] > '0' && body[0] < '9') {
            event.getHeaders().put("type", "number");
        }
        return event;
    }
    @Override
    public List<Event> intercept(List<Event> events) {
        for (Event event : events) {
            intercept(event);
        }
        return events;
    }

    @Override
    public void close() {
    }

    public static class Builder implements Interceptor.Builder {
        @Override
        public Interceptor build() {
            return new CustomInterceptor();
        }
        @Override
        public void configure(Context context) {
        }
    }
}
```

 

    -  a1.sources.r1.interceptors = i1  

a1.sources.r1.interceptors.i1.type = com.atguigu.flume.interceptor.CustomInterceptor$Builder  
a1.sources.r1.selector.type = multiplexing  
a1.sources.r1.selector.header = type  
	表示选择器的判断依据是事件的头信息中的type字段。  
a1.sources.r1.selector.mapping.letter = c1  
	表示当事件的type值为letter时，将该事件发送到名为c1的Channel中。  
a1.sources.r1.selector.mapping.number = c2  
	表示当事件的type值为number时，将该事件发送到名为c2的Channel中。 

+  自定义Sink 
   -  

```plain
public class MySink extends AbstractSink implements Configurable {

    //创建Logger对象
    private static final Logger LOG = LoggerFactory.getLogger(AbstractSink.class);

    private String prefix;
    private String suffix;

    @Override
    public Status process() throws EventDeliveryException {

        //声明返回值状态信息
        Status status;

        //获取当前Sink绑定的Channel
        Channel ch = getChannel();

        //获取事务
        Transaction txn = ch.getTransaction();

        //声明事件
        Event event;

        //开启事务
        txn.begin();

        //读取Channel中的事件，直到读取到事件结束循环
        while (true) {
            event = ch.take();
            if (event != null) {
                break;
            }
        }
        try {
            //处理事件（打印）
            LOG.info(prefix + new String(event.getBody()) + suffix);

            //事务提交
            txn.commit();
            status = Status.READY;
        } catch (Exception e) {

            //遇到异常，事务回滚
            txn.rollback();
            status = Status.BACKOFF;
        } finally {

            //关闭事务
            txn.close();
        }
        return status;
    }

    @Override
    public void configure(Context context) {

        //读取配置文件内容，有默认值
        prefix = context.getString("prefix", "hello:");

        //读取配置文件内容，无默认值
        suffix = context.getString("suffix");
    }
}
```

 

+  flume数据流 
   -  Ganglia  
      gmond（Ganglia Monitoring Daemon）是一种轻量级服务，安装在每台需要收集指标数据的节点主机上。使用gmond，你可以很容易收集很多系统指标数据，如CPU、内存、磁盘、网络和活跃进程的数据等。  
      gmetad（Ganglia Meta Daemon）整合所有信息，并将其以RRD格式存储至磁盘的服务。  
      gweb（Ganglia Web）Ganglia可视化工具，gweb是一种利用浏览器显示gmetad所存储数据的PHP前端。在Web界面中以图表方式展现集群的运行状态下收集的多种不同指标数据。 

