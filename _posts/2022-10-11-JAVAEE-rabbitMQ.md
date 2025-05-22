---
categories: [javaEE]
tags: [MQ]
---
# MQ

- AMQP

  - Advanced Message Queuing Protocol,是用于在应用程序
    之间传递业务消息的开放标准。该协议与语言和平台无关，更符合微服务中独立性的要求。
    
  - ```
    public class PublisherTest {
        @Test
        public void testSendMessage() throws IOException, TimeoutException {
            // 1.建立连接
            ConnectionFactory factory = new ConnectionFactory();
            // 1.1.设置连接参数，分别是：主机名、端口号、vhost、用户名、密码
            factory.setHost("192.168.150.101");
            factory.setPort(5672);
            factory.setVirtualHost("/");
            factory.setUsername("itcast");
            factory.setPassword("123321");
            // 1.2.建立连接
            Connection connection = factory.newConnection();
    
            // 2.创建通道Channel
            Channel channel = connection.createChannel();
    
            // 3.创建队列
            String queueName = "simple.queue";
            channel.queueDeclare(queueName, false, false, false, null);
    
            // 4.发送消息
            String message = "hello, rabbitmq!";
            channel.basicPublish("", queueName, null, message.getBytes());
            System.out.println("发送消息成功：【" + message + "】");
    
            // 5.关闭通道和连接
            channel.close();
            connection.close();
    
        }
    }
    
    public class ConsumerTest {
    
        public static void main(String[] args) throws IOException, TimeoutException {
            // 1.建立连接
            ConnectionFactory factory = new ConnectionFactory();
            // 1.1.设置连接参数，分别是：主机名、端口号、vhost、用户名、密码
            factory.setHost("192.168.150.101");
            factory.setPort(5672);
            factory.setVirtualHost("/");
            factory.setUsername("itcast");
            factory.setPassword("123321");
            // 1.2.建立连接
            Connection connection = factory.newConnection();
    
            // 2.创建通道Channel
            Channel channel = connection.createChannel();
    
            // 3.创建队列
            String queueName = "simple.queue";
            channel.queueDeclare(queueName, false, false, false, null);
    
            // 4.订阅消息
            channel.basicConsume(queueName, true, new DefaultConsumer(channel){
                @Override
                public void handleDelivery(String consumerTag, Envelope envelope,
                                           AMQP.BasicProperties properties, byte[] body) throws IOException {
                    // 5.处理消息
                    String message = new String(body);
                    System.out.println("接收到消息：【" + message + "】");
                }
            });
            System.out.println("等待接收消息。。。。");
        }
    }
    ```
    
    

- Spring-AMQP

  - Spring AMQP是基于AMQP协议定义的一套API规范，提供了模板来
    发送和接收消息。包含两部分，其中spring-amqp是基础抽象，
    spring-rabbit是底层的默认实现。
  - 自动声明队列、交换机及其绑定关系
  - 基于注解的监听器模式，异步接收消息
  - 封装了RabbitTemplate工具，用于发送消息 

- Basic Queue 简单队列模型.publish->quene->consumer

- WorkQueue   publish->quene->(consumer,consumer...)

  - 让多个消费者绑定到一个队列，共同消费队列中的消息

- 发布/订阅   publish->exchange->(quene->(consumer,consumer...)，quene->(consumer,consumer...))

  - Publisher：生产者，也就是要发送消息的程序，但是不再发送到队列中，而是发给X（交换机）
  - Exchange：交换机，图中的X。一方面，接收生产者发送的消息。另一方面，知道如何处理消息，例如递交给某个特别队列、递交给所有队列、或是将消息丢弃。到底如何操作，取决于Exchange的类型。Exchange有以下3种类型：
    - Fanout：广播，将消息交给所有绑定到交换机的队列
      - 1）  可以有多个队列
      - 2）  每个队列都要绑定到Exchange（交换机）
      - 3）  生产者发送的消息，只能发送到交换机，交换机来决定要发给哪个队列，生产者无法决定
      - 4）  交换机把消息发送给绑定过的所有队列
      - 5）  订阅队列的消费者都能拿到消息
      
    - Direct：定向，把消息交给符合指定routing key 的队列
    
      - 队列与交换机的绑定，不能是任意绑定了，而是要指定一个`RoutingKey`（路由key）
      - 消息的发送方在 向 Exchange发送消息时，也必须指定消息的 `RoutingKey`。
      - Exchange不再把消息交给每一个绑定的队列，而是根据消息的`Routing Key`进行判断，只有队列的`Routingkey`与消息的 `Routing key`完全一致，才会接收到消息
    
    - Topic：通配符，把消息交给符合routing pattern（路由模式） 的队列
    
      - `#`：匹配一个或多个词
    
        `*`：匹配不多不少恰好1个词
  - Consumer：消费者，与以前一样，订阅队列，没有变化
  - Queue：消息队列也与以前一样，接收消息、缓存消息。

- ```
  <!--AMQP依赖，包含RabbitMQ-->
  <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-amqp</artifactId>
  </dependency>
  
  spring:
    rabbitmq:
      host: 192.168.150.101 # 主机名
      port: 5672 # 端口
      virtual-host: / # 虚拟主机
      username: itcast # 用户名
      password: 123321 # 密码
      
  @Test
  public void testSendMessage2SimpleQueue() {
      String queueName = "simple.queue";
      String message = "hello, spring amqp!";
      rabbitTemplate.convertAndSend(queueName, message);
  }
  
  @Test
  public void testSendMessage2WorkQueue() throws InterruptedException {
      String queueName = "simple.queue";
      String message = "hello, message__";
      for (int i = 1; i <= 50; i++) {
      rabbitTemplate.convertAndSend(queueName, message + i);
      Thread.sleep(20);
  }
  
  @Test
  public void testSendFanoutExchange() {
      // 交换机名称
      String exchangeName = "itcast.fanout";
      // 消息
      String message = "hello, every one!";
      // 发送消息
      rabbitTemplate.convertAndSend(exchangeName, "", message);
  }
  
  @Test
  public void testSendDirectExchange() {
      // 交换机名称
      String exchangeName = "itcast.direct";
      // 消息
      String message = "hello, red!";
      // 发送消息
      rabbitTemplate.convertAndSend(exchangeName, "red", message);
  }
  
  @Test
  public void testSendTopicExchange() {
      // 交换机名称
      String exchangeName = "itcast.topic";
      // 消息
      String message = "今天天气不错，我的心情好极了!";
      // 发送消息
      rabbitTemplate.convertAndSend(exchangeName, "china.weather", message);
  }
  
  ```

- ```
  spring:
    rabbitmq:
      host: 192.168.150.101 # 主机名
      port: 5672 # 端口
      virtual-host: / # 虚拟主机
      username: itcast # 用户名
      password: 123321 # 密码
      listener:
        simple:
          prefetch: 1 # 每次只能获取一条消息，处理完成才能获取下一个消息
  
  使用RabbitListener注解开发
  @Component
  public class SpringRabbitListener {
      @RabbitListener(queues = "simple.queue")
      public void listenSimpleQueueMessage(String msg) throws InterruptedException {
          System.out.println("spring 消费者接收到消息：【" + msg + "】");
      }
      
      
    	@RabbitListener(bindings = @QueueBinding(
              value = @Queue(name = "direct.queue1"),
              exchange = @Exchange(name = "itcast.direct", type = ExchangeTypes.DIRECT),
              key = {"red", "blue"}
      ))
      
  }
  ```
  
- 消息转换器

  - Spring采用的序列化方式是JDK序列化

  - ```
    <dependency>
        <groupId>com.fasterxml.jackson.dataformat</groupId>
        <artifactId>jackson-dataformat-xml</artifactId>
        <version>2.9.10</version>
    </dependency>
    
    
    @Bean
    public MessageConverter jsonMessageConverter(){
        return new Jackson2JsonMessageConverter();
    }
    ```

    

