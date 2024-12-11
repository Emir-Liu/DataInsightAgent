
from langchain_experimental.utilities import PythonREPL

python_cmd = """
# 初始化任务图
task_graph = TaskGraph()

# 添加根节点
task_graph.add_root_node("2024年美国大选")

# 添加子问题节点
task_graph.add_node("election_date", "2024年美国大选的具体日期是什么时候？")
task_graph.add_node("election_positions", "这次大选将选举哪些职位（如总统、国会等）？")
task_graph.add_node("candidates", "目前有哪些主要候选人参与2024年总统选举？")
task_graph.add_node("candidates_policies", "各候选人的主要政策立场和背景是什么？")
task_graph.add_node("election_process", "2024年美国大选的选举流程是怎样的？")
task_graph.add_node("primaries_schedule", "预选赛和党内初选的时间安排是什么？")
task_graph.add_node("voter_registration", "选民注册的要求和流程是什么？")
task_graph.add_node("voting_methods", "如何投票（如提前投票、邮寄投票等）？")
task_graph.add_node("influencing_factors", "2024年大选可能受到哪些社会、经济或国际因素的影响？")
task_graph.add_node("polling_data", "目前的民调数据如何？")

# 添加边
task_graph.add_edge("root", "election_date")
task_graph.add_edge("root", "election_positions")
task_graph.add_edge("root", "candidates")
task_graph.add_edge("root", "election_process")
task_graph.add_edge("root", "voter_registration")
task_graph.add_edge("root", "influencing_factors")

# 添加 response 节点
task_graph.add_response_node("response")
"""

TaskGraph = r"""
class TaskGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.root = None

    def add_root_node(self, node_name):
        self.root = 'root'
        self.nodes['root'] = node_name

    def add_node(self, node_name, question):
        self.nodes[node_name] = question

    def add_edge(self, from_node, to_node):
        if from_node in self.edges:
            self.edges[from_node].append(to_node)
        else:
            self.edges[from_node] = [to_node]

    def add_response_node(self, response_name):
        self.nodes[response_name] = "Response"

    def get_task_list(self, current_node=None):
        task_list = []
        if current_node is None:
            current_node = self.root
        else:
            
            task_list.append(self.nodes[current_node])  # 添加当前节点的问题或响应

        # 遍历当前节点的所有边
        for neighbor in self.edges.get(current_node, []):
            task_list.extend(self.get_task_list(neighbor))  # 递归获取子节点的任务
        
        return task_list
"""

show_task_list = """
# 获取任务列表
task_list = task_graph.get_task_list()

for task in task_list:
    if task:
        print(task)

"""

if __name__ == '__main__':
    tool = PythonREPL()
    total_cmd_str = f'{TaskGraph}\n{python_cmd}\n{show_task_list}'
    # print(f'total_cmd_str:\n{total_cmd_str}')

    ans = tool.run(total_cmd_str)

    print(f'ans:{ans}')