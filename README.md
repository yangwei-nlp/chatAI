# README

本项目基于知识库搭建专属领域内的聊天机器人系统，主要使用到RAG技术来减少大模型的幻觉。


## 步骤

1、启动Milvus服务和MySQL服务

```shell
cd chatAI
docker-compose up -d
```


2、启动OCR服务


```shell
cd qanything_kernel/dependent_server/ocr_serve
python ocr_server.py
```


3、启动词向量服务

```shell
cd qanything_kernel/connector/embedding
python embedding.py
```


4、启动前端服务

注意，需要提前安装前端环境

```shell
cd front_end
cnpm run dev
```



依赖安装与下载：

```shell
conda activate xxx
pip install -U magic-pdf[full] --extra-index-url https://wheels.myhloli.com
pip install huggingface_hub
wget https://github.com/opendatalab/MinerU/raw/master/scripts/download_models_hf.py -O download_models_hf.py
python download_models_hf.py
```

