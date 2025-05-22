---
categories: [Machine Learing]
tags: [集成学习,Voting,Bagging,Boosting,Stacking,Random Forests]
---

# 集成学习

- #### majority-Voting                                                                                                                                                                                       
  - <img src="C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1665222146623.png" alt="1665222146623" style="zoom:50%;" />
  - 假设每一个分类模型的错误率只是比随机猜测好一点（错误率低于0.5)
  - 那么k个模型输出都是错误类别，造成最终是错误类别的概率
  - <img src="C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1665222233885.png" alt="1665222233885" style="zoom:50%;" />
  - soft-voting:加入权值

- #### Bagging

  - 有放回抽样构建数据集
  - <img src="C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1665222311817.png" alt="1665222311817" style="zoom:50%;" />
  - 则莫个样本不会被选择的概率为0.368
  - 解决一些过拟合的问题
  - <img src="C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1665222451464.png" alt="1665222451464" style="zoom:50%;" />
  - <img src="C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1665222478242.png" alt="1665222478242" style="zoom:50%;" />
  - <img src="C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1665222502162.png" alt="1665222502162" style="zoom:50%;" />
  - 假设我们有多组不相关的训练数据。为每一组训练数据训练一个复杂模型，集成多个模型的结果，相互抵消，可以减小Variance.



- #### Boosting

  - step：
    - 初始化一个权重向量，里面的值都相等
    - 循环：
      - 使用带权重的训练数据训练一个模型
        为预测错误的的训练数据增大权重
    - 使用带权重的majority voting
    - model_error 提高 model-weight 下降
    - data_error 提高 data-weight 提高 
    - 提高对分类错误的数据的权重，减少简单模型的权重

- #### Random Forests
  - Bagging +w.trees+ random featuresubsets

- #### Stacking

  - <img src="C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1665222841145.png" alt="1665222841145" style="zoom:50%;" />
  - 使用上一层模型输出训练下一层模型
  - 缺点：容易过拟合，如果第一层的模型已经过拟合了，第二层的模型基于过拟合的数据