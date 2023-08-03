"""
抓取后台数据
"""

from function.dataProcessor import dataProcessing
from errors import EmptyIndexError
from log import Log, LogType
from config import get_settings

__SUCCESS_LOG_PATH__ = './logs/success'  # 爬取成功日志
__ERROR_LOG_PATH__ = './logs/error'  # 错误日志


async def flight_response(response) -> None:
    """监听返回航班数据
    Args:
        response: 返回数据
    """
    try:
        if '/search/api/search/batchSearch' in response.url and response.status == 200:
            flightData = await response.json()
            # 特别注意这里，不能直接用 await response.json()['data']，只能先 await response.json()

            try:
                flightItineraryList = flightData['data']['flightItineraryList']
            except:
                raise EmptyIndexError("路线无航班信息！")

            # 进入数据处理
            dataProcessing(flightItineraryList)

    except EmptyIndexError as err:
        emptyLog = Log(path=__ERROR_LOG_PATH__, logType=LogType.empty_flight)
        emptyLog.add_log_row(username=get_settings().sysManager, content=err)
