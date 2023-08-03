"""携程数据校验模型
"""

from pydantic import BaseModel
from typing import Optional


class Flight(BaseModel):
    """航班信息校验模型
    """
    flightId: str  # 航班ID
    departureCityName: str  # 起点
    arrivalCityName: str  # 终点
    marketAirlineName: str  # 航空公司
    flightNo: str  # 航班
    aircraftName: Optional[str] = None  # 飞机型号
    departureAirportName: str  # 出发机场
    departureTerminal: Optional[str] = None  # 出发航站楼
    departureDateTime: str  # 出发时间
    arrivalAirportName: str  # 到达机场
    arrivalTerminal: Optional[str] = None  # 到达航站楼
    arrivalDateTime: str  # 到达时间
    duration: int  # 航班时长
    crossDays: int  # 跨越天数
    transfer: bool  # 是否中转


class Transfer(BaseModel):
    """中转信息模型
    """
    flightId: str  # 关联航班ID
    departureCityName: str  # 中转起点
    arrivalCityName: str  # 中转终点
    marketAirlineName: str  # 中转航空公司
    flightNo: str  # 中转航班
    aircraftName: Optional[str] = None  # 中转飞机型号
    departureAirportName: str  # 中转出发机场
    departureTerminal: Optional[str] = None  # 中转出发航站楼
    departureDateTime: str  # 中转出发时间
    arrivalAirportName: str  # 中转到达机场
    arrivalTerminal: Optional[str] = None  # 中转到达航站楼
    arrivalDateTime: str  # 中转到达时间
    transferDuration: Optional[str] = None  # 中转时间间隔


class FlightPrice(BaseModel):
    """航班价格等级校验模型
    """
    flightId: str  # 关联航班ID
    adultPrice: int  # 成人票价
    childPrice: Optional[int] = None  # 儿童票价
    cabin: str  # 座位类型
    baggageTag: Optional[str] = None  # 行李重量备注
    defaultPenaltyTag: Optional[str] = None   # 退改价格说明



