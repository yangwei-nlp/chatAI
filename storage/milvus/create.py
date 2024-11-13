"""
创建Milvus的collection,

"""

from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)

from config.settings import *


def createCollection(collection_name):
    vector_dim = 768
    index_type = "IVF_FLAT"
    metric = "L2"
    nlist = 128

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),   # id自增
        FieldSchema(name="chunkId", dtype=DataType.VARCHAR, max_length=100),           # 文本块id
        FieldSchema(name="fileId", dtype=DataType.VARCHAR, max_length=100),            # 文件id
        FieldSchema(name="fileName", dtype=DataType.VARCHAR, max_length=100),          # 文件名
        FieldSchema(name="chunkText", dtype=DataType.VARCHAR, max_length=CHUNK_SIZE),  # 文本块的文本
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=vector_dim),    # 文本块的嵌入向量
    ]

    schema = CollectionSchema(fields, collection_name)
    collection = Collection(collection_name, schema, using=COLLECTION_ALIAS)

    index = {
        "index_type": index_type,
        "metric_type": metric,
        "params": {"nlist": nlist},
    }
    # collection.create_partition("1")
    collection.create_index("embedding", index)

    return collection


if __name__ == "__main__":
    connections.connect(
        alias=COLLECTION_ALIAS,
        host=MILVUS_HOST,
        port=MILVUS_PORT,
    )

    collection_name = "chunk_vdb"
    if utility.has_collection(collection_name, using=COLLECTION_ALIAS):
        collection = Collection(collection_name)
        collection.load()
    else:
        collection = createCollection(collection_name)
