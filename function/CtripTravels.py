import asyncio
import time
import os
from playwright.async_api import async_playwright

from config import URLs, XpathOptions, get_settings, get_proxy
from function.nextRoute import get_nextRoute, pop_route
from function.fetchResponse import flight_response
from errors import StartBrowserError, XpathError

__USER_DATE_DIR_PATH__ = r'D:\tmp\tempUser'  # 浏览器缓存(登录信息)/书签/个人偏好舍设置内容存储位置，随便设置
__EXECUTABLE_PATH__ = r'C:\Program Files\Google\Chrome\Application\chrome.exe'  # 要使用的浏览器位置
__ROUTE_FILE_PATH__ = r'./data/city/nextRoute/'

num = get_settings().parameter.threadNum  # 开启标签页数量
proxies = get_proxy()  # 代理 (携程有反爬机制，不用代理的话，没动几下就会被封IP了)


async def ctripTravels(context, cityPath: str, firstRoute: tuple) -> None:
    """爬取数据
    驱动浏览器，以循环的方式输入 航班起点 航班终点
    多线程同时打开多个标签页，输入不同的路线
    实现多个抓手 抓取返回的航班数据
    Args:
        context: 浏览器上下文
        cityPath: 起点终点文件路径
        firstRoute: 首个起点终点
    :return: None
    """

    page = await context.new_page()  # 新建标签页
    # page.set_default_timeout(5000)  # 设置默认 timeout 时间

    page.on('response', flight_response)  # 监听函数

    await page.goto(URLs.flightURL)

    await page.get_by_text("单程").click()

    await page.get_by_placeholder("yyyy-mm-dd").click()  # 点击时间框

    dateList = await page.locator(XpathOptions.dateXpath).all()  # 时间列表

    for tripTime in dateList:

        await page.locator(XpathOptions.startXpath).fill(firstRoute[0])  # 起点

        await page.locator('div.poi-address > div.address').first.click()

        await page.locator(XpathOptions.destinationXpath).fill(firstRoute[1])  # 终点

        await page.locator('div.poi-address > div.address').first.click()

        await tripTime.click()  # 选择时间

        await page.get_by_role("button", name="搜索").click()

        try:
            element = await page.wait_for_selector('text="知道了"', timeout=3000)
            await element.click()
            time.sleep(1.03)
        except:
            pass

        pop_route(cityPath)  # 弹出一个路线

        # 完成第一环搜索，接下来只需循环输入终点

        while nextRoute := get_nextRoute(cityPath):
            await page.locator(XpathOptions.destinationXpath).fill(nextRoute[1])  # 终点
            await page.locator('div.poi-address > div.address').first.click()

            try:
                element = await page.wait_for_selector('text="知道了"', timeout=3000)
                await element.click()
                time.sleep(1.03)
            except:
                pass

            time.sleep(5.23)
            pop_route(cityPath)

        await page.close()


async def runBrowser() -> None:
    """驱动浏览器
    """
    async with async_playwright() as pw:
        try:
            browser = await pw.chromium.launch(
                executable_path=__EXECUTABLE_PATH__,  # 指定本机google客户端exe的路径
                headless=False,
                slow_mo=1000,
                # proxy=proxies
            )

            context = await browser.new_context()
        except Exception as err:
            print(err)
            raise StartBrowserError(f"浏览器启动异常：{err}")

        fileList = os.listdir(__ROUTE_FILE_PATH__)

        for i in range(0, len(fileList), num):
            tasks = []
            for file in fileList[i:i + num]:
                filePath = __ROUTE_FILE_PATH__ + file
                firstRoute = get_nextRoute(filePath)
                task = asyncio.create_task(ctripTravels(context, filePath, firstRoute))
                tasks.append(task)

            for t in tasks:
                await t
