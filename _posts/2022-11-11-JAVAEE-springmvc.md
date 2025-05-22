---
categories: [javaEE]
tags: [springmvc]
---
# springmvc

- 使用

  - ```
    1.package
    <dependencies>
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <version>3.1.0</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-webmvc</artifactId>
            <version>5.2.10.RELEASE</version>
        </dependency>
    </dependencies>
    
    2.定义处理请求的功能类
    @Controller
    public class UserController {
        //设置映射路径为/save，即外部访问路径
        @RequestMapping("/save")
        //设置当前操作返回结果为指定json数据
        @ResponseBody
        public String save(){
            System.out.println("user save ...");
            return "{'info':'springmvc'}";
        }
    }
    
    3.编写SpringMVC配置类
    //springmvc配置类，本质上还是一个spring配置类
    @Configuration
    @ComponentScan("test")
    public class SpringMvcConfig {
    }
    ---排除包
    excludeFilters = @ComponentScan.Filter(
                    type = FilterType.ANNOTATION,
                    classes = Controller.class
            )
    
    4.web容器配置类
    public class ServletContainersInitConfig extends AbstractDispatcherServletInitializer {
    
        //加载springmvc配置类，产生springmvc容器
        protected WebApplicationContext createServletApplicationContext() {
            //初始化WebApplicationContext对象
            AnnotationConfigWebApplicationContext ctx = new AnnotationConfigWebApplicationContext();
            //加载指定配置类
            ctx.register(SpringMvcConfig.class);
            return ctx;
        }
    
        //设置由springmvc控制器处理的请求映射路径
        protected String[] getServletMappings() {
            return new String[]{"/"};
        }
    
        //加载spring配置类
        protected WebApplicationContext createRootApplicationContext() {
            return null;
        }
        
        //乱码处理
        @Override
        protected Filter[] getServletFilters() {
            CharacterEncodingFilter filter = new CharacterEncodingFilter();
            filter.setEncoding("UTF-8");
            return new Filter[]{filter};
        }
    }
    ---简化
    public class ServletContainersInitConfig extends AbstractAnnotationConfigDispatcherServletInitializer{
        protected Class<?>[] getServletConfigClasses() {
            return new Class[]{SpringMvcConfig.class}
        };
        protected String[] getServletMappings() {
            return new String[]{"/"};
        }
        protected Class<?>[] getRootConfigClasses() {
            return new Class[]{SpringConfig.class};
        }
    }
    ```

  - @RequestMapping注解:请求访问路径

  - @ResponseBody注解:响应内容为当前返回值

  - AbstractDispatcherServletInitializer类

    - SpringMVC提供的快速初始化Web3.0容器的抽象类
    - 1.createServletApplicationContext()方法，创建Servlet容器时，加载SpringMVC对应的bean并放入WebApplicationContext对象范围中，而WebApplicationContext的作用范围为ServletContext范围，即整个web容器范围。
    - 2.getServletMappings()方法，设定SpringMVC对应的请求映射路径，设置为/表示拦截所有请求，任意请求都将转入到SpringMVC进行处理。
    - 3.createRootApplicationContext()方法，如果创建Servlet容器时需要加载非SpringMVC对应的bean，使用当前方法进行，使用方式同createServletApplicationContext()

- 请求与响应

  - 请求映射路径

    -  @RequestMapping注解，定义在类上，会与方法上的连接在一起

  - 请求参数

    - 普通参数

      - 日期参数

      - ```
        http://localhost:80/dataParam?date=2088/08/08&date1=2088-08-18&date2=2088/08/28 8:08:08
        @RequestMapping("/dataParam")
        @ResponseBody
        public String dataParam(Date date,
                          @DateTimeFormat(pattern="yyyy-MM-dd") Date date1,
                          @DateTimeFormat(pattern="yyyy/MM/dd HH:mm:ss") Date date2){
            System.out.println("参数传递 date ==> "+date);
            System.out.println("参数传递 date1(yyyy-MM-dd) ==> "+date1);
            System.out.println("参数传递 date2(yyyy/MM/dd HH:mm:ss) ==> "+date2);
            return "{'module':'data param'}";
        }
        ```

      - 请求参数与形参名称对应即可完成参数传递

      - @RequestParam注解关联请求参数与形参

      - ```
        @RequestMapping("/commonParamDifferentName")
        @ResponseBody
        public String commonParamDifferentName(@RequestParam("name") String userName , int age){
            System.out.println("普通参数传递 userName ==> "+userName);
            System.out.println("普通参数传递 age ==> "+age);
            return "{'module':'common param different name'}";
        }
        ```

    - POJO参数

      - 请求参数名与形参对象属性名相同

      - 嵌套，按照对象层次结构关系即可接收嵌套POJO属性参数

      - ```
        public class User {
            private String name;
            private int age;
            private Address address;
            //getter/setter/toString()方法
        }
        public class Address {
            private String province;
            private String city;
            private Address address;
        }
        @RequestMapping("/pojoContainPojoParam")
        @ResponseBody
        public String pojoContainPojoParam(User user){
            System.out.println("pojo嵌套pojo参数传递 user ==> "+user);
            return "{'module':'pojo contain pojo param'}";
        }
        ```

    - 数组类型参数

      - 同名请求参数：直接映射到对应名称的形参数组对象中

    - 集合类型参数

      - 同名请求参数：使用@RequestParam注解映射到对应名称的集合对象中作为数据

      - ```
        @RequestMapping("/listParam")
        @ResponseBody
        public String listParam(@RequestParam List<String> likes){
            System.out.println("集合参数传递 likes ==> "+ likes);
            return "{'module':'list param'}";
        }
        ```

    -  json数据

      - json普通数组（["","","",...]）

      - ```
        1.package集成
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>2.9.0</version>
        </dependency>
        
        2.开启json数据类型自动转换
        @EnableWebMvc
        
        3.使用@RequestBody注解将外部传递的json数组数据映射到形参的集合对象中作为数据
        @RequestMapping("/listParamForJson")
        @ResponseBody
        public String listParamForJson(@RequestBody List<String> likes){
            System.out.println("list common(json)参数传递 list ==> "+likes);
            return "{'module':'list common for json param'}";
        }
        ```

      - json对象（{key:value,key:value,...}）

      - ```
        定义pojo对象
        使用@RequestBody注解将外部传递的json数据映射到形参的实体类对象中，要求属性名称一一对应
        @RequestMapping("/pojoParamForJson")
        @ResponseBody
        public String pojoParamForJson(@RequestBody User user){
            System.out.println("pojo(json)参数传递 user ==> "+user);
            return "{'module':'pojo for json param'}";
        }
        使用@RequestBody注解将外部传递的json数据映射到形参的实体类对象中，要求属性名称一一对应
        ```

      - json对象数组（[{key:value,...},{key:value,...}]）

      - ```
        定义pojo对象集合
        使用@RequestBody注解将外部传递的json数组数据映射到形参的保存实体类对象的集合对象中，要求属性名称一一对应
        @RequestMapping("/listPojoParamForJson")
        @ResponseBody
        public String listPojoParamForJson(@RequestBody List<User> list){
            System.out.println("list pojo(json)参数传递 list ==> "+list);
            return "{'module':'list pojo for json param'}";
        }
        ```

  - 响应

    - 响应页面

      - ```
        @ResponseBody
        return "page.jsp";
        ```

    - 文本数据

      - ```
        @ResponseBody
        return "response text";
        ```

    -  json数据

      - ```
        响应POJO对象
        需要依赖@ResponseBody注解和@EnableWebMvc注解
        
        @RequestMapping("/toJsonPOJO")
        @ResponseBody
        public User toJsonPOJO(){
            System.out.println("返回json对象数据");
            User user = new User();
            user.setName("itcast");
            user.setAge(15);
            return user;
        }
        ```

- REST

  - 使用

    - ```
      http请求动作(请求方式)+设定请求参数（路径变量）
      @RequestMapping(value = "/users",method = RequestMethod.POST)
      ```

    - 请求参数

      - ```
        @RequestMapping(value = "/users",method = RequestMethod.POST)
        
        @RequestMapping(value = "/users/{id}",method = RequestMethod.DELETE)
        @ResponseBody
        public String delete(@PathVariable Integer id){
            System.out.println("user delete..." + id);
            return "{'module':'user delete'}";
        }
        
        @RequestMapping(value = "/users",method = RequestMethod.PUT)
        @ResponseBody
        public String update(@RequestBody User user){
            System.out.println("user update..."+user);
            return "{'module':'user update'}";
        }
        
        ```

    - @PathVariable

      - 绑定路径参数与处理器方法形参间的关系

    - ```
      @PostMapping
      @DeleteMapping("/{id}")
      @PutMapping 
      @GetMapping("/{id}") 
      
      @RestController=@Controller+@ResponseBody
      ```

    - @RequestBody、@RequestParam、@PathVariable区别和应用

      - 区别
        @RequestParam用于接收url地址传参或表单传参
        @RequestBody用于接收json数据
        @PathVariable用于接收路径参数，使用{参数名称}描述路径参数
      - 应用
        后期开发中，发送请求参数超过1个时，以json格式为主，@RequestBody应用较广
        如果发送非json格式数据，选用@RequestParam接收请求参数
        采用RESTful进行开发，当参数数量较少时，例如1个，可以采用@PathVariable接收请求路径变量，通常用于传递id值

- 整合
  - SSM整合
    - Spring
      - SpringConfig
    - MyBatis
      - MybatisConfig
      - JdbcConfig
      - jdbc.properties
    - SpringMVC
      - ServletConfig
      - SpringMvcConfig
  
- 异常

  - ```
    @RestControllerAdvice //用于标识当前类为REST风格对应的异常处理器
    public class ProjectExceptionAdvice {
        //@ExceptionHandler用于设置当前处理器类对应的异常类型
        @ExceptionHandler(SystemException.class)
        public Result doSystemException(SystemException ex){
            //记录日志
            //发送消息给运维
            //发送邮件给开发人员,ex对象发送给开发人员
            return new Result(ex.getCode(),null,ex.getMessage());
        }
    
        @ExceptionHandler(BusinessException.class)
        public Result doBusinessException(BusinessException ex){
            return new Result(ex.getCode(),null,ex.getMessage());
        }
    
        //除了自定义的异常处理器，保留对Exception类型的异常处理，用于处理非预期的异常
        @ExceptionHandler(Exception.class)
        public Result doOtherException(Exception ex){
            //记录日志
            //发送消息给运维
            //发送邮件给开发人员,ex对象发送给开发人员
            return new Result(Code.SYSTEM_UNKNOW_ERR,null,"系统繁忙，请稍后再试！");
        }
    }
    ```

- 拦截器

  - ```
    1.定义拦截器
    @Component //注意当前类必须受Spring容器控制
    //定义拦截器类，实现HandlerInterceptor接口
    public class ProjectInterceptor implements HandlerInterceptor {
        @Override
        //原始方法调用前执行的内容
        //返回值类型可以拦截控制的执行，true放行，false终止
        public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
            System.out.println("preHandle..."+contentType);
            return true;
        }
    
        @Override
        //原始方法调用后执行的内容
        public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
            System.out.println("postHandle...");
        }
    
        @Override
        //原始方法调用完成后执行的内容
        public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
            System.out.println("afterCompletion...");
        }
    }
    
    
    配置加载拦截器
    @Configuration
    public class SpringMvcSupport extends WebMvcConfigurationSupport {
        @Autowired
        private ProjectInterceptor projectInterceptor;
    
        @Override
        protected void addInterceptors(InterceptorRegistry registry) {
            //配置拦截器
            registry.addInterceptor(projectInterceptor)
                .addPathPatterns("/books","/books/*");
            registry.addInterceptor(projectInterceptor2)
                .addPathPatterns("/books","/books/*");
        }
    }
    ```
    
- ![1669201858684](https://github.com/xiangzheng666/picx-images-hosting/raw/master/1669201858684.5mo1d4kuus.webp)