import time

from coinmarketcapapi import CoinMarketCapAPI
from pytrends.request import TrendReq
import datetime
import operator
import tools
from typing import List, Dict


class Executor:
    def __init__(self, date, hours, limit, dir):
        self.date = date
        self.hours = hours
        self.limit = limit
        self.dir = dir
        self.CryptoDataCollector = CryptoDataCollector(self, str(self.hours) + " " + str(
            self.limit) + " " + self.dir + " " + str(self.date))

    def getCryptosPriceAndTrendsFromDateEveryXHoursTillToday(self, results):
        while self.date < datetime.datetime.now():
            print(self.date)
            priceResultsDictionary, resultsDictionary, resultsString = \
                self.CryptoDataCollector.matchTrendingCryptosAndPrices()
            results.append({'price': priceResultsDictionary, 'trends': resultsDictionary, 'date': self.date})
            self.date = self.date + datetime.timedelta(hours=self.hours)
            print(resultsString)
            print(results)
        return results

    def getResults(self) -> List[Dict]:
        results = []
        results = self.getCryptosPriceAndTrendsFromDateEveryXHoursTillToday(results)
        print(results)
        tools.updateCSVForListOfDict([{"NONE": 0}],
                                     "hours" + str(self.hours) + ".csv")
        for key in results[0].keys():
            if key != 'date':
                tools.updateCSVForListOfDict(tools.getListOfDictionariesAtKey(key, results),
                                             str(key) + str(results[0]['date'])[5:10].replace("-", "T") + ".csv")
        return results


class CryptoDataCollector:
    def __init__(self, executor=None, cmd=""):
        self.executor = executor
        self.cmd = cmd

    def parseCryptoCommand(self, parameter):
        if parameter == "hoursBeforeNow":
            return int(self.cmd.split(" ")[0])
        elif parameter == "cryptoLimit":
            return int(self.cmd.split(" ")[1])
        elif parameter == "sortDirection":
            return self.cmd.split(" ")[2]
        elif parameter == "startDate":
            return self.cmd.split(" ")[3] + " " + self.cmd.split(" ")[4]
        else:
            raise ValueError("This command requires hoursBeforeNow, cryptoLimit, or sortDirection for parameter")

    def checkIfCmdIsWrong(self):
        if (len(self.cmd.split(" ")) != 5):
            return "Enter # of hours before start date," \
                   " # of crypto limit, asc or desc," \
                   " and start date, like so: /cryptos 1 10 asc 2021-07-17 00:00:00"
        return 0

    def getPriceForCryptoAtTime(self, startDate, crypto):
        cmc = CoinMarketCapAPI('c47f6c83-d986-4e65-a540-10cd8f1c0e45')
        price = cmc.tools_priceconversion(amount=1, symbol=crypto, time=datetime.datetime.fromisoformat(startDate))
        return price.data['quote']['USD']['price']

    def getLatestCryptocurrencyListings(self, limit, sortDir):
        cmc = CoinMarketCapAPI('c47f6c83-d986-4e65-a540-10cd8f1c0e45')
        return cmc.cryptocurrency_listings_latest(limit=limit, sort_dir=sortDir)

    def getCryptoInterest(self, crypto, name, fromDate, today, sleep):
        pytrends = TrendReq(hl='en-US', tz=360)
        return sum(
            pytrends.get_historical_interest([str(crypto) + " crypto"], year_start=int(str(fromDate)[0:4]),
                                             month_start=int(str(fromDate)[6]), day_start=int(str(fromDate)[8:10]),
                                             hour_start=int(str(fromDate)[11:13]),
                                             year_end=int(str(today)[0:4]), month_end=int(str(today)[6]),
                                             day_end=int(str(today)[8:10]), hour_end=int(str(today)[11:13]), cat=0,
                                             geo='',
                                             gprop='',
                                             sleep=sleep).sum(axis=1, skipna=True).values) + (sum(
            pytrends.get_historical_interest([str(name)], year_start=int(str(fromDate)[0:4]),
                                             month_start=int(str(fromDate)[6]), day_start=int(str(fromDate)[8:10]),
                                             hour_start=int(str(fromDate)[11:13]),
                                             year_end=int(str(today)[0:4]), month_end=int(str(today)[6]),
                                             day_end=int(str(today)[8:10]), hour_end=int(str(today)[11:13]), cat=0,
                                             geo='',
                                             gprop='',
                                             sleep=sleep).sum(axis=1, skipna=True).values)) + (sum(
            pytrends.get_historical_interest([str(crypto) + " token"], year_start=int(str(fromDate)[0:4]),
                                             month_start=int(str(fromDate)[6]), day_start=int(str(fromDate)[8:10]),
                                             hour_start=int(str(fromDate)[11:13]),
                                             year_end=int(str(today)[0:4]), month_end=int(str(today)[6]),
                                             day_end=int(str(today)[8:10]), hour_end=int(str(today)[11:13]), cat=0,
                                             geo='',
                                             gprop='',
                                             sleep=sleep).sum(axis=1, skipna=True).values))

    def generateTrendingCryptosResultsDictsAndStrings(self, searches, values, prices, startDate, fromDate):
        d = dict(zip(searches, values))
        d2 = dict(zip(searches, prices))
        trendingCryptosResultsDict = {x: y for x, y in d.items() if y > 0}
        priceCryptosResultsDict = {x: y for x, y in d2.items() if y > 0}
        trendingCryptosResultsString = (
                "year_start=" + (str(fromDate)[0:4]) + ", month_start=" + (str(fromDate)[6]) + ", day_start=" + (
            str(fromDate)[8:10]) + ", hour_start=" + (str(fromDate)[11:13])
                + ", year_end=" + (str(startDate)[0:4]) + ", month_end=" + (str(startDate)[6]) + ", day_end=" + (
                    str(startDate)[8:10]) + ", hour_end=" + (str(startDate)[11:13])
                + " RESULTS: " + self.getResultsStringFromCryptoDict(trendingCryptosResultsDict))
        return priceCryptosResultsDict, trendingCryptosResultsDict, trendingCryptosResultsString

    def matchTrendingCryptosAndPrices(self):
        if self.checkIfCmdIsWrong():
            return self.checkIfCmdIsWrong()
        startDate = datetime.datetime.strptime(self.parseCryptoCommand("startDate"), '%Y-%m-%d %H:%M:%S')
        fromDate = startDate - datetime.timedelta(hours=self.parseCryptoCommand("hoursBeforeNow"))
        r = self.getLatestCryptocurrencyListings(self.parseCryptoCommand("cryptoLimit"),
                                                 self.parseCryptoCommand("sortDirection"))
        searches = []
        values = []
        prices = []
        for i in range(len(r.data)):
            print(r.data[i]['symbol'])
            if "USD" in r.data[i]['symbol'] or ("Wrapped" in r.data[i]['name']) or ("wrapped" in r.data[i]['name']):
                time.sleep(15)
                continue
            prices.append(self.getPriceForCryptoAtTime(self.parseCryptoCommand("startDate"), r.data[i]['symbol']))
            searches.append(r.data[i]['symbol'] + " crypto")
            values.append(self.getCryptoInterest(r.data[i]['symbol'], r.data[i]['name'], fromDate, startDate, 3))
            print(values)
        return self.generateTrendingCryptosResultsDictsAndStrings(searches, values, prices, startDate, fromDate)

    def getResultsStringFromCryptoDict(self, d):
        return str(dict(sorted(d.items(), key=operator.itemgetter(1), reverse=True)))


if __name__ == "__main__":
    Executor(
        datetime.datetime.strptime("2021-08-07 00:00:00","%Y-%m-%d %H:%M:%S"), 336, 5, "desc").getResults()
