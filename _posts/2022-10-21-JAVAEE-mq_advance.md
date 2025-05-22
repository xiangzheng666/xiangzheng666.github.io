---
categories: [javaEE]
tags: [MQ]
---
# 异步通信

- 生产者消息确认

  - 避免消息**发送到MQ过程**中丢失
  - 生产者确认机制
    - 返回结果有两种方式：

      - publisher-confirm，发送者确认
        - 消息成功投递到交换机，返回ack
        - 消息未投递到交换机，返回nack
      - publisher-return，发送者回执
        - 消息投递到交换机了，但是没有路由到队列。返回ACK，及路由失败原因。
  - mq持久化
    - 如果突然宕机，也可能导致消息丢失。要想确保消息在RabbitMQ中安全保存，必须开启消息持久化机制
    - 交换机持久化
    - 队列持久化
    - 消息持久化 delivery-mode

- 消费者消息确认

  - RabbitMQ确认消息被消费者消费后会立刻删除。而RabbitMQ是通过消费者回执来确认消费者是否成功处理消息的
  - 消费者确认机制
    - 而SpringAMQP则允许配置三种确认模式：
      - •manual：手动ack，需要在业务代码结束后，调用api发送ack。
      - •auto：自动ack，由spring监测listener代码是否出现异常，没有异常则返回ack；抛出异常则返回nack
      - •none：关闭ack，MQ假定消费者获取消息后会成功处理，因此消息投递后立即被删除
  - 当消费者出现异常后，消息会不断requeue（重入队）到队列，再重新发送给消费者，然后再次异常，再次requeue，无限循环，导致mq的消息处理飙升，带来不必要的压力：
    - 失败重试机制
      - 本地重试
        - **达到最大重试次数后，消息会被丢弃，这是由Spring内部机制决定的。**
        - Spring的retry机制，在消费者出现异常时利用本地重试，而不是无限制的requeue到mq队列。
      - 失败策略
        - 重试次数耗尽，如果消息依然失败，则需要有MessageRecovery接口来处理，它包含三种不同的实现：
          - RejectAndDontRequeueRecoverer：重试耗尽后，直接reject，丢弃消息。默认就是这种方式
          - ImmediateRequeueMessageRecoverer：重试耗尽后，返回nack，消息重新入队
          - RepublishMessageRecoverer：重试耗尽后，将失败消息投递到指定的交换机

- 死信

  - 消费者使用basic.reject或 basic.nack声明消费失败，并且消息的requeue参数设置为false

  - 消息是一个过期消息，超时无人消费

  - 要投递的队列消息满了，无法投递

  - **死信交换机**：包含死信的队列配置了`dead-letter-exchange`属性，指定交换机

    - 死信交换机
    - 死信交换机与死信队列绑定的RoutingKey

  - 死信

    - 消息被消费者reject或者返回nack

    - 消息超时未消费

      - 消息所在的队列设置了超时时间 x-message-ttl

      - 消息本身设置了超时时间 setExpiration

      - 延迟队列（Delay Queue）模式。

        - 声明一个交换机，添加delayed属性为true

          发送消息时，添加x-delay头，值为超时时间

    - 队列满了

- 消息堆积

  - 增加更多消费者，提高消费速度。也就是我们之前说的work queue模式
  - 扩大队列容积，提高堆积上限
  - 惰性队列
    - 接收到消息后直接存入磁盘而非内存
    - 消费者要消费消息时才会从磁盘中读取并加载到内存
    - 支持数百万条的消息存储

- MQ集群

  - •**普通集群**：是一种分布式集群，将队列分散到集群的各个节点，从而提高整个集群的并发能力。

    •**镜像集群**：是一种主从集群，普通集群的基础上，添加了主从备份功能，提高集群的数据可用性。

  

