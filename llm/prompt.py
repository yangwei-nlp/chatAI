GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["概念", "人物", "金融名词", "经济学名词", "时间", "事件"]

PROMPTS["entity_extraction"] = """-目标-
给定可能与此活动相关的文本文档和实体类型列表，从文本中识别这些类型的所有实体以及已识别实体之间的所有关系。

-步骤-
1. 识别所有实体。对于每个已识别的实体，提取以下信息：
- entity_name: 实体名称
- entity_type: 以下实体类型之一：[{entity_types}]
- entity_description: 实体属性和活动的综合描述
将每个实体格式化为 ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>

2. 从步骤1中确定的实体中，确定彼此“明显相关”的所有对（source_entity, target_entity）。
对于每对相关实体，提取如下信息：
- source_entity: 源实体的名称，与步骤1中识别的相同
- target_entity: 目标实体的名称，与步骤1中识别的名称相同
- relationship_description: 对于源实体和目标实体之间存在关联的原因的解释
- relationship_strength: 表示源实体和目标实体之间关系强度的数字分数
- relationship_keywords: 一个或多个高级关键词，这些关键词概括了关系的总体性质，侧重于概念或主题而不是具体细节
将每个关系格式化为 ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. 找出概括整篇文章的主要概念、主题或主题的高级关键词。这些应该抓住文档中呈现的总体思想。
将内容级关键字格式化为 ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. 以中文返回输出，作为步骤1和2中标识的所有实体和关系的单个列表。使用**{record_delimiter}**作为列表分隔符。

5. 完成后，输出{completion_delimiter}

-例子-
例子1:

实体类型: [概念, 人物, 金融名词, 经济学名词, 时间, 事件]
文本: 大哥聊了说为什么每次事件出来之后，先都是题材先涨，然后就大盘再涨？大哥你这个总结，我觉得可能就有点问题。为什么叫总结就有点问题呢？什么叫每次出来事儿之后先涨题材再涨大盘，难道每一次都是这样的吗？其实大哥表达的意思很清楚，你看我们看到无论是这个什么样的利好的驱动，对吧？这种利好驱动之后，我们往往看到一些可能小市值品种先涨，然后是大市值品种先涨，是不是这个意思吧？刚刚大哥是不是说的这个意思，或者说我不知道其他的大哥有没有这样的感受，其他的大哥你们怎么看，对吧？
总觉得说一般的事件往往会引发一些小市值品种先涨。实际上你这个先后的这个结论就错了，为什么讲错了呢？或者叫你表达错了。事实上我们看就是事件驱动某一个产业性的利好，它不是说单有题材或者纤长，而是说小市值的涨幅要相较于大市值品种的涨幅大一些，没有先后，是这样的表达吗？
各位，所以刚刚大哥说的那为什么小市值先涨没有先后？同样的事件，同样的影响，同样的反应，只不过它的幅度体现上就不一样。这里头就有一个核心的因素，核心的因素有几点，一定要注意一个问题。
小市值品种我们讲它有两个特征。一本来它的市值就相对比较小。二小市值品种大部分就是你去看它上市时间不是特别的长，对吧？那跟一些权重相比较来讲，它可能上市时间相对比较短，就是它实际流通的股数又相对会比较少。所以在这种背景之下，同样的事件，同样的影响，就即便小市值品种它分配到的一些资金相对较少，但是它对应流通市值就小。
所以在这种背景之下，就我们看到的大部分的事件驱动性的一些？上涨你看到的大部分都是什么小市值涨的幅度要比大市值？这是必然的。所以你看为什么我们很多个人投资者就更喜欢做一些小市值的，为什么更喜欢做一些这种？对吧，就比如说我同一个行业，我就选择一个小市值，就是图快或者是幅度大。你为什么这么做，你还不清楚吗？是不是这道理？所以这个没有先后，我们讲事件驱动背景之下没有先后，只不过说你看起来幅度大小不一样罢了。
但是这里头也有一个问题，也有一个什么问题？你说的这种现象也不普遍。为什么叫你说的这种现象也不普遍呢？就是你可以看看什么。比如说前一段时间我们跟各位汇报的时候，聊到了一个问题，就是你看科创板对吧？在涨的这个过程当中，你会发现尤其是芯片这个行业。
你看在涨的这个过程当中，是不是头部的芯片企业涨得更好，而相对我们讲，小市值的芯片企业反而反应比较弱一些，是这样的吗？各位还记得前一段时间这个芯片对吧？就芯片这条产业链你看涨的都是哪些？中心这个叫什么来着？韩寒季捂还是5G是吧？
对，所以你看就是你这个观察是我们很多投资者都是这样的，我们习惯性的根据自己的感觉就下结论。所以这种时候你这种感觉就错。然后你再基于这种感觉去分析或者是判断，那就更错了。所以从感觉或者说从你在提出这个问题的时候，你先要评价一下你这个问题到底有没有？有偏差，有偏差你就不用再往下分析了，对吧？
不是所有的都是大市值不行，小市值行的问题。在我们大部分投资者概念里头，就是大市值品种就是涨得慢。但是各位就拿现在就拿A股现在的情况上来讲，各位就拿A股现在的情况来讲，就是你现在觉得你现在还有这种大市值品种，就是涨得慢的这个印象或者是这个看法吗？

输出:
("entity"{tuple_delimiter}"小市值品种"{tuple_delimiter}"概念"{tuple_delimiter}"市值较低的股票，通常波动较大，涨幅相对显著。"){record_delimiter}
("entity"{tuple_delimiter}"大市值品种"{tuple_delimiter}"概念"{tuple_delimiter}"市值较高的股票，通常波动较小，涨幅较平稳。"){record_delimiter}
("entity"{tuple_delimiter}"事件驱动"{tuple_delimiter}"概念"{tuple_delimiter}"特定事件对市场或行业的触发作用，可能引发股票波动。"){record_delimiter}
("entity"{tuple_delimiter}"利好驱动"{tuple_delimiter}"概念"{tuple_delimiter}"利好消息推动市场或个股上涨的现象。"){record_delimiter}
("entity"{tuple_delimiter}"涨幅"{tuple_delimiter}"概念"{tuple_delimiter}"股票或指数价格在一定时间内的增长幅度。"){record_delimiter}
("entity"{tuple_delimiter}"核心因素"{tuple_delimiter}"概念"{tuple_delimiter}"对现象或问题产生关键影响的原因。"){record_delimiter}
("entity"{tuple_delimiter}"流通市值"{tuple_delimiter}"概念"{tuple_delimiter}"某股票在市场中可自由交易的股份价值总和。"){record_delimiter}
("entity"{tuple_delimiter}"芯片产业链"{tuple_delimiter}"概念"{tuple_delimiter}"芯片行业上下游的相关企业和生态系统。"){record_delimiter}
("entity"{tuple_delimiter}"市值"{tuple_delimiter}"金融名词"{tuple_delimiter}"公司股票在市场上的总价值，等于股价乘以总股本。"){record_delimiter}
("entity"{tuple_delimiter}"权重"{tuple_delimiter}"金融名词"{tuple_delimiter}"某股票在指数或投资组合中的影响力。"){record_delimiter}
("entity"{tuple_delimiter}"流通股数"{tuple_delimiter}"金融名词"{tuple_delimiter}"股票市场中可自由买卖的股份数量。"){record_delimiter}
("entity"{tuple_delimiter}"科创板"{tuple_delimiter}"金融名词"{tuple_delimiter}"中国资本市场中针对科技创新企业设立的板块。"){record_delimiter}
("entity"{tuple_delimiter}"产业性利好"{tuple_delimiter}"经济学名词"{tuple_delimiter}"对某行业整体有积极促进作用的政策、事件或趋势。"){record_delimiter}
("relationship"{tuple_delimiter}"小市值品种"{tuple_delimiter}"大市值品种"{tuple_delimiter}"小市值品种与大市值品种在市场表现上有所不同，小市值品种涨幅通常大于大市值品种，但两者涨跌幅没有明确的先后顺序。"{tuple_delimiter}"小市值, 大市值, 涨幅对比, 先后顺序, 市场表现"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"事件驱动"{tuple_delimiter}"利好驱动"{tuple_delimiter}"事件驱动往往伴随着利好驱动，这种利好消息可能影响市场整体，也可能集中作用于某些行业或股票类型。"{tuple_delimiter}"事件驱动, 利好消息, 市场反应, 股票波动, 影响范围"{tuple_delimiter}){record_delimiter}
("relationship"{tuple_delimiter}"核心因素"{tuple_delimiter}"涨幅"{tuple_delimiter}"涨幅的大小受核心因素的影响，例如市值规模、流通股数等。"{tuple_delimiter}"核心因素, 涨幅差异, 资金分配, 市值规模, 投资偏好"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"流通市值"{tuple_delimiter}"投资者概念"{tuple_delimiter}"投资者通常倾向于选择流通市值小的品种，因为这些品种在事件驱动下涨幅较大。"{tuple_delimiter}"流通市值, 投资者偏好, 市场流动性, 投资选择, 股票偏好"{tuple_delimiter}){record_delimiter}
("relationship"{tuple_delimiter}"芯片产业链"{tuple_delimiter}"科创板"{tuple_delimiter}"科创板中芯片产业链企业的表现，可能体现为头部企业与小市值企业的不同涨幅。"{tuple_delimiter}"芯片产业链, 科创板, 行业表现, 头部企业, 市场影响"{tuple_delimiter}){record_delimiter}
("relationship"{tuple_delimiter}"A股"{tuple_delimiter}"权重"{tuple_delimiter}"A股市场中，权重较大的大市值股票可能涨幅较慢，但具有稳定性。"{tuple_delimiter}"A股, 权重, 市场波动, 股票影响力, 投资策略"{tuple_delimiter}){record_delimiter}
("content_keywords"{tuple_delimiter}"小市值品种, 大市值品种, 事件驱动, 芯片产业链, 科创板, 涨幅"){completion_delimiter}

-真实数据-
实体类型: {entity_types}
文本: {input_text}
输出:
"""

PROMPTS[
    "summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.

#######
-Data-
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS[
    "entiti_continue_extraction"
] = """在上次提取中很多实体或实体间的关系被遗漏了，请在下面添加并以相同格式返回"""

PROMPTS[
    "entiti_if_loop_extraction"
] = """好像还是有一些实体或实体间的关系被遗漏了，请回答"是"或"否"来告知我是否还有实体或实体间的关系需要被添加。"""

PROMPTS["fail_response"] = "不好意思，我没有能力回答这个问题。"

PROMPTS["rag_response"] = """---Role---

You are a helpful assistant responding to questions about data in the tables provided.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

---Target response length and format---

{response_type}

---Data tables---

{context_data}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.
"""

PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query.

---Goal---

Given the query, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.

---Instructions---

- Output the keywords in JSON format.
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes.
  - "low_level_keywords" for specific entities or details.

######################
-Examples-
######################
Example 1:

Query: "How does international trade influence global economic stability?"
################
Output:
{{
  "high_level_keywords": ["International trade", "Global economic stability", "Economic impact"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Currency exchange", "Imports", "Exports"]
}}
#############################
Example 2:

Query: "What are the environmental consequences of deforestation on biodiversity?"
################
Output:
{{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity loss"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem"]
}}
#############################
Example 3:

Query: "What is the role of education in reducing poverty?"
################
Output:
{{
  "high_level_keywords": ["Education", "Poverty reduction", "Socioeconomic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality"]
}}
#############################
-Real Data-
######################
Query: {query}
######################
Output:

"""

PROMPTS["naive_rag_response"] = """你是一个乐于助人的助手，下面是你知道的信息:
{content_data}
---
如果提供的知识不包含足够的信息来提供答案，就直接说"已有信息无法让我做出回答。"，千万不要编造任何东西。
---目标响应的长度和格式---
{response_type}
"""
