import ollama
from llm.base import BaseKVStorage
from llm.utils import compute_args_hash


async def ollama_model_if_cache(
    model, prompt, system_prompt=None, history_messages=[], **kwargs
) -> str:
    kwargs.pop("max_tokens", None)
    kwargs.pop("response_format", None)
    host = kwargs.pop("host", None)
    timeout = kwargs.pop("timeout", None)

    ollama_client = ollama.AsyncClient(host=host, timeout=timeout)
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    hashing_kv: BaseKVStorage = kwargs.pop("hashing_kv", None)
    messages.extend(history_messages)
    messages.append({"role": "user", "content": prompt})
    if hashing_kv is not None:
        args_hash = compute_args_hash(model, messages)
        if_cache_return = await hashing_kv.get_by_id(args_hash)
        if if_cache_return is not None:
            return if_cache_return["return"]

    response = await ollama_client.chat(model=model, messages=messages, **kwargs)

    result = response["message"]["content"]

    if hashing_kv is not None:
        await hashing_kv.upsert({args_hash: {"return": result, "model": model}})

    return result



async def ollama_model_complete(
    prompt, system_prompt=None, history_messages=[], **kwargs
) -> str:
    # model_name = kwargs["hashing_kv"].global_config["llm_model_name"]
    model_name = 'qwen2.5:7b-instruct'
    return await ollama_model_if_cache(
        model_name,
        prompt,
        system_prompt=system_prompt,
        history_messages=history_messages,
        **kwargs,
    )
