# -*- encoding: utf8 -*-
# 计算首日涨停板后， 第二天开盘买入的获利概率
from jqdatasdk import *
auth('13723401432','Huawei123')
# 获取所有股票代号
stocks = list(get_all_securities(['stock']).index)
# 获取所有股票价格
allprices = get_price(stocks, start_date='2017-09-01',end_date='2019-12-01', frequency='daily')
'''
如果是多支股票, 则返回[pandas.Panel]对象, 里面是很多[pandas.DataFrame]对象, 索引是行情字段['date','open','high','low','close']
每个[pandas.DataFrame]的行索引是[datetime.datetime]对象, 列索引是股票代号. 比如get_price(['000300.XSHG', '000001.XSHE'])['open']
'''
# 判断当天出现收盘涨停后，计算第二天的开盘价是否比第三天的高点价低
num = 0
# 判断当天出现收盘涨停后，计算第三天的高点比第二天的开盘价高1%的数字
onepercent = 0
# 总数字
n = 0
# 找出2018-01-01之后的第一个交易日
index = 0
for i in range(len(allprices['close']['000001.XSHE'])):
    if (allprices['close']['000001.XSHE'].index[i].year == 2018 and allprices['close']['000001.XSHE'].index[i].month == 1):
        index = i
        break

# 计算60日线
def calculate60dayLine(pricesOfStock, index):
    if (index < 60):
        return None
    count = 0
    for i in range(1, 61):
        count = count + pricesOfStock[index - i]
    return count / 60

# 计算20日线
def calculate20dayLine(pricesOfStock, index):
    if (index < 20):
        return None
    count = 0
    for i in range(1, 21):
        count = count + pricesOfStock[index - i]
    return count / 20

for stock in stocks:
    lastday = 0
    for i in range(index, len(allprices['open'][stock]) - 4):
        # 计算当天是否涨停, 当天收盘价加1分钱， 再除以前一天价格大于1.1的认为是涨停
        if ((allprices['close'][stock][i] + 0.01) / allprices['close'][stock][i-1] >= 1.1):
            priceOf20dayLine = calculate20dayLine(allprices['close'][stock], i)
            priceOf60dayLine = calculate60dayLine(allprices['close'][stock], i)
            if (allprices['close'][stock][i] < priceOf60dayLine or priceOf20dayLine < priceOf60dayLine):
                continue
            if ((allprices['low'][stock][i+1] + 0.01)/allprices['close'][stock][i] >= 1.1):
                continue; # 如果第二天的最低价都是涨停价，则认为是封板无法买入
            n = n+1
            if (allprices['open'][stock][i+1] < allprices['high'][stock][i+2]):
                num = num + 1
            if (allprices['high'][stock][i+2] / allprices['open'][stock][i+1] >= 1.01):
                onepercent = onepercent + 1

# 只排除60日线时，计算结果是涨停16332次，次日上涨9672次，超过1%的8819次
# 排除60日线和满足20日线大于60日线时， 计算结果是10045次涨停， 6121次上涨，5631次超过1%