---
categories: [javaEE]
tags: [springboot]
---
# springboot

- 步骤

  - 使用idea创建springboot

  - 定义开发类

  - ```
    @RestController
    @RequestMapping("/books")
    public class BookController {
        @GetMapping("/{id}")
        public String getById(@PathVariable Integer id) {
            System.out.println("id ==> " + id);
            return "hello , spring boot! ";
        }
    }
    ```

  - 启动自动生成的类

- 起步依赖

  - starter

    - 定义了当前项目使用的所有项目坐标，以达到减少依赖配置的目的.

  - parent

    - 定义了若干个坐标版本号（依赖管理，而非依赖），以达到减少依赖冲突的目的

  - 变更服务器

    - ```
      <dependencies>
          <dependency>
              <groupId>org.springframework.boot</groupId>
              <artifactId>spring-boot-starter-web</artifactId>
              <!--web起步依赖环境中，排除Tomcat起步依赖-->
              <exclusions>
                  <exclusion>
                      <groupId>org.springframework.boot</groupId>
                      <artifactId>spring-boot-starter-tomcat</artifactId>
                  </exclusion>
              </exclusions>
          </dependency>
          <!--添加Jetty起步依赖，版本由SpringBoot的starter控制-->
          <dependency>
              <groupId>org.springframework.boot</groupId>
              <artifactId>spring-boot-starter-jetty</artifactId>
          </dependency>
      </dependencies>
      ```

- 配置文件

  - application.properties

  - application.yml

  - **application.yaml**

    - ```
      eg:
      #表示注释
      数据前面要加空格与冒号隔开
      server:
        port: 82
      ```

  - 读取配置文件的参数

    - 单个数据

      - ```
        @Value("${}")
        ```

    - 封装全部数据到Environment对象

      - ```
        @Autowired
        private Environment env
        ```

    - 自定义对象封装指定数据

      - ```
        @ConfigurationProperties(prefix = "server")
        public class server_test{
        	private String port
        }
        
        @Autowired
        private server_test test
        
        警告
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-configuration-processor</artifactId>
            <optional>true</optional>
        </dependency>
        ```

  - 内置参数

    - ```
      //application.properties
      spring.profiles.active=pro
      选择哪个配置文件
      application-pro.properties
      application-dev.properties
      application-test.properties
      
      与macen集合
      1.开启对默认占位符的解析
      <build>
          <plugins>
              <plugin>
                  <artifactId>maven-resources-plugin</artifactId>
                  <configuration>
                      <encoding>utf-8</encoding>
                      <useDefaultDelimiters>true</useDefaultDelimiters>
                  </configuration>
              </plugin>
          </plugins>
      </build>
      2.设置多环境属性
      <profiles>
          <profile>
              <id>dev_env</id>
              <properties>
                  <profile.active>dev</profile.active>
              </properties>
              <activation>
                  <activeByDefault>true</activeByDefault>
              </activation>
          </profile>
          <profile>
              <id>pro_env</id>
              <properties>
                  <profile.active>pro</profile.active>
              </properties>
          </profile>
          <profile>
              <id>test_env</id>
              <properties>
                  <profile.active>test</profile.active>
              </properties>
          </profile>
      </profiles>
      4.SpringBoot中引用Maven属性
      spring.profiles.active=${profile.active}
      ```

  - 文件位置

    - 1级： file ：config/application.yml 【最高】
    - 2级： file ：application.yml
    - 3级：classpath：config/application.yml
    - 4级：classpath：application.yml  【最低】

- 整合

  - 整合 Servlet，Filter，Listener 

    - ```
      1.注解
          @ServletComponentScan
          +
          @WebFilter
          @WebServlet
          @WebListener 
      2.bean
          @Bean
          public ServletRegistrationBean getServletRegistrationBean(){
              ServletRegistrationBean bean = new ServletRegistrationBean(new
              SecondServlet());
              bean.addUrlMappings("/second");
              return bean;
          }
          @Bean
          public FilterRegistrationBean getFilterRegistrationBean(){
              FilterRegistrationBean bean = new FilterRegistrationBean(new
              SecondFilter());
              //bean.addUrlPatterns(new String[]{"*.do","*.jsp"});
              bean.addUrlPatterns("/second");
              return bean;
          }
          @Bean
          public ServletListenerRegistrationBean<SecondListener>
          getServletListenerRegistrationBean(){
              ServletListenerRegistrationBean<SecondListener> bean= new
              ServletListenerRegistrationBean<SecondListener>(new SecondListener());
              return bean;
          }
      ```

      

  - 访问静态资源 

    - **classpath/static**
    - **ServletContext** 根目录下：src/main/webapp

  - 视图层

    - jsp，freemarker，Thymeleaf

    - ```
      spring.mvc.view.prefix=/WEB-INF/jsp/
      spring.mvc.view.suffix=.jsp
      
      <dependency>
          <groupId>org.springframework.boot</groupId>
          <artifactId>spring-boot-starter-freemarker</artifactId>
      </dependency>
      
      Thymeleaf:
      	<dependency>
              <groupId>org.springframework.boot</groupId>
              <artifactId>spring-boot-starter-thymeleaf</artifactId>
          </dependency>
          th:text    在页面中输出值
          th:value   可以将一个值放入到 input 标签的 value 中
          调用内置对象
          	${#strings.isEmpty(key)}
              	判断字符串是否为空，如果为空返回 true，否则返回 false
              ${#strings.contains(msg,'T')}
              	判断字符串是否包含指定的子串，如果包含返回 true，否则返回 false
              ${#strings.startsWith(msg,'a')}
              	判断当前字符串是否以子串开头，如果是返回 true，否则返回 false
              ${#strings.endsWith(msg,'a')}
              	判断当前字符串是否以子串结尾，如果是返回 true，否则返回 false
              ${#strings.length(msg)}
              	返回字符串的长度
              ${#strings.indexOf(msg,'h')}
              	查找子串的位置，并返回该子串的下标，如果没找到则返回-1
              ${#strings.substring(msg,13)}
              ${#strings.substring(msg,13,15)}
              	截取子串，用户与 jdk String 类下 SubString 方法相同
              ${#strings.toUpperCase(msg)}
              ${#strings.toLowerCase(msg)}
              	字符串转大小写。
              日期：
              ${#dates.format(key)}
              	格式化日期，默认的以浏览器默认语言为格式化标准
              ${#dates.format(key,'yyy/MM/dd')}
              	按照自定义的格式做日期转换
              ${#dates.year(key)}
              ${#dates.month(key)}
              ${#dates.day(key)}
              if
              	<span th:if="${sex} == '男'">
                  性别：男
                  </span>
                  <span th:if="${sex} == '女'">
                  性别：女
                  </span>
              switch
              	<div th:switch="${id}">
                      <span th:case="1">ID 为 1</span>
                      <span th:case="2">ID 为 2</span>
                      <span th:case="3">ID 为 3</span>
                  </div>
              th:each
                  <tr th:each="u，状态变量 : ${list}">
                      <td th:text="${u.userid}"></td>
                      <td th:text="${u.username}"></td>
                      <td th:text="${u.userage}"></td>
                  </tr>
                  1,index:当前迭代器的索引 从 0 开始
                  2,count:当前迭代对象的计数 从 1 开始
                  3,size:被迭代对象的长度
                  4,even/odd:布尔值，当前循环是否是偶数/奇数 从 0 开始
                  5,first:布尔值，当前循环的是否是第一条，如果是返回 true 否则返回 false
                  6,last:布尔值，当前循环的是否是最后一条，如果是则返回 true 否则返回 false
                  <tr th:each="maps : ${map}">
                      <td th:each="entry:${maps}" th:text="${entry.value.userid}" ></td>
                      <td th:each="entry:${maps}" th:text="${entry.value.username}"></td>
                      <td th:each="entry:${maps}" th:text="${entry.value.userage}"></td>
                  </tr>
              域对象
                  #httpServletRequest
                  session
                  application
              url 表达式
              	@{}
              	@{/show}
              	
              
      ```

  - 持久层

    - ```
      @MapperScan("com.bjsxt.mapper")
      ```

  - 校验

    - ```
      对bean的校验设置
      @NotBlank: 判断字符串是否为 null 或者是空串(去掉首尾空格)。
      @NotEmpty: 判断字符串是否 null 或者是空串。
      @Length: 判断字符的长度(最大或者最小)
      @Min: 判断数值最小值
      @Max: 判断数值最大值
      @Email: 判断邮箱是否合法
      
      /**
      * 完成用户添加
      *@Valid 开启对 Users 对象的数据校验
      *BindingResult:封装了校验的结果
      */
      @RequestMapping("/save")
      public String saveUser(@ModelAttribute("aa") @Valid Users users,BindingResult result){
          if(result.hasErrors()){
          return "add";
          }
          System.out.println(users);
          return "ok";
      }
      ```