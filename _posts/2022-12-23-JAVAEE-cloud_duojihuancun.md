---
categories: [javaEE]
tags: [缓存,多级缓存]
---
# 多级缓存

- 多级缓存

  - 浏览器访问静态资源时，优先读取浏览器本地缓存
  - 访问非静态资源（ajax查询数据）时，访问服务端
  - 请求到达Nginx后，优先读取Nginx本地缓存
  - 如果Nginx本地缓存未命中，则去直接查询Redis（不经过Tomcat）
  - 如果Redis查询未命中，则查询Tomcat
  - 请求进入Tomcat后，优先查询JVM进程缓存
  - 如果JVM进程缓存未命中，则查询数据库

- JVM进程缓存

  - Caffeine

    - 分布式缓存，例如Redis：

      - 优点：存储容量更大、可靠性更好、可以在集群间共享
      - 缺点：访问缓存有网络开销
      - 场景：缓存数据量较大、可靠性要求较高、需要在集群间共享

    - 进程本地缓存，例如HashMap、GuavaCache：

      - 优点：读取本地内存，没有网络开销，速度更快
      - 缺点：存储容量有限、可靠性较低、无法共享
      - 场景：性能要求较高，缓存数据量较小

    - ```
          Cache<String, String> cache = Caffeine.newBuilder().build();
      
          // 存数据
          cache.put("gf", "迪丽热巴");
      
          // 取数据
          String gf = cache.getIfPresent("gf");
          System.out.println("gf = " + gf);
      
          // 取数据，包含两个参数：
          // 参数一：缓存的key
          // 参数二：Lambda表达式，表达式参数就是缓存的key，方法体是查询数据库的逻辑
          // 优先根据key查询JVM缓存，如果未命中，则执行参数二的Lambda表达式
          String defaultGF = cache.get("defaultGF", key -> {
              // 根据key去数据库查询数据
              return "柳岩";
          });
      ```

    - 清除策略

      - ```
        基于容量：设置缓存的数量上
        Cache<String, String> cache = Caffeine.newBuilder()
            .maximumSize(1) // 设置缓存大小上限为 1
            .build();
        基于时间：设置缓存的有效时间
        Cache<String, String> cache = Caffeine.newBuilder()
            // 设置缓存有效期为 10 秒，从最后一次写入开始计时 
            .expireAfterWrite(Duration.ofSeconds(10)) 
            .build();
        
        ```

- OpenResty
  - 具备Nginx的完整功能
  - 基于Lua语言进行扩展，集成了大量精良的 Lua 库、第三方模块
  - 允许使用Lua**自定义业务逻辑**、**自定义库**
  - Lua
  - 缓存一致性
    - canal