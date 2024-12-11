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
# 初始化任务图
task_graph = TaskGraph()

# 添加根节点
task_graph.add_root_node("2024年美国大选")

# 添加子问题节点
task_graph.add_node("election_date", "2024年美国大选的时间是什么时候？")
task_graph.add_node("main_candidates", "2024年美国大选的主要候选人有哪些？")
task_graph.add_node("main_issues", "2024年美国大选的主要议题是什么？")
task_graph.add_node("election_system", "2024年美国大选的选举制度是怎样的？")
task_graph.add_node("voting_methods", "2024年美国大选的投票方式有哪些？")
task_graph.add_node("influencing_factors", "2024年美国大选的影响因素有哪些？")

# 添加边
task_graph.add_edge("root", "election_date")
task_graph.add_edge("root", "main_candidates")
task_graph.add_edge("root", "main_issues")
task_graph.add_edge("root", "election_system")
task_graph.add_edge("root", "voting_methods")
task_graph.add_edge("root", "influencing_factors")

# 添加 response 节点
task_graph.add_response_node("response")

# 获取任务列表
task_list = task_graph.get_task_list()

for task in task_list:
    if task:
        print(task)
