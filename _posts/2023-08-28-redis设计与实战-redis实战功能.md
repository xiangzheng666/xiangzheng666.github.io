---
categories: [redis]
tags: [redis]
---
# 慢查询日志

Redis 的慢查询日志功能用于记录执行时间超过给定时长的命令请求， 用户可以通过这个功能产生的日志来监视和优化查询速度。

服务器配置有两个和慢查询日志相关的选项：

* `slowlog-log-slower-than` 选项指定执行时间超过多少微秒（`1` 秒等于 `1,000,000` 微秒）的命令请求会被记录到日志上。
  举个例子， 如果这个选项的值为 `100` ， 那么执行时间超过 `100` 微秒的命令就会被记录到慢查询日志； 如果这个选项的值为 `500` ， 那么执行时间超过 `500` 微秒的命令就会被记录到慢查询日志； 诸如此类。
* `slowlog-max-len` 选项指定服务器最多保存多少条慢查询日志。
  服务器使用先进先出的方式保存多条慢查询日志： 当服务器储存的慢查询日志数量等于 `slowlog-max-len` 选项的值时， 服务器在添加一条新的慢查询日志之前， 会先将最旧的一条慢查询日志删除。
  举个例子， 如果服务器 `slowlog-max-len` 的值为 `100` ， 并且假设服务器已经储存了 `100` 条慢查询日志， 那么如果服务器打算添加一条新日志的话， 它就必须先删除目前保存的最旧的那条日志， 然后再添加新日志。

```powershell
redis> CONFIG SET slowlog-log-slower-than 0
OK

redis> CONFIG SET slowlog-max-len 5
OK


redis> SLOWLOG GET
1) 1) (integer) 4               # 日志的唯一标识符（uid）
   2) (integer) 1378781447      # 命令执行时的 UNIX 时间戳
   3) (integer) 13              # 命令执行的时长，以微秒计算
   4) 1) "SET"                  # 命令以及命令参数
      2) "database"
      3) "Redis"
2) 1) (integer) 3
   2) (integer) 1378781439
   3) (integer) 10
   4) 1) "SET"
      2) "number"
      3) "10086"
3) 1) (integer) 2
   2) (integer) 1378781436
   3) (integer) 18
   4) 1) "SET"
      2) "msg"
      3) "hello world"
4) 1) (integer) 1
   2) (integer) 1378781425
   3) (integer) 11
   4) 1) "CONFIG"
   2) "SET"
   3) "slowlog-max-len"
   4) "5"
5) 1) (integer) 0
   2) (integer) 1378781415
   3) (integer) 53
   4) 1) "CONFIG"
      2) "SET"
      3) "slowlog-log-slower-than"
      4) "0"
```


# 监视器

通过执行 MONITOR 命令， 客户端可以将自己变为一个监视器， 实时地接收并打印出服务器当前处理的命令请求的相关信息：

```powershell
redis> MONITOR
OK
1378822099.421623 [0 127.0.0.1:56604] "PING"
1378822105.089572 [0 127.0.0.1:56604] "SET" "msg" "hello world"
1378822109.036925 [0 127.0.0.1:56604] "SET" "number" "123"
1378822140.649496 [0 127.0.0.1:56604] "SADD" "fruits" "Apple" "Banana" "Cherry"
1378822154.117160 [0 127.0.0.1:56604] "EXPIRE" "msg" "10086"
1378822257.329412 [0 127.0.0.1:56604] "KEYS" "*"
1378822258.690131 [0 127.0.0.1:56604] "DBSIZE"
```
