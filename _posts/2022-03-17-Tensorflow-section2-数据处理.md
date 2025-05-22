---
categories: [Tensorflow]
tags: [数据处理]
---
# Tensorflow数据处理

- ## 图片

  - 读入数据

  - ```python
    tf.io.read_file(img_path)
    
    #<tf.Tensor: shape=(), dtype=string,numpy=b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00...
    ```

  -  解码为图像 tensor 

  - ```python
    tf.image.decode_image(img)
    
    #(212, 320, 3)
    #<dtype: 'uint8'>
    
    tf.image.resize(img_tensor, [192, 192])
    ```

  - 构建一个 tf.data.Dataset

  - ```python
    tf.data.Dataset.from_tensor_slices(all_image_paths)
    
    #<TensorSliceDataset element_spec=TensorSpec(shape=(), dtype=tf.string, name=None)>
    
    map()处理
    
    tf.data.Dataset.zip((slices, slices))
    
    # <ZipDataset element_spec=(TensorSpec(shape=(192, 192, 3), dtype=tf.float32, name=None), TensorSpec(shape=(), dtype=tf.int64, name=None))>
    
    batch()
    shuffle()
    take()
    reqeat()
    ```

- ## CSV文件

  - 读入文件

  - ```python
    tf.data.experimental.make_csv_dataset(file_path,batch_size)
    '''
    	column_names=CSV_COLUMNS 列名
    	select_columns = columns_to_use, 
    '''
    ```

  - 预处理

  - 很差不搞

- ## numpy保存文件

  - ```python
    tf.keras.utils.get_file(path)
    ```

  - panda使用value属性

- ##  TFRecord 格式 

-  TFRecord 格式是一种用于存储二进制记录序列的简单格式。 

- ```python
  message=tf.train.Example(
  	features=tf.train.Features(
      	feature={
              a:tf.train.Feature(tf.train.BytesList(value=[value]))
              ....
          }
      )
  )
  
  
  message.SerializeToString()
  #序列化
  
  tf.train.Example.FromString(serialized_message)
  
  #将序列化后的解析
      features {
        feature {
          key: "feature0"
          value {
            int64_list {
              value: 0
            }
          }
        }
        feature {
          key: "feature1"
          value {
            int64_list {
              value: 1
            }
          }
        }
          ....
      }
      
  #然后使用
  tf.data.Dataset.from_tensor_slice((....))
  #可以通过map函数将所有样本序列化
  #也可以定义一个生成器generator
  tf.data.Dataset.from_generator(generator,output_type=tf.string,output_shape=())
  
  #保存这个dataset
  with tf.data.TFRecordWriter(filename) as f:
      f.write(dataset)
  
  #加载这个dataset
  tf.data.TFRecordDataset(filename)
  #此时这个dataset中的每一个都是序列化之后的tf.train.Example，要解析成原本的数据
  #定义处理单个样本的函数
  
  feature_description = {
      'a': tf.io.FixedLenFeature([], tf.int64, default_value=0),
      ....
  }
  tf.io.parse_single_example(example,feature_description)
  
  #然后map即可
  
  FixedLenFeature与VarLenFeature
  ```

- ## 文本

- ```python
  tf.data.TextLineDataset()
  #以行间隔
  
  ```