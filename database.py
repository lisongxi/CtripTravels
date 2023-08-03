from config import get_settings
from playhouse.pool import PooledMySQLDatabase

__MYSQL_PARAMS__ = get_settings().mysql

# 连接池
mysqlPool = PooledMySQLDatabase(
    **__MYSQL_PARAMS__.dict(),
    max_connections=10,
    timeout=10
)
