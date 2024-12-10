
'''
下面是基于bing的搜索结果
'''

# import requests
# session = requests.Session()


from config import (
    BING_SEARCH_V7_SUBSCRIPTION_KEY,
    BING_SEARCH_V7_ENDPOINT,
    BING_SEARCH_MKT,
    SEARCH_ENGINE_TIMEOUT
)
# from configs import LoggerOperation
from base import SearchEngineOperator, get_url

from logging import Logger

logger = Logger(name='bing')


class BingSearchEngineOperator(SearchEngineOperator):
    '''
    Bing搜索引擎相关的操作对象
    '''

    def __init__(
            self,
            search_query,
            count
    ):
        super().__init__(search_query, count)
        # self.search_query = search_query
        # self.count = count
        self.subscription_key = BING_SEARCH_V7_SUBSCRIPTION_KEY
        self.endpoint = BING_SEARCH_V7_ENDPOINT
        self.mkt = BING_SEARCH_MKT

    async def api_find(
            self,
            timeout=SEARCH_ENGINE_TIMEOUT
    ):
        '''
        通过google的api进行单次网络搜索，
        Args:
            search_query:
            count:

        Returns:

        '''

        params = {'q': self.search_query, 'mkt': self.mkt}
        headers = {'Ocp-Apim-Subscription-Key': self.subscription_key}

        # Call the API
        # try:
        # 备注：我们当前使用的API接口和官方说明的API接口不一致，下面注释掉的是官方的接口
        # 参考来源：https://learn.microsoft.com/en-us/answers/questions/291951/httperror-404-client-error-resource-not-found-for
        # url = '{}/bing/v7.0/search'.format(self.endpoint)
        url = '{}//v7.0/search'.format(self.endpoint)
        logger.info('url:{}'.format(url))
        # print('url:{}'.format(url))

        # 将下面的替换为异步函数
        response = await get_url(url, headers=headers, params=params)
        # response = requests.get(url, headers=headers, params=params, timeout=SEARCH_ENGINE_TIMEOUT)

        data = response

        logger.info('data:{}'.format(data))
        print('data:{}'.format(data))
        ret_list = []
        if len(data['webPages']['value']) != 0:

            ret_text = 'Bing搜索引擎:<br/>'
            for idx, search_res in enumerate(data['webPages']['value']):

                ret_text += "<p style='text-indent:1em;'><a href='{}' >{}</a>{}</p>".format(
                    search_res['displayUrl'],
                    search_res['name'],
                    search_res['snippet']
                )
                tmp_ret_list = {
                    'link': search_res['displayUrl'],
                    'title': search_res['name'],
                    'desc': search_res['snippet'],
                    'search_engine': 'bing'
                }

                ret_list.append(tmp_ret_list)

                if idx == self.count - 1:
                    break
            print(f'ret_text:{ret_text}\nret_list:{ret_list}')
            return ret_text, ret_list
        else:
            return '', []
        # except Exception as e:
        #     logger.warning('使用Bing搜索引擎的API接口失败:{}'.format(e))
        #     return '', []

import asyncio

if __name__ == '__main__':
    ans_str, ans_list = asyncio.run(BingSearchEngineOperator(
        search_query='如何使用k8s进行docker管理',
        count=5
    ).api_find())
