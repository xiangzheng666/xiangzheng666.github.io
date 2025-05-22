---
categories: [javaEE]
tags: [jsp]
---
# jsp

- 脚本
  - <%...%>：内容会直接放到_jspService()方法之中
  - <%=…%>：内容会放到out.print()中，作为out.print()的参数
  - <%!…%>：内容会放到_jspService()方法之外，被类直接包含
  
- 原理
  - `tomcat` 会将 `hello.jsp` 转换为名为 `hello_jsp.java` 的一个 `Servlet`
  - `tomcat` 再将转换的 `servlet` 编译成字节码文件 `hello_jsp.class`
  - `tomcat` 会执行该字节码文件，向外提供服务
  
- 可以断开

- EL表达
  - page：当前页面有效
  - request：当前请求有效
  - session：当前会话有效
  - application：当前应用有效
  -  ${brands}，el 表达式获取数据，会先从page域对象中获取数据，如果没有再到 requet 域对象中获取数据，如果再没有再到 session 域对象中获取，如果还没有才会到 application 中获取数据
  - 存储数据到域
    
    - ```
      request.setAttribute("brands",brands);
      ```
  
  - el获取域数据
  
    - ```
      ${brands}
      ```
  
  - JSTL
  
    - 取代JSP页面上的Java代码
  
    - ```
      <dependency>
          <groupId>jstl</groupId>
          <artifactId>jstl</artifactId>
          <version>1.2</version>
      </dependency>
      <dependency>
          <groupId>taglibs</groupId>
          <artifactId>standard</artifactId>
          <version>1.1.2</version>
      </dependency>
      
      <%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %> 
      ```
  
    - ```
      <c:if test="${flag == 1}">
          男
      </c:if>
      <c:if test="${flag == 2}">
          女
      </c:if>
      
      items：被遍历的容器
      var：遍历产生的临时变量
      varStatus：遍历状态对象
      <c:forEach items="${brands}" var="brand">
          <tr align="center">
              <td>${brand.id}</td>
              <td>${brand.brandName}</td>
              <td>${brand.companyName}</td>
              <td>${brand.description}</td>
          </tr>
      </c:forEach>
      ```
  
- MVC模式和三层架构

  - M：Model，业务模型，处理业务

  - V：View，视图，界面展示

  - C：Controller，控制器，处理请求，调用模型和视图

    ----------------------------------------------------------------

  - 数据访问层：对数据库的CRUD基本操作

  - 业务逻辑层：对业务逻辑进行封装，组合数据访问层层中基本功能，形成复杂的业务逻辑功能。例如 `注册业务功能` ，我们会先调用 `数据访问层` 的 `selectByName()` 方法判断该用户名是否存在，如果不存在再调用 `数据访问层` 的 `insert()` 方法进行数据的添加操作

  - 表现层：接收请求，封装数据，调用业务逻辑层，响应数据