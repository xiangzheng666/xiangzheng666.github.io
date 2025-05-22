---
categories: [Tensorflow]
tags: [模型训练]
---
# Tensorflow模型训练

- ## 组件库

  ```
tf.keras.layers.
  ```
  
- ## 搭建网络

  - Sequential
  
    - ```
    import tensorflow as tf
      net = tf.keras.Sequential(
              tf.keras.layers.Linear(256),
              tf.keras.layers.ReLU(),
              tf.keras.layers.Linear(10), 
              )
      ```
    
  - 自定义层
  
    - ```python
      class layer(tf.keras.layer.Layer):
      	def __init__(self,input):
      		super(layer,self).__init__()
      		#self.w=self.add_variable(input)
      	def __call__(self,training,input):
      		..
      		return out
      ```
    
  - 自定义网络
  
    - ```python
    class layer(tf.keras.Model):
      	def __init__(self,input):
    		super(layer,self).__init__()
      		
      	def __call__(self,training,input):
      		..
      		return out
      ```
    
  - 函数式API
  
    -  创建一个输入节点 
  
    - ```
      inputs = keras.Input(shape=(784,))
      ```
  
    -  在此 `inputs` 对象上调用层，在层计算图中创建新的节点 
  
    - ```python
      dense = layers.Dense(64, activation="relu")
      x = dense(inputs)
      x = layers.Dense(64, activation="relu")(x)
      outputs = layers.Dense(10)(x)
      ```
  
    -  指定模型的输入和输出来创建 `Model` 
  
    - ```python
      model = keras.Model(inputs=inputs, outputs=outputs, name="mnist_model")
      ```
  
    -  模型可以包含子模型（因为模型就像层一样） 
  
    - 可以有多输入，输出
  
    - ```python
      model = keras.Model(    inputs=[title_input, body_input, tags_input],    outputs=[priority_pred, department_pred],)
      ```
  
    -  编译此模型时，可以为每个输出分配不同的损失 
  
    - ```python
      model.compile(    optimizer=keras.optimizers.RMSprop(1e-3),    loss=[        keras.losses.BinaryCrossentropy(from_logits=True),        keras.losses.CategoricalCrossentropy(from_logits=True),    ],    loss_weights=[1.0, 0.2],)
      ```
  
- ## 模型训练

  - 自定义

    - ```python
      #定义优化器，模型，损失函数
      optimizer=tf.keras.optimizer.Adm(lr)
      model
      loss
      #存储梯度
      with tf.GradientTape() as tape:
          out=model(input)
          loss=loss(out,label)
      grad =  tape.gradient(loss,model.trainable_variables)
      optimizer.apply_gradients(zip(grad,model.trainable_variables))    
      ```

      

  - 内置方法

    - compile()` 方法：指定损失、指标和优化器

    - ```python
      model.compile(
          optimizer=keras.optimizers.RMSprop(learning_rate=1e-3),
          loss=keras.losses.SparseCategoricalCrossentropy(),
          metrics=[keras.metrics.SparseCategoricalAccuracy()],
      )
      model.fit(x, y, batch_size=64, epochs=1)
      ```

- 优化器：
  - `SGD()`（有或没有动量）
  - `RMSprop()`
  - `Adam()`
  - 等等

- 损失：
  - `MeanSquaredError()`
  - `KLDivergence()`
  - `CosineSimilarity()`
  - 等等

- 指标：
  - `AUC()`
  - `Precision()`
  - `Recall()`
  - 等等