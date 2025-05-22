---
categories: [javaEE]
tags: [mybatisplus]
---
# mybatisplus

- ```
  <dependency>
      <groupId>com.baomidou</groupId>
      <artifactId>mybatis-plus-boot-starter</artifactId>
      <version>3.4.1</version>
  </dependency>
  
  设置jdbc参数
  ```

- 定义数据接口，继承**BaseMapper**

- ```
  @Mapper
  public interface UserDao extends BaseMapper<User> {
  }
  ```

- 使用

- ```
  userDao.selectList(null);
  ```

- Lombok

  - ```
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <version>1.18.12</version>
    </dependency>
    
    import lombok.*;
    /*
        1 生成getter和setter方法：@Getter、@Setter
          生成toString方法：@ToString
          生成equals和hashcode方法：@EqualsAndHashCode
    
        2 统一成以上所有：@Data
    
        3 生成空参构造： @NoArgsConstructor
          生成全参构造： @AllArgsConstructor
    
        4 lombok还给我们提供了builder的方式创建对象,好处就是可以链式编程。 @Builder【扩展】
     */
    @Data
    public class User {
        private Long id;
        private String name;
        private String password;
        private Integer age;
        private String tel;
    }
    1.表字段与编码属性设计不同步
    @TableField(value="pwd")
    private String password;
    
    2.编码中添加了数据库中未定义的属性
    @TableField(exist="fasle")
    private String ssss;
    
    3.采用默认查询开放了更多的字段查看权限,设置该属性是否参与查询
    @TableField(value="pwd",select=false)
    private String password;
    
    4.表名与编码开发设计不同步
    @Data
    @TableName("table_name")
    public class User {
    
    5.id生成策略
    @TableField(type=IDType.AUTO)
    private Long id;
    ```

- MyBatisPlus分页功能

  - 设置分页拦截器作为Spring管理的bean

    - ```
      @Configuration
      public class MybatisPlusConfig {
          
          @Bean
          public MybatisPlusInterceptor mybatisPlusInterceptor(){
              //1 创建MybatisPlusInterceptor拦截器对象
              MybatisPlusInterceptor mpInterceptor=new MybatisPlusInterceptor();
              //2 添加分页拦截器
              mpInterceptor.addInnerInterceptor(new PaginationInnerInterceptor());
              return mpInterceptor;
          }
      }
      ```

- 执行分页查询

  - ```
    //1 创建IPage分页对象,设置分页参数
    IPage<User> page=new Page<>(1,3);
    //2 执行分页查询
    userDao.selectPage(page,null);
    ```

- 开启日志

  - ```
    # 开启mp的日志（输出到控制台）
    mybatis-plus:
      configuration:
        log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
    ```

- 解决日志打印过多

  - logback.xml

    - ```
      <?xml version="1.0" encoding="UTF-8"?>
      <configuration>
      
      </configuration>
      ```

  - ```
    spring:
      main:
        banner-mode: off # 关闭SpringBoot启动图标(banner)
    ```

  - ```
    # mybatis-plus日志控制台输出
    mybatis-plus:
      configuration:
        log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
      global-config:
        banner: off # 关闭mybatisplus启动图标
    ```

- DQL

  - 条件查询
    
    - ```
      //方式一：按条件查询
      QueryWrapper<User> qw=new QueryWrapper<>();
      qw.lt("age", 18);
      List<User> userList = userDao.selectList(qw);
      System.out.println(userList);
      
      //方式二：lambda格式按条件查询
      QueryWrapper<User> qw = new QueryWrapper<User>();
      qw.lambda().lt(User::getAge, 10);
      List<User> userList = userDao.selectList(qw);
      System.out.println(userList);
      
      //方式三：lambda格式按条件查询
      LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
      lqw.lt(User::getAge, 10);
      List<User> userList = userDao.selectList(lqw);
      System.out.println(userList);
      ```
    
  -  组合条件
  
    - ```
      //并且关系
      LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
      //并且关系：10到30岁之间
      lqw.lt(User::getAge, 30).gt(User::getAge, 10);
      List<User> userList = userDao.selectList(lqw);
      System.out.println(userList);
      
      //或者关系
      LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
      //或者关系：小于10岁或者大于30岁
      lqw.lt(User::getAge, 10).or().gt(User::getAge, 30);
      List<User> userList = userDao.selectList(lqw);
      System.out.println(userList);
      ```
  
  - NULL值处理
  
    - ```
      Integer minAge=10;  
      Integer maxAge=null; 
      LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
      //参数1：如果表达式为true，那么查询才使用该条件
      lqw.gt(minAge!=null,User::getAge, minAge);
      lqw.lt(maxAge!=null,User::getAge, maxAge);
      ```
  
  - 查询投影
  
    - ```
      lqw.select("id", "name", "age", "tel");
      
      lqw.select("count(*) as count, tel");
      lqw.groupBy("tel");
      
      lqw.eq(User::getName, "Jerry").eq(User::getPassword, "jerry");
      
      lqw.between(User::getAge, 10, 30);
      
      lqw.likeLeft(User::getName, "J");
      ```
  
- DML

  - insert

    - ```
      bookdao.insert(entity)
      ```

  - Delete

    - ```
      bookdao.deleteBatchIds(list)
      
      逻辑删除
      @TableLogic
      private Integer deleted;
      
      mybatis-plus:
        global-config:
          db-config:
            table-prefix: tbl_
            # 逻辑删除字段名
            logic-delete-field: deleted
            # 逻辑删除字面值：未删除为0
            logic-not-delete-value: 0
            # 逻辑删除字面值：删除为1
            logic-delete-value: 1
      ```

  - update

    - 乐观锁

      - ```
        @Version
        private Integer version;
            
        添加乐观锁拦截器
        mpInterceptor.addInnerInterceptor(new OptimisticLockerInnerInterceptor());
        
        1.先通过要修改的数据id将当前数据查询出来
        User user = userDao.selectById(3L);
        2.将要修改的属性逐一设置进去
        user.setName("Jock888");
        userDao.updateById(user);
        ```

- 代码生成器

  - ```
    AutoGenerator autoGenerator = new AutoGenerator();
    
    DataSourceConfig datasource = new DataSourceConfig();
    datasource.setDriverName("com.mysql.cj.jdbc.Driver");
    datasource.setUrl("jdbc:mysql://localhost:3306/ssm_db?characterEncoding=utf-8");
    datasource.setUsername("root");
    datasource.setPassword("123456");
    autoGenerator.setDataSource(datasource);
    
    GlobalConfig globalConfig = new GlobalConfig();
    globalConfig.setOutputDir(System.getProperty("user.dir")+"/springboot_ssm/src/main/java");    //设置代码生成位置
    globalConfig.setOpen(false);    //设置生成完毕后是否打开生成代码所在的目录
    globalConfig.setAuthor("黑马程序员");    //设置作者
    globalConfig.setFileOverride(true);     //设置是否覆盖原始生成的文件
    globalConfig.setMapperName("%sDao");    //设置数据层接口名，%s为占位符，指代模块名称
    globalConfig.setIdType(IdType.ASSIGN_ID);   //设置Id生成策略
    autoGenerator.setGlobalConfig(globalConfig);
    
    //设置包名相关配置
    PackageConfig packageInfo = new PackageConfig();
    // packageInfo.setParent("com.aaa");   //设置生成的包名，与代码所在位置不冲突，二者叠加组成完整路径
    packageInfo.setEntity("pojo");    //设置实体类包名
    packageInfo.setMapper("dao");   //设置数据层包名
    autoGenerator.setPackageInfo(packageInfo);
    
    StrategyConfig strategyConfig = new StrategyConfig();
    strategyConfig.setRestControllerStyle(true);    //设置是否启用Rest风格
    strategyConfig.setVersionFieldName("version");  //设置乐观锁字段名
    strategyConfig.setLogicDeleteFieldName("deleted");  //设置逻辑删除字段名
    strategyConfig.setEntityLombokModel(true);  //设置是否启用lombok
    autoGenerator.setStrategy(strategyConfig);
    
    autoGenerator.execute();
    ```

    