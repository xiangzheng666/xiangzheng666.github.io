---
categories: [BigData]
tags: [Hive]
---
# Hive

HQL转化成MapReduce程序一般Hive元数据配置到MySql

+  Tez引擎 
   - Tez是一个Hive的运行引擎，性能优于MR
   - 将tez安装包拷贝到集群，并解压tar包
   - 上传tez依赖到HDFS
   - 新建tez-site.xml
   - 编辑hadoop-env.sh
+  用户接口：Client  
   CLI（command-line interface）、JDBC/ODBC(jdbc访问hive)、WEBUI（浏览器访问hive） 
+  元数据：Metastore  
   元数据包括：表名、表所属的数据库（默认是default）、表的拥有者、列/分区字段、表的类型（是否是外部表）、表的数据所在目录等；  
   默认存储在自带的derby数据库中，推荐使用MySQL存储Metastore 
+  Hadoop  
   使用HDFS进行存储，使用MapReduce进行计算。 
+  驱动器：Driver  
   （1）解析器（SQL Parser）：将SQL字符串转换成抽象语法树AST，这一步一般都用第三方工具库完成，比如antlr；对AST进行语法分析，比如表是否存在、字段是否存在、SQL语义是否有误。  
   （2）编译器（Physical Plan）：将AST编译生成逻辑执行计划。  
   （3）优化器（Query Optimizer）：对逻辑执行计划进行优化。  
   （4）执行器（Execution）：把逻辑执行计划转换成可以运行的物理计划。对于Hive来说，就是MR/Spark。 
+  hive命令 

```plain
1.启动hive
    hive --service metastore
    hive --service hiveserver2
2.beeline连接
	beeline -u jdbc:hive2://node01:1000 -n name
3.“-e”不进入hive的交互窗口执行sql语句
	hive -e "select ...
4.“-f”执行脚本中sql语句"
	hive -f sql.sql
5.查看hdfs文件系统
	dfs -ls /
6.日志管理
	/tmp/root/hive.log
	hive/conf/hive-log4j.properties--hive.log.dir=/opt/module/hive/logs
7.运行参数配置
	1.配置文件
	2.命令行，启动hive时 hive -hiveconf mapred.reduce.tasks=10 ..;
	3.参数声明 set mapred.reduce.tasks=100;
```

+  hive数据类型 

```plain
Hive数据类型	Java数据类型	长度				例子
TINYINT			byte		1byte有符号整数		20
SMALINT			short		2byte有符号整数		20
INT				int			4byte有符号整数		20
BIGINT			long		8byte有符号整数		20
BOOLEAN			boolean		TRUE  				FALSE
FLOAT			float		单精度浮点数		3.14159
DOUBLE			double		双精度浮点数		3.14159
STRING			string		字符系列。可以指定字符集。单引号，双引号。‘now ie’ “for almen”
TIMESTAMP		时间类型	
BINARY			字节数组	


STRUCT	
    和c语言中的struct类似，都可以通过“点”符号访问元素内容。
    例如，如果某个列的数据类型是STRUCT{first STRING, last STRING},
    那么第1个元素可以通过字段.first来引用。
    例如struct<street:string, city:string>
MAP	
	MAP是一组键-值对元组集合，使用数组表示法可以访问数据。
	例如，如果某个列的数据类型是MAP，其中键->值对是’first’->’John’和’last’->’Doe’，
	那么可以通过字段名[‘last’]获取最后一个元素	
	例如map<string, int>
ARRAY	
	数组是一组具有相同类型和名称的变量的集合。这些变量称为数组的元素，
	每个数组元素都有一个编号，编号从零开始。
	例如，数组值为[‘John’, ‘Doe’]，那么第2个元素可以通过数组名[1]进行引用。
	例如array<string>
```

+  DDL 
   -  内部表:删除一个管理表时，Hive也会删除这个表中数据 
   -  外部表:Hive并非认为其完全拥有这份数据。  
      	删除该表并不会删除掉这份数据，  
      	不过描述表的元数据信息会被删除掉。 
   -  alter table student2 set tblproperties('EXTERNAL'='TRUE'); 

```plain
create table test(
    name string,
    friends array<string>,
    children map<string, int>,
    address struct<street:string, city:string>
)
row format delimited fields terminated by ','
collection items terminated by '_'
map keys terminated by ':'
lines terminated by '\n';

数据库:
    创建数据库
        CREATE DATABASE [IF NOT EXISTS] database_name
        [COMMENT database_comment]
        [LOCATION hdfs_path]
        [WITH DBPROPERTIES (property_name=property_value, ...)];

    查询数据库
        show databases;
        show databases like 'db_hive*'

        查看数据库详情
        desc databases [extended] dbname

    修改数据库
        alter database db_hive set dbproperties('createtime'='20170830');

    删除数据库
        drop database db_hive2;空数据库
        drop database db_hive cascade;非空数据库
	
表:
	创建表
		CREATE [EXTERNAL] TABLE [IF NOT EXISTS] table_name 
        [(col_name data_type [COMMENT col_comment], ...)] 
        [COMMENT table_comment] 
        [PARTITIONED BY (col_name data_type [COMMENT col_comment], ...)] 
        [CLUSTERED BY (col_name, col_name, ...) 
        [SORTED BY (col_name [ASC|DESC], ...)] INTO num_buckets BUCKETS] 
        [ROW FORMAT row_format] 
        [STORED AS file_format] 
        [LOCATION hdfs_path]
        [TBLPROPERTIES (property_name=property_value, ...)]
        [AS select_statement]
  修改表
    	ALTER TABLE table_name RENAME TO new_table_name
    删除
    	drop table dept_partition;
```

+  DML 

```plain
添加数据
	1.向表中装载数据（Load）
    load data [local] inpath '/opt/module/datas/student.txt' 
    [overwrite] into table student [partition (partcol1=val1,…)];
    load data inpath '/path.data.txt' into table name
    （1）load data:表示加载数据
    （2）local:表示从本地加载数据到hive表；否则从HDFS加载数据到hive表
    （3）inpath:表示加载数据的路径
    （4）overwrite:表示覆盖表中已有数据，否则表示追加
    （5）into table:表示加载到哪张表
    （6）student:表示具体的表
    （7）partition:表示上传到指定分区

    2.insert into table  student_par partition(month='201709') 
    values(1,'wangwu'),(2,'zhaoliu');
    insert into：以追加数据的方式插入到表或分区，原有数据不会删除
	insert overwrite：会覆盖表或分区中已存在的数据
	
	3.insert overwrite table student partition(month='201708')
    select id, name from student
    insert overwrite table student partition(month='201707')
    select id, name where month='201709'
    insert overwrite table student partition(month='201706')
    select id, name where month='201709';
    
    4.create table if not exists student3 as select id, name from student;
    
    5.create external table if not exists student5(
              id int, name string
              )
              row format delimited fields terminated by '\t'
              location '/student;
    6.import table student2 partition(month='201709') from
 		'/user/hive/warehouse/export/student';
导出数据
	insert overwrite local directory '/opt/module/datas/export/student'
            select * from student;
            
    insert overwrite [local] directory '/opt/module/datas/export/student1'
           ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' 
           select * from student;
           
    export table default.student to  '/user/hive/warehouse/export/student';
清空表
truncate table student;
```

- 分区表  

分区表实际上就是对应一个HDFS文件系统上的独立的文件夹，该文件夹下是该分区所有的数据文件。Hive中的分区就是分目录，把一个大的数据集根据业务需要分割成小的数据集。在查询时通过WHERE子句中的表达式选择查询所需要的指定的分区，这样的查询效率会提高很多。  
_***查询分区表中数据***_

---

```plain
select * from dept_partition where month='201709'   month虚拟列
union
select * from dept_partition where month='201708'
union
select * from dept_partition where month='201707';
```


_***增加分区***_ 

```plain
alter table dept_partition add partition(month='201706') ;
```


_***删除分区***_ 

```plain
alter table dept_partition drop partition (month='201705'), partition (month='201706');
```


show partitions dept_partition;  
desc formatted dept_partition;  
_***创建二级分区表***_ 

```plain
create table dept_partition2(
               deptno int, dname string, loc string
               )
               partitioned by (month string, day string)
               row format delimited fields terminated by '\t';

load data local inpath '/opt/module/datas/dept.txt' into table
 default.dept_partition2 partition(month='201709', day='13');
```


_***数据直接上传到分区目录上***_***，******让分区表和数据产生关联的三种方式*** 

```plain
msck repair table dept_partition2;

alter table dept_partition2 add partition(month='201709',
 day='11');
 
 load data local inpath '/opt/module/datas/dept.txt' into table
 dept_partition2 partition(month='201709',day='10');
```

- 动态分区调整  对分区表Insert数据时候，数据库自动会根据分区字段的值，将数据插入到相应的分区中，Hive中也提供了类似的机制，即动态分区(Dynamic Partition)，只不过，使用Hive的动态分区，需要进行相应的配置。 
  - 开启动态分区参数设

```plain
（1）开启动态分区功能（默认true，开启）
hive.exec.dynamic.partition=true
（2）设置为非严格模式（动态分区的模式，默认strict，表示必须指定至少一个分区为静态分区，nonstrict模式表示允许所有的分区字段都可以使用动态分区。）
hive.exec.dynamic.partition.mode=nonstrict
（3）在所有执行MR的节点上，最大一共可以创建多少个动态分区。默认1000
hive.exec.max.dynamic.partitions=1000
（4）在每个执行MR的节点上，最大可以创建多少个动态分区。该参数需要根据实际的数据来设定。比如：源数据中包含了一年的数据，即day字段有365个值，那么该参数就需要设置成大于365，如果使用默认值100，则会报错。
hive.exec.max.dynamic.partitions.pernode=100
（5）整个MR Job中，最大可以创建多少个HDFS文件。默认100000
hive.exec.max.created.files=100000
（6）当有空分区生成时，是否抛出异常。一般不需要设置。默认false
hive.error.on.empty.partition=false
```

- 分桶表 

```plain
create table stu_buck(id int, name string)
clustered by(id) 
into 4 buckets
row format delimited fields terminated by '\t';
```

 