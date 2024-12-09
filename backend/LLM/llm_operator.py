
from config import DEFAULT_LLM_MODEL_API_KEY, DEFAULT_LLM_MODEL_API_BASE_URL, DEFAULT_LLM_MODEL_MODEL_NAME, DEFAULT_LLM_MODEL_MAX_LEN, DEFAULT_LLM_API_MAX_TRY_NUM
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def get_llm_model_config() -> dict:
    """ get config info of LLM model

    Returns:
        dict: config info,
        {
            "API_KEY": str,
            "API_BASE_URL": str,
            "MODEL": str,
            "MAX_LEN": int,
        }
    
    """

    ret_json = {
        "API_KEY": DEFAULT_LLM_MODEL_API_KEY,
        "API_BASE_URL": DEFAULT_LLM_MODEL_API_BASE_URL,
        "MODEL": DEFAULT_LLM_MODEL_MODEL_NAME,
        "MAX_LEN": DEFAULT_LLM_MODEL_MAX_LEN,
    }

    return ret_json


class LLMOperator:
    """基于Openai API接口的LLM模型基类"""

    def get_llm_model(self):
        """获取LLM模型，基于配置文件的信息"""
        model_config = get_llm_model_config()
        # logger.info("llm config:%s", model_config)
        print(f'llm config:{model_config}')

        model = ChatOpenAI(
            # verbose=BOOL_LANGCHAIN_LOG,
            verbose=True,
            max_retries=DEFAULT_LLM_API_MAX_TRY_NUM,
            api_key=model_config["API_KEY"],
            base_url=model_config["API_BASE_URL"],
            model_name=model_config["MODEL"],
            temperature=0,
        )
        return model

    def chat_with_prompt(self, content: str) -> str:
        """使用prompt进行对话

        Args:
            content (str): 输入文本内容

        Returns:
            str: 返回结果
        """
        llm = self.get_llm_model()

        prompt = PromptTemplate(
            template="""{question}""",
            input_variables=["question"],
        )

        parser = StrOutputParser()

        chain = prompt | llm | parser

        # print(f"question:{content}")
        ans = chain.invoke({"question": content})
        # print(f"ans:{ans}")

        # return ans.content
        return ans

