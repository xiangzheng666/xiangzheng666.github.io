---
categories: [javaEE]
tags: [缓存]
---
# 分布式缓存

# 1.Redis持久化

- RDB持久化

  - 把内存中的所有数据都记录到磁盘中。当Redis实例故障重启后，从磁盘读取快照文件，恢复数据。快照文件称为RDB文件
  - RDB持久化在四种情况下会执行：

    - 执行save命令
    - 执行bgsave命令
    - Redis停机时
    - 触发RDB条件时
      - redis.conf文件
      - save 60 1000
        - 代表60秒内至少执行1000次修改则触发RDB

- AOF持久化

  - Redis处理的每一个写命令都会记录在AOF文件，可以看做是命令日志文件

  - AOF默认是关闭的，需要修改redis.conf配置文件来开启AOF：

    - 是否开启AOF功能，默认是no

      - appendonly yes

    - AOF文件的名称

      - appendfilename "appendonly.aof"

    - ```
      # 表示每执行一次写命令，立即记录到AOF文件
      appendfsync always 
      # 写命令执行完先放入AOF缓冲区，然后表示每隔1秒将缓冲区数据写到AOF文件，是默认方案
      appendfsync everysec 
      # 写命令执行完先放入AOF缓冲区，由操作系统决定何时将缓冲区内容写回磁盘
      appendfsync no
      # AOF文件比上次文件 增长超过多少百分比则触发重写
      auto-aof-rewrite-percentage 100
      # AOF文件体积最小多大以上才触发重写 
      auto-aof-rewrite-min-size 64mb 
      ```

    - 执行bgrewriteaof命令，可以让AOF文件执行重写功能，用最少的命令达到相同效果
  
  
  