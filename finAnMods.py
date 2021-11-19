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
#get_financials is 2 times faster than get_balancesheet, get_incomestatement and get_cashflow
def getFinData(lst,year):
    finData = pd.DataFrame()
    bsData = pd.DataFrame()
    isData = pd.DataFrame()
    cfData = pd.DataFrame()
    cIData = pd.DataFrame()
    qDData = pd.DataFrame()
    for i in lst:
        fin = yf.get_financials(i)
        bsiData = fin['yearly_balance_sheet']
        isiData = fin['yearly_income_statement']
        cfiData = fin['yearly_cash_flow']
        qDiData = pd.DataFrame(yf.get_quote_data(i), index=[i])
        cIiData = yf.get_company_info(i)
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
        qDData = qDData.append(qDiData)
        cIData = cIData.append(cIiData.T)
    finData = pd.concat([bsData.T,isData.T,cfData.T])
    finData.columns = lst
    cIData.index = lst
    finData = pd.concat([finData.T, qDData, cIData], axis=1)
    finData = finData.T.drop_duplicates()
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
    df['grossProfitMargin'] = df['grossProfit']/df['totalRevenue']
    df['totalNonCurrentAssets'] = df['totalAssets'] - df['totalCurrentAssets']
    df['totalNonCurrentLiabilities'] = df['totalLiab'] - df['totalCurrentLiabilities']
    df['quick'] = (df['totalCurrentAssets']-df['inventory'])/df['totalCurrentLiabilities']
    df['capEx/netIn'] = df['capitalExpenditures']/df['netIncome']
    dfClean = pd.DataFrame()
    dfClean = df[['sector','industry','fullTimeEmployees','country','website'\
        ,'fullExchangeName','marketCap','regularMarketPreviousClose','epsTrailingTwelveMonths','trailingPE'\
        ,'totalAssets','totalCurrentAssets','cash','inventory','goodWill','totalLiab','totalCurrentLiabilities','totalNonCurrentLiabilities'\
        ,'currentRatio','quick','totalStockholderEquity'\
        ,'totalRevenue','grossProfit','netIncome','capitalExpenditures','roe','nettoDebtRate','grossProfitMargin','netProfitMargin' \
        ,'capEx/netIn','solvencyRatio','roa','roce']]
    return dfClean