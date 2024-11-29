"""
读取本地文件然后嵌入向量并存储到数据库
"""
import asyncio
import os.path

from chunk_text.chunk_by_length import make_inserting_chunks, embedding_chunks
from chunk_text.embedding import ollama_embedding
from kg.entity_extract import extract_entities
from loader.docx_loader import read_docx
from loader.ocr_pdf_loader import read_pdf
from insert.chunk_vdb_insert import insert_vdb
from storage import collection

from fastapi import APIRouter, File, UploadFile

insert_router = APIRouter()


async def chunk_func(fileInfos, milvusInfos):
    """
    解析pdf、分块、嵌入、写入db
    TODO 针对文件去过滤
    """
    try:
        file_path, all_text, file_create_date = fileInfos['file_path'], fileInfos['all_text'], fileInfos['file_create_date']
        collectionName, partitionName = milvusInfos['collectionName'], milvusInfos['partitionName']

        # 切割文本
        chunks = make_inserting_chunks(all_text, file_path, file_create_date)

        # 抽取实体和关系
        entities, relations = await extract_entities(chunks)

        # 嵌入向量
        embedding_data = embedding_chunks(chunks)

        # 写入向量数据库

        all_datas = {
            'collectionName': collectionName,
            'partitionName': partitionName,
            'data': embedding_data,
        }

        insert_vdb(all_datas)
        del fileInfos['all_text']
        print(f"存储成功，信息：{fileInfos}, {milvusInfos}")

    except Exception as e:
        del fileInfos['all_text']
        print(f"存储失败，信息：{fileInfos}, {milvusInfos}，失败原因：{e}")



def parse_file_path(file_path):
    """
    解析文件路径，得到文件名、文件类型、文件创建时间
    """
    collectionName, fileCreateDate, partitionName = None, None, None
    if '投机大拿' in file_path:
        collectionName = 'toujidana'
    elif '小司频道' in file_path:
        collectionName = 'xiaosipindao'
    elif '焦刚来了' in file_path:
        collectionName = 'jiaoganglaile'

    fileCreateDate = file_path[1:11]
    partitionName = file_path[1:8]

    if collectionName is None:
        print()
    return collectionName, fileCreateDate, partitionName



async def chunk_local_dir(dir):
    """
    读取文件夹下的所有文件
    得到 集合、分区
    """
    # TODO 去重
    for dir_path in os.listdir(dir):
        if os.path.isdir(dir + dir_path):
            for file_path in os.listdir(dir + dir_path):
                if file_path.endswith('.docx') or file_path.endswith('.doc'):
                    collectionName, fileCreateDate, partitionName = parse_file_path(file_path)
                    if collectionName is None:
                        continue

                    doc_path = dir + dir_path + '/' + file_path
                    all_texts = read_docx(doc_path)

                    fileInfos = {
                        "file_path": doc_path,
                        "all_text": all_texts,
                        "file_create_date": fileCreateDate,
                    }
                    milvusInfos = {
                        "collectionName": collectionName,
                        "partitionName": partitionName,
                    }
                    await chunk_func(fileInfos, milvusInfos)
                else:
                    continue


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

    # collectionName, fileCreateDate, partitionName = 'chunk_vdb', None, None
    #
    # # 文档解析
    # file_path = '/home/qilixin/桌面/普通高中教科书·历史必修 中外历史纲要（上）.pdf'
    #
    # if os.path.exists('/home/qilixin/yangwei/teach/chatAI/loader/历史.txt'):
    #     with open('/home/qilixin/yangwei/teach/chatAI/loader/历史.txt', 'r') as f:
    #         all_texts = f.read()
    # else:
    #     all_texts = read_pdf(file_path)
    #
    # fileInfos = {
    #     "file_path": file_path,
    #     "all_text": all_texts,
    #     "file_create_date": 'none',
    # }
    # milvusInfos = {
    #     "collectionName": collectionName,
    #     "partitionName": partitionName,
    # }
    # chunk_func(fileInfos, milvusInfos)

    dir = "/mnt/data/抖音股市直播/"
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(chunk_local_dir(dir))
    loop.close()

