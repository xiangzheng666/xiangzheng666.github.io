---
categories: [javaEE]
tags: [maven]
---
# maven

- 依赖管理

  - gav

- 依赖传递

  - 可选依赖

    - ```
      <dependency>
          <groupId>com.itheima</groupId>
          <artifactId>maven_03_pojo</artifactId>
          <version>1.0-SNAPSHOT</version>
          <!--可选依赖是隐藏当前工程所依赖的资源，隐藏后对应资源将不具有依赖传递性-->
          <optional>false</optional>
      </dependency>
      ```

  - 排除依赖

    - ```
      <dependency>
          <groupId>com.itheima</groupId>
          <artifactId>maven_04_dao</artifactId>
          <version>1.0-SNAPSHOT</version>
          <!--排除依赖是隐藏当前资源对应的依赖关系-->
          <exclusions>
              <exclusion>
                  <groupId>log4j</groupId>
                  <artifactId>log4j</artifactId>
              </exclusion>
              <exclusion>
                  <groupId>org.mybatis</groupId>
                  <artifactId>mybatis</artifactId>
              </exclusion>
          </exclusions>
      </dependency>
      ```

- 聚合

  - 将多个模块组织成一个整体，同时进行项目构建的过程称为聚合

  - 对多个模块同时进行lifecycle，及时更新

  - step

    - ```
      1.设置packaging
      <packaging>pom</packaging>
      2.设置子模块
      <modules>
          <module>../maven_ssm</module>
          <module>../maven_pojo</module>
          <module>../maven_dao</module>
      </modules>
      ```

- 继承

  - step	

    - ```
      1.父工程打包方设置packaging
      <packaging>pom</packaging>
      2.配置子工程中可选的依赖关系
      <dependencyManagement>
          <dependencies>
              ……
          </dependencies>
      </dependencyManagement>
      3.继承父工程
      <parent>
          <groupId>com.itheima</groupId>
          <artifactId>maven_parent</artifactId>
          <version>1.0-SNAPSHOT</version>
          <!--填写父工程的pom文件，根据实际情况填写-->
          <relativePath>../maven_parent/pom.xml</relativePath>
      </parent>
      4.可选依赖坐标
      <dependencies>
          <dependency>
              <groupId>com.alibaba</groupId>
              <artifactId>druid</artifactId>
          </dependency>
      </dependencies>
      ```

- 属性管理

  - 定义属性

    - ```
      <properties>
          <spring.version>5.2.10.RELEASE</spring.version>
          <junit.version>4.12</junit.version>
      </properties>
      ```

  - 引用属性

    - ```
      <dependency>
          <groupId>org.springframework</groupId>
          <artifactId>spring-context</artifactId>
          <version>${spring.version}</version>
      </dependency>
      ```

  - 资源文件引用属性

    - ```
      1.定义自定义属性
      <properties>
          <spring.version>5.2.10.RELEASE</spring.version>
          <junit.version>4.12</junit.version>
          <jdbc.url>jdbc:mysql://127.0.0.1:3306/ssm_db</jdbc.url>
      </properties>
      2.配置文件
      jdbc.driver=com.mysql.jdbc.Driver
      jdbc.url=${jdbc.url}
      jdbc.username=root
      jdbc.password=root
      3.开启资源文件目录加载属性的过滤器
      <build>
          <resources>
              <resource>
                  <directory>${project.basedir}/src/main/resources</directory>
                  <filtering>true</filtering>
              </resource>
          </resources>
      </build>
      ```

- 版本管理

  - SNAPSHOT（快照版本）
    - 项目开发过程中临时输出的版本，称为快照版本
    - 快照版本会随着开发的进展不断更新
  - RELEASE（发布版本）
    - 项目开发到进入阶段里程碑后，向团队外部发布较为稳定的版本，这种版本所对应的构件文件是稳定的
    - 即便进行功能的后续开发，也不会改变当前发布版本内容，这种版本称为发布版本

- 私服

  - Nexus：nexus.exe /run nexus

  - ![1669367207006](https://github.com/xiangzheng666/picx-images-hosting/raw/master/1669367207006.4ub5ve494l.webp)

  - 从私服中下载依赖

    - settings.xml

      - ```
        <mirror>
            <id>nexus-heima</id>
            <mirrorOf>*</mirrorOf>
            <url>http://localhost:8081/repository/maven-public/</url>
        </mirror>
        ```

  - 上传依赖到私服中

    - settings.xml

      - ```
        <server>
          <!--id任意，多个server的id不重复就行，后面会用到-->
          <id>heima-nexus</id>
          <username>admin</username>
          <password>123456</password><!--填写自己nexus设定的登录秘密-->
        </server>
        ```

    - pom

      - ```
        <distributionManagement>
            <repository>
              	<!--和maven/settings.xml中server中的id一致，表示使用该id对应的用户名和密码-->
                <id>heima-nexus</id>
              	<!--如果jar的版本是release版本，那么就上传到这个仓库，根据自己情况修改-->
                <url>http://localhost:8081/repository/heima-releases/</url>
            </repository>
            <snapshotRepository>
              	<!--和maven/settings.xml中server中的id一致，表示使用该id对应的用户名和密码-->
                <id>heima-nexus</id>
              	<!--如果jar的版本是snapshot版本，那么就上传到这个仓库，根据自己情况修改-->
                <url>http://localhost:8081/repository/heima-snapshots/</url>
            </snapshotRepository>
        </distributionManagement>
        ```

    - mvn deploy

      