import time
import asyncio
from openai import AsyncOpenAI
from config.settings import VLLM_HOST, VLLM_MODEL


aclient = AsyncOpenAI(
    base_url=VLLM_HOST,
    api_key="EMPTY"
)


async def async_query_openai(prompt, system_prompt=None, history_messages=[], **kwargs):
    max_tokens = kwargs.get("max_tokens", 512)
    temperature = kwargs.get("temperature", 0.5)
    top_p = kwargs.get("top_p", 0.9)

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.extend(history_messages)
    messages.append({"role": "user", "content": prompt})
    completion = await aclient.chat.completions.create(
        model=VLLM_MODEL,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )
    return completion.choices[0].message.content


async def main():
    query = "什么是卖飞？"
    system_prompt = """你是一个有用的助手，下面是你知道的信息，请根据以下信息回答问题，但请不要编造任何东西：也就是说刚刚我们讲的这个现象是构成你在过往市场当中不赚钱的，因为什么呢？因为你没有意识到都涨你的股票没涨它才是宝贝儿。所以在常态下你的判断是，人家都涨就他不涨他就是垃圾。结果你去追宝贝儿了，人家来宝贝你了，导致了什么？所谓你就是去弱追强了，结果强的人家不玩了，人家要玩弱的，是这样的吗？所以为什么很多大哥就经常感觉卖飞？

发言人1   18:20
所以我们一直在讲一个问题，就牛市的特产是卖飞，你为什么卖飞？原因就是这个。因为你不宝贝儿的，人家宝贝儿去了。所谓去弱留强你留的那个墙，人家都宝贝够了的，人家不饱和够了，他怎么能抢？是这道理吗？想清楚了吗？所以你们这帮渣男。那你说渣男，渣男炒股票不行是吧。

发言人1   19:13
有大哥就玩够了，突然来个老实人，对吧？事实是这样的，各位我不知道你我不知道各位真正经历过牛市的有没有？但凡你经历过的，你可以把那一年的你的交割单打出来，看看是不是这个结果。这玩意儿都不用猜的。你把你比如说你经历过15年，你看你15年的交割单是什么情况。看看不就知道了吗？这东西不用猜的。是不是特产，就是买水。
"""
    start_time = time.time()
    result = await async_query_openai(query, system_prompt)
    end_time = time.time()
    print(result)

    print(f"Total time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
