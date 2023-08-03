# 基于Playwright+Asyncio爬取携程网的机票数据

## 1、启动

> 1、将`CtripTravels.py`文件中的`__EXECUTABLE_PATH__ `修改为本机google客户端exe的路径。

> 2、运行`function.nextRoute.py`的`createRoute()`函数，生成路线文件。

> 3、运行`main.py`文件，即可启动爬虫。

## 2、注意事项
> 1、携程网的反爬机制比较强，如果你不用代理，那你的IP很快就会被封，所有路线都会提示无法查询了。
> 建议配置`settings`下的`proxy.json`文件，填写你自己的代理。
> 
> 2、如果配置了代理文件，记得要把`CtripTravels.py`文件中的`pw.chromium.launch`中的`proxy`参数注释去掉。