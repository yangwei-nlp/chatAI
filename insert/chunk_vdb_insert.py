"""
将向量存入Milvus
"""
from storage import chunkCollection
from config.settings import MILVUS_BATCH_SIZE

def insert_vdb(chunk_list):
    """
    注意，这里面有个坑，Milvus字段长度是按照字节编码长度，500个汉字可能长度达到2000多length，所以后续需要微调
    TODO, 存储时指定分区
    """
    batch_data = []
    for chunk in chunk_list:
        item = {
            "chunkId": chunk["__id__"],
            "fileId": chunk["full_doc_id"],
            "fileName": "temp_is_none",
            "chunkText": chunk["content"],
            "embedding": chunk["__vector__"].tolist(),
        }
        batch_data.append(item)

        if len(batch_data) == MILVUS_BATCH_SIZE:
            try:
                chunkCollection.insert(batch_data)
                batch_data = []
            except Exception as e:
                print(e)

    if len(batch_data) > 0:
        try:
            chunkCollection.insert(batch_data)
        except Exception as e:
            print(e)


