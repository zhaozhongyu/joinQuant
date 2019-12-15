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
price = get_price('510050.XSHG', start_date='2007-01-01',end_date='2019-12-01', frequency='daily')
# 买入时, 按high计价, 卖出时按low计价
buyPrice = price["high"]
sellPrice = price["low"]

# 用法 index 存放日期, values存放价格
begin_day = "2007-01-01"
