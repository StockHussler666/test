#imports for getFinData function
from requests.api import get
import yahoo_fin.stock_info as yf
import pandas as pd

#function that asks stocktickers as input
def enterTickers():
    lst = []
    dy = input('do you want to add a ticker? (y/n) ')
    while dy == 'y':
        lst.append(input('enter ticker: '))
        dy = input('do you want to add a ticker? (y/n) ')
    return lst

#function that puts balance sheet, income statement and cash flow data in a dataframe from given tickers
#the input is a list of tickers and a year, the output is a pandas dataframe with the tickers as indeces and the finance stats as columns
def getFinData(lst,year):
    finData = pd.DataFrame()
    bsData = pd.DataFrame()
    isData = pd.DataFrame()
    cfData = pd.DataFrame()
    for i in lst:
        bsiData = yf.get_balance_sheet(i)
        isiData = yf.get_income_statement(i)
        cfiData = yf.get_cash_flow(i)
        fData = pd.DataFrame()
        strlst = []
        for i in bsiData.columns:
            strlst.append(str(i)[0:4])
        bsData = bsData.append(bsiData.iloc[:, strlst.index(year)])
        for i in isiData.columns:
            strlst.append(str(i)[0:4])
        isData = isData.append(isiData.iloc[:, strlst.index(year)])
        for i in cfiData.columns:
            strlst.append(str(i)[0:4])
        cfData = cfData.append(cfiData.iloc[:, strlst.index(year)])
    finData = pd.concat([bsData.T,isData.T,cfData.T])
    finData.columns = lst
    finData = finData.drop_duplicates()
    return finData.T

#function that adds ratios and cleans up the dataframe
#the input is a pandas dataframe [amount of tickers x finan stats], the ouput is a pandas dataframe [amount of tickers x finan stats]
def addRatios(df):
    df['currentRatio'] = df['totalCurrentAssets']/df['totalCurrentLiabilities']
    df['solvencyRatio'] = df['totalStockholderEquity']/df['totalAssets']
    df['nettoDebtRate'] = (df['totalAssets'] - df['totalStockholderEquity'] - df['totalCurrentAssets'])/df['totalStockholderEquity']
    df['roa'] = df['netIncome']/df['totalAssets']
    df['roe'] = df['netIncome']/df['totalStockholderEquity']
    df['roce'] = df['ebit']/(df['totalAssets'] - df['totalCurrentLiabilities'])
    df['netProfitMargin'] = df['netIncome']/df['totalRevenue']
    dfClean = pd.DataFrame()
    dfClean = df[['currentRatio','solvencyRatio','nettoDebtRate','roa','roe','roce','netProfitMargin','totalAssets','totalCurrentAssets','totalLiab','totalCurrentLiabilities','totalStockholderEquity']]
    return dfClean