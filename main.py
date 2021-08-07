import json
import os

import historicalCryptoTrendsGenerator
import cryptoInvestmentAdvisor
import tools
from datetime import datetime
import pymongo


def createResponseCSVs(generate,startDate,hours,cryptoLimit,dollars):
    if(generate):
        cryptoInvestmentAdvisor.Executor(historicalCryptoTrendsGenerator.Executor(
            startDate,hours,cryptoLimit,"desc").getResults(),0,dollars).getResults()

if __name__ == "__main__":
    print('creating CSVs')
    #createResponseCSVs()
