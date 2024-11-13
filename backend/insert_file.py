"""
读取本地文件然后嵌入向量并存储到数据库
"""
import os.path

from chunk_text.chunk_by_length import make_inserting_chunks, embedding_chunks
from chunk_text.embedding import ollama_embedding
from loader.ocr_pdf_loader import read_pdf
from insert.chunk_vdb_insert import insert_vdb
from storage import chunkCollection

from fastapi import APIRouter

insert_router = APIRouter()


def chunk_and_insert(pdf_path):
    """
    解析pdf、分块、嵌入、写入db
    """
    # 文档解析
    pdf_path = '/home/qilixin/桌面/普通高中教科书·历史必修 中外历史纲要（上）.pdf'

    if os.path.exists('/home/qilixin/yangwei/teach/chatAI/loader/历史.txt'):
        with open('/home/qilixin/yangwei/teach/chatAI/loader/历史.txt', 'r') as f:
            all_texts = f.read()
    else:
        all_texts = read_pdf(pdf_path)

    # 切割文本
    chunks = make_inserting_chunks(all_texts)

    # 嵌入向量
    embedding_data = embedding_chunks(chunks)

    # 写入向量数据库
    insert_vdb(embedding_data)




def search(query):
    # 要进行KNN搜索的查询向量
    query_vector = ollama_embedding([query], embed_model="nomic-embed-text", host="http://localhost:11434")

    # 指定要搜索的分区名称
    partition_names = ["your_partition_name"]

    # 执行KNN搜索
    results = chunkCollection.search(
        data=query_vector,  # 查询数据
        anns_field="embedding",  # 向量字段名
        param={"metric_type": "L2", "params": {"nprobe": 10}},  # 搜索参数
        limit=10,  # 返回前10个结果
        # partition_names=partition_names  # 指定分区
        output_fields=['chunkId', 'fileId', 'fileName', 'chunkText'],
    )

    # 打印结果
    for i, result in enumerate(results[0]):
        chunkText = result.get('chunkText')
        fileName = result.get('fileName')
        print(f'idx: {i}, chunkText: {chunkText}, fileName: {fileName}')


# chunk_and_insert('xxx')
search("朱元璋")
