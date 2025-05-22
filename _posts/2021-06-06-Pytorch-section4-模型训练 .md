---
categories: [Pytorch]
tags: [模型训练]
---
# Pytorch模型训练

- ## 模型组件

  - torch.nn
    - Con2d(in_chanal,out_chanal,kernel_size,stride,padding)
    - Linear(in_chanal,out_chanal, bias)
    - MaxPool2d(henal_size,strde,padding)
    - ...
  
- ## 模型创建

  - Sequential
  
    - ```
      import torch.nn as nn
      net = nn.Sequential(
              nn.Linear(784, 256),
              nn.ReLU(),
              nn.Linear(256, 10), 
              )
      print(net)
      Sequential(
        (0): Linear(in_features=784, out_features=256, bias=True)
        (1): ReLU()
        (2): Linear(in_features=256, out_features=10, bias=True)
      )
      ```
  
  - Swquential+OrderedDict 
  
    - ```
      import collections
      import torch.nn as nn
      net2 = nn.Sequential(collections.OrderedDict([
                ('fc1', nn.Linear(784, 256)),
                ('relu1', nn.ReLU()),
                ('fc2', nn.Linear(256, 10))
                ]))
      print(net2)
      
      Sequential(
        (fc1): Linear(in_features=784, out_features=256, bias=True)
        (relu1): ReLU()
        (fc2): Linear(in_features=256, out_features=10, bias=True)
      )
      ```
  
  - ModuleList
  
    -  ModuleList 接收一个子模块（或层，需属于nn.Module类）的列表作为输入，然后也可以类似List那样进行append和extend操作。同时，子模块或层的权重也会自动添加到网络中来。 
  
    -  nn.ModuleList 并没有定义一个网络 ,只是
  
    - ```
      net = nn.ModuleList([nn.Linear(784, 256), nn.ReLU()])
      net.append(nn.Linear(256, 10)) # # 类似List的append操作
      print(net[-1])  # 类似List的索引访问
      print(net)
      Linear(in_features=256, out_features=10, bias=True)
      ModuleList(
        (0): Linear(in_features=784, out_features=256, bias=True)
        (1): ReLU()
        (2): Linear(in_features=256, out_features=10, bias=True)
      )
      ```
  
  - ModuleDict
  
    -  ModuleDict和ModuleList的作用类似，只是ModuleDict能够更方便地为神经网络的层添加名称。 
  
    - ```
      net = nn.ModuleDict({
          'linear': nn.Linear(784, 256),
          'act': nn.ReLU(),
      })
      net['output'] = nn.Linear(256, 10) # 添加
      print(net['linear']) # 访问
      print(net.output)
      print(net)
      Linear(in_features=784, out_features=256, bias=True)
      Linear(in_features=256, out_features=10, bias=True)
      ModuleDict(
        (act): ReLU()
        (linear): Linear(in_features=784, out_features=256, bias=True)
        (output): Linear(in_features=256, out_features=10, bias=True)
      )
      ```
  
  - 自定义class
  
    - ```
      class MLP(nn.Module):
        # 声明带有模型参数的层，这里声明了两个全连接层
        def __init__(self, **kwargs):
          # 调用MLP父类Block的构造函数来进行必要的初始化。这样在构造实例时还可以指定其他函数
          super(MLP, self).__init__(**kwargs)
          self.hidden = nn.Linear(784, 256)
          self.act = nn.ReLU()
          self.output = nn.Linear(256,10)
        
         # 定义模型的前向计算，即如何根据输入x计算返回所需要的模型输出
        def forward(self, x):
          o = self.act(self.hidden(x))
          return self.output(o)   
      ```

- ## 初始化参数
  
  - torch.nn.init 
  
  - 使用 torch.nn.init 包中的初始化方法
  
    - ```
      torch.nn.init.~(net.weight)
      ```
  
- ## 损失函数

  - torch.nn.BCELoss()
  
    -  二分类交叉熵
    
    - $$
    loss=1/N\sum_n(l_n) ;l_n=y_n*\log(x_n)+(1-y_n)*\log(1-x_n)
      $$
  
  - torch.nn.CrossEntropyLoss()
  
    - 交叉熵
  
    - $$
      \operatorname{loss}(x, \text { class })=-\log \left(\frac{\exp (x[\text { class }])}{\sum_{j} \exp (x[j])}\right)=-x[\text { class }]+\log \left(\sum_{j} \exp (x[j])\right)
      $$
  
  - torch.nn.L1Loss()
  
    -  差值的绝对值 
  
    - $$
      L_{n} = |x_{n}-y_{n}|
      $$
  
  - torch.nn.MSELoss()
  
    - MSE损失
  
    - $$
      l_{n}=\left(x_{n}-y_{n}\right)^{2}
      $$
  
  - troch.nn.SmoothL1Loss
  
    -  L1的平滑输出，减轻离群点带来的影响 
  
    - $$
      z_{i}=\left\{\begin{array}{ll}
      0.5\left(x_{i}-y_{i}\right)^{2}, & \text { if }\left|x_{i}-y_{i}\right|<1 \\
      \left|x_{i}-y_{i}\right|-0.5, & \text { otherwise }
      \end{array}\right.
      $$
  
  - troch.cosine_similarity 
  
    - 计算余弦相似度 
  
  - torch.nn.KLDivLoss()
  
    - 计算KL散度/相对熵。
  
    - $$
      DKL(P,Q)=EX∼P[log⁡P(X)Q(X)]=EX∼P[log⁡P(X)−log⁡Q(X)]=∑i=1nP(xi)(log⁡P(xi)−log⁡Q(xi))
      $$
  
  - torch.nn.MarginRankingLoss()
  
    -  计算两个向量之间的相似度，用于排序任务
  
    - $$
      loss(x1,x2,y)=max(0,−y∗(x1−x2)+margin)
      $$
  
  - torch.nn.MultiLabelMarginLoss()
  
    - 对于多标签分类问题计算损失函数。
  
    - $$
      loss(x,y)=∑ijmax(0,1−x[y[j]]−x[i])x⋅size(0)
      $$
  
  - torch.nn.SoftMarginLoss()
  
    -  计算二分类的 logistic 损失。
  
    - $$
      loss(x,y)=∑ilog⁡(1+exp⁡(−y[i]⋅x[i]))x⋅nelement()
      $$
  
  - torch.nn.MultiMarginLoss(）
  
    - 计算多分类的折页损失
  
    - $$
      loss(x,y)=∑imax(0,margin−x[y]+x[i])px⋅size(0)
      $$
  
  - torch.nn.TripletMarginLoss()
  
    - 计算三元组损失。
  
    - $$
      L(a,p,n)=max({d(ai,pi)−d(ai,ni)+margin,0})  ，其中 d(xi,yi)=‖xi−yi‖
      $$
  
  - torch.nn.HingeEmbeddingLoss()
  
    -  对输出的embedding结果做Hing损失计算
  
    - $$
      l_{n}=\left\{\begin{array}{ll}
      x_{n}, & \text { if } y_{n}=1 \\
      \max \left\{0, \Delta-x_{n}\right\}, & \text { if } y_{n}=-1
      \end{array}\right.
      $$
  
  - torch.nn.CosineEmbeddingLoss()
  
    -  对两个向量做余弦相似度,判断相似
  
    - $$
      \operatorname{loss}(x, y)=\left\{\begin{array}{ll}
      1-\cos \left(x_{1}, x_{2}\right), & \text { if } y=1 \\
      \max \left\{0, \cos \left(x_{1}, x_{2}\right)-\text { margin }\right\}, & \text { if } y=-1
      \end{array}\right.
      $$
  
    - $$
      \cos (\theta)=\frac{A \cdot B}{\|A\|\|B\|}=\frac{\sum_{i=1}^{n} A_{i} \times B_{i}}{\sqrt{\sum_{i=1}^{n}\left(A_{i}\right)^{2}} \times \sqrt{\sum_{i=1}^{n}\left(B_{i}\right)^{2}}}
      $$
  
  - torch.nn.CTCLoss()
  
    -  时序类数据的分类 

- ## 优化器
  - 优化函数
    - torch.optim.ASGD
      - 
    - torch.optim.Adadelta
      - 
    - torch.optim.Adagrad
      - 
    - torch.optim.Adam
      - 
    - torch.optim.AdamW
      - 
    - torch.optim.Adamax
      - 
    - torch.optim.LBFGS
      - 
    - torch.optim.RMSprop
      - 
    - torch.optim.Rprop
      - 
    - torch.optim.SGD
      - 
    - torch.optim.SparseAdam
      - 
  - 属性
    - defaults = defaults  优化器的超参数 
    - state = defaultdict(dict)  参数的缓存 
    - param_groups = []   参数组，是一个list 
  - 方法
    -  zero_grad:   清空所管理参数的梯度  
    - step：执行一步梯度更新，参数更新
    -  add_param_group：添加参数组 
    -  load_state_dict() ：加载状态参数字典 
    - state_dict()：获取优化器当前状态信息字典

- ## 模型训练

  - ```
    model.train()   # 训练状态
    model.eval()   # 验证/测试状态
    
    optimizer.zero_grad()
    ...
    loss = criterion(output, label)
    loss.backward()
    optimizer.step()
    ```