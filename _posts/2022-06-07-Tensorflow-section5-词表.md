---
categories: [Tensorflow]
tags: [词表]
---
# tensorflow创建词表

```python
#1.构建层，一般用于构建dataset中，使用map函数
#tf.Tensor(b'First Citizen:', shape=(), dtype=string)
#tf.Tensor(b'Before we proceed any further, hear me speak.', shape=(), dtype=string)
layer=tf.keras.layers.TextVectorization(
    standardize=过滤器函数,
    max_tokens=vocab_size,
    output_mode='int',
    output_sequence_length=sequence_length)
#2.
layer.adapt(data)
layer.get_vocabulary()
#['', '[UNK]', 'the', 'and', 'to'...]
#3.
layer(data)
#tf.Tensor([ 83 225  0  0  0  0  0  0  0  0], #shape=(10,), dtype=int64)
#tf.Tensor([ 147   32 1605  130  1  124  26  555  0 #0], shape=(10,), dtype=int64)
#...
```

# gensim过滤前1000个词频

```python
dictionary = corpora.Dictionary(texts)
#[['First', 'Citizen:'],
# ['Before', 'we', 'proceed', 'any', 'further,', 'hear', 'me', 'speak.'],
# ['All:'],
# ['Speak,', 'speak.'],..]
diction={j:i for i,j in dictionary.token2id.items()}
# 0: 'Citizen:',
# 1: 'First',
# 2: 'Before',
# 3: 'any',
# 4: 'further,',
# 5: 'hear',
# 6: 'me',
# 7: 'proceed',
fre_w=[i[0] for i in sorted(dictionary.dfs.items(),key=lambda x:x[1],reverse=True)]
#[0, 1, 10, 9, 8, 20, 2, 7, 3, 4, 5, 6, 11, 12, 14, 13,..]按照词频排序的字典索引
fre_w=[diction[i] for i in fre_w]
#['Citizen:', 'First', 'All:', 'we', 'speak.', 'to', 'Before', 'proceed', 'any','further,','hear', 'me', 'Speak,', 'You', 'are'..]按照词频排序的字典单词
fre_w=fre_w[:10000]
#获得到频率前1000的单词
```

# gensim过滤词频小于

```python
dictionary = corpora.Dictionary(texts)
#[['First', 'Citizen:'],
# ['Before', 'we', 'proceed', 'any', 'further,', 'hear', 'me', 'speak.'],
# ['All:'],
# ['Speak,', 'speak.'],..]
dicts={j:i for i,j in dictionary.token2id.items()}
# 0: 'Citizen:',
# 1: 'First',
# 2: 'Before',
# 3: 'any',
# 4: 'further,',
# 5: 'hear',
# 6: 'me',
# 7: 'proceed',
once_ids = [tokenid for tokenid, docfreq in dicts.dfs.items() if docfreq <= 1]
dicts.filter_tokens(once_ids)
```

# tensorflow的制作skipgrane语料

```python
#[1, 2, 3, 4, 5, 1, 6, 7]
positive_skip_grams, _ = tf.keras.preprocessing.sequence.skipgrams(
      example_sequence,
      vocabulary_size=vocab_size,
      window_size=window_size,
      negative_samples=0
)
```

### [接力学习tensorflow的文本处理api](https://tensorflow.google.cn/versions/r2.3/api_docs/python/tf/keras/preprocessing/text)