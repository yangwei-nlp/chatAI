from llm.prompt import PROMPTS
from llm.vllm_llm import async_query_openai
from llm.utils import pack_user_ass_to_openai_messages, split_string_by_multi_markers


async def process_single_chunk(chunk, context_base):
    content = chunk["content"]
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
    print(records)



async def extract_entities(chunks, ):
    context_base = dict(
        tuple_delimiter=PROMPTS["DEFAULT_TUPLE_DELIMITER"],
        record_delimiter=PROMPTS["DEFAULT_RECORD_DELIMITER"],
        completion_delimiter=PROMPTS["DEFAULT_COMPLETION_DELIMITER"],
        entity_types=",".join(PROMPTS["DEFAULT_ENTITY_TYPES"]),
    )

    for chunkId, chunkData in chunks.items():
        await process_single_chunk(chunkData, context_base)



if __name__ == "__main__":
    pass
