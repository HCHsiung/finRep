import parseFinRep as pfr
import readFinRep as rfr
import analyzeFinRep as afr
import dailyPrice as dp

stock_list=["6697","6752","6865"]

#從網頁爬取財報三表
pfr.parseFinRep(stock_list)
#讀取財報三表計算各項指標
rfr.readFinRep(stock_list)
#獲得每日股價
dp.dailyPrice(stock_list)
#財報指標對股價的相關係數
afr.analyzeFinRep(stock_list)
