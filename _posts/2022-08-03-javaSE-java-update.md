---
categories: [javaSE]
tags: []
---
# star
1. **Java SE就是标准版，包含标准的JVM和标准库**，而**Java EE是企业版，它只是在Java SE的基础上加上了大量的API和库**，以便方便开发Web应用、数据库、消息服务等，Java EE的应用使用的虚拟机和Java SE完全相同。**Java ME就和Java SE不同，它是一个针对嵌入式设备的“瘦身版”**，Java SE的标准库无法在Java ME上使用，Java ME的虚拟机也是“瘦身版”。
2. SUN公司搞了一个**JSR规范**，凡是想给Java平台加一个功能，比如说访问数据库的功能，大家要先创建一个JSR规范，定义好接口，这样，各个数据库厂商都按照规范写出Java驱动程序，所以JSR是一系列的规范,而**负责审核JSR的组织就是JCP**。
3. **JRE就是运行Java字节码的虚拟机**。但是，如果只有Java源码，要编译成Java字节码，就需要JDK，因为JDK除了包含JRE，还提供了编译器、调试器等开发工具。
4.  **命名时不能以数字开**头，后接字母，数字和下划线的组合
5.  导入System类的所有静态字段和静态方法:   **import static** java.lang.System.*;
6. package，**包作用域**是指一个类允许访问同一个`package`的没有`public`、`private`修饰的`class`，以及没有`public`、`protected`、`private`修饰的字段和方法。
7. **classpath**是JVM用到的一个环境变量，它用来指示JVM如何搜索`class`
8. **jar包**，它可以把`package`组织的目录层级，以及各个目录下的所有文件（包括`.class`文件和其他文件）都打成一个jar文件
9. **jar包还可以包含其它jar包**，这个时候，就需要在`MANIFEST.MF`文件里配置`classpath`了。
10. == 和equals()，一个引用比较一个内容比较

# Stream对象

- 获取对象

  - Stream.of()

    -  没啥实质性用途 

  - 基于数组或Collection

    -  把数组变成Stream使用Arrays.strem()方法。对于Collection（List，Set，Queue等），直接调用stream()`方法就可以获得`Stream

    - ```
      Arrays.strem(array)
      Collection.stream()
      ```

  - 基于Supplier

    - stream.generate(Supplier<String> sp); 

- 对象方法

  - map

    -  `map()`方法用于将一个`Stream`的每个元素映射成另一个元素并转换成一个新的`Stream` 

    -  `map()`方法接收的对象是`Function`接口对象 

    - ```
      Stream<Integer> s2 = s.map(n -> n * n);
      ```

  - filter

    -  使用`filter()`方法可以对一个`Stream`的每个元素进行测试，通过测试的元素被过滤后生成一个新的`Stream` 
    -  `filter()`方法接收的对象是`Predicate`接口对象，它定义了一个`test()`方法，负责判断元素是否符合条件： 

    - ```
      stream.filter(n -> n % 2 !=0)
      ```

  - reduce

    - `reduce()`方法将一个`Stream`的每个元素依次作用于`BinaryOperator`，并将结果合并。

    - `reduce()`是聚合方法，聚合方法会立刻对`Stream`进行计算。

    -  `reduce()`方法传入的对象是`BinaryOperator`接口，它定义了一个`apply()`方法，负责把上次累加的结果和本次的元素进行运算，并返回累加的结果： 

    - ```
      stream.reduce((acc, n) -> acc + n); 
      ```

  -  对于`Stream`来说，对其进行转换操作*并不会触发任何计算* 

  -  而聚合操作则不一样，聚合操作会立刻促使`Stream`输出它的每一个元素，并依次纳入计算，以获得最终结果 

- 输出为List

  - ```
    stream.collect(Collectprs.toList())
    ```

- 输出数组

  - ```
    stream.toArray(int[]::new)
    ```

- 输出map

  - ```
    stream.collect(Collectors.map(s -> s.substring(0,1),s -> s.substring(0,1) ))
    ```

- 分组输出

  -  分组输出使用`Collectors.groupingBy()`，它需要提供两个函数：一个是分组的key，这里使用`s -> s.substring(0, 1)`，表示只要首字母相同的`String`分到一组，第二个是分组的value，这里直接使用`Collectors.toList()`，表示输出为`List` 

  - ```
    stream.collect(Collectors.groupingBy(
    	s -> s.substring(0, 1),
    	Collectors.toList()
    ))
    
    返回map对象
    ```

- ```
  排序
  stream.sort()
  去重
  stream.distinct()
  截取
  stream.limit(n)
  合并
  Stream.concat(stream1,stream2)
  flatMap
  Stream<List<Integer>> s = Stream.of(
          Arrays.asList(1, 2, 3),
          Arrays.asList(4, 5, 6),
          Arrays.asList(7, 8, 9));
  Stream<Integer> i = s.flatMap(list -> list.stream());
  并行
  stream.parallel()
  其他聚合方法
  除了reduce()和collect()外，Stream还有一些常用的聚合方法：
  
  count()：用于返回元素个数；
  max(Comparator<? super T> cp)：找出最大元素；
  min(Comparator<? super T> cp)：找出最小元素。
  针对IntStream、LongStream和DoubleStream，还额外提供了以下聚合方法：
  
  sum()：对所有元素求和；
  average()：对所有元素求平均数。
  还有一些方法，用来测试Stream的元素是否满足以下条件：
  
  boolean allMatch(Predicate<? super T>)：测试是否所有元素均满足测试条件；
  boolean anyMatch(Predicate<? super T>)：测试是否至少有一个元素满足测试条件。
  最后一个常用的方法是forEach()，它可以循环处理Stream的每个元素，我们经常传入System.out::println来打印Stream的元素：
  ```

  