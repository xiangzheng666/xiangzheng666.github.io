---
categories: [javaEE]
tags: [REDIS]
---
# REDIS

- 6379

- 字符串 string
  - **SET** key value 					         设置指定key的值
  - **GET** key                                        获取指定key的值
  - **SETEX** key seconds value         设置指定key的值，并将 key 的过期时间设为 seconds 秒
  - **SETNX** key value 只有在 key    不存在时设置 key 的值
  
- 哈希 hash
  - **HSET** key field value             将哈希表 key 中的字段 field 的值设为 value
  - **HGET** key field                       获取存储在哈希表中指定字段的值
  - **HDEL** key field                       删除存储在哈希表中的指定字段
  - **HKEYS** key                              获取哈希表中所有字段
  - **HVALS** key                              获取哈希表中所有值
  - **HGETALL** key                         获取在哈希表中指定 key 的所有字段和值
  
- 列表 list
  - **LPUSH** key value1 [value2]         将一个或多个值插入到列表头部
  - **LRANGE** key start stop                获取列表指定范围内的元素
  - **RPOP** key                                       移除并获取列表最后一个元素
  - **LLEN** key                                        获取列表长度
  - **BRPOP** key1 [key2 ] timeout       移出并获取列表的最后一个元素， 如果列表没有元素会阻塞列表直到等待超    时或发现可弹出元素为止
  
- 集合 set
  - **SADD** key member1 [member2]            向集合添加一个或多个成员
  - **SMEMBERS** key                                         返回集合中的所有成员
  - **SCARD** key                                                  获取集合的成员数
  - **SINTER** key1 [key2]                                   返回给定所有集合的交集
  - **SUNION** key1 [key2]                                 返回所有给定集合的并集
  - **SDIFF** key1 [key2]                                      返回给定所有集合的差集
  - **SREM** key member1 [member2]            移除集合中一个或多个成员
  
- 有序集合 sorted set / zset
  - **ZADD** key score1 member1 [score2 member2]     向有序集合添加一个或多个成员，或者更新已存在成员的 分数
  - **ZRANGE** key start stop [WITHSCORES]                     通过索引区间返回有序集合中指定区间内的成员
  - **ZINCRBY** key increment member                              有序集合中对指定成员的分数加上增量 increment
  - **ZREM** key member [member ...]                                移除有序集合中的一个或多个成员

- key
  - **KEYS** pattern  查找所有符合给定模式( pattern)的 key 
  - **EXISTS** key  检查给定 key 是否存在
  - **TYPE** key  返回 key 所储存的值的类型
  - **TTL** key  返回给定 key 的剩余生存时间(TTL, time to live)，以秒为单位
  - **DEL** key  该命令用于在 key 存在是删除 key

- Jedis

  - ```
    <dependency>
    	<groupId>redis.clients</groupId>
    	<artifactId>jedis</artifactId>
    	<version>2.8.0</version>
    </dependency>
    
    //1 获取连接
    Jedis jedis = new Jedis("localhost",6379);
    //2 执行具体的操作
    jedis.set("username","xiaoming");
    //3 关闭连接
    jedis.close();
    ```

- spring-redis

  - ```
    <dependency>
    	<groupId>org.springframework.data</groupId>
    	<artifactId>spring-data-redis</artifactId>
    	<version>2.4.8</version>
    </dependency>
    
    ```

  - ValueOperations：简单K-V操作

  - SetOperations：set类型数据操作

  - ZSetOperations：zset类型数据操作

  - HashOperations：针对hash类型的数据操作

  - ListOperations：针对list类型的数据操作

  - ```
    @Autowired
    private RedisTemplate redisTemplate;
    ```

- 注解

  - @EnableCaching  开启缓存注解功能  

  - @Cacheable  在方法执行前spring先查看缓存中是否有数据，如果有数据，则直接返回缓存数据；若没有数据，调用方法并将方法返回值放到缓存中  

  - @CachePut  将方法的返回值放到缓存中  

  - @CacheEvict  将一条或多条数据从缓存中删除

  - ```
    注入CacheManager
    EhCacheCacheManager使用EhCache作为缓存技术GuavaCacheManager使用Google的GuavaCache作为缓存技术RedisCacheManager使用Redis作为缓存技术
    
    @Autowired
    private CacheManager cachemanager
    
    引导类上加@EnableCaching
    @EnableCaching
    
    @CachePut(value = "userCache", key = "#user.id")
    @CacheEvict(value = "setmealCache",allEntries = true) //清除setmealCache名称下,所有的缓存数据
    @CacheEvict(value = "userCache",key = "#p0")  //#p0 代表第一个参数
    ```