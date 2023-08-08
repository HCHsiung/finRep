import pandas as pd
import os
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

#繪製財報指標與股價散佈圖
def drawFigure(stock,s,p,toldf,tolVar,key):
    plt.subplots(figsize=(6,6))
    plt.scatter(toldf,tolVar)
    plt.rcParams['font.sans-serif']=['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus']=False
    plt.title(f'{stock}-{key}與股價散佈圖',fontsize=20)
    plt.xlabel(f'{key}%',fontsize=18)
    plt.ylabel(f'{stock}股價%',fontsize=18)
    plt.savefig(f'./{stock}/{stock}-{key}與股價散步圖')
    plt.show()

#讀取每日股價與財報指標
#def analyzeFinRep(stock_codes):
key=["流動比率","速動比率","毛利率","利益率","淨利率","EPS","營業現金流","投資現金流","籌資現金流"]
dates=["112/05/12","112/03/14","111/11/11","111/08/12"]
stock_codes=["6697","6752","6865"]

for stock in stock_codes:
    toldf=[]
    tolVar=[]
    #讀取各項財報指標及每日股價
    #bsdf=pd.read_csv(f'./{stock}/{stock}-BSCollection.csv',encoding='utf-8-sig')
    #cidf=pd.read_csv(f'./{stock}/{stock}-CICollection.csv',encoding='utf-8-sig')
    #cfdf=pd.read_csv(f'./{stock}/{stock}-CFCollection.csv',encoding='utf-8-sig')
    frdf=pd.read_csv(f'./{stock}/{stock}-FRCollection.csv',encoding='utf-8-sig')
    
    stock_price=pd.read_csv(f'./{stock}/{stock}_DailyPrice.csv',encoding='utf-8-sig')
    stock_pri_idx=stock_price.columns
    
    for i in range(0,9):
        toldf.append(frdf.loc[i].values.tolist())
    #print(toldf)
    
    
    #取得財報公布當日的股價漲跌幅度(%)
    tolVar=[]
    for date in dates:
        if date in stock_price[stock_pri_idx[0]].unique():
            tarDate=stock_price.loc[stock_price[stock_pri_idx[0]]==date]
            preDate=stock_price.loc[tarDate.index-1]
            prePrice=float(preDate.iloc[0][stock_pri_idx[6]])
            todayVar=float(tarDate.iloc[0][stock_pri_idx[7]])
            varRatio=todayVar/prePrice*100
            tolVar.append(float(f'{varRatio:.2f}'))
    print(tolVar)
    
    """
    print(stock)
    for i in range(0,9):
        if stock=="6865":
            toldf[i].pop(-1)
            toldf[i].pop(-1)
            s,p=pearsonr(toldf[i],tolVar)
            print(f'{key[i]}: s={s:.3f}, p={p:.3f}')
            #drawFigure(stock,s,p,toldf[i],tolVar,key[i])
        else:
            s,p=pearsonr(toldf[i],tolVar)
            print(f'{key[i]}: s={s:.3f}, p={p:.3f}')
            #drawFigure(stock,s,p,toldf[i],tolVar,key[i])"""