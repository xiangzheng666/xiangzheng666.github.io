---
categories: [Pytorch]
tags: [环境搭建]
---
# Pytorch环境搭建
- pip换源
	- pip.ini文件
	```
	[global]
	index-url = http://pypi.douban.com/simple
	[install]
	use-mirrors =true
	mirrors =http://pypi.douban.com/simple/
	trusted-host =pypi.douban.com
	```
- conda换源
	
	- .condarc文件
```
	channels:
	  - defaults
	show_channel_urls: true
	default_channels:
	  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
	  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
	  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
	custom_channels:
	  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
	  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
	  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
	  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
	  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
	  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud`
```

- 根据gpu版本安装最新
```
conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
```
- 使用gpu

  - ```
    import os
    os.environ["CUDA_VISIBLE_DEVICE"]=0,1,2
    
    device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")
    ```

- 坑：
> 在cuda与cudnn正确安装下，如果还是提升ddl not found，可以修改ddl的名称