"""
各种query方法
"""
from llm.generate import ollama_model_complete
from llm.prompt import PROMPTS
from llm.utils import truncate_list_by_token_size


async def naive_query(query_text, chunks):
    """
    朴素RAG的思路
    """
    maybe_trun_chunks = truncate_list_by_token_size(
        chunks,
        key=lambda x: x["content"],
        max_token_size=4000,
    )
    section = "--New Chunk--\n".join([c["content"] for c in maybe_trun_chunks])

    sys_prompt_temp = PROMPTS["naive_rag_response"]
    sys_prompt = sys_prompt_temp.format(
        content_data=section, response_type="Multiple Paragraphs"
    )
    response = await ollama_model_complete(
        query_text,
        system_prompt=sys_prompt,
    )

    if len(response) > len(sys_prompt):
        response = (
            response[len(sys_prompt) :]
            .replace(sys_prompt, "")
            .replace("user", "")
            .replace("model", "")
            .replace(query_text, "")
            .replace("<system>", "")
            .replace("</system>", "")
            .strip()
        )

    return response



async def global_query(query_text, chunks):
    """
    全局RAG的思路
    """
    pass
