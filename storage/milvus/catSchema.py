"""
查看Milvus的collection的schema
"""

from pymilvus import utility, connections, Collection

from config.settings import *


connections.connect(
    alias="test",
    host="localhost",
    port=19530,
)

for collName in utility.list_collections(using="test"):
    print(f"########################## [{collName}] ##########################")
    collection = Collection(collName, using="test")
    print(collection)
