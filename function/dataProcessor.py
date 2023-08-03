"""数据处理
"""
import json
import uuid

from config import get_settings
from log import Log, LogType
from models.ctripVD import Flight, FlightPrice, Transfer
from models.ctripDM import FlightDM, TransferDM, FlightPriceDM
from database import mysqlPool
from errors import ParameterValidateError, ToDataBaseError

__SUCCESS_LOG_PATH__ = './logs/success'  # 爬取成功日志
__ERROR_LOG_PATH__ = './logs/error'  # 错误日志


def dataProcessing(flightItineraryList: list) -> None:
    """
    处理航班数据，返回字典
    :param flightItineraryList: 航班数据列表
    """
    flightInfoDictList = []  # 航班信息结果字典列表
    flightTransferList = []  # 航班中转结果字典列表（一条路线可能有多个中转航班）
    flightPriceDictList = []  # 价格信息结果字典列表（一个航班可能对应多个价格信息）

    if flightItineraryList:
        for flightInfos in flightItineraryList:
            try:
                flightId = str(uuid.uuid4())  # 生成唯一值ID

                flightList = flightInfos['flightSegments'][0]['flightList']  # 乘坐航线列表
                priceList = flightInfos['priceList']  # 航班价格列表

                flightNum = len(flightList)  # 航线数
                modelDict = Flight.__fields__ if flightNum == 1 else Transfer.__fields__  # 模型字典

                for flightInfo in flightList:

                    flightInfoDict = {tk: flightInfo.get(tk, None) for tk in modelDict}
                    flightInfoDict['flightId'] = flightId

                    if flightNum == 1:
                        flightInfoDict['crossDays'] = flightInfos['flightSegments'][0]['crossDays']
                        flightInfoDict['transfer'] = False

                        try:
                            flight = Flight(**flightInfoDict)  # 数据校验
                        except Exception as err:
                            print(err)
                            raise ParameterValidateError(f"数据校验出错 {err}")

                        flightInfoDictList.append(flight.dict())

                    else:
                        try:
                            transfer = Transfer(**flightInfoDict)  # 数据校验
                        except Exception as err:
                            raise ParameterValidateError(f"数据校验出错 {err}")

                        flightTransferList.append(transfer.dict())

                if flightNum > 1:
                    # 有中转
                    flightNo1 = flightList[0]  # 第一趟航班
                    flightNo2 = flightList[-1]  # 最后一趟航班

                    # 航班信息模型字典
                    flightInfoDict = {'flightId': flightId,
                                      'departureCityName': flightNo1['departureCityName'],
                                      'arrivalCityName': flightNo2['arrivalCityName'],
                                      'marketAirlineName': flightNo1['marketAirlineName'],
                                      'flightNo': flightNo1['flightNo'],
                                      'aircraftName': flightNo1['aircraftName'],
                                      'departureAirportName': flightNo1['departureAirportName'],
                                      'departureTerminal': flightNo1['departureTerminal'],
                                      'departureDateTime': flightNo1['departureDateTime'],
                                      'arrivalAirportName': flightNo2['arrivalAirportName'],
                                      'arrivalTerminal': flightNo2['arrivalTerminal'],
                                      'arrivalDateTime': flightNo2['arrivalDateTime'],
                                      'duration': flightInfos['flightSegments'][0]['duration'],
                                      'crossDays': flightInfos['flightSegments'][0]['crossDays'],
                                      'transfer': True
                                      }
                    try:
                        flight2 = Flight(**flightInfoDict)  # 数据校验
                    except Exception as err:
                        raise ParameterValidateError(f"数据校验出错 {err}")

                    flightInfoDictList.append(flight2.dict())

                for price in priceList:
                    # 价格信息模型字典
                    flightPriceDict = {'flightId': flightId,
                                       'adultPrice': price.get('adultPrice'),
                                       'childPrice': price.get('childPrice'),
                                       'cabin': price.get('cabin'),
                                       'baggageTag': price.get('baggage').get('baggageTag'),
                                       'defaultPenaltyTag': price.get('penalty').get('defaultPenaltyTag')
                                       }

                    try:
                        flightPrice = FlightPrice(**flightPriceDict)  # 数据校验
                    except Exception as err:
                        raise ParameterValidateError(f"数据校验出错 {err}")

                    flightPriceDictList.append(flightPrice.dict())

            except ParameterValidateError as err:
                paramLog = Log(path=__ERROR_LOG_PATH__, logType=LogType.param_error)
                paramLog.add_log_row(username=get_settings().sysManager, content=err)
                continue

    try:
        to_DB(DB_Model=FlightDM, flightData=flightInfoDictList, sync=False)
        to_DB(DB_Model=TransferDM, flightData=flightTransferList, sync=False)
        to_DB(DB_Model=FlightPriceDM, flightData=flightPriceDictList, sync=False)

        print(flightInfoDictList[-1]['departureCityName'] + ' --> ' +
              flightInfoDictList[-1]['arrivalCityName'] + ' 路线爬取成功')

    except ToDataBaseError as err:
        dbLog = Log(path=__ERROR_LOG_PATH__, logType=LogType.write_db_err)
        dbLog.add_log_row(username=get_settings().sysManager, content=err)


def to_DB(DB_Model, flightData: list, sync: bool) -> None:
    """数据写入数据库
    Args:
        DB_Model: 数据库模型
        flightData: 待写入的数据
        sync: 同步方式（增量True，全量False）
    """
    try:
        if not sync:
            mysqlPool.create_tables([DB_Model])

        with mysqlPool.atomic():
            for i in range(0, len(flightData), num := 100):  # 一次插入100条
                (DB_Model
                 .insert_many([dict(flow) for flow in flightData[i:i + num]])
                 .on_conflict_replace()  # 唯一约束发生冲突时，进行替换操作
                 .execute()
                 )
    except Exception as err:
        raise ToDataBaseError(f"数据写入数据库异常 {err}")


if __name__ == "__main__":
    with open('../data/temp.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        dataProcessing(data)
