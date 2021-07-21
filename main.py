import historicalCryptoTrendsGenerator
import cryptoInvestmentAdvisor
import tools

def createResponseCSVs(generate,startDate,hours,cryptoLimit,dollars):
    if(generate):
        cryptoInvestmentAdvisor.getResults(historicalCryptoTrendsGenerator.getResults(
            startDate,hours,cryptoLimit)
                                           ,dollars)
    else:
        cryptoInvestmentAdvisor.getResults(tools.generateHistoricalCryptoTrendsGeneratorResultsFromCSV(startDate)
                                           ,dollars)
