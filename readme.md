# README

## devices 支持（工作中测试过的）

huawei ce系列、s系列、Eudemon系列

## 环境搭建

### 在线环境搭建

```
pip install -r requirements.txt -i https://pypi.douban.com/simple
```

### 离线环境搭建

+ 离线下载 pip 包

```
pip download -r requirements.txt -d c:\pip 
```

+ 离线安装 pip 包

```
pip install --no-index --find-links=c:\pip -r requirements.txt
```

## 执行程序

```
python network_check.py
```