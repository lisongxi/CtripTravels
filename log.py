"""日志
"""
import json
from enum import Enum
from datetime import datetime
from functools import reduce
from typing import Union, Optional
from pydantic import BaseModel
import os
import pipe

from config import get_settings

__FREQ__ = {'month': '%Y%m', 'day': '%Y%m%d', 'hour': '%Y%m%d%H'}
# 日志频率。例如 day 表示一个日志文件记录一天的记录，hour 表示一个日志文件记录一个小时的日志

freq = __FREQ__[get_settings().log.freq.value]


class LogType(Enum):
    """日志类型
    """
    crawl_success = '爬取成功'
    write_db_err = '写入数据库失败'
    run_error = '运行出错'
    param_error = '参数校验异常'
    empty_flight = '无航班信息'
    xpath_error = 'xpath定位异常'
    browser_error = '浏览器启动异常'


class Log:
    """日志处理类
    """
    _file_format = '.txt'  # 日志文件类型
    _intro_template = "by: {username}, time: {logtime}, content: \n"

    def __init__(self, *, path: str, fq: str = freq, useUTC: bool = get_settings().log.useUTC,
                 logType: LogType):  # 参数 * 代表后面的参数强制使用关键字参数传递的命名关键字参数
        """
        初始化
        生成文件名后缀
        :param path: 文件夹路径
        :param fq: 日志频率
        :param useUTC: 是否使用UTC时间
        :param logType: 日志类型
        """
        nowTime = datetime.utcnow() if useUTC else datetime.now()
        file_suffix = nowTime.strftime(fq)
        self.file = os.path.join(path, logType.value + '_' + file_suffix + self._file_format)  # 拼接路径，生成文件
        self.logtime = nowTime.isoformat()  # 将一个datetime对象转换为ISO 8601格式的字符串。

    @classmethod
    def _trace_error(cls, err: Exception) -> str:
        """追溯异常
        """
        err_name = (
                err.__class__.mro()[:-2] |
                pipe.map(lambda x: str(x)) |
                pipe.map(lambda x: x.lstrip("<class '").rstrip("'>")) |
                pipe.map(lambda x: x.split('.')[-1]) |
                pipe.Pipe(lambda x: reduce(lambda a, b: a + ' ' + u'\u2190' + ' ' + b, x))  # 箭头分隔符
        )
        return err_name

    def add_log_row(self, *, username: Optional[str] = None, content: Union[Exception, BaseModel, str]):
        """添加一行日志
        Args:
            username: 用户账号，None表示为系统管理员
            content: 日志内容
        """
        if username is None:
            username = get_settings().sysManager
        if isinstance(content, str):
            text = content
        elif isinstance(content, Exception):
            text = self._trace_error(err=content) + '-' * 200 + ('\n%s' % content)
        elif isinstance(content, BaseModel):
            text = json.dumps(
                content.dict(exclude_unset=True), indent=4, ensure_ascii=False
            )
        with open(self.file, 'at') as f:
            f.write(
                self._intro_template.format(username=username, logtime=self.logtime)
            )
            f.write('-' * 200 + '\n')
            f.write(text + '\n')
            f.write('=' * 200 + '\n\n')
