# -*- coding: UTF-8 -*-
import talib
import numpy as np
import pandas as pd
import tushare as ts
import time
import math
from operator import itemgetter, attrgetter

#定义配置
up_range = 0.01
down_range = 0.04
mid_range = 0.02
box_mid_range = 0.02
box_high_range = 0.05
def dingzi_model(open, high, low, close, pctChg, up_check=False):
    if up_check:
        if pctChg < 0:
            return False
    if open == 0:
        return False

    if pctChg < 0:
        high_value = open
        low_value = close
    else:
        high_value = close
        low_value = open

    if(abs(high - high_value) / open >  up_range):
        return False

    if(abs(low - low_value) / abs(close - open) < 2):
        return False

    # if(abs(close - open) / open > mid_range):
    #     return False
    #
    # if(abs(low - low_value) / open < down_range):
    #     return False


    return True

before_yesterday_range = 0.02
today_range = 0.0
yesterday_mid_range = 0.02
yesterday_down_range = 0.02
def zangling_model(before_yesterday_row, yesterday_row, today_row):
    print('前天浮动范围：', abs(float(before_yesterday_row[2]) - float(before_yesterday_row[5])) /
            float(before_yesterday_row[2]))
    if(abs(float(before_yesterday_row[2]) - float(before_yesterday_row[5])) /
            float(before_yesterday_row[2]) < before_yesterday_range):
        return False
    # if(before_yesterday_row[1] == 'sh.600313'):
    #     print(float(before_yesterday_row[2]) - float(before_yesterday_row[5]))
    if(float(before_yesterday_row[2]) >= float(before_yesterday_row[5])):
        return False

    # print('今天浮动范围：', (float(today_row[5]) - float(today_row[2])) /
    #         float(today_row[2]))
    # if((float(today_row[5]) - float(today_row[2])) /
    #         float(today_row[2]) < today_range):
    #     return False

    # 当天上涨
    print('今日涨幅：', today_row[6])
    if(not today_row[6]):
        return False

    if(float(today_row[6]) < 0 or float(today_row[5]) < float(today_row[2])):
        return False
    # 昨天也涨
    # if (float(yesterday_row[6]) < 0 or float(yesterday_row[5]) < float(yesterday_row[2])):
    #     return False


    # print('昨天中间浮动范围：', abs(float(yesterday_row[2]) - float(yesterday_row[5])) /
    #         float(yesterday_row[2]))
    # if(abs(float(yesterday_row[2]) - float(yesterday_row[5])) /
    #         float(yesterday_row[2]) > yesterday_mid_range):
    #     return False
    if(max(float(yesterday_row[2]), float(yesterday_row[5])) >  max(float(before_yesterday_row[2]), float(before_yesterday_row[5]))):
        return False
    if(min(float(yesterday_row[2]), float(yesterday_row[5])) > min(float(before_yesterday_row[2]), float(before_yesterday_row[5]))):
        return False
    if(max(float(yesterday_row[2]), float(yesterday_row[5])) > max(float(today_row[2]), float(today_row[5]))):
        return False

    if (float(yesterday_row[6]) < 0):
        return False

    # if(float(yesterday_row[6]) > 0):
    #     high_value = float(yesterday_row[5])
    #     low_value = float(yesterday_row[2])
    # else:
    #     high_value = float(yesterday_row[2])
    #     low_value = float(yesterday_row[5])
    #
    # print('昨天插针浮动范围：', (low_value - float(yesterday_row[4])) / float(yesterday_row[2]))
    # if((low_value - float(yesterday_row[4])) / float(yesterday_row[2]) < yesterday_down_range):
    #     return False

    return True

#破箱模型
def break_box(ma5, ma10, ma20, trade):
    max_price = max(ma5, ma10, ma20)
    min_price = min(ma5, ma10, ma20)
    # print("最高价：" + str(max_price) + ",最低价：" + str(min_price))
    if((max_price - min_price)/min_price > box_mid_range):
    # if((max_price - min_price) > 0.5):
        return False
    if((trade - max_price) / max_price < box_high_range):
        return False
    return True

#当天时间
today = time.strftime('%Y-%m-%d', time.localtime(time.time()))


def macd_model(stock_code):
    # df = ts.get_hist_data('601398', start='2018-01-04', end='2019-04-04')
    df = ts.get_hist_data(stock_code, start='2018-01-04', end=today)
    # print(len(df))
    if (df is None):
        return False
    if len(df) == 0:
        return False
    df = df.sort_index()
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
    # 收市股价
    close = df.close
    # 调用talib计算MACD指标
    df['DIFF'], df['DEA'], df['MACD'] = talib.MACD(np.array(close),
                                                   fastperiod=12, slowperiod=26, signalperiod=9)
                                                   # fastperiod = 9, slowperiod = 13, signalperiod = 7)
    diff = df.DIFF
    dea = df.DEA
    print("----------------------------------")
    print("三天前，diff:" + str(diff[len(diff) - 3]) + "dea:" + str(dea[len(dea) - 3]))
    print("最近一天，diff:" + str(diff[len(diff) - 1]) + "dea:" + str(dea[len(dea) - 1]))
    if(diff[len(diff) - 3] > 0):
        return False
    if(diff[len(diff) - 3] < dea[len(dea) - 3] and diff[len(diff) - 1] > dea[len(dea) - 1]):
        return True

    # ###求MACD
    # df_2 = ts.get_k_data(stock_code)
    # close = [float(x) for x in df_2['close']]
    # # 调用talib计算指数移动平均线的值
    # df_2['EMA12'] = talib.EMA(np.array(close), timeperiod=6)
    # df_2['EMA26'] = talib.EMA(np.array(close), timeperiod=12)
    # # 调用talib计算MACD指标
    # df_2['MACD'], df_2['MACDsignal'], df_2['MACDhist'] = talib.MACD(np.array(close),
    #                                                           fastperiod=6, slowperiod=12, signalperiod=9)
    # df_2.tail(12)
    # print("----------------------")
    # print(df_2)
    return False

# print (macd_model('601398'))
# macd_model('600145')


def fan_macd_model(stock_code):
    # df = ts.get_hist_data('601398', start='2018-01-04', end='2019-04-04')
    df = ts.get_hist_data(stock_code, start='2018-01-04', end=today)
    # print(len(df))
    if (df is None):
        return False
    if len(df) == 0:
        return False
    df = df.sort_index()
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
    # 收市股价
    close = df.close
    # 调用talib计算MACD指标
    df['DIFF'], df['DEA'], df['MACD'] = talib.MACD(np.array(close),
                                                   fastperiod=12, slowperiod=26, signalperiod=9)
                                                   # fastperiod = 9, slowperiod = 13, signalperiod = 7)
    diff = df.DIFF
    dea = df.DEA
    print("----------------------------------")
    print("三天前，diff:" + str(diff[len(diff) - 5]) + "dea:" + str(dea[len(dea) - 5]))
    print("最近一天，diff:" + str(diff[len(diff) - 3]) + "dea:" + str(dea[len(dea) - 3]))
    # if(diff[len(diff) - 3] > 0):
    #     return False
    if(diff[len(diff) - 5] < dea[len(dea) - 5] and diff[len(diff) - 3] > dea[len(dea) - 3]):
        return True

    # ###求MACD
    # df_2 = ts.get_k_data(stock_code)
    # close = [float(x) for x in df_2['close']]
    # # 调用talib计算指数移动平均线的值
    # df_2['EMA12'] = talib.EMA(np.array(close), timeperiod=6)
    # df_2['EMA26'] = talib.EMA(np.array(close), timeperiod=12)
    # # 调用talib计算MACD指标
    # df_2['MACD'], df_2['MACDsignal'], df_2['MACDhist'] = talib.MACD(np.array(close),
    #                                                           fastperiod=6, slowperiod=12, signalperiod=9)
    # df_2.tail(12)
    # print("----------------------")
    # print(df_2)
    return False

#定义配置
# 大宗买入交易与大宗卖出交易的倍数
block_proportion = 2
# 设置大宗交易阀值，10000只
# block_threshold = 3000
# 设置大宗交易金额阀值，100万元
block_price = 5000000
date_now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
def check_block_transaction(stock_code, stock_price, buy_date):
    buy_count = 0
    sell_count = 0
    # print(stock_code, stock_price, end="")
    block_threshold = math.ceil(block_price / (stock_price * 100))
    df = ts.get_sina_dd(stock_code, date=buy_date, vol=block_threshold)
    if df is None:
       return False, 0
    for i in range(0,len(df)):
        if(df['type'][i] == '卖盘'):
            sell_count = sell_count + df['volume'][i]
        elif(df['type'][i] == '买盘'):
            buy_count = buy_count + df['volume'][i]
    mess = stock_code + '买盘：' + str(buy_count) + '卖盘：' + str(sell_count)
    print(mess)
    if(buy_count > block_proportion * sell_count):
        if sell_count == 0:
            return True, buy_count
        return True, buy_count / sell_count
    return False, 0

##纺缍体（刺透形态）
pctChg = 1 #涨幅
highChg = 2 #最高价是收盘价的比值
lowChg = 1 #最低价是收盘价的比值
def spindle_model(stock_row):

    # print((float(stock_row[5]) - float(stock_row[2])) / float(stock_row[2]) * 100)
    # print((float(stock_row[3]) - float(stock_row[5])) / float(stock_row[2]) * 100)
    #涨幅大于标准值
    if((float(stock_row[5]) - float(stock_row[2])) / float(stock_row[2]) * 100 < pctChg):
        print("不符合涨幅标准")
        return False

    #针长与实体的比值大于标准值
    if ((float(stock_row[3]) - float(stock_row[5])) / float(stock_row[2]) * 100 < highChg):
        print("针值不符合")
        return False

    # 尾针长大于标准值
    if ((float(stock_row[2]) - float(stock_row[4])) / float(stock_row[2]) * 100 > lowChg):
        print("尾针值不符合")
        return False

    return True

##吞没形态（抱线形态）
def embezzle_model(yesterday_row, today_row):
    #前一天是下跌
    if(float(yesterday_row[2]) <= float(yesterday_row[5])):
        return False
    #今天是涨的
    if (float(today_row[2]) > float(today_row[5])):
        return False
    #今天的开盘比昨天的收盘低，今天的收盘比昨天的开盘高
    if(float(today_row[2]) >= float(yesterday_row[5]) or
        float(today_row[5]) <= float(yesterday_row[2])):
        return False

    return True


difference = 0.03 #底部误差
high_needle = 0.3 #针与实体比例
low_needle = 0.01
##启明星前半部分（飞哥改）
def star_model(last_month, this_month):
    #上个月是下跌
    if(float(last_month[2]) <= float(last_month[5])):
        return False
    #这个月涨的
    print(this_month[1], this_month[6], "-------------")
    if not this_month[6]:
        return False

    if (float(this_month[2]) > float(this_month[5]) or float(this_month[6]) < 0):
        return False
    #两月底部相差不大
    if(abs(float(last_month[5]) - float(this_month[2])) / float(last_month[5]) > difference):
        return False
    #底部针长度
    if(abs(float(last_month[5]) - float(last_month[4])) / float(last_month[5]) > low_needle or
        abs(float(this_month[2]) - float(this_month[4])) / float(this_month[2]) > low_needle):
        return False

    if(abs(float(this_month[5]) - float(this_month[2])) == 0):
        return True

    #顶部针长占实体比例
    if(abs(float(this_month[3]) - float(this_month[5])) / abs(float(this_month[5]) - float(this_month[2])) < high_needle):
        return False

    return True

##破箱模型（抱线形态）
def breakBox_2_model(all_stock, start_num, count_day, sliding_scales):
    high_price = 0
    low_price = 99999
    for i in range(0,count_day):
        if float(all_stock[start_num + i][3]) > high_price:
            high_price = float(all_stock[start_num + i][3])
        if float(all_stock[start_num + i][4]) < low_price:
            low_price = float(all_stock[start_num + i][4])
    if (high_price - low_price) / low_price > sliding_scales:
        return False, high_price, low_price
    return True, high_price, low_price