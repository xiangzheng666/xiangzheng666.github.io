---
categories: [nlp]
tags: [词向量]
---


# 词向量学习

- **skipgrame语言模型与CBOW类似**

- 在skipgrame中使用单词为主题，预测单词的上下文，而CBOW中使用context预测中心词

- 假设相邻的单词相似度最高

- 使用一种无监督的方法训练(dense)词向量

- 定义window_size使用单词对context的单词进行预测

  - 数据集采用自身语料库中的**上下文环境(可以加入权重)**进行训练的其中context作为真样本，并采样负样本

  - 目标最大化

  $$
  \Bigg(\prod_{word\in(vocab)}{P(word-context/word)}\Bigg)
  $$

  $$
  ---P(context/word)采用context向量之间的内积占全部vocab的比例
  $$

  - 改进

- $$
  \Bigg(\prod_{context}{P(1，context；word)}*\prod_{not-context}{P(0，not-context/word)}\Bigg)
  $$


$$
---P(1，context；word)采用context向量之间的内积在经过singmoid函数
$$

  - 这样做避免了求和，降低了计算量
- 注意，当一个单词的词频大大超于其他词频，经过训练之后的模型会对该单词产生过拟合现象，相似词频小的会产生欠拟合。
  - 应用
    - 推荐系统（根据相似度推荐）
    - ....

- 矩阵分解

  - 通过统计词频矩阵分解词向量

  - 全局视角