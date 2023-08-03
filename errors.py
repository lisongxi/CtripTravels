"""
自建项目异常体系，便于捕获异常类型，并关联日志体系
"""


class RootError(Exception):
    """根异常
    """


class EmptyIndexError(RootError):
    """空索引异常
    """


class ParameterValidateError(RootError):
    """参数校验异常
    """


class ToDataBaseError(RootError):
    """写入数据库异常
    """


class StartBrowserError(RootError):
    """启动浏览器异常
    """


class XpathError(RootError):
    """Xpath定位异常
    """
