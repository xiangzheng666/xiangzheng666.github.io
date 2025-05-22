---
categories: [BigData]
tags: [Hive]
---
# Hive


+  查询 

```plain
1------------------
select * from emp;
select empno, ename from emp;

2------------------+
A+B	A和B 相加
A-B	A减去B
A*B	A和B 相乘
A/B	A除以B
A%B	A对B取余
A&B	A和B按位取与
A|B	A和B按位取或
A^B	A和B按位取异或
~A	A按位取反
select sal +1 from emp;

3------------------count
1）求总行数（count）
hive (default)> select count(*) cnt from emp;
2）求工资的最大值（max）
hive (default)> select max(sal) max_sal from emp;
3）求工资的最小值（min）
hive (default)> select min(sal) min_sal from emp;
4）求工资的总和（sum）
hive (default)> select sum(sal) sum_sal from emp; 
5）求工资的平均值（avg）
hive (default)> select avg(sal) avg_sal from emp;

4-----------------where
select * from emp limit 5;
select * from emp where sal >1000;
    A=B
    A<=>B
    A<>B, A!=B
    A<B
    A<=B
    A>B
    A>=B
    A [NOT] BETWEEN B AND C
    A IS NULL
    A IS NOT NULL
    IN(数值1, 数值2)
    A [NOT] LIKE B      % 代表零个或多个字符(任意个字符)。_ 代表一个字符。
    A RLIKE B, A REGEXP B JDK中的正则表达式
    AND
    OR
    NOT

5.--------------------Group By
select t.deptno, avg(t.sal) avg_sal from emp t 
	group by t.deptno
	having avg_sal > 2000;
	
6---------------------join
select e.empno, e.ename, d.deptno, d.dname from emp e join dept d on e.deptno = d.deptno;
1.join 内连接：只有进行连接的两个表中都存在与连接条件相匹配的数据才会被保留下来
2.left join 左外连接：JOIN操作符左边表中符合WHERE子句的所有记录将会被返回。
3.right join 右外连接：JOIN操作符右边表中符合WHERE子句的所有记录将会被返回
4.full join 满外连接：将会返回所有表中符合WHERE语句条件的所有记录。NULL值替代。
5.多表连接
	SELECT e.ename, d.dname, l.loc_name
        FROM   emp e 
        JOIN   dept d
        ON     d.deptno = e.deptno 
        JOIN   location l
        ON     d.loc = l.loc;
```

 

+  排序 

```plain
1.order by 全局排序，只有一个Reducer
select * from emp order by sal;

2.Sort By 每个Reducer内部进行排序
select * from emp sort by deptno desc;

3.Distribute By：distribute by类似MR中partition（自定义分区），进行分区，结合sort by使用。 

4.Cluster By distribute by和sorts by字段相同时，可以使用cluster by方式。只能是升序排序
```

 

+  抽样查询 

```sql
TABLESAMPLE(BUCKET x OUT OF y)y抽多少个分区，x从多少分区开始抽
select * from stu tablesample(bucket 1 out of 4 on id);
```

 

+  函数 

```plain
1.--nvl空字段赋值
select comm, nvl(comm, -1) from emp;

2.--case when
--统计不同部门男女各有多少人
select
    dept_id,
    count(*) total,
    sum(case sex when '男' then 1 else 0 end) male,
    sum(case sex when '女' then 1 else 0 end) female
from
    emp_sex
group by
    dept_id;

3.--行转列
select
    concat(constellation,",",blood_type) xzxx,
    concat_ws("|", collect_list(name)) rentou
from
    person_info
group by
    constellation,blood_type;

CONCAT(string A/col, string B/col…)：返回输入字符串连接后的结果，支持任意个输入字符串;
CONCAT_WS(separator, str1, str2,...)：它是一个特殊形式的 CONCAT()。
    第一个参数剩余参数间的分隔符。分隔符可以是与剩余参数一样的字符串。
    如果分隔符是 NULL，返回值也将为 NULL。这个函数会跳过分隔符参数后的任何 NULL 和空字符串。
    分隔符将被加到被连接的字符串之间;
COLLECT_SET(col)：函数只接受基本数据类型，它的主要作用是将某字段的值进行去重汇总，产生array类型字段。

--列转行
select
    m.movie,
    tbl.cate
from
    movie_info m
lateral view
    explode(split(category, ",")) tbl as cate;
EXPLODE(col)：将hive一列中复杂的array或者map结构拆分成多行
LATERAL VIEW：用于和split, explode等UDTF一起使用，它能够将一列数据拆成多行数据，在此基础上可以对拆分后的数据进行聚合。
```

 

+  窗口函数 

```plain
OVER()：指定分析函数工作的数据窗口大小，这个数据窗口大小可能会随着行的变而变化。
    CURRENT ROW：当前行
    n PRECEDING：往前n行数据
    n FOLLOWING：往后n行数据
    UNBOUNDED：起点，UNBOUNDED PRECEDING 表示从前面的起点， 
    			UNBOUNDED FOLLOWING表示到后面的终点
    LAG(col,n,default_val)：往前第n行数据
    LEAD(col,n, default_val)：往后第n行数据
    NTILE(n)：把有序窗口的行分发到指定数据的组中，各个组有编号，
    			编号从1开始，对于每一行，NTILE返回此行所属的组的编号。注意：n必须为int类型。
```

 

+  排序 

```plain
select name,
subject,
score,
rank() over(partition by subject order by score desc) rp,
dense_rank() over(partition by subject order by score desc) drp,
row_number() over(partition by subject order by score desc) rmp
from score;

RANK() 排序相同时会重复，总数不会变
DENSE_RANK() 排序相同时会重复，总数会减少
ROW_NUMBER() 会根据顺序计算
```

 

+  日期 

```plain
select current_date();

--今天开始90天以后的日期
select date_add(current_date(), 90);
--今天开始90天以前的日期
select date_sub(current_date(), 90);

--今天和1990年6月4日的天数差
SELECT datediff(CURRENT_DATE(), "1990-06-04");
```

 

+  自定义函数 
    -  UDF（User-Defined-Function） 
        * 一进一出
    -  UDAF（User-Defined Aggregation Function） 
        * 聚集函数，多进一出类似于：count/max/min
    -  UDTF（User-Defined Table-Generating Functions） 
        * 一进多出如lateral view explore()
    -  1.继承org.apache.hadoop.hive.ql.exec.UDF 
    -  2.需要实现evaluate函数；evaluate函数支持重载； 
        *  

```plain
package com.atguigu.hive;
import org.apache.hadoop.hive.ql.exec.UDF;

public class Lower extends UDF {

	public String evaluate (final String s) {
		
		if (s == null) {
			return null;
		}
		
		return s.toLowerCase();
	}
}
```

 

    -  3.在hive的命令行窗口创建函数 
        * add jar linux_jar_path
        * create [temporary] function [dbname.]function_name AS class_name;
        * Drop [temporary] function [if exists] [dbname.]function_name;
+ 

