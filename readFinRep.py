import pandas as pd
import os

#讀取資產負債表
def readBalanceSheet(stock,year,quarter):
    #資產負債-流動比率、速動比率
    #檢查有無資產負債表
    path=f'./{stock}'
    filename=f'{stock}-{year}Q{quarter}BS.csv'
    if not os.path.exists(f'{path}/{filename}'):
        print(f'{filename} does not exist.')
    else:
        print(f'read {filename}')
        bsdata=pd.read_csv(f'{path}/{filename}',encoding="utf-8-sig")
        bscol=bsdata.columns
        #以會計代號獲取各季度金額
        curAssets=bsdata.loc[bsdata[bscol[0]]=='11XX']
        curLiability=bsdata.loc[bsdata[bscol[0]]=='21XX']
        if '130X' in bsdata[bscol[0]].unique():
            inventory=bsdata.loc[bsdata[bscol[0]]=='130X']
        else:
            print(f'{filename} does not have "130X"')
            
        if '1410' in bsdata[bscol[0]].unique():
            prepayment=bsdata.loc[bsdata[bscol[0]]=='1410']
        else:
            print(f'{filename} does not have "1410"')
        newAsset=int(curAssets.iloc[0][bscol[2]])
        newLiability=int(curLiability.iloc[0][bscol[2]])
        if '130X' in bsdata[bscol[0]].unique():
            newInventory=int(inventory.iloc[0][bscol[2]])
        else:
            newInventory=0
        
        if '1410' in bsdata[bscol[0]].unique():
            newPrepayment=int(prepayment.iloc[0][bscol[2]])
        else:
            newPrepayment=0
        #流動比率
        currentRatio=newAsset/newLiability
        #速動比率
        quickRatio=(newAsset-newInventory-newPrepayment)/newLiability
        #return [f'{year}Q{quarter}',f'{currentRatio:.2f}',f'{quickRatio:.2f}']
        return [f'{currentRatio:.2f}',f'{quickRatio:.2f}']
    
#讀取綜合損益表
def readComprehensiveIncome(stock,year,quarter):
    #綜合損益-毛利率、利益率、淨利率
    #檢查有無綜合損益表
    path=f'./{stock}'
    filename=f'{stock}-{year}Q{quarter}CI.csv'
    if not os.path.exists(f'{path}/{filename}'):
        print(f'{filename} does not exist.')
    else:
        print(f'read {filename}')
        cidata=pd.read_csv(f'{path}/{filename}',encoding="utf-8-sig")
        cicol=cidata.columns
        #以會計代號獲取各季度金額
        tolRevenue=cidata.loc[cidata[cicol[0]]==4000]
        tolCosts=cidata.loc[cidata[cicol[0]]==5000]
        tolExpenses=cidata.loc[cidata[cicol[0]]==6000]
        tolNonOperating=cidata.loc[cidata[cicol[0]]==7000]
        tolTax=cidata.loc[cidata[cicol[0]]==7950]
        baseEPS=cidata.loc[cidata[cicol[0]]==9750]
        newRevenue=int(tolRevenue.iloc[0][cicol[2]])
        newCosts=int(tolCosts.iloc[0][cicol[2]])
        newExpenses=int(tolExpenses.iloc[0][cicol[2]])
        newNonOp=-float(str(tolNonOperating.iloc[0][cicol[2]]).strip("()"))
        newTax=-float(str(tolTax.iloc[0][cicol[2]]).strip("()"))
        newEPS=float(baseEPS.iloc[0][cicol[2]])
        #毛利率
        grossProfit=(newRevenue-newCosts)/newRevenue*100
        #利益率
        operatingIncome=(newRevenue-newCosts-newExpenses)/newRevenue*100
        #淨利率
        netIncome=(newRevenue-newCosts-newExpenses+newNonOp-newTax)/newRevenue*100
        #return [f'{year}Q{quarter}',f'{grossProfit:.2f}',f'{operatingIncome:.2f}',f'{netIncome:.2f}',f'{newEPS:.2f}']
        return [f'{grossProfit:.2f}',f'{operatingIncome:.2f}',f'{netIncome:.2f}',f'{newEPS:.2f}']

#讀取現金流量表
def readCashFlows(stock,year,quarter):
    #營業、投資、籌資現金流
    #檢查有無綜合損益表
    path=f'./{stock}'
    filename=f'{stock}-{year}Q{quarter}CF.csv'
    if not os.path.exists(f'{path}/{filename}'):
        print(f'{filename} does not exist.')
    else:
        print(f'read {filename}')
        cfdata=pd.read_csv(f'{path}/{filename}',encoding="utf-8-sig")
        cfcol=cfdata.columns
        #以會計代號獲取各季度金額
        operateCF=cfdata.loc[cfdata[cfcol[0]]=='AAAA']
        investCF=cfdata.loc[cfdata[cfcol[0]]=='BBBB']
        financeCF=cfdata.loc[cfdata[cfcol[0]]=='CCCC']
        newOper=int(operateCF.iloc[0][cfcol[2]].strip("()"))
        newInve=int(investCF.iloc[0][cfcol[2]].strip("()"))
        newFina=int(financeCF.iloc[0][cfcol[2]].strip("()"))
        tolCF=newOper+newInve+newFina
        #營業現金流比例
        operRatio=newOper/tolCF*100
        #投資現金流比例
        inveRatio=newInve/tolCF*100
        #籌資現金流比例
        finaRatio=newFina/tolCF*100
        #return [f'{year}Q{quarter}',f'{operRatio:.2f}',f'{inveRatio:.2f}',f'{finaRatio:.2f}']
        return [f'{operRatio:.2f}',f'{inveRatio:.2f}',f'{finaRatio:.2f}']
    


def writeFinacialReports(stock, years, quarters):
    
    frdata=[["","流動比率","速動比率","毛利率%","利益率%","淨利率%","EPS","營業現金流%","投資現金流%","籌資現金流%"]]
    for i in range(0,4):
        frrow=[]
        frnumber=f'{years[i]}Q{quarters[i]}'
        frrow.append(frnumber)
        newBSRatio=readBalanceSheet(stock, years[i], quarters[i])
        for bsdata in newBSRatio:
            frrow.append(bsdata)
        
        newCIRatio=readComprehensiveIncome(stock, years[i], quarters[i])
        for cidata in newCIRatio:
            frrow.append(cidata)
        
        newCFRatio=readCashFlows(stock, years[i], quarters[i])
        for cfdata in newCFRatio:
            frrow.append(cfdata)
        
        frdata.append(frrow)
    
    #各季度流動比率、速動比率集成表輸出csv
    frtable=pd.DataFrame(frdata).transpose()
    frtable.columns=frtable.iloc[0]
    frtable=frtable.drop(0)
    print(frtable)
    frtable.to_csv(f'{stock}/{stock}-FRCollection.csv',encoding='utf-8-sig',index=False)

#讀取財報並輸出相關指標
years=["2023","2022","2022","2022"]
quarters=["1","4","3","2"]
stock_codes=["6697","6752","6865"]
for stock in stock_codes:
    writeFinacialReports(stock, years, quarters)
