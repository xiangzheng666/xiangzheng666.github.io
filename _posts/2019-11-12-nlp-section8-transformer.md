---
categories: [nlp]
tags: [transformer,self attention]
---
# transformer

- self-attention

  - 不同于attenstion使用输入X序列与当前Y输出的attention，self-attenstion主要是使用输入X序列直间的attention表示Y输出序列

  - $$
    Y_i=\sum_jw_{i,j}*X_i\quad w_{i,j}为X_i与X_j的相似度计算内积称为self-attention\\使用q,k,v表示：
    \\w_{i,j}=x_i*x_j==>w_{i,j}=Q(x_i)*K(x_j)==>w_{i,j}={Q(x_i)*K(x_j) \over \sqrt{(dx)}}
    \\Y_i=\sum_jw_{i,j}*X_i==>\sum_jw_{i,j}*V(X_i)
    $$

    

  - 这种y的计算方法与输入x序列的顺序无关，这是不合理的

  - Multi-head attention

    - 将输入x向量分成多份，每份做self-attention,最后concat成y
    - <img src="./img/1664874951606.png" style="zoom:50%;">
  
- transformer block
  
  - <img src="./img/1664874999639.png" style="zoom:50%;">
  
- poistion_encoding

  - 计数
    - pose=1，2，3，4.....T
    -  如果 T很大那最后一个字的编码就会比第一个位置的编码大太多，带来的问题就是和字嵌入合并以后难免会出现特征在数值上的倾斜和干扰字嵌入，对模型可能有一定的干扰。  
  - 计数+归一化
    - psoe=pose/T-1
    -  但是不同长度的位置编码的步长是不同的，在较短的文本中相邻的两个字的位置编码的差异会和长文本中的相邻两个个字的位置编码差异一致
  -  有界周期函数 
    - sin(pose/超参数)
    - 但是超参数不好调整，太大，太小有上面问题
  - 有界周期函数映射高维空间
    - 将位置编码为一个embeding的维度，每个维度可以使用不同函数
    -  这使得每一维度上都包含了一定的位置信息，而各个位置字符的位置编码又各不相同。 
  
- mask操作

  - loss_mask
  - decoder_self-attention_mask
