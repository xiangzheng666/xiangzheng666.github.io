---
categories: [Pytorch]
tags: [模型操作]
---
# Pytorch模型操作

- ## 迁移学习

  - from torchvision import models

  - 修改模型的组件层

    - model.layer=model

  - 冻结模型

    - ```python
      for i in model.parameters():
      	i.requires_grad=False
      ```

- # 模型保存与读取

  - ```
    # 保存整个模型
    torch.save(model, save_dir)
    # 保存模型权重
    torch.save(model.state_dict, save_dir)
    ```

  - ```
    os.environ['CUDA_VISIBLE_DEVICES'] = '0' # 如果是多卡改成类似0,1,2
    model = model.cuda()  # 单卡
    model = model.cuda()  # 单卡
    model = torch.nn.DataParallel(model).cuda()  # 多卡
    ```

- ## GPU

  -   device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")  
  - ().to(device)
  -   os.environ['CUDA_VISIBLE_DEVICES']="0"  