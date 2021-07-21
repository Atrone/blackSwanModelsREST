from coinmarketcapapi import CoinMarketCapAPI
from pytrends.request import TrendReq
import datetime
import operator
import tools
from typing import List, Dict

def getPriceForCryptoAtTime(startDate,crypto):
    cmc = CoinMarketCapAPI('c47f6c83-d986-4e65-a540-10cd8f1c0e45')
    price = cmc.tools_priceconversion(amount=1, symbol=crypto, time=datetime.datetime.fromisoformat(startDate))
    return price.data['quote']['USD']['price']


def parseCryptoCommand(cmd, parameter):
    if parameter == "hoursBeforeNow":
        return int(cmd.split(" ")[0])
    elif parameter == "cryptoLimit":
        return int(cmd.split(" ")[1])
    elif parameter == "sortDirection":
        return cmd.split(" ")[2]
    elif parameter == "startDate":
        return cmd.split(" ")[3] + " " + cmd.split(" ")[4]
    else:
        raise ValueError("This command requires hoursBeforeNow, cryptoLimit, or sortDirection for parameter")


def getLatestCryptocurrencyListings(limit,sortDir):
    cmc = CoinMarketCapAPI('c47f6c83-d986-4e65-a540-10cd8f1c0e45')
    return cmc.cryptocurrency_listings_latest(limit=limit,sort_dir=sortDir)


def getCryptoInterest(crypto,fromDate,today,sleep):
    pytrends = TrendReq(hl='en-US', tz=360)
    return sum(
        pytrends.get_historical_interest([str(crypto) + " crypto"], year_start=int(str(fromDate)[0:4]),
                                         month_start=int(str(fromDate)[6]), day_start=int(str(fromDate)[8:10]),
                                         hour_start=int(str(fromDate)[11:13]),
                                         year_end=int(str(today)[0:4]), month_end=int(str(today)[6]),
                                         day_end=int(str(today)[8:10]), hour_end=int(str(today)[11:13]), cat=0, geo='',
                                         gprop='',
                                         sleep=sleep).sum(axis=1, skipna=True).values) + (sum(
        pytrends.get_historical_interest([str(crypto) + " coin"], year_start=int(str(fromDate)[0:4]),
                                         month_start=int(str(fromDate)[6]), day_start=int(str(fromDate)[8:10]),
                                         hour_start=int(str(fromDate)[11:13]),
                                         year_end=int(str(today)[0:4]), month_end=int(str(today)[6]),
                                         day_end=int(str(today)[8:10]), hour_end=int(str(today)[11:13]), cat=0, geo='',
                                         gprop='',
                                         sleep=sleep).sum(axis=1, skipna=True).values)) + (sum(
        pytrends.get_historical_interest([str(crypto) + " token"], year_start=int(str(fromDate)[0:4]),
                                         month_start=int(str(fromDate)[6]), day_start=int(str(fromDate)[8:10]),
                                         hour_start=int(str(fromDate)[11:13]),
                                         year_end=int(str(today)[0:4]), month_end=int(str(today)[6]),
                                         day_end=int(str(today)[8:10]), hour_end=int(str(today)[11:13]), cat=0, geo='',
                                         gprop='',
                                         sleep=sleep).sum(axis=1, skipna=True).values))


def getResultsStringFromCryptoDict(d):
    return str(dict(sorted(d.items(), key=operator.itemgetter(1), reverse=True)))


def checkIfCmdIsWrong(cmd):
    if(len(cmd.split(" ")) != 5):
        return "Enter # of hours before start date," \
               " # of crypto limit, asc or desc," \
               " and start date, like so: /cryptos 1 10 asc 2021-07-17 00:00:00"
    return 0


def generateTrendingCryptosResultsDictsAndStrings(searches, values, prices, startDate, fromDate):
    d = dict(zip(searches, values))
    d2 = dict(zip(searches, prices))
    trendingCryptosResultsDict = {x: y for x, y in d.items() if y > 0}
    priceCryptosResultsDict = {x: y for x, y in d2.items() if y > 0}
    trendingCryptosResultsString = (
                "year_start=" + (str(fromDate)[0:4]) + ", month_start=" + (str(fromDate)[6]) + ", day_start=" + (
        str(fromDate)[8:10]) + ", hour_start=" + (str(fromDate)[11:13])
                + ", year_end=" + (str(startDate)[0:4]) + ", month_end=" + (str(startDate)[6]) + ", day_end=" + (
                str(startDate)[8:10]) + ", hour_end=" + (str(startDate)[11:13])
                + " RESULTS: " + getResultsStringFromCryptoDict(trendingCryptosResultsDict))
    return priceCryptosResultsDict, trendingCryptosResultsDict, trendingCryptosResultsString


def matchTrendingCryptosAndPrices(cmd):
    if checkIfCmdIsWrong(cmd):
        return checkIfCmdIsWrong(cmd)
    startDate = datetime.datetime.strptime(parseCryptoCommand(cmd,"startDate"),'%Y-%m-%d %H:%M:%S')
    fromDate = startDate - datetime.timedelta(hours=parseCryptoCommand(cmd,"hoursBeforeNow"))
    r = getLatestCryptocurrencyListings(parseCryptoCommand(cmd,"cryptoLimit"),parseCryptoCommand(cmd,"sortDirection"))
    searches = []
    values = []
    prices = []
    for crypto in r.data:
        print(crypto['symbol'])
        prices.append(getPriceForCryptoAtTime(parseCryptoCommand(cmd,"startDate"),crypto['symbol']))
        searches.append(crypto['symbol'] + " crypto")
        values.append(getCryptoInterest(crypto['symbol'], fromDate, startDate, 3))
        print(values)
    return generateTrendingCryptosResultsDictsAndStrings(searches, values, prices, startDate, fromDate)


def getCryptosPriceAndTrendsFromDateEveryXHoursTillToday(date,hours,limit,results):
    while date < datetime.datetime.now():
        print(date)
        priceResultsDictionary, resultsDictionary, resultsString = \
            matchTrendingCryptosAndPrices(str(hours) + " " + str(limit) + " desc " + str(date))
        results.append({'price': priceResultsDictionary, 'trends': resultsDictionary, 'date': date})
        date = date + datetime.timedelta(hours=hours)
        print(results)
    return results


def getListOfDictionariesAtKey(key, listOfDictInDict):
    return [dictInDict[key] for dictInDict in listOfDictInDict]


def getResults(date,xHours,limit) -> List[Dict]:
    results = []
    results = getCryptosPriceAndTrendsFromDateEveryXHoursTillToday(date, xHours, limit, results)
    print(results)
    for key in results[0].keys():
        if key != 'date':
            tools.updateCSVForListOfDict(getListOfDictionariesAtKey(key, results),
                                   str(key) + str(results[0]['date'])[5:10].replace("-", "T") + ".csv")
    return results
