"""携程数据库模型
"""

from database import mysqlPool

from peewee import (Model,
                    CharField,
                    UUIDField,
                    DateTimeField,
                    SmallIntegerField,
                    BooleanField,
                    BigAutoField)


class FlightDM(Model):
    """航班信息数据库模型
    """
    flightId = UUIDField(primary_key=True, null=False, verbose_name='航班ID')
    departureCityName = CharField(max_length=6, null=False, verbose_name='起点')
    arrivalCityName = CharField(max_length=6, null=False, verbose_name='终点')
    marketAirlineName = CharField(max_length=6, null=False, verbose_name='航空公司')
    flightNo = CharField(max_length=6, null=False, verbose_name='航班')
    aircraftName = CharField(max_length=10, verbose_name='飞机型号')
    departureAirportName = CharField(max_length=6, null=False, verbose_name='出发机场')
    departureTerminal = CharField(max_length=3, verbose_name='出发航站楼')
    departureDateTime = DateTimeField(verbose_name='出发时间')
    arrivalAirportName = CharField(max_length=6, null=False, verbose_name='到达机场')
    arrivalTerminal = CharField(max_length=3, verbose_name='到达航站楼')
    arrivalDateTime = DateTimeField(null=False, verbose_name='到达时间')
    duration = SmallIntegerField(verbose_name='航班总时长')
    crossDays = SmallIntegerField(verbose_name='跨越天数')
    transfer = BooleanField(verbose_name='是否中转')

    class Meta:
        database = mysqlPool
        table_name = 't_flight'
        table_comment = '航班信息'


class TransferDM(Model):
    """中转航班信息数据库模型
    """
    transferId = BigAutoField(null=False, primary_key=True)
    flightId = UUIDField(null=False, verbose_name='关联航班ID')
    departureCityName = CharField(max_length=6, null=False, verbose_name='起点')
    arrivalCityName = CharField(max_length=6, null=False, verbose_name='终点')
    marketAirlineName = CharField(max_length=6, null=False, verbose_name='航空公司')
    flightNo = CharField(max_length=6, null=False, verbose_name='航班')
    aircraftName = CharField(max_length=10, verbose_name='飞机型号')
    departureAirportName = CharField(max_length=6, null=False, verbose_name='出发机场')
    departureTerminal = CharField(max_length=3, verbose_name='出发航站楼')
    departureDateTime = DateTimeField(verbose_name='出发时间')
    arrivalAirportName = CharField(max_length=6, null=False, verbose_name='到达机场')
    arrivalTerminal = CharField(max_length=3, verbose_name='到达航站楼')
    arrivalDateTime = DateTimeField(null=False, verbose_name='到达时间')
    transferDuration = SmallIntegerField(verbose_name='中转时长')

    class Meta:
        database = mysqlPool
        table_name = 't_transfer'
        table_comment = '中转航班信息'


class FlightPriceDM(Model):
    """航班价格等级数据库模型
    """
    priceId = BigAutoField(null=False, primary_key=True)
    flightId = UUIDField(null=False, verbose_name='关联航班ID')
    adultPrice = SmallIntegerField(null=False, verbose_name='成人票价')
    childPrice = SmallIntegerField(verbose_name='儿童票价')
    cabin = CharField(max_length=6, verbose_name='座位类型')
    baggageTag = CharField(max_length=30, verbose_name='行李重量备注')
    defaultPenaltyTag = CharField(max_length=30, verbose_name='退改价格说明')

    class Meta:
        database = mysqlPool
        table_name = 't_flight_price'
        table_comment = '航班价格信息'
