---
categories: [javaEE]
tags: [cloud]
---
# cloud

- --》》
  - 单体架构
  - 分布式架构
  - 微服务

- words

  - 服务拆分

  - 远程调用

  - 服务注册

    - ```
      @Bean
      @LoadBalanced
          public RestTemplate restTemplate() {
              return new RestTemplate();
          }
      ```

- Eureka

  - 注册中心--server

    - ```
      1.
      <dependency>
        <groupId>org.springframework.cloud</groupId>
          <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
      </dependency>
      
      2.
      @EnableEurekaServer
      
      3.
      server:
        port: 10086
      spring:
        application:
          name: eureka-server
      eureka:
        client:
          service-url: 
            defaultZone: http://127.0.0.1:10086/eureka
      ```

  - 服务注册

    - ```
      <dependency>
        <groupId>org.springframework.cloud</groupId>
          <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
      </dependency>
      
      eureka:
        client:
          service-url:
            defaultZone: http://127.0.0.1:10086/service_name
      ```

  - 服务发现

    - ```
      <dependency>
        <groupId>org.springframework.cloud</groupId>
          <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
      </dependency>
      
      RestTemplate.getForObject(url,class)
      url为service_name
      ```

- Ribbon

  - ```
  修改负载均衡规则
    @Bean
    public IRule randomRule(){
        return new RandomRule();
    }
    userservice: # 给某个微服务配置负载均衡规则，这里是userservice服务
      ribbon:
        NFLoadBalancerRuleClassName: com.netflix.loadbalancer.RandomRule # 负载均衡规则 
    
    饥饿加载  
    ribbon:
      eager-load:
        enabled: true
        clients: userservice
    ```
  
  # Nacos
  
  - 注册中心下载
  
  - 服务注册
  
    - ```
      <dependency>
          <groupId>com.alibaba.cloud</groupId>
          <artifactId>spring-cloud-alibaba-dependencies</artifactId>
          <version>2.2.6.RELEASE</version>
          <type>pom</type>
          <scope>import</scope>
      </dependency>
      
      <dependency>
          <groupId>com.alibaba.cloud</groupId>
          <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
      </dependency>
      
      配置nacos地址
      spring:
        cloud:
          nacos:
            server-addr: localhost:8848
      application:
        name: orderservice
      ```
  
  - 服务发现
  
    - ```
      <dependency>
          <groupId>com.alibaba.cloud</groupId>
          <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
      </dependency>
      
      RestTemplate.getForObject(url,class)
      ```
  
  - yaml
  
    - ```
      spring:
        cloud:
          nacos:
            server-addr: localhost:8848
            discovery:
              cluster-name: are1
        application:
          name: orderservice
      
      在服务消费方采用同集群优先
      userservice:
        ribbon:
          NFLoadBalancerRuleClassName: com.alibaba.cloud.nacos.ribbon.NacosRule # 负载均衡规则 
          
      权重配置热更新
      ```
  
  - namespace
  
    - 不同namespace不可见
  
    - ```
      namespace-group-。。。
      spring:
        cloud:
          nacos:
            server-addr: localhost:8848
            discovery:
              cluster-name: are1
              namespace: id.....
      ```
  
- eraka与nacos

  - 临时实例：如果实例宕机超过一定时间，会从服务列表剔除，默认的类型。
  - 非临时实例：如果实例宕机，不会从服务列表剔除，也可以叫永久实例。
  - Nacos与Eureka的区别
    - Nacos支持服务端主动检测提供者状态：临时实例采用心跳模式，非临时实例采用主动检测模式
    - 临时实例心跳不正常会被剔除，非临时实例则不会被剔除
    - Nacos支持服务列表变更的消息推送模式，服务列表更新更及时
    - Nacos集群默认采用AP方式，当集群中存在非临时实例时，采用CP模式；Eureka采用AP方式

- nacos配置管理

  - 定义配置文件定义格式

    - ```
      service-name_profile.yaml
      ```

  - 创建bootstrap.yaml文件在读取appliaction.yaml前获得nacos的url以及配置文件信息。

  - ```
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
    </dependency>
    
    bootstrap.yaml
    
    spring:
      profiles:
        active: dev
      application:
        name: userservice
      cloud:
        nacos:
          server-addr: localhost:8848
          
    删除application中重复的配置	
    ```

- nacos配置热更新管理

  - ```
    @RefreshScope
    @ConfigrationProperties(prefix="")
    ```

- nacos共享配置

  - ```
    service-name.yaml会被共享
    ```

- nacos集群

# Feign

- ```
  <dependency>
      <groupId>org.springframework.cloud</groupId>
      <artifactId>spring-cloud-starter-openfeign</artifactId>
  </dependency>
  
  定义服务接口类
  @FeignClient("userservice")
  public interface userservice {
  
      @GetMapping("/user/{id}")
      User findbyid(@PathVariable("id") Long id);
  }
  
  开启feign
  @EnableFeignClients
  ```

- 配置

- feign.Logger.Level

  - 修改日志级别
    包含四种不同的级别：NONE、BASIC、HEADERS、FULL

- feign.codec.Decoder

  - 响应结果的解析器
    http远程调用的结果做解析，例如解析json字符串为java对象

- feign.codec.Encoder

  - 请求参数编码
    将请求参数编码，便于通过http请求发送

- feign.Contract

  - 支持的注解格式
    默认是SpringMVC的注解

- feign.Retryer

  - 失败重试机制
    请求失败的重试机制，默认是设没有，不过会使用Ribbon的重试

- ```
  feign:
    client:
      config:
        default/service_name:
          logger-level: FULL
  
  声明bean    
  public class FeignclientConfiguration{
      @Bean
      public Logger.Level feignLogLevel(){
      return Logger.Level.BASIC;
  }
  全局配置
  @EnableFeignClients(defaultConfiguration=FeignclientConfiguration.class)
  局部配置
  @FeignClient("userservice"，Configuration=FeignclientConfiguration.class)
  
  
  --------------------------
  
  <!--httpClient的依赖 -->
  <dependency>
      <groupId>io.github.openfeign</groupId>
      <artifactId>feign-httpclient</artifactId>
  </dependency>
  feign:
    httpclient:
       enabled: true # 开启feign对HttpClient的支持
       max-connections: 200 # 最大的连接数
       max-connections-per-route: 50 # 每个路径的最大连接数
  ```

# Dubbo

- 节点

  - Provider  暴露服务的服务提供方。 
  -  Consumer  调用远程服务的服务消费方。  
  - Registry  服务注册与发现的注册中心。  
  - Monitor  统计服务的调用次数和调用时间的监控中心。

- ```
  dubbo:
    protocol:
      name: dubbo
      port: 20881
    registry:
      address: nacos://127.0.0.1:8848
    scan:
      base-packages: cn.itcast.user.service
      
  <!--dubbo的起步依赖-->
  <dependency>
      <groupId>org.apache.dubbo</groupId>
      <artifactId>dubbo-spring-boot-starter</artifactId>
      <version>2.7.8</version>
  </dependency>
  <dependency>
      <groupId>org.apache.dubbo</groupId>
      <artifactId>dubbo-registry-nacos</artifactId>
      <version>2.7.8</version>
  </dependency>
  
  @DubboService
  public class UserServiceImpl implements UserService {
  
      @Autowired
      private UserMapper userMapper;
  
  	//根据id查询用户名称
      public String queryUsername(Long id) {
          return userMapper.findById(id).getUsername();
      }
  }
  ```

- ```
  <!--dubbo的起步依赖-->
  <dependency>
      <groupId>org.apache.dubbo</groupId>
      <artifactId>dubbo-spring-boot-starter</artifactId>
      <version>2.7.8</version>
  </dependency>
  <dependency>
      <groupId>org.apache.dubbo</groupId>
      <artifactId>dubbo-registry-nacos</artifactId>
      <version>2.7.8</version>
  </dependency>
      
  dubbo:
    registry:
      address: nacos://127.0.0.1:8848
      
  @DubboReference
  private UserService userService;
  ```

- 超时与重试

  - ```
    dubbo:
      registry:
        address: nacos://127.0.0.1:8848
      consumer:
        timeout: 3000
        retries: 0
    ```

- 启动检查

  - ```
    dubbo:
      registry:
        address: nacos://127.0.0.1:8848
      consumer:
        check: false
    ```

- 多版本

  - ```
    @DubboService(version = “2.0.0”)
    
    @DubboReference(version = "2.0.0")
    ```

- 负载均衡

  - ```
    @DubboReference(loadbalance = "Random")
    ```

- SpringCloud Alibaba

  - 将Dubbo集成至SpringCloud主要是替换Ribbo或者Feign实现远程调用

  - ```
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-alibaba-dependencies</artifactId>
        <version>2.2.5.RELEASE</version>
        <type>pom</type>
        <scope>import</scope>
    </dependency>
    
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-dubbo</artifactId>
    </dependency>
    ```

    

# gateway

- ```
  <dependency>
      <groupId>org.springframework.cloud</groupId>
      <artifactId>spring-cloud-starter-gateway</artifactId>
  </dependency>
  <!--nacos服务发现依赖-->
  <dependency>
      <groupId>com.alibaba.cloud</groupId>
      <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
  </dependency>
  ```

- springboot程序

- 主要是配置文件

- ```
  server:
    port: 10010 # 网关端口
  spring:
    application:
      name: gateway # 服务名称
    cloud:
      nacos:
        server-addr: localhost:8848 # nacos地址
      gateway:
        routes: # 网关路由配置
          - id: user-service # 路由id，自定义，只要唯一即可
            # uri: http://127.0.0.1:8081 # 路由的目标地址 http就是固定地址
            uri: lb://userservice # 路由的目标地址 lb就是负载均衡，后面跟服务名称
            predicates: # 路由断言，也就是判断请求是否符合路由规则的条件
              - Path=/user/** # 这个是按照路径匹配，只要以/user/开头就符合要求
            filters: # 过滤器
          	- AddRequestHeader=Truth, Itcast is freaking awesome! # 添加请求头
        default-filters: # 默认过滤项
        - AddRequestHeader=Truth, Itcast is freaking awesome! 
        
        globalcors: # 全局的跨域处理
          add-to-simple-url-handler-mapping: true # 解决options请求被拦截问题
          corsConfigurations:
            '[/**]':
              allowedOrigins: # 允许哪些网站的跨域请求 
                - "http://localhost:8090"
              allowedMethods: # 允许的跨域ajax的请求方式
                - "GET"
                - "POST"
                - "DELETE"
                - "PUT"
                - "OPTIONS"
              allowedHeaders: "*" # 允许在请求中携带的头信息
              allowCredentials: true # 是否允许携带cookie
              maxAge: 360000 # 这次跨域检测的有效期
  ```

- 全局过滤器

- ```
  @Order(-1)
  @Component
  public class AuthorizeFilter implements GlobalFilter {
      @Override
      public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
          // 1.获取请求参数
          MultiValueMap<String, String> params = exchange.getRequest().getQueryParams();
          // 2.获取authorization参数
          String auth = params.getFirst("authorization");
          // 3.校验
          if ("admin".equals(auth)) {
              // 放行
              return chain.filter(exchange);
          }
          // 4.拦截
          // 4.1.禁止访问，设置状态码
          exchange.getResponse().setStatusCode(HttpStatus.FORBIDDEN);
          // 4.2.结束处理
          return exchange.getResponse().setComplete();
      }
  }
  ```

- 每一个过滤器都必须指定一个int类型的order值，**order值越小，优先级越高，执行顺序越靠前**。

- GlobalFilter通过实现Ordered接口，或者添加@Order注解来指定order值，由我们自己指定

- 路由过滤器和defaultFilter的order由Spring指定，默认是按照声明顺序从1递增。

- 当过滤器的order值一样时，会按照 defaultFilter > 路由过滤器 > GlobalFilter的顺序执行。

