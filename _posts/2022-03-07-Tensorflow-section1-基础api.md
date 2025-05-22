---
categories: [Tensorflow]
tags: [基础知识]
---
# Tensorflow基础api

- ## 创建Tensor

  - tf.convert_to_tensor(data)
  - tf.zeros(shape)
  - tf.ones()
  - tf.zeros_like()
  - tf.ones_like()
  - tf.full(shape,value)
  - 
  - tf.random.normal(mean.std)
  - tf.random.uniform(v)
  - tf.truncated_normal()去除小概率的正态分布
  - tf.random.shuffle()
  - 
  - tf.constant()
  - tf.range()
  - tf.linspace

- ## Tensor属性

  - tensor.device()
  - tensor.numpy()
  - tensor.ndim()
  - tensor.shape
  - tf.is_tensor()
  - tf.Variable()    name  trainable
  - tf.cast(data,type)
  - **不可直接赋值**

- ## Tensor操作

  - 索引

    - tf.gather(data,dim,index)  收集指定维度上的index数据
    - tf.boolean_mask(data,mask,axis)

  - 维度变换

    - tf.reshape
    - tf.transpose(a,[])

    - tf.expand_dims(data,axis) axis>0 前，axis<0 后

    - tf.squzee(a,axis)
    - tf.title(a,x),[shape]==>[x,shape]
    - tf.broadcast_to(b,[])

  - 合并

    - tf.concat([a,b],axis)
    - tf.stack([a,b],axis) 合并增加axis一维
    - tf.unstack(data,axis) 拆开axis维
    - tf.split(data,num_orsize_split,axis)

  - 统计

    - tf.norm() 范数
    - tf.reduce_mean()平均值
    - tf.reduce_min()
    - tf.reduce_max() 
    - tf.reduce_sum() 求和
    - tf.reduce_square()  平方
    - tf.reduce_argmax() 
    - tf.reduce_argmin()
    - tf.reduce_equeal()
    - tf.reduce_unique() 不重复的index

  - 排序

    - tf.sort(a,direction="DESCENDING")
    - tf.argsort(a,d)
    - tf.math_top_k(a,2)

  - 限制范围

    - tf.clip_by_value(a,k,k)
    - tf.clip_by_norm(a,范数)等比缩放
    - tf.clip_by_global_norm
    - tf.maximum()
    - tf.minimum()

  - tf.one_hot(d,depth)

    