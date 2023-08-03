"""主文件
"""
import asyncio
from function.CtripTravels import runBrowser
from errors import StartBrowserError
from log import Log, LogType
from config import get_settings

__ERROR_LOG_PATH__ = './logs/error'  # 错误日志

if __name__ == "__main__":
    try:
        asyncio.run(runBrowser())
    except StartBrowserError as err:
        browserLog = Log(path=__ERROR_LOG_PATH__, logType=LogType.browser_error)
        browserLog.add_log_row(username=get_settings().sysManager, content=err)
