"""
将向量存入Milvus
"""
from storage import collection_dict
from config.settings import MILVUS_BATCH_SIZE

def insert_vdb(all_chunk_info):
    """
    注意，这里面有个坑，Milvus字段长度是按照字节编码长度，500个汉字可能长度达到2000多length，所以后续需要微调
    TODO, 存储时指定分区
    """
    chunk_list = all_chunk_info['data']
    collectionName = all_chunk_info['collectionName']
    partitionName = all_chunk_info['partitionName']
    collection = collection_dict.get(collectionName)

    batch_data = []
    for chunk in chunk_list:
        item = {
            "chunkId": chunk["__id__"],
            "chunkText": chunk["content"],
            "embedding": chunk["__vector__"].tolist(),
            "fileId": chunk["full_doc_id"],
            "fileName": chunk["file_path"],
            "fileCreateDate": chunk["file_create_time"],
        }
        batch_data.append(item)

        if len(batch_data) == MILVUS_BATCH_SIZE:
            try:
                collection.insert(batch_data, partitionName=partitionName)
                batch_data = []
            except Exception as e:
                print(e)

    if len(batch_data) > 0:
        try:
            collection.insert(batch_data, partitionName=partitionName)
        except Exception as e:
            print(e)


