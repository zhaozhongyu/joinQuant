from jqdatasdk import *
auth('13723401432','Huawei123')
'''
上证: XSHG
深证: XSHE
上证指数代码:
华夏上证50: 510050
创业板ETF： 159952
df = get_all_securities(['etf']) 获取etf
'''
code= "510050.XSHG"
price = get_price('510050.XSHG', start_date='2015-01-01',end_date='2019-12-31', frequency='daily')
# 买入时, 按high计价, 卖出时按low计价
buyPrice = price["high"]
sellPrice = price["low"]
# 假设每月投入10000, 数组第一个字段存放成本, 第二个字段存放当前持有, 第三个字段存放计算出的价格, 每个月的第一个交易日买入
# 用法 index 存放日期, values存放价格
month = 1
data = [[0, 0, 0]]
for i in range(len(buyPrice)):
    if (buyPrice.index[i].month != month):
        continue
    if (month < 12):
        month = month +1
    else:
        month = 1
    num = 10000 // buyPrice[i] + data[len(data) - 1][1]
    cost = data[len(data) - 1][0] + 10000
    worth = num * sellPrice[i]
    data.append([cost, num, worth])

print(data[len(data) - 1])