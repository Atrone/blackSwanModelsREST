import datetime
from aiohttp import web
import json
import main
import tools
import os

async def handle(request):
    filelist = [f for f in os.listdir('./') if f.endswith(".csv")]
    for f in filelist:
        os.remove(os.path.join('./', f))
    startDate = datetime.datetime.strptime(request.rel_url.query['startDate'],"%Y-%m-%d %H:%M:%S")
    today = datetime.datetime.now()

    main.createResponseCSVs(True,startDate,
                            int(request.rel_url.query['hours']),
                            int(request.rel_url.query['limit']),
                            int(request.rel_url.query['dollars']))
    priceData = (tools.make_json('price'+tools.dateTimeToMonthTDay(startDate)+".csv"))
    trendsData = (tools.make_json('trends'+tools.dateTimeToMonthTDay(startDate)+".csv"))
    trendBuysData = (tools.make_json('trendBuys'+tools.dateTimeToMonthDay(today)+".csv"))

    return web.Response(text=(priceData + trendsData + trendBuysData))

if __name__ == "__main__":
    app = web.Application()
    app.router.add_get('/generateHistoricalPriceTrendsAndAdvise', handle)

    web.run_app(app)