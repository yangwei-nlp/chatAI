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


collection_dict = {}
for collection_name in COLLECTION_NAME_LIST:
    collection = Collection(collection_name, using=COLLECTION_ALIAS)
    collection.load()
    collection_dict[collection_name] = collection

