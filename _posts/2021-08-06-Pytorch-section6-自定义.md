---
categories: [Pytorch]
tags: [自定义]
---
# Pytorch自定义

- ## 自定义损失函数

  - 函数方式

    - ```python
      def my_loss(output, target):
          loss = torch.mean((output - target)**2)
          return loss
      ```

  - 类方式

    - ```python
      class DiceLoss(nn.Module):
          def __init__(self,weight=None,size_average=True):
              super(DiceLoss,self).__init__()
              
          def forward(self,inputs,targets,smooth=1):
              inputs = F.sigmoid(inputs)       
              inputs = inputs.view(-1)
              targets = targets.view(-1)
              intersection = (inputs * targets).sum()                   
              dice = (2.*intersection + smooth)/(inputs.sum() + targets.sum() + smooth)  
              return 1 - dice
      ```

- ## 自定义动态学习率scheduler

  - scheduler的API

    - lr_scheduler.LambdaLR
    - lr_scheduler.MultiplicativeLR
    - lr_scheduler.StepLR
    - lr_scheduler.MultiStepLR
    - lr_scheduler.ExponentialLR
    - lr_scheduler.CosineAnnealingLR
    - lr_scheduler.CyclicLR
    - lr_scheduler.OneCycleLR
    - lr_scheduler.CosineAnnealingWarmRestarts

  - 自定义scheduler

    - ```python
      def adjust_learning_rate(optimizer, epoch):
          lr = lr * (0.1 ** (epoch // 30))
          for param_group in optimizer.param_groups:
              param_group['lr'] = lr
              
      for epoch in range(10):
          train(...)
          validate(...)
          adjust_learning_rate(optimizer,epoch)
      ```

- ## 半精度训练

  -  半精度训练主要适用于数据本身的size比较大 

  - ```python
    from torch.cuda.amp import autocast
    
    
    在定义模型时加上装饰器
    @autocast()   
    def forward(self, x):
        ...
        return x
    
    训练阶段加上with autocast():
    for x in train_loader:
        x = x.cuda()
        with autocast():
            output = model(x)
    ```

- ## argparse的使用

  - 创建`ArgumentParser()`对象

  - 调用`add_argument()`方法添加参数

  - 使用`parse_args()`解析参数 在接下来的内容中，我们将以实际操作来学习argparse的使用方法。

  - ```python
    import argparse
    
    # 创建ArgumentParser()对象
    parser = argparse.ArgumentParser()
    
    # 添加参数
    parser.add_argument('-o', '--output', action='store_true', 
        help="shows output")
    # action = `store_true` 会将output参数记录为True
    # type 规定了参数的格式
    # default 规定了默认值
    parser.add_argument('--lr', type=float, default=3e-5, help='select the learning rate, default=1e-3') 
    
    parser.add_argument('--batch_size', type=int, required=True, help='input batch size')  
    # 使用parse_args()解析函数
    args = parser.parse_args()
    
    if args.output:
        print("This is some output")
        print(f"learning rate:{args.lr} ")
    ```

- ## 随机数

  - ```
    def set_seed(seed):
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        random.seed(seed)
        np.random.seed(seed)
        torch.backends.cudnn.benchmark = False
        torch.backends.cudnn.deterministic = True
    ```