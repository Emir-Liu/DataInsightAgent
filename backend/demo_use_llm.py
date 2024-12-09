
# import os
from dotenv import load_dotenv

load_dotenv()

from LLM.llm_operator import LLMOperator


if __name__ == '__main__':
    ans = LLMOperator().chat_with_prompt(content='hello')
    print(f'ans:{ans}')


