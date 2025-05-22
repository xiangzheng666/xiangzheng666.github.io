---
categories: [nlp]
tags: [RNN,LSTM]
---
# RNN

- to用近似定理 (Universal approximation theorem)
  如果一个前馈神经网络具有线性输出层和至少一层隐藏层，只要给予网络足够数量的神经元，便可以实现以足够高精度来逼近任意一个在 ℝn 的紧子集 (Compact subset) 上的连续函数

- 为什么使用RNN：FNN的输入固定,RN共享U，W，V参数

- 模型：

  - $$
    h^{(t)}=\sigma \Big( Uh^{(t-1)}+Wx^{(t)} \Big)\\y^{(t)}=softmax\Big(Vh^{(t)}\Big)
    $$

- 但是由于序列本身，如果序列长度太长，会导致梯度消失，爆炸的问题

# LSTM

- LSTM可以理解为一个特征提取器（遗忘门选择过去的特征输入到cell，输入门选择输入的特征加入到cell，输出门结合遗忘门与输入门，cell输出）
- 输入门：
  - ![1664091221911](https://github.com/xiangzheng666/picx-images-hosting/raw/master/1664091221911.3d50tipvwk.webp)

- 遗忘门
  - ![1664091264391](https://github.com/xiangzheng666/picx-images-hosting/raw/master/1664091264391.1e8u36kdl3.webp)

- 输入与遗忘门的特征加入cell
  - ![1664091306923](https://github.com/xiangzheng666/picx-images-hosting/raw/master/1664091306923.1e8u36kdl4.webp)

- 输出门
  - ![1664091330201](https://github.com/xiangzheng666/picx-images-hosting/raw/master/1664091330201.5tr98fwrt6.webp)

- lstm的变体
  - gru
    - ![1664091470390](https://github.com/xiangzheng666/picx-images-hosting/raw/master/1664091470390.1e8u36kdl7.webp)
  - LSTM: A Search Space Odyssey
  - 