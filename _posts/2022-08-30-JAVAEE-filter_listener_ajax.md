---
categories: [javaEE]
tags: [Filter]
---
# Filter

- 使用

  - 实现Filter接口类

  - 编写@WebFilter(value="/")注解

  - ```
    @WebFilter(filterName = "demoFilter",value = "/*")
    public class demoFilter implements Filter {
        public void init(FilterConfig config) throws ServletException {
        }
    
        public void destroy() {
        }
    
        @Override
        public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws ServletException, IOException {
            System.out.println("fliter..........");
            chain.doFilter(request, response);
        }
    }
    
    ```

- 流程

  - ![1668834453180](https://github.com/xiangzheng666/picx-images-hosting/raw/master/1668834453180.26lpl1b7sg.webp)
  - 优先级是按照过滤器类名(字符串)的自然排序
  - ![1668834495454](https://github.com/xiangzheng666/picx-images-hosting/raw/master/1668834495454.maz9jk1e.webp)

- 路径配置

  - 拦截具体的资源：/index.jsp：只有访问index.jsp时才会被拦截
  - 目录拦截：/user/*：访问/user下的所有资源，都会被拦截
  - 后缀名拦截：*.jsp：访问后缀名为jsp的资源，都会被拦截
  - 拦截所有：/*：访问所有资源，都会被拦截

# Listener

- 使用

  - 实现xxxxxContextListener接口类

  - 编写@WebListener注解

  - ```
    @WebListener
    public class ContextLoaderListener implements ServletContextListener {
        @Override
        public void contextInitialized(ServletContextEvent sce) {
            //加载资源
            System.out.println("ContextLoaderListener...");
        }
    
        @Override
        public void contextDestroyed(ServletContextEvent sce) {
            //释放资源
        }
    }
    ```

- 生命周期监听器

  - ServletRequest的生命周期监听器
    - ServletRequestListener接口
      - 监听ServletRequest对象的创建与销毁
  - HttpSession的生命周期监听器

    - HttpSessionListener接口
      - 监听HttpSession对象的创建与销毁

  - ServletContext的生命周期监听器

    - ServletContextListener

      - 监听ServletContext对象的创建与销毁

- 属性变化监听器

  - ServletRequest的属性变化监听器
    - ServletRequestAttributeListener接口
      - 监听request域中的属性的添加、替换、移除
  - HttpSession的属性变化监听器
    - HttpSessionAttributeListener接口
      - 监听session域中的属性的添加、替换、移除
  - ServletContext的属性变化监听器
    - ServletContextAttributeListener接口
      - 监听application域中的属性的添加、替换、移除

# AJAX

- 异步请求

- ```
  document.getElementById("username").onblur = function () {
          var xhttp;
          if (window.XMLHttpRequest) {
              xhttp = new XMLHttpRequest();
          } else {
              // code for IE6, IE5
              xhttp = new ActiveXObject("Microsoft.XMLHTTP");
          }
  
          xhttp.open("GET", "http://localhost:8080/el_jsp/checkusernameServlet?username="+this.value);
          //发送请求
          xhttp.send();
  
          xhttp.onreadystatechange = function() {
              if (this.readyState == 4 && this.status == 200) {
                  // 通过 this.responseText 可以获取到服务端响应的数据
                  if(this.responseText!=null){
                      //用户名存在，显示提示信息
                      document.getElementById("username_err").style.display = '';
                  }else {
                      //用户名不存在 ，清楚提示信息
                      document.getElementById("username_err").style.display = 'none';
                  }
              }
          };
      }
  ```

- axios库

  - 使用

    - ```
      <script src="js/axios-0.18.0.js"></script>
      
      axios
      axios({
          method:"get",
          url:"http://localhost:8080/ajax-demo1/aJAXDemo1?username=zhangsan",
          data:"username=zhangsan"
      }).then(function (resp){
          alert(resp.data);
      })
      method 属性：用来设置请求方式的。取值为 `get` 或者 `post`。
      url 属性：用来书写请求的资源路径。如果是 `get` 请求，需要将请求参数拼接到路径的后面，格式为： 
      data 属性：作为请求体被发送的数据。也就是说如果是 `post` 请求的话，数据需要作为 `data` 属性的值。
      ```

- json

  - 格式

  - ```
    var 变量名 = '{"key":value,"key":value,...}';
    ```

  - js转换

    - string2json

      - ```
        JSON.parse(str)
        ```

    - json2string

      - ```
        JSON.stringfy(json)
        ```

  - java转化

    - bean2json
      - JSON.toJSONString(bean)
    - json2bean
      - JSON.parseObject(jsonStr, bean.class);