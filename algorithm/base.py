'''

针对单个搜索引擎的基本操作，所有操作引擎的具体实现需要继承该类

'''

from abc import ABC
from typing import Optional

import aiohttp

# from configs import LoggerOperation
from config import (
    SEARCH_ENGINE_TIMEOUT
)

from logging import Logger

logger = Logger(name='bing')

# logger = LoggerOperation().get_logger(name='search_engine')


async def get_url(
        url: str,
        headers={},
        params={},
        timeout: Optional[int] = None,
        return_type: Optional[str] = 'json',
        bool_return_status: Optional[bool] = False
):
    '''

    异步访问页面，

    Args:
        url: 访问的路由
        timeout: 页面访问的延迟时间
        headers: 部分请求存在headers
        params: 部分请求的传入参数
        return_type: 新增的返回格式参数，使用json或者text这两种格式

    Returns:

    '''
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params, timeout=timeout) as response:
                if return_type == 'json':
                    data = await response.json()
                elif return_type == 'text':
                    data = await response.text()
                else:
                    logger.error('异步访问界面出错了，传入的return type参数未知:{},仅仅支持json和text两种类型的数据'.format(
                        return_type
                    ))

                # return data
                if bool_return_status == True:
                    status = response.status
                    return status, data
                else:
                    return data
    except Exception as e:
        logger.error(f'访问报错:{e}')
        # return 


class SearchEngineOperator(ABC):

    def __init__(
            self,
            search_query,
            count,
    ):
        self.search_query = search_query
        self.count = count

    # @abstractmethod
    # async def api_find(
    #         self,
    # ):
    #     pass

    async def api_find_thread(
            self,
            ans_str_q,
            ans_json_q,
    ):
        '''
         使用api进行并发的访问请求，用于并发的封装，个数应该可以大于10
         Args:
             search_query:
             count:

         Returns:

         '''
        # logger.info('开始调用api find th')
        logger.info('search query:{}'.format(self.search_query))
        logger.info('count:{}'.format(self.count))

        ans_str, ans_json = await self.api_find()

        logger.info('ans:{}'.format(ans_str))
        logger.info('ans json:{}'.format(ans_json))

        for tmp_ans_json in ans_json:
            ans_json_q.put(tmp_ans_json)

        ans_str_q.put(ans_str)
