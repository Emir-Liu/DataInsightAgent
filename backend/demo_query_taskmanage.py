# 获取用户的问题，将用户的问题分解为若干个子任务


from dotenv import load_dotenv

load_dotenv()

from langchain_community.tools.bing_search import BingSearchResults
from langchain_community.utilities import BingSearchAPIWrapper

from LLM.llm_operator import LLMOperator

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
"""


# api_wrapper = BingSearchAPIWrapper()
# tool = BingSearchResults(api_wrapper=api_wrapper)

# ans = tool.invoke({"query": "2024年美国选举情况"})

# print(f'search ans:{ans}')

if __name__ == '__main__':
    query = '2024年美国大选'
    print(f'用户提出的问题:{query}')
    # 任务分解
    
    # 思考
    print('将任务分解为若干个子任务：')
    prompt_task_ana = f'为了解决用户提出的问题，我们需要将复杂的问题进行分解，分解为若干个简单的问题，请一步一步思考。\n约束条件：1.如果用户提出的问题比较简单，可以直接回答，则复述用户的问题\n2.如果用户提出的问题比较复杂，则将问题分解，并且对各个子任务进行描述。\n用户问题:{query}'
    print(f'输入:{prompt_task_ana}')
    task_ana_ans = LLMOperator().chat_with_prompt(content = prompt_task_ana)
    print(f'输出:{task_ana_ans}')

    # 构建图
    print('将子任务分解为任务图：')
    prompt_task_tree = f'{sys_build_task_tree}\n根据用户提出的问题{query},我们将其分解为如下的任务:\n{task_ana_ans}\n将任务使用python代码构造对应的任务节点'
    print(f'输入:{prompt_task_tree}')
    task_tree_ans = LLMOperator().chat_with_prompt(content = prompt_task_tree)
    print(f'输出:{task_tree_ans}')

