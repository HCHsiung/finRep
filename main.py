import parseFinRep as pfr
import readFinRep as rfr

stock_list=["6697","6752","6865"]

#從網頁爬取財報三表
pfr.parseFinRep(stock_list)
#讀取財報三表計算各項指標
rfr.readFinRep(stock_list)

