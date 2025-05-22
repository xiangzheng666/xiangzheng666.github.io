---
categories: [nlp]
tags: [最大期望,隐马尔可夫]
---
# 	最大期望算法（EM）

- 是一种对含有隐变量模型估计的方法

- 算法思路

  - $$
    argmax_\theta log(p(Y|\theta))==>argmax_\theta log\sum_zp(Y,Z|\theta)
    $$

  - 按照最大似然估计的算法求解使得当前的Y的出现概率最大的\theta类似

  - 但是最大似然估计对于多个模型（不可观测）（即隐变量）无法估计

  - 将\theta对Y的概率分布变成\theta对Y与Z的联合概率分布的形式描述

  - 变形目标公式

  - $$
    argmax_\theta log\sum_zp(Y,Z|\theta)==>argmax_\theta log\sum_z p(Y|Z,\theta)*p(Z|\theta)
    $$

  - 此时Z是无法观测的，并且该公式没有解析解

  - EM算法首先随机初始化\theta，获取当前参数下，Z的分布，然后通过当前Z的分布更新下一步的\theta

  - 如何根据当前Z分布更新\theta，换句话说：如何根据当前Z分布使得下一步的\theta使得上式的值更大,我们将其相减后求取关于\theta的最大化即可

  - $$
    argmax_\theta log\sum_z p(Y|Z,\theta)*p(Z|\theta)-log(p(Y|\theta_i))
    $$

  - 利用jensn不等式获取其下届并且化简得到

  - $$
    \theta_{i+1}=argmax_\theta\sum_ZP(Z|Y,\theta_i)*logP(Y,Z|\theta))\\P(Z|Y,\theta_i)\quad为上一步迭代所获得的Z分布\\也可以写成\quad E_Z[logP(Y|Z,\theta),\theta_i]
    $$

  - 这个就是期望形式

  - 其的收敛性也是利用jesen不等式推导的。。。。

# 隐马尔可夫模型（HMM）

- 基本形式

  - 矩阵 (A,B,pai)

- 假设

  - 任意时刻当前的状态只与前一个时刻的状态有关（状态转移矩阵A）
  - 当前观测只与当前状态有关（观测矩阵B）

- 理解

  - $$
    学习目标：P(Z)*P(X|Z)=P(X,Z)
    $$

    

- pai是初始状态概率向量

- ## HMM的三个基本问题

  - 概率计算问题：一直模型参数(A,B,pai)计算观测序列的发生概率；
    - 直接计算法：穷举所有可能状态序列然后求和
    - 前向算法：通过递推的求得前向概率，最后求和
    - 后向算法：与前向类似
  - 学习问题：已知观测序列，估计模型参数使得P(o|(A,B,pai))最大
    - 监督算法：统计问题
    - 非监督：EM算法求解
  - 预测问题：已知模型参数与观测序列，求出对应的最大的状态序列P(I|O)
    - 近似算法：每个时刻最有可能的状态序列，但是可能状态转移矩阵中有可能为0
    
    - 维特比算法：
    
      - 先找出时刻t前的路径中最大概率路径（删除其余边）
    
      - 递推至最后时刻
    
      - 然后回溯找到最大路径节点
    
      - 维特比算法实现
    
      - ```python
        import numpy as np
        A=np.array([[0.5,0.2,0.3],[0.3,0.5,0.2],[0.2,0.3,0.5]])
        B=np.array([[0.5,0.5],[0.4,0.6],[0.7,0.3]])
        c=np.array([0.2,0.4,0.4])
        
        p=[0,1,0]
        
        score=[]
        index=[]
        score.append(c*B[:,p[0]].tolist())
        for i in range(len(p)-1):
            best=[]
            ind=[]
            for j in range(3):
                tmp=np.array(score[i]*A[:,j]*B[j,p[i+1]])
                best.append(tmp[np.argmax(tmp)])
                ind.append(np.argmax(tmp))
            score.append(best)
            index.append(ind)
        
        m=[]
        s=np.argmax(score[-1])
        m.append(s)
        for i in range(len(p)-1):
            s=index[len(p)-1-i-1][s]
            m.append(s)
        m.reverse()
        print(m)
        ```
    
        