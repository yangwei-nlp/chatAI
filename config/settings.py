CHUNK_SIZE = 4096
COLLECTION_ALIAS = "chunk_collection"

COLLECTION_NAME_LIST = [
    "chunk_vdb",
    "toujidana",
    "xiaosipindao",
    "jiaoganglaile",
]

EMBEDDING_BATCH_SIZE = 16

META_FIELDS = [

]

# milvus主机信息
MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"
MILVUS_BATCH_SIZE = 100


# ollama信息
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:7b-instruct"

# vllm信息
VLLM_HOST = "http://120.220.247.120:8010/v1"
VLLM_MODEL = "/nvme1/code/yangwei/Qwen/Qwen2___5-72B-Instruct/"
