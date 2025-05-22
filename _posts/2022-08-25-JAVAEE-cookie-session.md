---
categories: [javaEE]
tags: [会话]
---
# 会话

- 作用

  - 请求间共享数据

- 客户端会话跟踪技术：Cookie

  - 将数据保存到客户端

  - ```
    创建cookie,发送Cookie到客户端
    response.addCookie(new("key","value"))
    ```

  - ```
    获取cookie
    Cookie[] cookies = request.getCookies();
    cookies[i].getName();
    cookies[i].getValue();
    ```

  - cookie存活时间

    - 默认情况下，Cookie存储在浏览器内存中，当浏览器关闭，内存释放，则Cookie被销毁

    - 设置Cookie存活时间

    - ```
      cookies.setMaxAge()
      
      1.正数：将Cookie写入浏览器所在电脑的硬盘，持久化存储。到时间自动删除
      2.负数：默认值，Cookie在当前浏览器内存中，当浏览器关闭，则Cookie被销毁
      3.零：删除对应Cookie
      ```

  - cookie中的中文问题

    - ```
      存入
      String value = "张三";
      value=URLEncoder.encode(value,"UTF-8")
      new Cookie("username",value);
      获取
      String value = cookie.getValue();
      value = URLDecoder.decode(value,"UTF-8");
      ```

- 服务端会话跟踪技术：Session

  - 将数据保存到服务端

  - ```
    获取session
    request.getSesssion();
    ```

  - ```
    session
    HttpSession session = request.getSession();
    session.setAttribute("username","zs");
    session.getAttribute("username");
    ```

  - 关闭浏览器，session消失

  - 服务器关闭，session存在 钝化与活化

  - 原理

    - 在浏览器第一次发送request时,
    - tomcat服务器发现业务处理中使用了session对象，就会把session的唯一标识`id:10`当做一个cookie，添加`Set-Cookie:JESSIONID=10`到响应头中，并响应给浏览器
    - 浏览器在同一会话中访问其他资源的时候，会把cookie中的数据按照`cookie: JESSIONID=10`的格式添加到请求头中并发送给服务器Tomcat

  - session销毁

    - 默认情况下，无操作，30分钟自动销毁

    - 在项目的web.xml中配置

    - ```
      <?xml version="1.0" encoding="UTF-8"?>
      <web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
               version="3.1">
      
          <session-config>
              <session-timeout>100</session-timeout>
          </session-config>
      </web-app>
      ```

      

