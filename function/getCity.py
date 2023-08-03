"""
获取城市列表 , 保存到本地文件
"""
import json
import time

from playwright.sync_api import Playwright, sync_playwright

# 城市列表路径
__CITY_PATH__ = '../data/city/city1.json'

cityList = []  # 城市列表
hotList = []  # 热门城市


def city_response(response) -> None:
    """
    监听返回城市地点数据
    Args:
        response: 返回数据
    """
    try:
        if '/flights.ctrip.com/online/api/poi/get' in response.url and response.status == 200:
            chinaCity = response.json()['data']

            chinaHot = chinaCity.pop("热门")
            for h in chinaHot:
                hotList.append(h['display'])

            for _, init in chinaCity.items():
                for _, cities in init.items():
                    for city in cities:
                        cityList.append(city['display'])

            allCity = {"chinaHot": hotList, "allChinaCity": cityList}

            # 保存到本地文件
            with open(__CITY_PATH__, 'w', encoding='utf-8') as f:
                json.dump(allCity, f, ensure_ascii=False, indent=4)
                # ensure_ascii=False 不用 ASCII 编码，中文可以正常显示
    except Exception as err:
        print(err)


def getCity(pw: Playwright) -> None:
    browser = pw.chromium.launch(headless=True, slow_mo=500)
    context = browser.new_context()
    page = context.new_page()

    page.on('response', city_response)  # 监听函数

    page.goto("https://flights.ctrip.com/online/channel/domestic")

    time.sleep(1)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    getCity(playwright)
