---
categories: [Pytorch]
tags: [基础知识]
---
# Pytorch基础知识
- ## 创建Tensor
| 函数                |                       功能                        |
| :------------------ | :-----------------------------------------------: |
| Tensor(shape/data)       |                   基础构造函数                    |
| tensor(data)        |                  类似于np.array                   |
|from_numpy           |                   通过numpy创建                    |
| -| -|
| ones(sizes)         |                        全1                        |
| zeros(sizes)        |                        全0                        |
| eye(sizes)          |                 对角为1，其余为0                  |
|full(shape,value)|全value的shape的tensor|
|-|-|
| arange(s,e,step)    |                从s到e，步长为step                 |
| linspace(s,e,steps) |              从s到e，均匀分成step份               |
|-|-|
|empty|未初始化|
|FloatTensor|未初始化|
|IntTensor|未初始化|
|-|-|
| rand/randn(sizes)   | rand是(0,1)均匀分布 randn是服从N(0，1)的正态分布 |
|randint()|自定义区间|
| normal(mean,std)    |         正态分布(均值为mean，标准差是std)         |
| randperm(m)         |                     随机排列                      |
| .cuda().to(device).cpu() | 转换device的内存或者显存 |
- 注意empty返回，返回是未初始化的tensor

  - ```
    >>>torch.empty(5,3)
    tensor([[9.1837e-39, 4.6837e-39, 9.9184e-39],
    [9.0000e-39, 1.0561e-38, 1.0653e-38],
    [4.1327e-39, 8.9082e-39, 9.8265e-39],
    [9.4592e-39, 1.0561e-38, 1.0653e-38],
    
    >>>torch.zeros(5,3)
    tensor([[0., 0., 0.],
            [0., 0., 0.],
            [0., 0., 0.],
            [0., 0., 0.],
            [0., 0., 0.]])
    ```
- ## torch维度变化
	
	- **view**
	  注意 **view()** 返回的新tensor与源tensor共享内存(其实是同一个tensor)，也即更改其中的一个，另 外一个也会跟着改变。**(顾名思义，view仅仅是改变了对这个张量的观察⻆度**)
	   reshape() 可以改变形状，但是此函数并不能保证返回的是其拷贝，所以不推荐使用。推荐先用 clone 创造一个副本然后再使用 view 。
	
	  - ```
	     >>> a=torch.ones(2,2)
	     >>> b=a.view(4,1)
	     >>> b[0]=2
	     >>> a
	     tensor([[2., 1.],
	     [1., 1.]])	
	    ```
	
	- unsqueeze(axis)
	
	  - 在axis上增加一维
	
	  - ```
	    >>> a.shape
	    torch.Size([2, 2])
	    >>> a.unsqueeze(-1).shape
	    torch.Size([2, 2, 1])
	    >>> a.unsqueeze(1).shape
	    torch.Size([2, 1, 2])
	    ```
	
	- stack()
	
	  - stack()合并增加新的一维
	
	  - ```
	    >>> a
	    tensor([[ 1,  2,  3,  4,  5,  6],
	            [ 7,  8,  9, 10, 11, 12]])
	    >>> b
	    tensor([[ 1,  2,  3,  4,  5,  6],
	            [ 7,  8,  9, 10, 11, 12]])
	    >>> torch.stack([a,b],dim=0)
	    tensor([[[ 1,  2,  3,  4,  5,  6],
	             [ 7,  8,  9, 10, 11, 12]],
	    
	            [[ 1,  2,  3,  4,  5,  6],
	             [ 7,  8,  9, 10, 11, 12]]])
	    >>> torch.stack([a,b],dim=0).shape
	    torch.Size([2, 2, 6])
	    >>> torch.stack([a,b],dim=1)
	    tensor([[[ 1,  2,  3,  4,  5,  6],
	             [ 1,  2,  3,  4,  5,  6]],
	    
	            [[ 7,  8,  9, 10, 11, 12],
	             [ 7,  8,  9, 10, 11, 12]]])
	    >>> torch.stack([a,b],dim=1).shape
	    torch.Size([2, 2, 6])
	    ```
	
	    
	
	- repeat(d1,d2)
	
	  - 在原来的维度上重复d1，d2
	
	  - ```
	    >>> a
	    tensor([[2., 1.],
	            [1., 1.]])
	    >>> a.repeat(1,2)
	    tensor([[2., 1., 2., 1.],
	            [1., 1., 1., 1.]])
	    ```
	
	- transpose(axis,axis)
	
	  - 交换axis,axis
	
	  - ```
	    >>> a
	    tensor([[[ 1.,  2.],
	             [ 3.,  4.],
	             [ 5.,  6.],
	             [ 7.,  8.]],
	    
	            [[ 9., 10.],
	             [11., 12.],
	             [13., 14.],
	             [15., 16.]]])
	    >>> a.transpose(1,2)
	    tensor([[[ 1.,  3.,  5.,  7.],
	             [ 2.,  4.,  6.,  8.]],
	    
	            [[ 9., 11., 13., 15.],
	             [10., 12., 14., 16.]]])
	    >>> a.transpose(1,2).transpose(0,1)
	    tensor([[[ 1.,  3.,  5.,  7.],
	             [ 9., 11., 13., 15.]],
	    
	            [[ 2.,  4.,  6.,  8.],
	             [10., 12., 14., 16.]]])
	    ```
	
	- permute(d1,d2,d3)
	
	  - 维度变成d1,d2,d3
	
	  - ```
	    >>> a.shape
	    torch.Size([2, 4, 2])
	    >>> a.permute([0,2,1])
	    tensor([[[ 1.,  3.,  5.,  7.],
	             [ 2.,  4.,  6.,  8.]],
	    
	            [[ 9., 11., 13., 15.],
	             [10., 12., 14., 16.]]])
	    >>> c=a.permute([0,2,1])
	    >>> c[0][0][0]=100
	    >>> c
	    tensor([[[100.,   3.,   5.,   7.],
	             [  2.,   4.,   6.,   8.]],
	    
	            [[  9.,  11.,  13.,  15.],
	             [ 10.,  12.,  14.,  16.]]])
	    >>> a
	    tensor([[[100.,   2.],
	             [  3.,   4.],
	             [  5.,   6.],
	             [  7.,   8.]],
	    
	            [[  9.,  10.],
	             [ 11.,  12.],
	             [ 13.,  14.],
	             [ 15.,  16.]]])
	    ```
	
- ## torch拼接

  - cat

    - torch.cat([a,b],din)

    - ```
      >>> a
      tensor([[ 1,  2,  3,  4,  5,  6],
              [ 7,  8,  9, 10, 11, 12]])
      >>> b
      tensor([[ 1,  2,  3,  4,  5,  6],
              [ 7,  8,  9, 10, 11, 12]])
      >>> torch.cat((a,b),dim=0)
      tensor([[ 1,  2,  3,  4,  5,  6],
              [ 7,  8,  9, 10, 11, 12],
              [ 1,  2,  3,  4,  5,  6],
              [ 7,  8,  9, 10, 11, 12]])
      >>> torch.cat((a,b),dim=1)
      tensor([[ 1,  2,  3,  4,  5,  6,  1,  2,  3,  4,  5,  6],
              [ 7,  8,  9, 10, 11, 12,  7,  8,  9, 10, 11, 12]])
      ```

  - split()

    - split(length,dim)等分

    - split([d,d],dim)不等分

    - ```
      >>>a.split([2,3,1],dim=1)
      (tensor([[1, 2],
              [7, 8]]),
      tensor([[ 3,  4,  5],
            [ 9, 10, 11]]), 
      tensor([[ 6],
             [12]]))
      >>> a.split(2,dim=1)
      (tensor([[1, 2],
              [7, 8]]), 
      tensor([[ 3,  4],
              [ 9, 10]])
      tensor([[ 5,  6],
              [11, 12]]))
                  
      ```

- ## torch统计函数

  - | 名称     | 描述                                           |
    | -------- | ---------------------------------------------- |
    | norm     | 2范数-欧几里德范数                             |
    | min      | 最小值                                         |
    | max      | 最大值                                         |
    | mean     | 均值                                           |
    | argmax   | 最大索引                                       |
    | argmin   | 最小索引                                       |
    | sum      | 求和                                           |
    | prod     | 在指定dim上的乘积                              |
    | topk     | 数组在维度上最大的值                           |
    | kthvalue | 取输入张量input指定维度上第k个最小值           |
    | eq()     | 放回一个torch.ByteTensor张量(相等为1，不等为0) |
    | equal    | 相同的形状和元素值，返回true，False            |

    - torch.autograd.grad(loss,[parameters])-求导

    