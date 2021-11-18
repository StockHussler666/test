import yahoo_fin.stock_info as yf
import pandas as pd
from pandas import ExcelWriter
import finAnMods as fam

tcks1 = fam.enterTickers()
print(tcks1)
#tcks2 = ['WMT','AMZN','COST','WBA','KR','HD','JD','CRRFY','TSCDY','TGT']

dataf = fam.getFinData(tcks1,'2020')

datac = fam.addRatios(dataf).T

name = 'test'
for i in tcks1: name = name + '-' + i 

datac.to_csv('%s.xlsx'%(name))