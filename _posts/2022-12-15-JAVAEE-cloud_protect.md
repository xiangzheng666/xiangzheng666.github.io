---
categories: [javaEE]
tags: [雪崩]
---
# Sentinel

- 雪崩问题

  - 超时处理
  - 仓壁模式
  - 断路器
  - 限流

- sentinel

  - https://sentinelguard.io/zh-cn/index.html

  - https://github.com/alibaba/Sentinel/releases)

  - java -jar sentinel-dashboard-1.8.1.jar

    - server.port  8080  服务端口  
    - sentinel.dashboard.auth.username  sentinel  默认用户名  
    - sentinel.dashboard.auth.password  sentinel  默认密码

  - ```
    <!--sentinel-->
    <dependency>
        <groupId>com.alibaba.cloud</groupId> 
        <artifactId>spring-cloud-starter-alibaba-sentinel</artifactId>
    </dependency>
    
    server:
      port: 8088
    spring:
      cloud: 
        sentinel:
          transport:
            dashboard: localhost:8080
    ```
    
  - Service中的方法是不被Sentinel监控的，需要我们自己通过注解来标记要监控的方法
  
  - ```
    @SentinelResource("goods")
    public void queryGoods(){
        System.err.println("查询商品");
    }
    ```
  
  - 流控模式
  
    - 直接：统计当前资源的请求，触发阈值时对当前资源直接限流，也是默认的模式
    - 关联：统计与当前资源相关的另一个资源，触发阈值时，对当前资源限流
    - 链路：统计从指定链路访问到本资源的请求，触发阈值时，对指定链路限流
    - 流控效果：
  
      - 快速失败：达到阈值后，新的请求会被立即拒绝并抛出FlowException异常。是默认的处理方式。
      - warm up：预热模式，对超出阈值的请求同样是拒绝并抛出异常。但这种模式阈值会动态变化，从一个较小值逐渐增加到最大阈值。
      - 排队等待：让所有的请求按照先后次序排队执行，两个请求的间隔不能小于指定时长
  
  - 热点参数限流
  
    - 热点参数限流是**分别统计参数值相同的请求**，判断是否超过QPS阈值。
    - 而在实际开发中，可能部分商品是热点商品，例如秒杀商品，我们希望这部分商品的QPS限制与其它商品不一样，高一些。那就需要配置热点参数限流的高级选项
  
  - 隔离
  
    - SpringCloud中，微服务调用都是通过Feign来实现的，因此做客户端保护必须整合Feign和Sentinel。
  
    - ```
      feign:
        sentinel:
          enabled: true # 开启feign对sentinel的支持
      ```
  
    - 业务失败后，不能直接报错，而应该返回用户一个友好提示或者默认结果，这个就是失败降级逻辑。
  
      - ①方式一：FallbackClass，无法对远程调用的异常做处理
      - ②方式二：FallbackFactory，可以对远程调用的异常做处理
        - 实现FallbackFactory
        - 将UserClientFallbackFactory注册为一个Bean
        - @FeignClient(value = "userservice", fallbackFactory = UserClientFallbackFactory.class)
  
    - 线程隔离的两种手段
  
      - 信号量隔离
        - 给每个服务调用业务分配一个线程池，利用线程池本身实现隔离效果
      - 线程池隔离
        - 而是计数器模式，记录业务使用的线程数量，达到信号量上限时，禁止新的请求
  
  - 降级
  
    - 其思路是由**断路器**统计服务调用的异常比例、慢请求比例，如果超出阈值则会**熔断**该服务。即拦截访问该服务的一切请求；而当服务恢复时，断路器会放行访问该服务的请求。
    - 状态机包括三个状态：
  
      - closed：关闭状态，断路器放行所有请求，并开始统计异常比例、慢请求比例。超过阈值则切换到open状态
      - open：打开状态，服务调用被**熔断**，访问被熔断服务的请求会被拒绝，快速失败，直接走降级逻辑。Open状态5秒后会进入half-open状态
      - half-open：半开状态，放行一次请求，根据执行结果来判断接下来的操作。
        - 请求成功：则切换到closed状态
        - 请求失败：则切换到open状态
    - 断路器熔断策略有三种：慢调用、异常比例、异常数
      - **慢调用**:业务的响应时长（RT）大于指定时长的请求认定为慢调用请求。在指定时间内，如果请求数量超过设定的最小数量，慢调用比例大于设定的阈值，则触发熔断。
      - **异常比例或异常数**：统计指定时间内的调用，如果调用次数超过指定请求数，并且出现异常的比例达到设定的比例阈值（或超过指定异常数），则触发熔断。
  
  - 授权规则
  
    - 授权规则可以对调用方的来源做控制，有白名单和黑名单两种方式。
  
      - 白名单：来源（origin）在白名单内的调用者允许访问
      - 黑名单：来源（origin）在黑名单内的调用者不允许访问
  
  - 持久化
  
    - 
  
  - 
  
    

# jmeter

- http://jmeter.apache.org/download_jmeter.cgi

- 发送请求
