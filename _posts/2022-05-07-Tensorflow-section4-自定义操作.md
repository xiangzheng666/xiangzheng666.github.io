---
categories: [Tensorflow]
tags: [自定义]
---
# Tensorflow自定义

- ### 自定义损失

  -  函数形式

    - ```python
      def custom_mean_squared_error(y_true, y_pred):    
        return tf.math.reduce_mean(tf.square(y_true - y_pred))
      
      model.compile(optimizer=keras.optimizers.Adam(),loss=custom_mean_squared_error)
      ```

  - 定义子类

    - ```python
      class CustomMSE(keras.losses.Loss):    
          def __init__(self, regularization_factor=0.1, name="custom_mse"):   
              super().__init__(name=name)        
              self.regularization_factor = regularization_factor    
          def call(self, y_true, y_pred):        
              mse = tf.math.reduce_mean(tf.square(y_true - y_pred))        
              reg = tf.math.reduce_mean(tf.square(0.5 - y_pred))        
              return mse + reg * self.regularization_factor
      
          
      #__init__(self)：接受要在调用损失函数期间传递的参数
      #call(self, y_true, y_pred)：使用目标 (y_true) 和模型预测 (y_pred) 来计算模型的损失
      ```

- ### 自定义指标

  - 子类化

    - ```python
      class CategoricalTruePositives(keras.metrics.Metric):    
          def __init__(self, name="categorical_true_positives", **kwargs):        
              super(CategoricalTruePositives, self).__init__(name=name, **kwargs)     
              self.true_positives = self.add_weight(name="ctp", initializer="zeros")    def update_state(self, y_true, y_pred, sample_weight=None):        
                  y_pred = tf.reshape(tf.argmax(y_pred, axis=1), shape=(-1, 1))      
                  values = tf.cast(y_true, "int32") == tf.cast(y_pred, "int32")       
                  values = tf.cast(values, "float32")        
                  if sample_weight is not None:            
                      sample_weight = tf.cast(sample_weight, "float32")            
                      values = tf.multiply(values, sample_weight)        
                      self.true_positives.assign_add(tf.reduce_sum(values))    
          def result(self):        
              return self.true_positives    
          def reset_states(self):        
              # The state of the metric will be reset at the start of each epoch.     
              self.true_positives.assign(0.0)
              
              
      #__init__(self)，您将在其中为指标创建状态变量。
      #update_state(self, y_true, y_pred, sample_weight=None)，使用目标 y_true 和模型预测 y_pred 更新状态变量。
      #result(self)，使用状态变量来计算最终结果。
      #reset_states(self)，用于重新初始化指标的状态。
      ```