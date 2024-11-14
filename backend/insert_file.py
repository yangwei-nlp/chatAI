"""
读取本地文件然后嵌入向量并存储到数据库
"""
import os.path

from chunk_text.chunk_by_length import make_inserting_chunks, embedding_chunks
from chunk_text.embedding import ollama_embedding
from loader.ocr_pdf_loader import read_pdf
from insert.chunk_vdb_insert import insert_vdb
from storage import chunkCollection

from fastapi import APIRouter, File, UploadFile

insert_router = APIRouter()


def chunk_func():
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



@insert_router.post("/insert_file")
def chunk_and_insert(doc: UploadFile = File(None)):
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





if __name__ == "__main__":
    # chunk_and_insert('xxx')
    # search("朱元璋")
    chunk_func()
