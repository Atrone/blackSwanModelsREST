import historicalCryptoTrendsGenerator
import datetime
import time
from typing import List, Dict
import tools


def getTotalOverTrendForCryptos(result):
    totalOverTrend = {}
    for key, value in result['price'].items():
        for key1, value1 in result['trends'].items():
            if key == key1:
                totalOverTrend[key1] = (abs((sum(result['trends'].values())/value1)))
                break
    return totalOverTrend


def getBuysForCryptosAccordingToTrends(result,totalOverTrend,dollarAmount):
    buys = []
    for key, value in result['price'].items():
        for key1, value1 in result['trends'].items():
            if key == key1:
                buys.append({key1:(abs(totalOverTrend[key1]/sum(totalOverTrend.values()))*dollarAmount/value)})
                break
    print(buys)
    return buys


def getBuysForCryptos(result,dollarAmount):
    buys = []
    for key, value in result['price'].items():
        for key1, value1 in result['trends'].items():
            if key == key1:
                buys.append({key1:(dollarAmount/len(result['price'].keys()))/value})
                break
    print(buys)
    return buys


def getCurrentPortfolioWorthFromBuys(buys):
    total = 0
    for buy in buys:
        for key, value in buy.items():
            total += value*historicalCryptoTrendsGenerator.getPriceForCryptoAtTime(str(datetime.datetime.now()),key.split(" ")[0])
    print(total)
    return total

    # total / trend proportionate to price / crypto
    # it's a hype market

results = [{'price': {'BTC crypto': 31796.810138247813, 'ETH crypto': 1895.5521368013024, 'USDT crypto': 1.00062070229279, 'BNB crypto': 302.4804892006454, 'ADA crypto': 1.18369795434564, 'USDC crypto': 1.00057362658003, 'XRP crypto': 0.58792189594955, 'DOGE crypto': 0.18223326670003, 'DOT crypto': 12.68214591960496, 'BUSD crypto': 1.00048936213312}, 'trends': {'BTC crypto': 60157.0, 'ETH crypto': 60325, 'USDT crypto': 53684, 'BNB crypto': 56661.0, 'ADA crypto': 58618.0, 'USDC crypto': 37877, 'XRP crypto': 57397.0, 'DOGE crypto': 56497.0, 'DOT crypto': 41280, 'BUSD crypto': 39459}, 'date': datetime.datetime(2021, 7, 19, 0, 0)}]

def getResults(results : List[Dict], amountToInvest):
    for result in results:

        print(result['date'])

        totalOverTrend = getTotalOverTrendForCryptos(result)

        buysAccordingToTrends = getBuysForCryptosAccordingToTrends(result,totalOverTrend,amountToInvest)

        tools.updateCSVForListOfDict(tools.mergeListOfDicts(buysAccordingToTrends), "trendBuys"+
                                str(datetime.datetime.now().month)+
                                str(datetime.datetime.now().day)+".csv")

        print(getCurrentPortfolioWorthFromBuys(buysAccordingToTrends))

        buys = getBuysForCryptos(result, amountToInvest)

        tools.updateCSVForListOfDict(tools.mergeListOfDicts(buys), "nonTrendBuys"+
                                str(datetime.datetime.now().month)+
                                str(datetime.datetime.now().day)+".csv")

        print(getCurrentPortfolioWorthFromBuys(buys))

        time.sleep(65)

if __name__ == "__main__":
    getResults(results,100)
