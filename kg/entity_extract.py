import re
from collections import defaultdict

from llm.prompt import PROMPTS
from llm.vllm_llm import async_query_openai
from llm.utils import pack_user_ass_to_openai_messages, split_string_by_multi_markers, clean_str, is_float_regex





async def _handle_single_entity_extraction(
    record_attributes: list[str],
    chunk_key: str,
):
    """处理大模型回答中的实体数据"""
    if len(record_attributes) < 4 or record_attributes[0] != '"entity"':
        return None
    # add this record as a node in the G
    entity_name = clean_str(record_attributes[1].upper())
    if not entity_name.strip():
        return None
    entity_type = clean_str(record_attributes[2].upper())
    entity_description = clean_str(record_attributes[3])
    entity_source_id = chunk_key
    return dict(
        entity_name=entity_name,
        entity_type=entity_type,
        description=entity_description,
        source_id=entity_source_id,
    )


async def _handle_single_relationship_extraction(
    record_attributes: list[str],
    chunk_key: str,
):
    """处理大模型回答中的关系数据"""
    if len(record_attributes) < 5 or record_attributes[0] != '"relationship"':
        return None
    # add this record as edge
    source = clean_str(record_attributes[1].upper())
    target = clean_str(record_attributes[2].upper())
    edge_description = clean_str(record_attributes[3])

    edge_keywords = clean_str(record_attributes[4])
    edge_source_id = chunk_key
    weight = (
        float(record_attributes[-1]) if is_float_regex(record_attributes[-1]) else 1.0
    )
    return dict(
        src_id=source,
        tgt_id=target,
        weight=weight,
        description=edge_description,
        keywords=edge_keywords,
        source_id=edge_source_id,
    )


async def process_single_chunk(chunkId, chunkData, context_base):
    content = chunkData["content"]
    entity_extract_prompt = PROMPTS["entity_extraction"]
    hint_prompt = entity_extract_prompt.format(**context_base, input_text=content)
    continue_prompt = PROMPTS["entiti_continue_extraction"]
    if_loop_prompt = PROMPTS["entiti_if_loop_extraction"]

    final_result = await async_query_openai(hint_prompt)

    history = pack_user_ass_to_openai_messages(hint_prompt, final_result)
    entity_extract_max_gleaning = 1
    for now_glean_index in range(entity_extract_max_gleaning):  # 再次尝试次数
        glean_result = await async_query_openai(continue_prompt, history_messages=history)

        history += pack_user_ass_to_openai_messages(continue_prompt, glean_result)
        final_result += glean_result
        if now_glean_index == entity_extract_max_gleaning - 1:
            break

        if_loop_result: str = await async_query_openai(
            if_loop_prompt, history_messages=history
        )
        if_loop_result = if_loop_result.strip().strip('"').strip("'").lower()
        if if_loop_result != "yes":
            break

    records = split_string_by_multi_markers(
        final_result,
        [context_base["record_delimiter"], context_base["completion_delimiter"]],
    )
    maybe_nodes = defaultdict(list)
    maybe_edges = defaultdict(list)
    for record in records:
        record = re.search(r"\((.*)\)", record)
        if record is None:
            continue
        record = record.group(1)
        record_attributes = split_string_by_multi_markers(
            record, [context_base["tuple_delimiter"]]
        )
        if_entities = await _handle_single_entity_extraction(
            record_attributes, chunkId
        )
        if if_entities is not None:
            maybe_nodes[if_entities["entity_name"]].append(if_entities)
            continue

        if_relation = await _handle_single_relationship_extraction(
            record_attributes, chunkId
        )
        if if_relation is not None:
            maybe_edges[(if_relation["src_id"], if_relation["tgt_id"])].append(
                if_relation
            )
    return dict(maybe_nodes), dict(maybe_edges)


async def extract_entities(chunks, ):
    context_base = dict(
        tuple_delimiter=PROMPTS["DEFAULT_TUPLE_DELIMITER"],
        record_delimiter=PROMPTS["DEFAULT_RECORD_DELIMITER"],
        completion_delimiter=PROMPTS["DEFAULT_COMPLETION_DELIMITER"],
        entity_types=",".join(PROMPTS["DEFAULT_ENTITY_TYPES"]),
    )

    results = []
    for chunkId, chunkData in chunks.items():
        # TODO 并发处理
        nodes, edges = await process_single_chunk(chunkId, chunkData, context_base)
        results.append((nodes, edges))
    maybe_nodes = defaultdict(list)
    maybe_edges = defaultdict(list)
    for m_nodes, m_edges in results:
        for k, v in m_nodes.items():
            maybe_nodes[k].extend(v)
        for k, v in m_edges.items():
            maybe_edges[tuple(sorted(k))].extend(v)

    for k, v in maybe_nodes.items():
        pass




if __name__ == "__main__":
    pass
