from llm.query import naive_query
from fastapi import APIRouter, File, UploadFile
from chunk_text.embedding import ollama_embedding
from storage import collection_dict

rag_router = APIRouter()


@rag_router.post("/naive_rag")
async def naive_rag(query, collectionName):
    try:
        # 要进行KNN搜索的查询向量
        query_vector = ollama_embedding([query], embed_model="bge-m3", host="http://localhost:11434")

        # 指定要搜索的分区名称
        partition_names = ["your_partition_name"]

        # 执行KNN搜索
        collection = collection_dict.get(collectionName)
        results = collection.search(
            data=query_vector,                                              # 查询数据
            anns_field="embedding",                                         # 向量字段名
            param={"metric_type": "IP", "params": {"nprobe": 10}},          # 搜索参数
            limit=10,                                                       # 返回前10个结果
            # partition_names=partition_names                               # 指定分区
            output_fields=['chunkId', 'fileId', 'fileName', 'chunkText'],   # 返回字段
        )

        assert len(results[0]) == 10

        # 整理召回的文档
        rag_chunks = []
        for i, result in enumerate(results[0]):
            chunkText = result.get('chunkText')
            fileName = result.get('fileName')
            # print(f'idx: {i}, chunkText: {chunkText}, fileName: {fileName}')
            # print("\n\n\n#######################################################################\n\n\n")
            rag_chunks.append({
                "content": chunkText,
                "fileName": fileName
            })

        # 送入大模型生成回答
        response = await naive_query(query, rag_chunks)

        return {'code': 200, 'message': 'success', 'data': response}

    except Exception as e:
        return {'code': 400, 'message': f'Error in search, msg: {e}', 'data': None}



@rag_router.post("/global_rag")
async def global_rag(query):
    try:
        pass
    except Exception as e:
        return {'code': 400, 'message': f'Error in search, msg: {e}', 'data': None}
