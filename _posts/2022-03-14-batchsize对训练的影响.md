---
layout: post
author: liuxiangzheng
categories: study
---

# Batchsize对训练影响

- 主要认为是loss值的区别
- 不同Batchsize有着不同loss，[batchsize,x]*[wx,outy]=[batchsize个y]得到结果与label相减，在对wx进行求导，不同loss值对导数有着不同影响，导致batchsize对训练产生影响
- 太大 会让loss对部分精度降低，会增大epoch数量
- 太小 会让每一个epoch边长
- 综合太大与太小，会达到一个最优batchsize的值