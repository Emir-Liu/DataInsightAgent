"""
路由配置
"""

import json
import logging

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from LLM.llm_operator import LLMOperator

logger = logging.getLogger("system")
router = APIRouter()

sys_build_task_tree = """
你是一个可以利用 Jupyter 环境 Python 编程的程序员。你可以利用提供的 API 来构建 任务节点图，最终生成代码并执行。

## API 介绍

下面是包含属性详细说明的 `TaskGraph` 类的 API 文档：

### 类：`TaskGraph`

此类用于管理网络搜索图的节点和边，并通过网络代理进行搜索。

#### 初始化方法

初始化 `TaskGraph` 实例。

**属性：**

- `nodes` (Dict[str, Dict[str, str]]): 存储图中所有节点的字典。每个节点由其名称索引，并包含内容、类型以及其他相关信息。
- `adjacency_list` (Dict[str, List[str]]): 存储图中所有节点之间连接关系的邻接表。每个节点由其名称索引，并包含一个相邻节点名称的列表。


#### 方法：`add_root_node`

添加原始问题作为根节点。
**参数：**

- `node_content` (str): 用户提出的问题。
- `node_name` (str, 可选): 节点名称，默认为 'root'。


#### 方法：`add_node`

添加搜索子问题节点并返回搜索结果。
**参数：

- `node_name` (str): 节点名称。
- `node_content` (str): 子问题内容。

**返回：**

- `str`: 返回任务结果。


#### 方法：`add_response_node`

当前获取的信息已经满足问题需求，添加回复节点。

**参数：**

- `node_name` (str, 可选): 节点名称，默认为 'response'。


#### 方法：`add_edge`

添加边。

**参数：**

- `start_node` (str): 起始节点名称。
- `end_node` (str): 结束节点名称。


#### 方法：`reset`

重置节点和边。


#### 方法：`node`

获取节点信息。

```python
def node(self, node_name: str) -> str
```

**参数：**

- `node_name` (str): 节点名称。

**返回：**

- `str`: 返回包含节点信息的字典，包含节点的内容、类型、思考过程（如果有）和前驱节点列表。

## 任务介绍
通过将一个问题拆分成能够子问题(没有关联的问题可以同步执行），每个节点应该是一个单一问题，即单个具体人、事、物、具体时间点、地点或知识点的问题，不是一个复合问题(比如某个时间段), 一步步构建任务图，最终回答问题。

## 注意事项

1. 注意，每个节点的内容必须单个问题，不要包含多个问题(比如同时问多个知识点的问题或者多个事物的比较加筛选，类似 A, B, C 有什么区别,那个价格在哪个区间 -> 分别查询)
2. 不要杜撰结果，要等待代码返回结果
3. 同样的问题不要重复提问，可以在已有问题的基础上继续提问
4. 添加 response 节点的时候，要单独添加，不要和其他节点一起添加，不能同时添加 response 节点和其他节点
5. 一次输出中，不要包含多个代码块，每次只能有一个代码块
6. 如下所示：
    ```python
    # 你的代码块
    ```
7. 最后一次回复应该是添加node_name为'response'的 response 节点，必须添加 response 节点，不要添加其他节点
8. 所有的节点都必须和根节点连接在一起
"""

@router.get("/", tags=["test"])
async def index():
    logger.info("访问api:/")
    ret_json = {"status": 0, "msg": "hello world"}
    return ret_json




class StreamOperator:
    def build_stream_json(
        self, type_json: str, value_json: str, status_json: str, id_json=str
    ) -> dict:
        """build stream json data

        Args:
            type (str): type in stream json data
            value (str): value in stream json data
            status (str): status in stream json data
            id_json (str): id in stream json data

        Returns:
            dict: return stream json data.
            {
                'code':200,
                'type':'',
                'value':'',
                'status':'',
                'id_json':''
            }
        """
        stream_json_data = {
            "code": 200,
            "type": type_json,
            "value": value_json,
            "status": status_json,
            "id": id_json,
        }
        return stream_json_data

    def build_json_str(
        self, type_json: str, value_json: str, status_json: str, id_json=str
    ) -> str:
        """build stream json data

        Args:
            type (str): type in stream json data
            value (str): value in stream json data
            status (str): status in stream json data
            id_json (str): id in stream json data

        Returns:
            str:
        """
        stream_json_data = self.build_stream_json(
            type_json=type_json,
            value_json=value_json,
            status_json=status_json,
            id_json=id_json,
        )
        return self.trans_json2str_in_stream(stream_json=stream_json_data)

    def trans_json2str_in_stream(self, stream_json: dict) -> str:
        """transform json to str in stream response

        Args:
            stream_json (dict): stream json
            {
                'code': 200,
                'type': '',
                'value': '',
                'status': '',
                'id_json':''
            }

        Returns:
            str: string stream response
        """
        stream_str = f"data:{json.dumps(stream_json, ensure_ascii=False)}\n\n"
        return stream_str

    def return_stream_response(
        self, type_json: str, value_json: str, status_json: str, id_json: str
    ):
        """return SSE response

        Args:
            type_json (str): type in json
            value_json (str): value in json
            status_json (str): status in json
            id_json (str): id in json

        Returns:
            _type_: streaming response
        """
        stream_json = self.build_stream_json(
            type_json=type_json,
            value_json=value_json,
            status_json=status_json,
            id_json=id_json,
        )
        stream_str = self.trans_json2str_in_stream(stream_json=stream_json)
        return StreamingResponse(stream_str, media_type="text/event-stream")


async def search_engine_qa_iter(content: str):
    question_id = ''
    yield StreamOperator().build_json_str(
        type_json="process", value_json='\n开始进行问答\n', status_json="ok", id_json=question_id
    )

    yield StreamOperator().build_json_str(
        type_json="process", value_json='\n开始进行任务分解\n', status_json="ok", id_json=question_id
    )


    import datetime

    current_time = datetime.datetime.now()

    # query = '2024年美国大选的结果'

    query = content

    print(f'用户提出的问题:{query}')
    # 任务分解
    
    # 思考
    print('将任务分解为若干个子任务：')
    prompt_task_ana = f'为了解决用户提出的问题，我们需要将复杂的问题进行分解，分解为若干个简单的问题，请一步一步思考。\n约束条件：1.如果用户提出的问题比较简单，可以直接回答，则复述用户的问题\n2.如果用户提出的问题比较复杂，则将问题分解，并且对各个子任务进行描述。\n用户问题:{query}\n当前时间：{current_time}'
    print(f'输入:{prompt_task_ana}')

    task_ana_ans = ''
    async for part in LLMOperator().chat_with_prompt_stream(content=prompt_task_ana):
        yield StreamOperator().build_json_str(
            type_json="response_part",
            value_json=part,
            status_json="ok",
            id_json=question_id,
        )
        task_ana_ans += part
        print(f'task_ana_ans:{task_ana_ans}')
    # task_ana_ans = LLMOperator().chat_with_prompt(content = prompt_task_ana)
    print(f'输出:{task_ana_ans}')


    yield StreamOperator().build_json_str(
        type_json="process", value_json='\n开始构造任务图\n', status_json="ok", id_json=question_id
    )
    # 构建图
    print('将子任务分解为任务图：')
    prompt_task_tree = f'{sys_build_task_tree}\n根据用户提出的问题{query},我们将其分解为如下的任务:\n{task_ana_ans}\n将任务使用python代码构造对应的任务节点'
    print(f'输入:{prompt_task_tree}')
    task_tree_ans = ''
    async for part in LLMOperator().chat_with_prompt_stream(content=prompt_task_tree):
        # yield StreamOperator().build_json_str(
        #     type_json="response_part",
        #     value_json=part,
        #     status_json="ok",
        #     id_json=question_id,
        # )
        task_tree_ans += part
        print(f'task_tree_ans:{task_tree_ans}')
    # task_tree_ans = LLMOperator().chat_with_prompt(content = prompt_task_tree)
    print(f'输出:{task_tree_ans}')


    yield StreamOperator().build_json_str(
        type_json="process", value_json='\n开始执行python代码\n', status_json="ok", id_json=question_id
    )
    import re
    pattern = r'```python(.*?)```' 
    matches = re.findall(pattern, task_tree_ans, re.DOTALL)
    print(f'matches:{matches}')
    python_cmd = matches[0]

    # 获取图中节点
    from demo_build_task_graph import TaskGraph, show_task_list
    from langchain_experimental.utilities import PythonREPL
    tool = PythonREPL()
    total_cmd_str = f'{TaskGraph}\n{python_cmd}\n{show_task_list}'
    # print(f'total_cmd_str:\n{total_cmd_str}')

    ans = tool.run(total_cmd_str)


    ans_list = ans.split('\n')
    filter_ans_list = []
    for tmp_ans_list in ans_list:
        if tmp_ans_list:
            filter_ans_list.append(tmp_ans_list)
    print(f'filter_ans_list:{filter_ans_list}')

    filter_ans_dict = {key:{} for key in filter_ans_list}



    # 遍历问题，进行问题的检索，挑选及整理
    for question, value in filter_ans_dict.items():
        print(f'开始解决子问题：{question}')
        yield StreamOperator().build_json_str(
            type_json="process", value_json=f'\n开始解决子问题：{question}\n', status_json="ok", id_json=question_id
        )
        from dotenv import load_dotenv

        load_dotenv()

        from langchain_community.tools.bing_search import BingSearchResults
        from langchain_community.utilities import BingSearchAPIWrapper

        api_wrapper = BingSearchAPIWrapper()
        tool = BingSearchResults(api_wrapper=api_wrapper)

        ans = tool.invoke({"query": question})

        print(f'search ans:{ans}')

        # 对问题和答案进行初步汇总
        prompt_part_sum = f'为了解决用户的问题：{query},\n我们首先需要解决：{question},\n下面是这个问题的结果：{ans}\n, 对这个子任务的结果进行汇总'

        part_task_sum_ans = ''
        async for part in LLMOperator().chat_with_prompt_stream(content=prompt_part_sum):
            yield StreamOperator().build_json_str(
                type_json="response_part",
                value_json=part,
                status_json="ok",
                id_json=question_id,
            )
            part_task_sum_ans += part
            print(f'part_task_sum_ans:{part_task_sum_ans}')
        # part_task_sum_ans = LLMOperator().chat_with_prompt(content = prompt_part_sum)
        print(f'输出:{part_task_sum_ans}')
        filter_ans_dict[question]['ans'] = part_task_sum_ans

    # 对之前内容进行汇总
    total_ana_ans = ''
    for question, value in filter_ans_dict.items():
        part_total_ana_ans = f"对于子任务{question},得到下面的结果：\n{value['ans']}\n"
        total_ana_ans += part_total_ana_ans

    total_ans = f'为了解决用户的问题：{query}\n我们按照下面的步骤进行分析:\n{total_ana_ans}\n根据上面的问题和步骤，分析最终的结果。\n约束条件：\n1.最终的结果需要包含分析的各个步骤，分点回答\n2.最终的结果需要有详细的说明和分析内容'
    yield StreamOperator().build_json_str(
        type_json="process",
        value_json='\n开始对答案进行汇总\n',
        status_json="ok",
        id_json=question_id,
    )
    total_sum_ans = ''
    async for part in LLMOperator().chat_with_prompt_stream(content=total_ans):
        yield StreamOperator().build_json_str(
            type_json="response_part",
            value_json=part,
            status_json="ok",
            id_json=question_id,
        )
        total_sum_ans += part
        print(f'total_sum_ans:{total_sum_ans}')
    # total_sum_ans = LLMOperator().chat_with_prompt(content = total_ans)
    print(f'最终的分析结果:{total_sum_ans}')

from typing import List

@router.get("/search_engine_qa", tags=["search engine qa"])
async def search_engine_qa_stream(content: str, history: List[dict], ):
    logger.info("访问api:/")
    r = search_engine_qa_iter(
        content=content,
    )

    return StreamingResponse(r, media_type="text/event-stream")