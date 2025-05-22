---
categories: [Machine Learing]
tags: [PCA]
---
# PCA

-  对数据集投影到向量之后的方差最大化

- 推导

  - $$
    \mu^T:投影向量/矩阵\quad;
    \mu^T*x_i：数据集x_i投影之后的向量\\
    投影之后的数据集的均值表示：{1\over n}\sum_{i=1}^{n}u^T*x_i=0;(X之前会进行均值化)\\
    投影之后的数据集的方差表示：{1\over n}\sum_{i=1}^{n}(u^T*x_i-0)^2\\
    方差表示：{1\over n}\sum_{i=1}^{n}u^T*x_i*x_i^T*u^=u^T*{1\over n}\sum_{i=1}^{n}x_i*x_i^T*u\\
    方差表示：{1\over n}*\mu^T*S*\mu\quad S=(X^T*X)协方差矩阵
    $$

  - 目标函数

    - $$
      Max\quad \mu^T*S*\mu\\
      st:||\mu||_2^2=1
      $$

    - 由拉格朗日乘子可得

    - $$
      S*\mu=\lambda*\mu
      $$

    - 可得

    - $$
      Max\quad \mu^T*S*\mu=\mu^T*\lambda*\mu=Max\quad \lambda
      $$

    - 求解S的最大特征值对于的特征向量