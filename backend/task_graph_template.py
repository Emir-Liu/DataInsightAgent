class TaskGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.root = None

    def add_root_node(self, root_name):
        """添加根节点"""
        self.root = root_name
        self.nodes[root_name] = {"type": "root", "question": question,"children": []}
    
    def add_node(self, node_name, question):
        """添加子问题节点"""
        self.nodes[node_name] = {"type": "task", "question": question, "children": []}
    
    def add_edge(self, parent_name, child_name):
        """添加边，将子节点与父节点关联"""
        if parent_name in self.nodes and child_name in self.nodes:
            self.nodes[parent_name]["children"].append(child_name)
            if parent_name not in self.edges:
                self.edges[parent_name] = []
            self.edges[parent_name].append(child_name)
        else:
            raise ValueError("父节点或子节点不存在")
    
    def add_response_node(self, response_name):
        """添加响应节点"""
        self.nodes[response_name] = {"type": "response", "content": ""}
    
    def set_response_content(self, response_name, content):
        """设置响应节点的内容"""
        if response_name in self.nodes and self.nodes[response_name]["type"] == "response":
            self.nodes[response_name]["content"] = content
        else:
            raise ValueError("响应节点不存在或类型不匹配")
    
    def get_graph(self):
        """获取任务图的结构"""
        return {
            "nodes": self.nodes,
            "edges": self.edges,
            "root": self.root
        }