---
layout: post
author: liuxiangzheng
categories: study
---

**OCoR: An Overlapping-Aware Code Retriever** 

- 提出了句子之间的重叠问题
- CNN+ MultiHead Attention 
- 解决
  - 字符重叠--onehot
    - 每个word限制字母
  - 句子重叠矩阵
    - quire与code之间的单词相似矩阵
    - maxpools将矩阵转化成向量
    - 作为权重值
- ![1652405207704](C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1652405207704.png)

**Enriching query semantics for code search with reinforcement learning**

- 提出知识差距
- 想对quire句子进行扩展，丰富
- 使用强化学习进行扩展网络的学习策略

![1652405378271](C:\Users\lxz\AppData\Roaming\Typora\typora-user-images\1652405378271.png)

**Query Expansion Based on Crowd  Knowledge for Code Search **

- BM25指标
  - 计算quire与document的相似度
  - 

