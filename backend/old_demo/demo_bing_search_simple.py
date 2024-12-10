
from config import BING_SEARCH_V7_SUBSCRIPTION_KEY, BING_SEARCH_V7_ENDPOINT, BING_SEARCH_MKT

subscription_key = BING_SEARCH_V7_SUBSCRIPTION_KEY
endpoint = BING_SEARCH_V7_ENDPOINT
mkt = BING_SEARCH_MKT


search_query = 'AI科技'

params = {'q': search_query, 'mkt': mkt}
headers = {'Ocp-Apim-Subscription-Key': subscription_key}

# Call the API
# try:
# 备注：我们当前使用的API接口和官方说明的API接口不一致，下面注释掉的是官方的接口
# 参考来源：https://learn.microsoft.com/en-us/answers/questions/291951/httperror-404-client-error-resource-not-found-for
# url = '{}/bing/v7.0/search'.format(self.endpoint)
url = '{}//v7.0/search'.format(endpoint)
print(f'url:{url}')

import requests
import aiohttp
import asyncio


async def get_data(url, params=None, headers=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            response.raise_for_status()  # 如果返回状态码不是200，会抛出异常
            return await response.json()  # 返回JSON格式的数据
        
# data = await get_data(url=url, params=params, headers=headers)

data = asyncio.run(get_data(url=url, params=params, headers=headers))
print(f'data:{data}')