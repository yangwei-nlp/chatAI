import os
import pickle

import pandas as pd

from config.settings import *

from pymilvus import connections, Collection


# 初始化milvus
connections.connect(
    alias=COLLECTION_ALIAS,
    host=MILVUS_HOST,
    port=MILVUS_PORT
)

# 实体集合
chunkCollection = Collection(CHUNK_COLLECTION_NAME, using=COLLECTION_ALIAS)
chunkCollection.load()

