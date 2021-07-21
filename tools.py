import csv
import os.path
import json


from collections import ChainMap


def mergeListOfDicts(listOfDicts):
    return [dict(ChainMap(*listOfDicts))]


def seeIfFileExists(fname):
    return os.path.isfile(fname)


def dateTimeToMonthTDay(datetime):
    if (len(str(datetime.month)) == 1 and len(str(datetime.day)) == 1):
        return "0" + str(datetime.month) + "T0" + str(datetime.day)
    elif len(str(datetime.day)) == 1:
        return str(datetime.month) + "T0" + str(datetime.day)
    elif len(str(datetime.month)) == 1:
        return "0" + str(datetime.month) + "T" + str(datetime.day)
    else:
        return str(datetime.month) + "T" + str(datetime.day)


def updateCSVForListOfDict(listOfDictionary, fname):

    fileExists = seeIfFileExists(fname)

    keys = listOfDictionary[0].keys()

    with open(fname, "a") as a_file:
        dict_writer = csv.DictWriter(a_file,fieldnames=keys)

        if not fileExists:
            dict_writer.writeheader()
        dict_writer.writerows(listOfDictionary)

def dateTimeToMonthDay(date):
    return str((date).month) + str((date).day)

def getListOfDictFromCSV(fname):
    with open(fname) as f:
        a = [{k: float(v) for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]
    return a


def generateHistoricalCryptoTrendsGeneratorResultsFromCSV(date):

    prices = getListOfDictFromCSV('price'+dateTimeToMonthTDay(date)+'.csv')
    trends = getListOfDictFromCSV('trends'+dateTimeToMonthTDay(date)+'.csv')
    results = []

    for price, trend in zip(prices, trends):
        results.append({})
        results[prices.index(price)]['price'] = price
        results[prices.index(price)]['trends'] = trend
        results[prices.index(price)]['date'] = date
    return results


def make_json(csvFilePath):
    with open(csvFilePath, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        data_list = [row for row in reader]
    data = [dict(zip(data_list[0], row)) for row in data_list]
    data.pop(0)
    s = json.dumps(data)
    print(s)
    return s

