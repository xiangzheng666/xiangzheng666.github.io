---
categories: [javaEE]
tags: [spring]
---
# spring

- **简化开发**，降低企业级开发的复杂性

  - 目标：充分解耦

    - 使用IoC容器管理bean（IOC)
    - 在IoC容器内将有依赖关系的bean进行关系绑定（DI）

  - **IOC(反转控制)**

    - 使用对象时，由主动new产生对象转换为由**外部**提供对象，此过程中对象创建控制权由程序转移到外部，此思想称为控制反转

    - IOC容器：用来充当IoC思想中的“外部

    - Bean：在IoC容器中，被创建或被管理的对象

    - DI(依赖注入)：建立bean与bean之间的依赖关系的整个过程，称为依赖注入。

    - 使用

      - ```
        1.导入
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context</artifactId>
            <version>5.2.10.RELEASE</version>
        </dependency>
        2.配置bean
        <bean id="bookdao" name="bookdaobieming" class="Dao.impl.bookdaoimpl"/>
        <bean id="bookservice" class="service.impl.bookserviceimpl">
        	<property name="dao" ref="bookdao"></property>
        </bean>
        3使用
        new ClassPathXmlApplicationContext("applicationContext.xml");
        从IOC容器中获取Bean对象(BookService对象)
        BookService bookService= (BookService)ctx.getBean("bookService");
        调用Bean对象(BookService对象)的方法
        bookService.save();
        
        DL使用
        1.提供依赖对象对应的setter方法
        2.配置依赖
        <bean id="bookservice" class="service.impl.bookserviceimpl">
        	<property name="dao" ref="bookdao"></property>
        </bean>
        ```

      - bean配置

        - ```
          <bean id="bookdao" name="bookdaobieming" class="Dao.impl.bookdaoimpl"/>
          name：别名
          scope="singleton/prototype/..":范围，是否单例模式
          ```

        - ```
          实例化
          1.无参构造方法实现，没有无参构造报错
          <bean id="bookdao" name="bookdaobieming" class="Dao.impl.bookdaoimpl"/>
          2.静态工厂
          public class OrderDaoFactory {
              public static OrderDao getOrderDao(){
                  System.out.println("factory setup....");
                  return new OrderDaoImpl();
              }
          }
          <bean id="orderDao" class="factory.OrderDaoFactory" factory-method="getOrderDao"/>
          3.实例工厂
          public class UserDaoFactory {
              public UserDao getUserDao(){
                  return new UserDaoImpl();
              }
          }
          <bean id="userFactory" class="factory.UserDaoFactory"/>
          <bean id="userDao" factory-method="getUserDao" factory-bean="userFactory"/>
          
          public class UserDaoFactoryBean implements FactoryBean<UserDao> {
              //代替原始实例工厂中创建对象的方法
              public UserDao getObject() throws Exception {
                  return new UserDaoImpl();
              }
          
              public Class<?> getObjectType() {
                  return UserDao.class;
              }
          }
          <bean id="userDao" class="factory.UserDaoFactoryBean"/>
          ```

        - 生命周期

          - 提供生命周期控制方法

          - ```
            <bean id="bookDao" class="dao.impl.BookDaoImpl" init-method="init" destroy-method="destory"/>
            ```

          - 实现InitializingBean, DisposableBean接口

          - ```
            public class BookServiceImpl implements BookService, InitializingBean, DisposableBean {
                private BookDao bookDao;
                public void setBookDao(BookDao bookDao) {
                    System.out.println("set .....");
                    this.bookDao = bookDao;
                }
                public void save() {
                    System.out.println("book service save ...");
                    bookDao.save();
                }
                public void destroy() throws Exception {
                    System.out.println("service destroy");
                }
                public void afterPropertiesSet() throws Exception {
                    System.out.println("service init");
                }
            }
            ```

      - 依赖注入

        - setter方式注入

          - 需要set方法

          - 引用类型

          - ```
            <bean id="bookservice" class="service.impl.bookserviceimpl">
            	<property name="dao" ref="bookdao"></property>
            </bean>
            ```

          - 简单类型

          - ```
            <bean id="bookservice" class="service.impl.bookserviceimpl">
            	<property name="dao" value=""></property>
            </bean>
            ```

        - 构造器方法注入

          - 需要构造方法

          - 引用类型

          - ```
            <constructor-arg name="dao" ref="bookdao"/>
            ```

          - 简单类型

          - ```
            <constructor-arg name="dao" value=""/>
            ```

        - 自动装配

          - ```
            set方法需要
            <bean id="bookservice" class="service.impl.bookserviceimpl" autowire="byType"/>
            byType:按类型自动注入
            byName:按名称自动注入
            ```

        - 集合注入

         -  注入数组类型数据

          ```xml
          <property name="array">
              <array>
                  <value>100</value>
                  <value>200</value>
                  <value>300</value>
              </array>
          </property>
          ```

          -  注入List类型数据

          ```xml
          <property name="list">
              <list>
                  <value>itcast</value>
                  <value>itheima</value>
                  <value>boxuegu</value>
                  <value>chuanzhihui</value>
              </list>
          </property>
          ```

          -  注入Set类型数据

          ```xml
          <property name="set">
              <set>
                  <value>itcast</value>
                  <value>itheima</value>
                  <value>boxuegu</value>
                  <value>boxuegu</value>
              </set>
          </property>
          ```

           -    注入Map类型数据

          ```xml
          <property name="map">
              <map>
                  <entry key="country" value="china"/>
                  <entry key="province" value="henan"/>
                  <entry key="city" value="kaifeng"/>
              </map>
          </property>
          ```

          -  注入Properties类型数据

          ```xml
          <property name="properties">
              <props>
                  <prop key="country">china</prop>
                  <prop key="province">henan</prop>
                  <prop key="city">kaifeng</prop>
              </props>
          </property>
          ```

          > 说明：property标签表示setter方式注入，构造方式注入constructor-arg标签内部也可以写\<array>、\<list>、\<set>、\<map>、\<props>标签

      - 三方资源配置

        - ```
          <bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource">
              <property name="driverClassName" value="com.mysql.jdbc.Driver"/>
              <property name="url" value="jdbc:mysql://localhost:3306/spring_db"/>
              <property name="username" value="root"/>
              <property name="password" value="root"/>
          </bean>
          ```

        - 配置文件解耦合

        - ```java
          <context:property-placeholder location="jdbc.properties"/>
          不加载系统属性
          <context:property-placeholder location="jdbc.properties" system-properties-mode="NEVER"/>
          
          location加载：
          location="jdbc.properties,msg.properties"
          location="*.properties"
          location="classpath:*.properties"
          location="classpath*:*.properties"
          
          <bean class="com.alibaba.druid.pool.DruidDataSource">
              <property name="driverClassName" value="${jdbc.driver}"/>
              <property name="url" value="${jdbc.url}"/>
              <property name="username" value="${jdbc.username}"/>
              <property name="password" value="${jdbc.password}"/>
          </bean>
          ```

    - 注解使用

      - 核心容器

        -  创建容器

          - ```java
            1.new ClassPathXmlApplicationContext("applicationContext.xml");
            	  ClassPathXmlApplicationContext("bean1.xml", "bean2.xml");
            2.FileSystemXmlApplicationContext("D:\\applicationContext.xml");
            ```

        - 获取bean对象

          - ```
            1.(BookDao) ctx.getBean("bookDao");
            2.ctx.getBean("bookDao", BookDao.class);
            3.ctx.getBean(BookDao.class);
            ```

        - BeanFactory

          - ```
            new ClassPathResource("applicationContext.xml");
            BeanFactory bf = new XmlBeanFactory(resources);
            所有的Bean均为延迟加载
            ```

      - 注解开发

        - **@Component**注解的三个衍生注解

          - **`@Controller`**：用于表现层bean定义
          - **`@Service`**：用于业务层bean定义
          - **`@Repository`**：用于数据层bean定义

        - ```
          【第一步】在applicationContext.xml中开启Spring注解包扫描
          <context:component-scan base-package="com.itheima"/>
          【第二步】在类上使用@Component注解定义Bean。
          @Component("bookDao")
          public class BookDaoImpl implements BookDao {
              public void save() {
                  System.out.println("book dao save ...");
              }
          }
          ```

      - 纯注解

        - **【第一步】定义配置类代替配置文件**

          - ```
            //声明当前类为Spring配置类
            @Configuration
            //Spring注解扫描，相当于<context:component-scan base-package="com.itheima"/>
            @ComponentScan("com.itheima")
            //设置bean扫描路径，多个路径书写为字符串数组格式
            //@ComponentScan({"com.itheima.service","com.itheima.dao"})
            public class SpringConfig {
            }
            ```

        - **【第二步】使用**
          
          - AnnotationConfigApplicationContext加载Spring配置类初始化Spring容器
            
          - ```
            //AnnotationConfigApplicationContext加载Spring配置类初始化Spring容器
            new AnnotationConfigApplicationContext(SpringConfig.class);
            BookDao bookDao = (BookDao) ctx.getBean("bookDao");
            System.out.println(bookDao);
            //按类型获取bean
            BookService bookService = ctx.getBean(BookService.class);
            System.out.println(bookService);
            ```
          
            
          
        - Bean作用范围和生命周期
          
          - bean作用范围注解配置	
          
            - 使用@Scope定义bean作用范围
          
              - ```
                @Repository
                @Scope("singleton")
                public class BookDaoImpl implements BookDao {
                }
                ```
          
          - bean生命周期注解配置
          
            - 使用@PostConstruct、@PreDestroy定义bean生命周期
          
              - ```
                @Repository
                @Scope("singleton")
                public class BookDaoImpl implements BookDao {
                    public BookDaoImpl() {
                        System.out.println("book dao constructor ...");
                    }
                    @PostConstruct
                    public void init(){
                        System.out.println("book init ...");
                    }
                    @PreDestroy
                    public void destroy(){
                        System.out.println("book destory ...");
                    }
                }
                ```
          
        - 依赖注入

          - 使用@Autowired注解开启自动装配模式（按类型）

            - ```
              @Service
              public class BookServiceImpl implements BookService {
                  //@Autowired：注入引用类型，自动装配模式，默认按类型装配
                  @Autowired
                  private BookDao bookDao;
              
                  public void save() {
                      System.out.println("book service save ...");
                      bookDao.save();
                  }
              }
              ```

          -  使用@Qualifier注解指定要装配的bean名称

            - ```
              @Service
              public class BookServiceImpl implements BookService {
                  //@Autowired：注入引用类型，自动装配模式，默认按类型装配
                  @Autowired
                  //@Qualifier：自动装配bean时按bean名称装配
                  @Qualifier("bookDao")
                  private BookDao bookDao;
              
                  public void save() {
                      System.out.println("book service save ...");
                      bookDao.save();
                  }
              }
              ```

          - 使用@Value实现简单类型注入

            - ```
              @Configuration
              @ComponentScan("com.itheima")
              //@PropertySource加载properties配置文件
              @PropertySource({"classpath:jdbc.properties"}) //{}可以省略不写
              public class SpringConfig {
              }
              
              @Repository("bookDao")
              public class BookDaoImpl implements BookDao {
                  //@Value：注入简单类型（无需提供set方法）
                  @Value("${name}")
                  private String name;
              
                  public void save() {
                      System.out.println("book dao save ..." + name);
                  }
              }
              ```

          - 第三方Bean

            - 1.单独定义配置类

              - ```
                public class JdbcConfig {
                    //@Bean：表示当前方法的返回值是一个bean对象，添加到IOC容器中
                    @Bean
                    public DataSource dataSource(){
                        DruidDataSource ds = new DruidDataSource();
                        ds.setDriverClassName("com.mysql.jdbc.Driver");
                        ds.setUrl("jdbc:mysql://localhost:3306/spring_db");
                        ds.setUsername("root");
                        ds.setPassword("root");
                        return ds;
                    }
                }
                ```

            - 2.将独立的配置类加入核心配置

              - ```
                @Configuration
                @ComponentScan("com.itheima")
                //@Import:导入配置信息
                @Import({JdbcConfig.class})
                public class SpringConfig {
                }
                
                @Configuration
                @ComponentScan({"com.itheima.config","com.itheima.service","com.itheima.dao"})  //只要com.itheima.config包扫到了就行，三个包可以合并写成com.itheima
                public class SpringConfig {
                }
                ```

            - 第三方Bean注入

              - 简单类型

                - ```
                  @Value("com.mysql.jdbc.Driver")
                  private String driver;
                  ```

              - 引用

                - 自动装配对象

      - 整合mybatis

        - ```
          <dependency>
              <groupId>org.mybatis</groupId>
              <artifactId>mybatis-spring</artifactId>
              <version>1.3.0</version>
          </dependency>
          <dependency>
              <groupId>org.springframework</groupId>
              <artifactId>spring-jdbc</artifactId>
              <version>5.3.2</version>
          </dependency>
          ```

        - 将mybatisconfig.xml写成config类

        - ```
          <?xml version="1.0" encoding="UTF-8" ?>
          <!DOCTYPE configuration
                  PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
                  "http://mybatis.org/dtd/mybatis-3-config.dtd">
          <configuration>
              <!--起别名-->
              <typeAliases>
                  <package name="pojo"/>
              </typeAliases>
          
              <environments default="development">
                  <environment id="development">
                      <transactionManager type="JDBC"/>
                      <dataSource type="POOLED">
                          <property name="driver" value="com.mysql.jdbc.Driver"/>
                          <property name="url" value="jdbc:mysql:///test?useSSL=false&amp;useServerPrepStmts=true"/>
                          <property name="username" value="root"/>
                          <property name="password" value="123456"/>
                      </dataSource>
                  </environment>
              </environments>
              <mappers>
                  <!--扫描mapper-->
                  <package name="maper"/>
              </mappers>
          </configuration>
          ```

        - ```
          package mybatis.config;
          
          import com.alibaba.druid.pool.DruidDataSource;
          import org.springframework.beans.factory.annotation.Value;
          import org.springframework.context.annotation.Bean;
          
          import javax.sql.DataSource;
          
          public class jdbcconfig {
              @Value("${jdbc.driver}")
              private String driver;
              @Value("${jdbc.url}")
              private String url;
              @Value("${jdbc.username}")
              private String userName;
              @Value("${jdbc.password}")
              private String password;
          
              @Bean
              public DataSource dataSource(){
                  DruidDataSource ds = new DruidDataSource();
                  ds.setDriverClassName(driver);
                  ds.setUrl(url);
                  ds.setUsername(userName);
                  ds.setPassword(password);
                  return ds;
              }
          }
          
          
          public class mybatisconfig {
          
              @Bean
              public SqlSessionFactoryBean sqlSessionFactory(DataSource dataSource){
                  SqlSessionFactoryBean ssfb = new SqlSessionFactoryBean();
                  ssfb.setTypeAliasesPackage("mybatis.dao");
                  ssfb.setDataSource(dataSource);
                  return ssfb;
              }
              //定义bean，返回MapperScannerConfigurer对象
              @Bean
              public MapperScannerConfigurer mapperScannerConfigurer(){
                  MapperScannerConfigurer msc = new MapperScannerConfigurer();
                  msc.setBasePackage("mybatis");
                  return msc;
              }
          }
          ```

          

  - **AOP(面向切面编程)**
    
    - 连接点（JoinPoint）：正在执行的方法，例如：update()、delete()、select()等都是连接点。
    
    - 切入点（Pointcut）：进行功能增强了的方法，例如:update()、delete()方法，select()方法没有被增强所以不是切入点，但是是连接点。
    
      - 在SpringAOP中，一个切入点可以只描述一个具体方法，也可以匹配多个方法
        - 一个具体方法：com.itheima.dao包下的BookDao接口中的无形参无返回值的save方法
        - 匹配多个方法：所有的save方法，所有的get开头的方法，所有以Dao结尾的接口中的任意方法，所有带有一个参数的方法
    
    - 通知（Advice）：在切入点前后执行的操作，也就是增强的共性功能
    
      - 在SpringAOP中，功能最终以方法的形式呈现
    
    - 通知类：通知方法所在的类叫做通知类
    
    - 切面（Aspect）：描述通知与切入点的对应关系，也就是哪些通知方法对应哪些切入点方法。
    
    - 使用
    
      - ```
        <dependencies>
            <!--spring核心依赖，会将spring-aop传递进来-->
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-context</artifactId>
                <version>5.2.10.RELEASE</version>
            </dependency>
            <!--切入点表达式依赖，目的是找到切入点方法，也就是找到要增强的方法-->
            <dependency>
                <groupId>org.aspectj</groupId>
                <artifactId>aspectjweaver</artifactId>
                <version>1.9.4</version>
            </dependency>
        </dependencies>
        ```
    
      - 定义通知类，在其中定义切入点，与通知方法  
    
      - @Aspect
    
      - @Pointcut("execution(void aop_test.dao.dao.print())")
    
      - @Before("tp()")
    
      - ```
        @Component
        @Aspect
        public class advice {
        
            @Pointcut("execution(void aop_test.dao.dao.print())")
            private void tp(){}
        
            @Before("tp()")
            public void method(){
                System.out.println(System.currentTimeMillis());
            }
        }
        ```
    
      - 在spring配置中开启aop
    
      - ```
        @EnableAspectJAutoProxy
        ```
    
    - AOP工作流程
    
      1. Spring容器启动
      2. 读取所有切面配置中的切入点
      3. 初始化bean，判定bean对应的类中的方法是否匹配到任意切入点
         - 匹配失败，创建原始对象
         - 匹配成功，创建原始对象（目标对象）的代理对象
      4. 获取bean执行方法
         - 获取的bean是原始对象时，调用方法并执行，完成操作
         - 获取的bean是代理对象时，根据代理对象的运行模式运行原始方法与增强的内容，完成操作
    
    - 切入点
    
      - 可以定义接口或者实现类的方法
    
      - 切入点表达式标准格式：动作关键字(访问修饰符  返回值  包名.类/接口名.方法名(参数) 异常名）
    
        - ```
          execution(public User com.itheima.service.UserService.findById(int))
          ```
    
      - 通配符
    
        - *：单个独立的任意符号
        - ..：多个连续的任意符号
        - +：专用于匹配子类类型
    
    - 通知类型
    
      -  前置通知
    
        - @Before
    
      -  后置通知
    
        - @After
    
      - 返回后通知
    
        - @AfterReturning
    
      - 抛出异常后通知
    
        - @AfterThrowing
    
      - **环绕通知**
    
        - @Around
    
        - ```
          @Around("pt()")
          public Object around(ProceedingJoinPoint pjp) throws Throwable {
              System.out.println("around before advice ...");
              Object ret = pjp.proceed();
              System.out.println("around after advice ...");
              return ret;
          }
          
          ProceedingJoinPoint pjp
          pjp.proceed()
          
          //获取执行的签名对象
          Signature signature = pjp.getSignature();
          //获取接口/类全限定名
        String className = signature.getDeclaringTypeName();
          //获取方法名
          String methodName = signature.getName();
           //获取连接点方法的参数们
          pjp.getArgs();
          //获取连接点方法的参数们
          pjp.getArgs(); 
          ```
          
        - 环绕通知方法形参必须是ProceedingJoinPoint，表示正在执行的连接点，使用该对象的proceed()方法表示对原始对象方法进行调用，返回值为原始对象方法的返回值。
    
        - 环绕通知方法的返回值建议写成Object类型，用于将原始对象方法的返回值进行返回，哪里使用代理对象就返回到哪里。
    
      - **Around Before**
        **Before**
        **main**
        **AfterReturning**
        **After**
        **Around After**
    
    - **事务处理**
    
      - 事务作用：在数据层保障一系列的数据库操作同成功同失败
    
        - 事务管理员：发起事务方，在Spring中通常指代业务层开启事务的方法
        - 事务协调员：加入事务方，在Spring中通常指代数据层方法，也可以是业务层方法
    
      - Spring事务作用：在数据层或**业务层**保障一系列的数据库操作同成功同失败
    
      - 【第一步】在业务层接口上添加Spring事务管理
    
        - ```
          public interface AccountService {
              //配置当前接口方法具有事务
              @Transactional
              public void transfer(String out,String in ,Double money) ;
          }
          ```
    
        - 对于RuntimeException类型异常或者Error错误，Spring事务能够进行回滚操作。但是对于编译器异常，Spring事务是不进行回滚的，所以需要使用rollbackFor来设置要回滚的异常。
    
        - ```
          public interface AccountService {
              //配置当前接口方法具有事务
              @Transactional(rollbackFor={..})
              public void transfer(String out,String in ,Double money) ;
          }
          ```
    
        - 事务传播行为：事务协调员对事务管理员所携带事务的处理态度
    
        - ```
        @Transactional(propagation = Propagation.REQUIRES_NEW)
          ```
      
      - 【第二步】设置事务管理器(将事务管理器添加到IOC容器中)
      
        - ```
          //配置事务管理器，mybatis使用的是jdbc事务
          @Bean
          public PlatformTransactionManager transactionManager(DataSource dataSource){
              DataSourceTransactionManager dtm = new DataSourceTransactionManager();
            transactionManager.setDataSource(dataSource);
              return transactionManager;
        }
          ```
      
      - 【第三步】开启注解式事务驱动
      
      - ```
          //开启注解式事务驱动
        @EnableTransactionManagement
        ```
      
      - test
      
        - ```
           accountService.transfer("Tom","Jerry",100D);
          ```

- **框架整合**，高效整合其他技术，提高企业级应用开发与运行效率

