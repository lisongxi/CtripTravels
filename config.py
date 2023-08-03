"""基础配置
"""
import json
from enum import Enum
from cachier import cachier
from pydantic import BaseModel
import yaml

__SETTINGS_PATH__ = './settings/settings.yaml'
__PROXY_PATH__ = './settings/proxy.json'


class URLs:
    """关键URL清单
    """
    homeURL = "https://www.ctrip.com/"  # 携程首页（酒店预订首页）
    flightURL = "https://flights.ctrip.com/online/channel/domestic"  # 携程机票预订首页
    trainURL = "https://trains.ctrip.com/"  # 携程火车预订首页


class XpathOptions:
    """关键Xpath
    """
    startXpath = "#searchForm input[name=\"owDCity\"]"  # 起点输入框
    destinationXpath = "#searchForm input[name=\"owACity\"]"  # 终点输入框
    dateXpath = 'xpath=/html/body/div[5]/div/div[2]/div[1]/div/div/div/div[contains(@class, "date-day") and not(contains(@class, "date-disabled"))]'  # 本月日期框
    nextDateXpath = 'xpath=/html/body/div[5]/div/div[2]/div[2]/div/div/div/div[contains(@class, "date-day") and not(contains(@class, "date-disabled"))]'  # 下月日期框


class LoginUser(BaseModel):
    """用户配置
    """
    username: str
    password: str


class Freq(Enum):
    """日志文件频率
    """
    month = 'month'
    day = 'day'
    hour = 'hour'


class Logs(BaseModel):
    """日志配置
    """
    freq: Freq
    useUTC: bool


class MysqlParam(BaseModel):
    """MySQL配置
    """
    database: str
    host: str
    port: int
    user: str
    password: str


class Parameter(BaseModel):
    """基本参数
    """
    threadNum: int  # 线程数


class Settings(BaseModel):
    """配置模型
    """
    log: Logs
    loginUser: LoginUser
    sysManager: str
    mysql: MysqlParam
    parameter: Parameter


# 获取配置文件，全局缓存
@cachier(backend='memory')
def get_settings() -> Settings:
    with open(__SETTINGS_PATH__, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return Settings(**data)


# 获取代理文件，全局缓存
@cachier(backend='memory')
def get_proxy() -> dict:
    with open(__PROXY_PATH__, 'r', encoding='utf-8') as f:
        proxies = json.load(f)
    return proxies
