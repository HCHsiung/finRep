"""
輸入股票代號、年分、季度取得財務報表
資產負債表 BalanceSheet
綜合損益表 ComprehensiveIncome
現金流量表 CashFlows
"""
import requests
import pandas as pd
import time
import os
from bs4 import BeautifulSoup

#檢查財報檔案
def checkFinancialReports(stock,year,quarter):
    #檢查是否已有資料夾
    path=f'./{stock}'
    if not os.path.exists(path):
        os.mkdir(path)

    table_list=["BS","CI","CF"]             #table簡稱
    flag=False
    #檢查是否已有財報三表
    for table in table_list:
        fileName=f'{stock}-{year}Q{quarter}{table}.csv'
        if not os.path.exists(f'{path}/{fileName}'):
            flag=True
    return flag

#
def getFinancialReports(stock,year,quarter):
    URL=""         
    #組成網址取得財報網頁並以BS4物件儲存
    if stock=="6865":
        URL = "https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID="+stock+"&SYEAR="+year+"&SSEASON="+quarter+"&REPORT_ID=A"
    else:
        URL = "https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID="+stock+"&SYEAR="+year+"&SSEASON="+quarter+"&REPORT_ID=C"
   
    response= requests.get(URL)
    response.encoding="big5"
    sp = BeautifulSoup(response.text, "lxml")
    ti=0
    while ti<3:
        #取得table標籤的內容
        datas = sp.select("table")[ti]
        #取得表格中文標頭
        t_headers=datas.select("th span.zh")
        headers_zh=[]
        for i in t_headers:
            headers_zh.append(i.text)
        headers_zh.pop(0)
        #取得會計項目中文名稱
        a_title=datas.select("td span.zh")
        title_zh=[]
        for i in a_title:
            title_zh.append(i.text)
        #取出儲存格資料並消除千分位符號再重排成表格
        rows=datas.select("tr")
        tableout=[]
        for row in rows:
            cols=row.select("td")
            rowout=[]
            for col in cols:
                rowout.append(col.text.replace(',',''))
            tableout.append(rowout)
        #排出空白儲存格
        tableout.pop(0)
        tableout.pop(0)
        #以中文替換中英混合的會計項目
        i=0
        for zh in title_zh:
           tableout[i][1]=zh
           i=i+1
        
        #以Dataframe輸出csv
        df=pd.DataFrame(tableout)
        df.columns=headers_zh
        path=f'./{stock}'
        table_list=["BS","CI","CF"]             #table簡稱
        fileName=f'{stock}-{year}Q{quarter}{table_list[ti]}.csv'
        df.to_csv(f'{path}/{fileName}',encoding='utf-8-sig',index=False)
        print(f'Save {fileName}')
        #做下個表,資產負債:0,綜合損益:1,現金流量:2
        ti=ti+1

#決定是否從網頁爬取財報
def finReportCrawler(stock,year,quarter):

    crawlerFlag=checkFinancialReports(stock, year, quarter)
    
    if crawlerFlag==True:
        getFinancialReports(stock, year, quarter)
    else:
        print(f'{stock}-{year}Q{quarter} all files exist.')

#依股票代號、年分、季度爬取財報
def parseFinRep(stock_codes):    
    years=["2023","2022","2022","2022"]
    quarters=["1","4","3","2"]
    
    for stock in stock_codes:
        for i in range(0,4):
            finReportCrawler(stock, years[i], quarters[i])
            time.sleep(3)
