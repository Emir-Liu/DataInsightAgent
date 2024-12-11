# 解析，执行python脚本

from langchain_experimental.utilities import PythonREPL



if __name__ == '__main__':
    tool = PythonREPL()

    ans = tool.run("""print('hello')""")

    print(f'ans:{ans}')