"""
创建知识库的API，页面用户创建知识库=Milvus创建分区/partition
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

connections.connect(
    alias=COLLECTION_ALIAS,
    host=MILVUS_HOST,
    port=MILVUS_PORT,
)

collection = Collection(CHUNK_COLLECTION_NAME, using=COLLECTION_ALIAS)

# 创建partition
collection.create_partition(partition_name="test111112112314")



def new_partition():
    pass



def merge_partition():
    """"""
    pass
