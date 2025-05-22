---
categories: [Pytorch]
tags: [数据处理]
---
# Pytorch数据处理

- ## 数据读入

  - torch.utils.data
  
  1. 构建DataSet(data,label)
  
     ```python
     #可以自定义,会自动中断__getitem__
     class MyDataset(Dataset):
         def __init__(self, data_dir, info_csv, image_list, transform=None):       
         def __getitem__(self, index):
         def __len__(self):
     ```
  
  2. 构建DataLoader(set,batch_szie...)
  
     ```python
     #自动读取，
     train_data = datasets.ImageFolder(train_path, transform=data_transform)
     torch.utils.data.DataLoader(val_data, batch_size=batch_size, num_workers=4, shuffle=False)
     ```
  
- ## 数据增强

  - torchvision.transforms
  - 裁剪
    - transforms.RandomCrop(num,padding)
      - 将原始图片pading后，随机裁剪num*num的大小图片
    - transforms.CenterCrop(num)
      - 中心裁剪num*num的大小图片
    - transforms.FiveCrop(size)
      - 返回一个4Dtensor，上下左右中间的size*size的图片  5张
    - transforms.TenCrop(size)
      - 返回一个4Dtensor，上下左右中间的size*size的图片,然后翻转  10张
  - 旋转
    - transforms.RandomHorizontalFlip(P)
      - 依概率翻转水平
    - transforms.RandomVerticalFlip(P)
      - 依概率翻转垂直
  - 图片变换
    - transforms.resize(size=[])
      - resize操作
    - transforms.Normalize(mean,std)
      - 标准化
    - transforms.ToTensor()
      - 转tensor并且归一化
    - transforms.ToPILImage(model)
      - 转PIL
  - Transforms的操作
    - transforms.RandomChoice(transorms)
      - 随机选择一个transforms操作
    - transforms.RadnomApply(transorms,p)
      - 以概率执行操作
    - transforms.RandomRoder(transforms)
      - 顺序打乱
    - transforms.Compose( [transforms ])
      - 顺序连接

  