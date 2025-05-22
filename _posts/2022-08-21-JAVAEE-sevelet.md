---
categories: [javaEE]
tags: [sevelet]
---
# sevelet

- 使用
  - 1.导包

    - ```
      <dependency>
          <groupId>javax.servlet</groupId>
          <artifactId>javax.servlet-api</artifactId>
          <version>3.1.0</version>
          <!--
            此处为什么需要添加该标签?
            provided指的是在编译和测试过程中有效,最后生成的war包时不会加入
             因为Tomcat的lib目录中已经有servlet-api这个jar包，如果在生成war包的时候生效就会和Tomcat中的jar包冲突，导致报错
          -->
          <scope>provided</scope>
      </dependency>
      ```

  - 编写实现sevelet接口的类

    - ```
      public class ServletDemo1 implements Servlet {}
      ```

    - 接口方法

      - init
        - 调用时机：默认情况下，Servlet被第一次访问时，调用loadOnStartup: 默认为-1，修改为0或者正整数，则会在服务器启动的时候，调用
        *  调用次数: 1次
      - service
        *  调用时机:每一次Servlet被访问时，调用
        * 调用次数: 多次
      - destroy
        * 1.调用时机：内存释放或者服务器关闭的时候，Servlet对象会被销毁
        * 2.调用次数: 1次
      - getServletConfig
        
      * 获取ServletConfig对象
  
- 在类上定义注解
  
    - ```
      @WebServlet("/demo1")
      public class ServletDemo1 implements Servlet {}
    ```
  
- 执行流程

  - 根据`localhost:8080`可以找到要访问的Tomcat Web服务器
  - 根据`web-demo`可以找到部署在Tomcat服务器上的web-demo项目
  - 根据`demo1`可以找到要访问的是项目中的哪个Servlet类，根据@WebServlet后面的值进行匹配
  - ServletDemo1实现了Servlet接口，所以类中必然会重写service方法供Tomcat Web服务器进行调用
  - service方法中有ServletRequest和ServletResponse两个参数，ServletRequest封装的是请求数据，ServletResponse封装的是响应数据，后期我们可以通过这两个参数实现前后端的数据交互

- 周期

  1. ==加载和实例化==：默认情况下，当Servlet第一次被访问时，由容器创建Servlet对象

     ```
     默认情况，Servlet会在第一次访问被容器创建，但是如果创建Servlet比较耗时的话，那么第一个访问的人等待的时间就比较长，用户的体验就比较差，那么我们能不能把Servlet的创建放到服务器启动的时候来创建，具体如何来配置?
     
     @WebServlet(urlPatterns = "/demo1",loadOnStartup = 1)
     loadOnstartup的取值有两类情况
       （1）负整数:第一次访问时创建Servlet对象
       （2）0或正整数:服务器启动时创建Servlet对象，数字越小优先级越高
     ```

  2. ==初始化==：在Servlet实例化之后，容器将调用Servlet的==init()==方法初始化这个对象，完成一些如加载配置文件、创建连接等初始化的工作。该方法只==调用一次==
  3. ==请求处理==：==每次==请求Servlet时，Servlet容器都会调用Servlet的==service()==方法对请求进行处理
  4. ==服务终止==：当需要释放内存或者容器关闭时，容器就会调用Servlet实例的==destroy()==方法完成资源的释放。在destroy()方法调用之后，容器会释放这个Servlet实例，该实例随后会被Java的垃圾收集器所回收

- HttpServlet
  
- 继承HttpServlet重写doget，dopost方法
  
- urlPattern

  -  一个Servlet,可以配置多个

    - ```
      @WebServlet({“/demo1”，"/demo2"})
      ```

  - urlPattern精确匹配

    - ```
      @WebServlet(“/demo1/a”})
      ```

  - 目录匹配

    - ```
      @WebServlet(“/demo1/*”})
      ```

  - 扩展名匹配

    - ```
      @WebServlet(“/demo1/*.html”})
      ```

  - 任意匹配

    - ```
      @WebServlet(“/”})
      @WebServlet(“/*”})
      ```

- XML配置

  - 配置web.xml

    - ```
      <?xml version="1.0" encoding="UTF-8"?>
      <web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
               version="4.0">
          
          
          
          <!-- 
              Servlet 全类名
          -->
          <servlet>
              <!-- servlet的名称，名字任意-->
              <servlet-name>demo13</servlet-name>
              <!--servlet的类全名-->
              <servlet-class>com.itheima.web.ServletDemo13</servlet-class>
          </servlet>
      
          <!-- 
              Servlet 访问路径
          -->
          <servlet-mapping>
              <!-- servlet的名称，要和上面的名称一致-->
              <servlet-name>demo13</servlet-name>
              <!-- servlet的访问路径-->
              <url-pattern>/demo13</url-pattern>
          </servlet-mapping>
      </web-app>
      ```


# Request和Response

- Request对象

  - servletRequst 接口

  - HttpServletRequst  子接口

  - RequestFacade tomcat 实现类

  - Request的继承体系为ServletRequest-->HttpServletRequest-->RequestFacade

  - 请求行

    - 获取请求方式: `GET`

    ```
    String getMethod()
    ```

    * 获取虚拟目录(项目访问路径): `/request-demo`

    ```
    String getContextPath()
    ```

    * 获取URL(统一资源定位符): `http://localhost:8080/request-demo/req1`

    ```
    StringBuffer getRequestURL()
    ```

    * 获取URI(统一资源标识符): `/request-demo/req1`

    ```
    String getRequestURI()
    ```

    * 获取请求参数(GET方式): `username=zhangsan&password=123`

    ```
    String getQueryString()
    ```

    - 获取所有参数Map集合

    ```
    Map<String,String[]> getParameterMap()
    ```

    * 根据名称获取参数值（数组）

    ```
    String[] getParameterValues(String name)
    ```

    * 根据名称获取参数值(单个值)

    ```
    String getParameter(String name)
    ```

    接下来，我们通过案例来把上述的三个方法进行实例演示:

  - 请求头

    - ```
      String getHeader(String name)
      ```

  - 请求体

    - 获取字节输入流，如果前端发送的是字节数据，比如传递的是文件数据，则使用该方法

    ```
    ServletInputStream getInputStream()
    该方法可以获取字节
    ```

    * 获取字符输入流，如果前端发送的是纯文本数据，则使用该方法

    ```
    BufferedReader getReader()
    ```

  - 中文乱码

    - POST的请求参数是通过request的getReader()来获取流中的数据

      - ```
        request.setCharacterEncoding("UTF-8");
        ```

    - GET请求获取请求参数的方式是`request.getQueryString()`

      - 将乱码string转化byte  使用默认编码"ISO-8859-1"

      - 将byte转化string使用浏览器发送的编码"utf-8"

      - ```
        s.getBytes(StandardCharsets.ISO_8859_1)
        
        String(s.getBytes(StandardCharsets.ISO_8859_1),StandardCharsets.UTF_8)
        ```

  - 请求转发

    - ```
      req.getRequestDispatcher("/ziyuanb").forward(req,resp);
      ```

    - 地址不变化

    - 请求转发资源间共享数据

      - 存储数据到request域[范围,数据是存储在request对象]中

      ```
      void setAttribute(String name,Object o);
      ```

      * 根据key获取值

      ```
      Object getAttribute(String name);
      ```

      * 根据key删除该键值对

      ```
      void removeAttribute(String name);
      ```

- Request对象

  - ServletResponse 接口

  - HttpServletResponse  子接口

  - ResponseFacade tomcat 实现类

    - 响应行

      - ```
        void setStatus(int sc);状态码:
        ```

    - 响应头

      - ```
        void setHeader(String name,String value);
        ```

    - 响应体

      - 获取字符输出流:

        ```
        PrintWriter getWriter();
        ```

      - 获取字节输出流

        ```
        ServletOutputStream getOutputStream();
        ```

  - 重定向

    - ```
      resp.setStatus(302);
      resp.setHeader("location","资源B的访问路径");
      
      resposne.sendRedirect("资源B的访问路径")；
      ```

    - 地址变化

    - 无法共享

  - 虚拟地址

    - 只有转发不用

    - ```
      String contextPath = request.getContextPath();
      ```

  - 响应数据

    - ```
      response.setContentType("text/html;charset=utf-8");
      ```

    - 字符

      - ```
        PrintWriter writer = response.getWriter();
        writer.write("aaa");
        ```

    - 字节

      - ```
        FileInputStream fis = new FileInputStream("d://a.jpg");
        //2. 获取response字节输出流
        ServletOutputStream os = response.getOutputStream();
        //3. 完成流的copy
        byte[] buff = new byte[1024];
        int len = 0;
        while ((len = fis.read(buff))!= -1){
        	os.write(buff,0,len);
        }
        fis.close();
        ```

      - 三方工具

        - ```
          <dependency>
              <groupId>commons-io</groupId>
              <artifactId>commons-io</artifactId>
              <version>2.6</version>
          </dependency>
          ```

        - ```
          FileInputStream fis = new FileInputStream("d://a.jpg");
                  //2. 获取response字节输出流
                  ServletOutputStream os = response.getOutputStream();
                  //3. 完成流的copy
                	IOUtils.copy(fis,os);
                  fis.close();
          ```

          