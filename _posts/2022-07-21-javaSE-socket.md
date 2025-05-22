---
categories: [javaSE]
tags: [socket]
---
# socket

- TCP

  - ```
     new ServerSocket(6666); // 监听指定端口 
    ```

  -  ss.accept()就返回一个Socket实例，这个`Socket`实例就是用来和刚连接的客户端进行通信的 

    - newclient.getRemoteSocketAddress()

  - 获取输入输出接口

  - ```
    inputStream in = this.socket.getInputStream()
    OutputStream out = this.socket.getOutputStream()
    ```

  - 输入输出与客户端交流

  - client

  - ```
    Socket sock = new Socket("localhost", 6666); // 连接指定服务器和端口
    ```

  - 获取输入输出接口

  - ```
    inputStream in = this.socket.getInputStream()
    OutputStream out = this.socket.getOutputStream()
    ```

  - 输入输出与客户端交流

- UDP

  - ```
    DatagramSocket ds = new DatagramSocket(6666); // 监听指定端口
    ```

  - // 数据缓冲区

    - ```
      byte[] buffer = new byte[1024];
      DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
      ```

  - 数据输入输出

    - ```
      ds.receive(packet);
      ds.send(packet);
      
      //packet 
      packet.getData(), packet.getOffset(), packet.getLength()
      packet.setData(data)
      ```

  - client

    - ```
      DatagramSocket ds = new DatagramSocket();
      ds.connect(InetAddress.getByName("localhost"), 6666); // 连接指定服务器和端口
      
      ds.disconnect();
      ```

      