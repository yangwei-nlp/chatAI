""" 查看集合包含的向量数目 """

from pymilvus import (
    connections,
    utility,
    Collection,
)


if __name__ == "__main__":
    connections.connect(
        alias="new_platform",
        host="localhost",
        port="19530",
    )
    collection_name = "entityCollection"
    if utility.has_collection(collection_name, using="new_platform"):
        collection = Collection(collection_name, using="new_platform")
        collection.load()
        print(f"向量数目: {collection.num_entities}")
    else:
        print("Milvus没有该集合")
