from dotenv import load_dotenv

load_dotenv()

from langchain_community.tools.bing_search import BingSearchResults
from langchain_community.utilities import BingSearchAPIWrapper

api_wrapper = BingSearchAPIWrapper()
tool = BingSearchResults(api_wrapper=api_wrapper)

ans = tool.invoke({"query": "2024年美国选举情况"})

print(f'search ans:{ans}')
