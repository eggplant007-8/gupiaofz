import tushare as ts
import time
import math

#定义配置
up_range = 0.02
down_range = 0.04
mid_range = 0.02
block_transaction = True
# 大宗买入交易与大宗卖出交易的倍数
block_proportion = 1.5
# 设置大宗交易阀值，10000只
# block_threshold = 10000
# 设置大宗交易金额阀值，500万元
block_price = 5000000
date_now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
def dingzi_model(open, high, low, close, pctChg, up_check=False):
    if up_check:
        if pctChg < 0:
            return False
    if open == 0:
        return False

    if pctChg < 0:
        high_value = close
        low_value = open
    else:
        high_value = open
        low_value = close

    print(abs(high - high_value) / open)
    if(abs(high - high_value) / open >  up_range):
        return False

    print('比例：', abs(low - low_value) / abs(close - open))
    if(abs(low - low_value) / abs(close - open) < 2):
        return False

    # if(abs(close - open) / open > mid_range):
    #     return False
    #
    # if(abs(low - low_value) / open < down_range):
    #     return False

    return True

def check_block_transaction(stock_code, stock_price):
    buy_count = 0
    sell_count = 0
    block_threshold = math.ceil(block_price / (stock_price * 100))
    df = ts.get_sina_dd(stock_code, date=date_now, vol=block_threshold)
    if df is None:
        print('无操作大于' + str(block_price) + '元的stock')
        return False
    # print(df)
    for i in range(0,len(df)):
        if(df['type'][i] == '卖盘'):
            sell_count = sell_count + df['volume'][i]
        elif(df['type'][i] == '买盘'):
            buy_count = buy_count + df['volume'][i]
    mess =  '买盘：' + str(buy_count) + '卖盘：' + str(sell_count)
    print(mess)
    if(buy_count > block_proportion * sell_count):
        return True
    return False

#获取当天钉子模型
def get_today_dingzi_stock():

    results = ts.get_today_all()
    date_list = []

    print('--------------------')
    j = 0
    for i in range(0,len(results)):
        print(results['code'][i], results['name'][i], results['open'][i], results['high'][i], results['low'][i], results['trade'][i], results['changepercent'][i])
        print('钉子模型：', dingzi_model(results['open'][i], results['high'][i], results['low'][i], results['trade'][i], results['changepercent'][i], block_transaction))
        if dingzi_model(results['open'][i], results['high'][i], results['low'][i], results['trade'][i], results['changepercent'][i], block_transaction):
            if block_transaction:
                print(results['code'][i], results['name'][i], end='')
                if(check_block_transaction(results['code'][i], results['name'][i], results['trade'][i])):
                    date_list.append([results['code'][i], results['name'][i]])
                    j = j + 1
            else:
                date_list.append([results['code'][i], results['name'][i]])
                j = j + 1
    print(date_list)
    print('目前共' + str(j) + "只股票符合钉子模型")

#获取当天大宗交易模型
def get_today_block_transaction_stock():

    results = ts.get_today_all()
    date_list = []

    print('--------------------')
    j = 0
    for i in range(0,len(results)):
        if check_block_transaction(results['code'][i], results['name'][i]):
                date_list.append([results['code'][i], results['name'][i]])
                j = j + 1
        print('已处理完' + str(i) + '支股票')
    print(date_list)
    print('目前共' + str(j) + "只股票符合大宗交易模型")


# get_today_dingzi_stock()
is_ok = 0
i = 0
while is_ok == 0 and i < 100:
    try:
        get_today_dingzi_stock()
        # get_today_block_transaction_stock()
        is_ok = 1
    except:
        i = i + 1
        print('over')