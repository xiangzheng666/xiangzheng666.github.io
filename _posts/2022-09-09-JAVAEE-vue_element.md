---
categories: [javaEE]
tags: [VUE]
---
# VUE

- 思想：mvvm

- vue代码放到后面

- 指令

  - **v-bind**

    - 单向绑定

    - ```
      <a v-bind:href="url">点击一下</a><br>
      ```

  - v-model

    - 双向绑定

    - ```
      <input v-model="username"><br>
      ```

  - v-on

    - 绑定事件

    - ```
      <button v-on:click="show()">点我一下</button><br>
      ```

  - v-if

  - v-show

    - 条件判断

    - ```
      <h1 v-if="username==1">1</h1>
      <h1 v-else-if="username==2">2</h1>
      <h1 v-else>else</h1>
      <h1 v-show="username==1">1</h1>
      ```

- 生命周期

  - 八个阶段
  - ![1668858172908](https://github.com/xiangzheng666/picx-images-hosting/raw/master/1668858172908.2h8je6qfxv.webp)
  - `mounted`：挂载完成，Vue初始化成功，HTML页面渲染成功。而以后我们会在该方法中**发送异步请求，加载数据**