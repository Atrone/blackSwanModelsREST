import historicalCryptoTrendsGenerator
import datetime
import time

import tools


class Executor:
    def __init__(self, results, command, amountToInvest):
        self.results = results
        self.command = command
        self.amountToInvest = amountToInvest
        self.Advisor = Advisor(self.results, self.amountToInvest)

    def loopThroughResult(self, result):
        options = {0: self.Advisor.getBuysForCryptosAccordingToTrendsInverse,
                   1: self.Advisor.getBuysForCryptosAccordingToTrends
                   }
        buys = []
        for key, value in result['price'].items():
            for key1, value1 in result['trends'].items():
                if key == key1:
                    self.Advisor.prices[key] = (
                        historicalCryptoTrendsGenerator.CryptoDataCollector().getPriceForCryptoAtTime(
                            str(datetime.datetime.now()),
                            key.split(" ")[0]))
                    buys.append(options[self.command](result, key1, value))
                    time.sleep(10)
        return buys

    def getResults(self):
        for result in self.results:
            buys = [{k: v for d in self.loopThroughResult(result) for k, v in d.items()}]
            if (self.command == 1):
                tools.updateCSVForListOfDict(buys, "trendBuys" + tools.dateTimeToMonthTDay((datetime.datetime.now())) + ".csv")
            else:
                tools.updateCSVForListOfDict(buys,
                                             "trendBuysInverse" + tools.dateTimeToMonthTDay((datetime.datetime.now())) + ".csv")


# each advice function should be like this: if i were to buy at value, according to the algorithm,
# what would it be at self.price[key1]
class Advisor:
    def __init__(self, results, amountToInvest):
        self.results = results
        self.amountToInvest = amountToInvest
        self.prices = {}

    def getBuysForCryptosAccordingToTrends(self, result, key1, value):
        totalOverTrend = self.getTotalOverTrend(result)
        buy = (
            {key1: ((abs(totalOverTrend[key1] / sum(totalOverTrend.values())) * self.amountToInvest / value)
                    * self.prices[key1])})
        print(buy)
        return buy

    def getBuysForCryptosAccordingToTrendsInverse(self, result, key1, value):
        trendOverTotal = self.getTrendOverTotal(result)
        buy = ({key1: ((abs(trendOverTotal[key1] / sum(trendOverTotal.values())) * self.amountToInvest / value)
                       * self.prices[key1])})
        print(buy)
        return buy

    def getTotalOverTrend(self, result):
        totalOverTrend = {}
        for key, value in result['price'].items():
            for key1, value1 in result['trends'].items():
                if key == key1:
                    totalOverTrend[key1] = (abs((sum(result['trends'].values()) / value1)))
        return totalOverTrend

    def getTrendOverTotal(self, result):
        trendOverTotal = {}
        for key, value in result['price'].items():
            for key1, value1 in result['trends'].items():
                if key == key1:
                    trendOverTotal[key1] = (abs((value1 / sum(result['trends'].values()))))
        return trendOverTotal


results = [{'price': {'BTC crypto': 31796.810138247813, 'ETH crypto': 1895.5521368013024,
                      'USDT crypto': 1.00062070229279, 'BNB crypto': 302.4804892006454,
                      'ADA crypto': 1.18369795434564, 'USDC crypto': 1.00057362658003,
                      'XRP crypto': 0.58792189594955, 'DOGE crypto': 0.18223326670003,
                      'DOT crypto': 12.68214591960496, 'BUSD crypto': 1.00048936213312},
            'trends': {'BTC crypto': 60157.0, 'ETH crypto': 60325, 'USDT crypto': 53684, 'BNB crypto': 56661.0,
                       'ADA crypto': 58618.0, 'USDC crypto': 37877, 'XRP crypto': 57397.0, 'DOGE crypto': 56497.0,
                       'DOT crypto': 41280, 'BUSD crypto': 39459}, 'date': datetime.datetime(2021, 7, 19, 0, 0)}]

if __name__ == "__main__":
    Executor(results=results, command=0, amountToInvest=100).getResults()
