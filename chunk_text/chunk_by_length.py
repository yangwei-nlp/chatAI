"""
将文本按照 token长度=固定长度 分块，分块会添加重叠文本
"""
import numpy as np

from chunk_text.embedding import ollama_embedding

from chunk_text.lightrag.utils import (
    logger,
    clean_str,
    compute_mdhash_id,
    decode_tokens_by_tiktoken,
    encode_string_by_tiktoken,
    is_float_regex,
    list_of_list_to_csv,
    pack_user_ass_to_openai_messages,
    split_string_by_multi_markers,
    truncate_list_by_token_size,
    process_combine_contexts,
)

from config.settings import *


def chunking_by_token_size(
    content: str, overlap_token_size=128, max_token_size=1024, tiktoken_model="gpt-4o"
):
    """将纯文本按token的总长度进行分块"""
    tokens = encode_string_by_tiktoken(content, model_name=tiktoken_model)
    results = []
    for index, start in enumerate(
        range(0, len(tokens), max_token_size - overlap_token_size)
    ):
        chunk_content = decode_tokens_by_tiktoken(
            tokens[start : start + max_token_size], model_name=tiktoken_model
        )
        results.append(
            {
                "tokens": min(max_token_size, len(tokens) - start),
                "content": chunk_content.strip(),
                "chunk_order_index": index,
            }
        )
    return results


def make_inserting_chunks(content, ):
    """准备需要存储的文本块数据"""
    chunks = chunking_by_token_size(content, overlap_token_size=100, max_token_size=500, tiktoken_model="gpt-4o")
    new_docs = {
        compute_mdhash_id(content.strip(), prefix="doc-"): {"content": content.strip()}
    }
    # TODO 重复md5的doc无法存储
    inserting_chunks = {}
    for doc_key, doc in new_docs.items():
        for dp in chunks:
            key = compute_mdhash_id(dp["content"], prefix="chunk-")
            value = {
                **dp,
                "full_doc_id": doc_key,
            }
            inserting_chunks[key] = value

    # TODO 单个doc中重复md5的chunk无法存储

    return inserting_chunks


def embedding_chunks(chunks):
    """将文本chunk嵌入为向量"""
    list_data = []
    for chunk_id, chunk_data in chunks.items():
        item = {
            "__id__": chunk_id,
            "content": chunk_data["content"],
            "tokens": chunk_data["tokens"],
            "chunk_order_index": chunk_data["chunk_order_index"],
            "full_doc_id": chunk_data["full_doc_id"],
            "__vector__": None,
        }
        list_data.append(item)

    contents = [v["content"] for v in list_data]
    batches = [
        contents[i: i + EMBEDDING_BATCH_SIZE]
        for i in range(0, len(contents), EMBEDDING_BATCH_SIZE)
    ]
    embeddings_list = [ollama_embedding(batch, embed_model="nomic-embed-text", host="http://localhost:11434")
                       for batch in batches]
    embeddings = np.concatenate(embeddings_list)

    for idx, chunk_item in enumerate(list_data):
        chunk_item["__vector__"] = embeddings[idx]
    # results = self._client.upsert(datas=list_data)
    return list_data


if __name__ == "__main__":
    with open('/home/qilixin/yangwei/teach/chatAI/loader/历史.txt', 'r') as f:
        content = f.read()

    chunks = make_inserting_chunks(content)

    embedding_chunks(chunks)
