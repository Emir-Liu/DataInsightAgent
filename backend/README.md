```bash
.
├── Agents
├── base.py
├── config
│   ├── __init__.py
│   ├── llm_config.py
│   ├── search_engine_config.py
│   └── server_config.py
├── demo_bing_search.py # 使用bing搜索引擎
├── demo_build_task_tree.py # 构建任务图
├── demo_chat.py # 使用LLM进行对话
├── demo_exec_python.py # 执行python脚本
├── demo_query_taskmanage.py # 询问，再进行任务分解
├── demo_select_web.py # 搜索的时候，选择网页
├── dockerfile
├── LLM
│   └── llm_operator.py
├── main.py
├── README.md
├── requirements.txt
├── resolv.conf
├── TaskManager
├── taskTree_template.py # python直接执行构造的代码，检查构造的代码的正确性
└── Tools
```