---
categories: [nlp]
tags: [条件随机场,CRF]
---
# 条件随机场CRF

- HMM

  - 任意时刻当前的状态只与前一个时刻的状态有关（状态转移矩阵A）

  - 当前观测只与当前状态有关（观测矩阵B）

  - 这两个假设在nlp领域不合理

  - $$
    P(X,Z)=\prod \limits_{i=1}^{T}p(z_i|z_{i-1})p(x_i|z_i)
    $$

    

- HEMM

  - 打破hmm假设

  - $$
    P(Z|X)=\prod \limits_{i=1}^{T}p(z_i|z_{i-1},x)
    $$

  - 但是由于局部归一化的原因（就是观测概率）出现了[标签偏差问题](https://awni.github.io/label-bias/)（就是对莫一种隐状态的偏向）

- 线性链CRF

  - 将有向图转化成无向图,使用最大团分解无向图模型
  
  - 将概率变成分数函数，最后使用全局归一化操作
  
  - $$
    P(Y|X)={1\over Z}\prod \limits_i^k \phi_i(x_{c_i})\\\phi_i(x_{c_i})为最大团的分数函数要保证大于0\\
    P(Y|X)={1\over Z}\prod \limits_i^k \exp F(x_{c_i})={1\over Z}\exp{\sum_i^kF(x_{c_i})}\\对于F(x_{c_i})团来说，是关于x,y_i,y_{i-1}的函数可以写成
    \\P(Y|X)={1\over Z}\exp{\sum_i^kF_t(y_{t-1},y,x)}\quad F_t也可以设置同一个函数\\然后拆分F_t变成两部分，一部分是关于y_t,x提取的的特征，以及关于y_{t-1},y,x提取的特征\\
    $$
    
  - 为什么这么拆，暂时不清楚,说是什么状态特征与转移特征。
  
  - $$
    P(Y|X)={1\over Z}\exp{\sum_i^{k个团} \Big(\sum_{k=1}^{提取特征的个数}\lambda_kf_k(y_{t-1},y,x)   +\sum_l^{提取特征个数}\beta_lg_l(y_t,x) \Big)}
    $$
  
  - 这样就推导出了线性crf的pdf，其中的f_k,g_l的个数以及形式都是自定义的，但是每一个特征都有一个不同的权重
  
  - 这里可以这么理解，给定随机变量Y，X,我们先提取他们的特征，比如 是否是同班同学，是否满足什么条件 获得的分数在累计求和，得到随机变量序列Y的分数，在进行全局归一化，就可以得到当前x最大可能的Y
  
  - 转化从向量形式
  
  - $$
    \lambda=(\lambda_1,\lambda_2....\lambda_k)^T\\
    \beta=(\beta_1,\beta_2....\beta_k)^T\\
    f=(f_1,f_2...f_k)\\
    g=(g_1,g_2...g_l)\\
    \theta=(\lambda,\beta)^T\\
    H=(\sum_i^{k个团}f,\sum_i^{k个团}g)^T\\
    P(Y|X)={1 \over z(\theta,x)}exp(\theta^T*H)
    $$
    
  

## CRF的inference

- 通过P(Y|X)求解P(Y=y|X)

- 学习算法,有监督

  - $$
    学习目标：\theta=(\lambda,\beta)^T\\
    argmax_\theta(\prod _i^np(y_i|x_i))
    $$