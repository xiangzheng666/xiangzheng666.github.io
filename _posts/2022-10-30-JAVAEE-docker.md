---
categories: [javaEE]
tags: [docker]
---
# docker

- images
  - docker images
  - docker pull 
  - docker save -o 导出镜像到磁盘 
  - docker rmi 删除本地的镜像
  
- container
  - docker run：创建并运行一个容器，处于运行状态
    - docker run --name containerName -p 80:80 -d nginx
      - --name：指定容器名称
      - -p：指定端口映射
      - -d：让容器后台运行
  - docker pause：让一个运行的容器暂停
  - docker unpause：让一个容器从暂停状态恢复运行
  - docker stop：停止一个运行的容器
  - docker start：让一个停止的容器再次运行
  - docker rm：删除一个容器
  - docker ps：查看容器状态
  
- volume
  - docker volume
    - create 创建一个volume
    - inspect 显示一个或多个volume的信息
    - ls 列出所有的volume
    - prune 删除未使用的volume
    - rm 删除一个或多个指定的volume
  - -v 参数来挂载一个数据卷到某个容器内目录
    - -v [宿主机目录]:[容器内目录]

- Dockerfile

  - ```
    # 指定基础镜像
    FROM ubuntu:16.04
    # 配置环境变量，JDK的安装目录
    ENV JAVA_DIR=/usr/local
    
    # 拷贝jdk和java项目的包
    COPY ./jdk8.tar.gz $JAVA_DIR/
    COPY ./docker-demo.jar /tmp/app.jar
    
    # 安装JDK
    RUN cd $JAVA_DIR \
     && tar -xf ./jdk8.tar.gz \
     && mv ./jdk1.8.0_144 ./java8
    
    # 配置环境变量
    ENV JAVA_HOME=$JAVA_DIR/java8
    ENV PATH=$PATH:$JAVA_HOME/bin
    
    # 暴露端口
    EXPOSE 8090
    # 入口，java项目的启动命令
    ENTRYPOINT java -jar /tmp/app.jar
    ```

  - docker build

- Docker-Compose.yml

  - ```
    version: "3.2"
    
    services:
      nacos:
        image: nacos/nacos-server
        environment:
          MODE: standalone
        ports:
          - "8848:8848"
      mysql:
        image: mysql:5.7.25
        environment:
          MYSQL_ROOT_PASSWORD: 123
        volumes:
          - "$PWD/mysql/data:/var/lib/mysql"
          - "$PWD/mysql/conf:/etc/mysql/conf.d/"
      userservice:
        build: ./user-service
      orderservice:
        build: ./order-service
      gateway:
        build: ./gateway
        ports:
          - "10010:10010"
    ```

  - docker-compose up
  
- 私有仓库

  - ```
    version: '3.0'
    services:
      registry:
        image: registry
        volumes:
          - ./registry-data:/var/lib/registry
      ui:
        image: joxit/docker-registry-ui:static
        ports:
          - 8080:80
        environment:
          - REGISTRY_TITLE=传智教育私有仓库
          - REGISTRY_URL=http://registry:5000
        depends_on:
          - registry
    ```

    