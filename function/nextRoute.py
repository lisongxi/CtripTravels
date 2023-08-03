"""
获取下一组路线
"""
import json
import os

# 下一路线文件夹
__NEXT_ROUTE_PATH__ = r'../data/city/nextRoute/'

# 城市列表路径
__CITY_PATH__ = r'../data/city/classifiedCities.json'

ii = 1000
oo = 2000


def getCityFile() -> dict:
    """返回城市列表
    """
    with open(__CITY_PATH__, 'r', encoding='utf-8') as f:
        city = json.load(f)
        return city


def createRoute() -> None:
    """创建路线文件
    """
    cityDict = getCityFile()

    allChinaCity = cityDict["allChinaCity"]
    chinaHot = cityDict["chinaHot"]
    internationalCities = cityDict["internationalCities"]

    createRoute2(allChinaCity, allChinaCity, True)  # 国内互通
    createRoute2(internationalCities, internationalCities, False)  # 国际互通
    createRoute2(chinaHot, internationalCities, True)  # 国内出发
    createRoute2(internationalCities, chinaHot, False)  # 国际出发


def createRoute2(beginList: list, endList: list, io: bool):
    for begin in beginList:
        routeList = []
        for end in endList:
            if begin == end:
                continue
            routeList.append(end)

        global ii, oo
        fileName = ii + 1 if io else oo + 1
        ii += io
        oo += not io

        with open(__NEXT_ROUTE_PATH__ + str(fileName) + '.json', 'w', encoding='utf-8') as f:
            json.dump({begin: routeList}, f, ensure_ascii=False)


def get_nextRoute(filepath: str) -> tuple:
    """获取下一个城市路线
    如果完成所有路线读取，则删掉路径文件
    """
    with open(filepath, 'r', encoding='utf-8') as f1:
        routeDataDict = json.load(f1)

    departure, routeData = routeDataDict.popitem()

    if routeData:
        nextRoute = routeData[0]
        return departure, nextRoute
    else:
        os.remove(filepath)  # 删除已完成读取的文件
        return ()


def pop_route(filepath: str) -> None:
    """移除已读的城市路线，实现断点续爬
    """
    with open(filepath, 'r', encoding='utf-8') as f2:
        routeDataDict = json.load(f2)

    with open(filepath, 'w', encoding='utf-8') as f3:
        departure, routeData = routeDataDict.popitem()
        routeData.pop(0)
        json.dump({departure: routeData}, f3, ensure_ascii=False)


if __name__ == "__main__":
    createRoute()
    # pop_route('../data/city/nextRoute/1103.json')
