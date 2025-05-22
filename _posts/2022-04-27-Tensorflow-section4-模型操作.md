---
categories: [Tensorflow]
tags: [模型操作]
---
# Tensorflow模型操作

- ## GPU设置

  - ```python
os.environ['CUDA_VISIBLE_DEVICES']="0，1，2"
    gpus=tf.config.list_physical_device("GPU")
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)按需使用
        tf.config.experimental.set_visible_devices(devices=gpus[0:2], device_type='GPU')
    #限制使用的gpu
    gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
    tf.config.experimental.set_virtual_device_configuration(
            gpus[0],
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024)])
    
    ```
  
- ## 网络冻结

  - 在定义层的时候使用 **trainable=False** 
  -  使用tf.stop_gradient() 函数冻结
  - 在计算梯度的时候选择tape.gradient

- # 保存，读取
  - 参数保存

    - model.save_weight(filename)
    - model.load_weight(filename)

  - 保存所有

    - model.save(filename)
    - model=tf.keras.models.load_model()

  - 断点续训

    - ```
      checkpoint_path = './checkpoint/train'
      ckpt = tf.train.Checkpoint(transformer=transformer,optimizer=optimizer)
      # ckpt管理器
      ckpt_manager = tf.train.CheckpointManager(ckpt, checkpoint_path, max_to_keep=3)
      
      tf.train.Checkpoint（）训练的模型，优化器
      tf.train.CheckpointManager()要保存的参数，保存的路径，保存的模型数量。
      
      #重新加载模型
      checkpoint = tf.train.Checkpoint(transformer=transformer, optimizer=optimizer)
      checkpoint.restore(tf.train.latest_checkpoint(checkpoint_path1))
      ```

      