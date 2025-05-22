---
categories: [nlp]
tags: [seq2seq,attention_mask]
---
# seq2seq

- 计算方式
  -  在decode阶段的每一个rnn的y是一个可以使用交叉熵衡量损失的结果
  - 为了不让每次只出现最大可能的结果，有防止计算量太大在greed与exhaustic中使用了beam search
  - beam search使用每次选择所有概率中最大的beam size个候选集
- attention
  - 对于encoder中的每个rnn的输出与当前decoder输出计算分数，归一化处理，再根据归一化处理得到的概率分别与对应的encoder输出相乘在求和得到了具有注意力机制的上下文向量表示，将其与decode输出的隐状态一起输出y
  - <img src="./img/1664095569365.png" style="zoom:40%;">

- attention_mask

  - 使用并行操作时需要对sentence进行padding操作

  - 在计算attention的score时，可以对padding出的word设置极小的score

  - ```
    atten_make=tf.math.logical_not(tf.math.equal(inputs, 0))
    a=tf.where(atten_make, tf.squeeze(score), -1e6)
    ```