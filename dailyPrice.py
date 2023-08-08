#每日股價
import requests
import pandas as pd
import time
import os

def getDailyStockValue(stock_no):
    #檢查是否已有資料夾
    path=f'./{stock_no}'
    if not os.path.exists(path):
        os.mkdir(path)

    # 指定日期範圍
    start_year = 111
    start_month = 6
    end_year = 112
    end_month = 6
    
    # 創建空的 DataFrame
    all_data = pd.DataFrame()
    
    # 迭代日期範圍
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            # 檢查是否在指定的日期範圍內
            if year == start_year and month < start_month:
                continue
            if year == end_year and month > end_month:
                continue
            
            # 格式化日期
            date = f'{year:03d}/{month:02d}'
    
            # 發送請求並解析資料
            url = f'https://www.tpex.org.tw/web/stock/aftertrading/daily_trading_info/st43_result.php?&stkno={stock_no}&d={date}'
            r = requests.get(url)
            data = r.json()
            columns = ['日期', '成交千股', '成交千元', '開盤', '最高', '最低', '收盤', '漲跌', '筆數']
            formated_data = pd.DataFrame(data['aaData'], columns=columns)
            
            # 加入到 all_data
            all_data = pd.concat([all_data, formated_data], ignore_index=True)
    
    # 儲存為 CSV 檔案
    filename = f'./{stock_no}/{stock_no}_DailyPrice.csv'
    all_data.to_csv(filename, index=False, encoding="utf-8-sig")
    
    print(f'Save {stock_no}_DailyPrice.csv')
    time.sleep(3)
    #function end

def dailyPrice(stock_List):
    # 要爬取的股票編號 6697-東捷 6752-叡揚 6865-偉康
    for stock in stock_List:
        getDailyStockValue(stock)
    