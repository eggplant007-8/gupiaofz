# -*- coding: UTF-8 -*-
import baostock as bs
import pymysql
import time
import text
import model
import tushare as ts
import send_message
import talib
import numpy as np
import pandas as pd

db_user = 'root'
db_pwd = 'root'
db_name = 'db_gpfz'

def get_strong_stock():

    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)
    #### 获取证券信息 ####
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    print(today)

    rs = bs.query_all_stock(day='2019-03-01')
    print('query_all_stock respond error_code:' + rs.error_code)
    print('query_all_stock respond  error_msg:' + rs.error_msg)

    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "root", "db_gpfz")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "select * from all_stock_historydata where stock_code = %s"

    # data_list = []
    i = 1
    while (rs.error_code == '0') & rs.next():
        gp = rs.get_row_data()
        # print("---------------")
        # print(gp)
        cursor.execute(sql, gp[0])
        results = cursor.fetchall()
        rise_day = 0
        drop_day = 0

        for row in results:

            # print(row[6])
            # print("---------------")
            if(row[6]):
                pctChg = float(row[6])
                if(pctChg > 0):
                    rise_day = rise_day + 1
                elif(pctChg < 0):
                    drop_day = drop_day + 1

        sql_update = "update all_stock_list set year_rise_day_2018 = %d, year_drop_day_2018 = %d where stock_code = '%s'"
        cursor.execute(sql_update % (rise_day, drop_day, gp[0]))
        # print(gp[0])
        db.commit()
        # data_list.append([gp[0], gp[2], rise_day, drop_day])
        print('已导入' + str(i) + '支股票涨跌天数')
        i = i + 1
    print('¥¥¥¥导入完成¥¥¥¥')
    # print(data_list)
    # strong_list = text.bubbleSort(data_list, 2)
    # print(strong_list[1:20])

    #倒序
    # strong_list.reverse()
    db.close()
    bs.logout()

def get_this_year_strong_stock():

    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)
    #### 获取证券信息 ####
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    print(today)

    rs = bs.query_all_stock(day='2019-03-01')
    print('query_all_stock respond error_code:' + rs.error_code)
    print('query_all_stock respond  error_msg:' + rs.error_msg)

    # 打开数据库连接
    db = pymysql.connect("localhost", db_user, db_pwd, db_name)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "select * from all_stock_historydata where stock_code = %s"

    # data_list = []
    i = 1
    this_year = '2019-01-01'
    while (rs.error_code == '0') & rs.next():
        gp = rs.get_row_data()
        # print("---------------")
        # print(gp)
        cursor.execute(sql, gp[0])
        results = cursor.fetchall()
        rise_day = 0
        drop_day = 0

        for row in results:

            # print(row[0])
            # print("---------------")
            # print(text.compare_time(row[0], this_year))
            if(text.compare_time(row[0], this_year) < 0):
                continue
            if(row[6]):
                pctChg = float(row[6])
                if(pctChg > 0):
                    rise_day = rise_day + 1
                elif(pctChg < 0):
                    drop_day = drop_day + 1

        sql_update = "update all_stock_list set year_rise_day_2019 = %d, year_drop_day_2019 = %d where stock_code = '%s'"
        cursor.execute(sql_update % (rise_day, drop_day, gp[0]))
        # print(gp[0])
        db.commit()
        # data_list.append([gp[0], gp[2], rise_day, drop_day])
        print('已导入' + str(i) + '支股票2019年涨跌天数')
        i = i + 1

    print('¥¥¥¥导入完成¥¥¥¥')
    # print(data_list)
    # strong_list = text.bubbleSort(data_list, 2)
    # print(strong_list[1:20])

    #倒序
    # strong_list.reverse()
    db.close()
    bs.logout()

#获取往期钉子模型
def get_dingzi_stock():

    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    date = "'2019-03-01'"
    print(date)

    # 打开数据库连接
    db = pymysql.connect("localhost", db_user, db_pwd, db_name)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "select * from all_stock_historydata where date = " + date
    cursor.execute(sql)
    results = cursor.fetchall()

    date_list = []
    i = 0
    for row in results:
        if model.dingzi_model(float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6])):
            date_list.append(row[1])
            i = i + 1
    print(date_list)
    print('共' + str(i) + "只股票符合钉子模型")

#获取当天钉子模型
def get_today_dingzi_stock():

    results = ts.get_today_all()
    date_list = []

    print('--------------------')
    j = 0
    for i in range(0,len(results)):
        print(results['code'][i], results['name'][i], results['open'][i], results['high'][i], results['low'][i], results['trade'][i], results['changepercent'][i])
        if model.dingzi_model(results['open'][i], results['high'][i], results['low'][i], results['trade'][i], results['changepercent'][i]):
            date_list.append([results['code'][i], results['name'][i]])
            j = j + 1

    print(date_list)
    print('目前共' + str(j) + "只股票符合钉子模型")

#获得过去符合藏铃模型
def get_zangling_stock():

    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    old_date = "2020-04-17"
    # print(date)

    # 打开数据库连接
    db = pymysql.connect("localhost", db_user, db_pwd, db_name)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "select * from all_stock_historydata where date > %s and date <= %s order by stock_code, date"
    # sql = "select * from all_stock_historydata where date > %s and date <= %s and stock_code = 'sh.600699' order by stock_code"
    # sql = "select * from all_stock_historydata where date > %s order by stock_code, date"
    cursor.execute(sql, (old_date, today))
    # print(old_date)
    # cursor.execute(sql, old_date)
    results = cursor.fetchall()

    if(results == None):
        return
    date_list = []
    j = 0
    count = 0
    s = 0

    print('results 行数= ', len(results))
    while s < len(results) - 2:

        print(results[s][1], results[s + 1][1], results[s + 2][1])
        if(results[s][1] == results[s + 1][1] and results[s][1] == results[s + 2][1]):
            # if(results[s][1] == 'sh.600699'):
            #     print('come')
            print('股票代码：', results[s][1])
            if model.zangling_model(results[s], results[s + 1], results[s + 2]):
                date_list.append([results[s][1], results[s][5]])
                j = j + 1
                print('找到一支股票符合条件:', results[s])

            s = s + 3
            count = count + 1
            print('已处理', count, '支股票')
            continue
        else:
            s = s + 1
        print('已处理', count, '支股票')

    print(date_list)
    print('共' + str(j) + "只股票符合藏铃模型")
    print('开始检验大宗交易')
    today = None
    yesterday = None
    before_yesterday = None
    if(results[0][1] == results[1][1] and results[1][1] == results[2][1]):
        today = results[2][0]
        yesterday = results[1][0]
        before_yesterday = results[0][0]
    if(today == None):
        print('第一组股票不是同一支')
        return

    big_list = []
    count = 0
    for row in date_list:
        print(row)
        check_value, than = model.check_block_transaction(row[0][3:9], float(row[1]), today)
        if(check_value):
            count = count + 1
            print('今天发现一支大宗交易！：', row)
        time.sleep(1)

        check_value, than = model.check_block_transaction(row[0][3:9], float(row[1]), yesterday)
        if(check_value):
            count = count + 1
            print('昨天发现一支大宗交易！：', row)
        time.sleep(1)

        check_value, than = model.check_block_transaction(row[0][3:9], float(row[1]), yesterday)
        if(check_value):
            count = count + 1
            print('前天发现一支大宗交易！：', row)
        time.sleep(1)
        if(count > 0):
            big_list.append([row, count])
        count = 0
    print('符合藏铃模型且有大宗交易的股有：', big_list)


    # for row in results:
    #     if (float(row[2]) > 200):
    #         continue
    #
    #     i = 0
    #     get_two_mess = 0
    #     yesterday_row = None
    #     before_yesterday_row = None
    #
    #     print(row)
    #     if text.check_stock_complete(row) == False:
    #         continue
    #     while get_two_mess < 2:
    #         while get_two_mess < 1:
    #             yesterday = text.get_next_day(row[0], -1 + i)
    #             cursor.execute(sql1, (yesterday, row[1]))
    #             yesterday_row = cursor.fetchone()
    #             print(yesterday_row)
    #             if yesterday_row and text.check_stock_complete(yesterday_row):
    #                 get_two_mess = 1
    #                 break
    #             i = i - 1
    #
    #         before_yesterday = text.get_next_day(row[0], -2 + i)
    #         cursor.execute(sql1, (before_yesterday, row[1]))
    #         before_yesterday_row = cursor.fetchone()
    #         print(before_yesterday_row)
    #         if before_yesterday_row and text.check_stock_complete(before_yesterday_row):
    #             get_two_mess = 2
    #             break
    #         i = i - 1
    #
    #     if model.zangling_model(before_yesterday_row, yesterday_row, row):
    #         date_list.append(row[1])
    #         j = j + 1
    #         print('找到一支股票符合条件！！！！！')
    #         # break
    #     count = count + 1
    #     print('已处理', count, '支股票')
    # print(date_list)
    # print('共' + str(j) + "只股票符合藏铃模型")

# 2018年以来，所有股票出现符合钉子模型时间的有1117次
# 出现钉子模型后，后一天就上涨的有503次, 占比 45.03%
# 出现钉子模型后，后两天就上涨的有398次, 占比 35.63%
# 出现钉子模型后，后三天就上涨的有596次, 占比 53.35%
# 出现钉子模型后，后一天收盘价就上升的有504次, 占比 45.12%
# 出现钉子模型后，后两天收盘价就上升的有426次, 占比 38.13%
# 出现钉子模型后，后三天收盘价就上升的有467次, 占比 41.80%
def check_dingzi_isstrong():
    # 打开数据库连接
    db = pymysql.connect("localhost", db_user, db_pwd, db_name)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "select * from all_stock_historydata"
    cursor.execute(sql)
    results = cursor.fetchall()
    sql_1 = "select * from all_stock_historydata where date = %s and stock_code = %s"

    oneday_up = 0
    secondday_up = 0
    third_up = 0
    dingzi_model = 0

    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    count = 1
    oneclose_count = 1
    towclose_count = 1
    third_count = 1
    y = 0
    for row in results:
        if text.check_stock_complete(row) == False:
            continue
        if model.dingzi_model(float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6])):
            data = row[0]
            dingzi_model = dingzi_model + 1
            print('当天数据为',row)
            while count < 4 and text.compare_time(data, today) < 0:
                print("----------------------")
                data = text.get_next_day(data)
                cursor.execute(sql_1, (data, row[1]))
                result = cursor.fetchone()
                print(str(count) + '天后数据为', result)
                if result == None:
                    continue
                # print("************")
                # print(result[5])
                # print(row[5])

                if (float(result[6]) > 0):
                    if count == 1:
                        oneday_up = oneday_up + 1
                    if count == 2:
                        secondday_up = secondday_up + 1
                    if count == 3:
                        third_up = third_up + 1
                if(float(result[5]) > float(row[5])):
                    if count == 1:
                        oneclose_count = oneclose_count + 1
                    if count == 2:
                        towclose_count = towclose_count + 1
                    if count == 3:
                        third_count = third_count + 1

                count = count + 1
            count = 1
        print('解析完' + str(y) + '条数据')
    print('2018年以来，所有股票出现符合钉子模型时间的有' + str(dingzi_model) + '次')
    print('出现钉子模型后，后一天就上涨的有' + str(oneday_up) + '次, 占比', oneday_up / dingzi_model * 100, '%')
    print('出现钉子模型后，后两天就上涨的有' + str(secondday_up) + '次, 占比', secondday_up / dingzi_model * 100, '%')
    print('出现钉子模型后，后三天就上涨的有' + str(third_up) + '次, 占比', third_up / dingzi_model * 100, '%')
    print('出现钉子模型后，后一天收盘价就上升的有' + str(oneclose_count) + '次, 占比', oneclose_count / dingzi_model * 100, '%')
    print('出现钉子模型后，后两天收盘价就上升的有' + str(towclose_count) + '次, 占比', towclose_count / dingzi_model * 100, '%')
    print('出现钉子模型后，后三天收盘价就上升的有' + str(third_count) + '次, 占比', third_count / dingzi_model * 100, '%')

#找到破箱模型
def get_breakbox_model():
    #获得两个工作日的时间
    # data1 = get_tow_datas()
    data1 = '2020-07-17'
    date_list = []
    j = 0
    results = ts.get_today_all()
    for i in range(0, len(results)):
        up_stock = ts.get_hist_data(results['code'][i], start=data1, end=data1)
        print(results['code'][i],)
        if up_stock is None:
            continue
        if (len(up_stock) == 0):
            continue
        print(up_stock['ma5'][0], up_stock['ma10'][0], up_stock['ma20'][0], results['trade'][i])
        if(model.break_box(up_stock['ma5'][0], up_stock['ma10'][0], up_stock['ma20'][0], results['trade'][i])):
            date_list.append([results['code'][i], results['name'][i]])
            print("入选------------------------------------------")
            print(results['code'][i], results['name'][i])
            j = j + 1
        print('已处理完' + str(i) + '只股票')
    print(date_list)
    print("共" + str(j) + '只股票符合破箱模型' )
    return

def get_macd_model():
    results = ts.get_stock_basics()
    date_list = []

    j = 0
    for i in range(0, len(results)):
        # print(results['code'][i], results['name'][i], results['open'][i], results['high'][i], results['low'][i],
        #       results['trade'][i], results['changepercent'][i])
        print([results.index[i], results['name'][i]])
        # if model.macd_model(results.index[i]):
        #     print("1+++++++++符合macd")
        #     if(text.check_block_transaction(results.index[i])):
        #         date_list.append([results.index[i], results['name'][i]])
        #         j = j + 1
        #         print("2入选================================")

        if model.fan_macd_model(results.index[i]):
            print("1+++++++++符合macd")
            date_list.append([results.index[i], results['name'][i]])
            j = j + 1

        print('已处理完' + str(i + 1) + '只股票')
        print("================================")

    print(date_list)
    print('目前共' + str(j) + "只股票符合MACD模型")
# get_macd_model()

#2020年因疫情狂跌未恢复的股票
def get_not_recovered_stock():

    date_now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    date_now = '2020-02-10'
    special_date = "2020-01-23"
    # print(date)

    # 打开数据库连接
    db = pymysql.connect("localhost", db_user, db_pwd, db_name)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # sql = "select * from all_stock_historydata where date = %s and stock_code like %s"
    # sql_now = "select * from all_stock_historydata where date = '2020-01-23' and stock_code like '%002385'"
    sql = "select * from all_stock_historydata where date = %s"
    cursor.execute(sql, date_now)
    now_results = cursor.fetchall()

    cursor.execute(sql, special_date)
    special_results = cursor.fetchall()

    # results = ts.get_stock_basics()

    date_list = []
    j = 0
    count = 0
    weight = 0.95

    for special_row in special_results:
        for now_row in now_results:
            if(special_row[1] == now_row[1]):
                if (float(now_row[5]) < weight * float(special_row[5])):
                    date_list.append(now_row[1])
                    j = j + 1
                    print('找到一支股票符合条件！！！！！')
                break
        count = count + 1
        print('已处理', count, '支股票')

    print(date_list)
    print('共' + str(j) + "只股票符合未恢复模型")

#底部纺缍体 111
day_num = 2 #比较股票 num 天的数据io
check_day = 1 #迭代检查几天的数据
def get_bottom_spindle_stock():

    # 打开数据库连接
    db = pymysql.connect("localhost", db_user, db_pwd, db_name)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # sql_all_stock = "select stock_code from all_stock_historydata group by stock_code"
    # sql = "select * from all_stock_historydata where stock_code like %s order by date desc limit 3"
    # sql = "select * from all_stock_historydata where stock_code like '%300025' order by date desc limit 15"
    sql = "select * from all_stock_historydata where date > '2020-01-01' order by stock_code, date desc"
    cursor.execute(sql)
    all_stock = cursor.fetchall()
    # last_date = '2020-03-13'

    #查询所有数据，统计每支股票数据数
    i = 0
    stock_count = [0]
    while i < len(all_stock) - 1:
        print('----------')
        print(all_stock[i][1], all_stock[i + 1][1])
        if(all_stock[i][1] != all_stock[i + 1][1]):
            # if(results[s][1] == 'sh.600699'):
            #     print('come')
            stock_count.append(i + 1)
        i = i + 1
        print('已统计', i, '条数据')
    stock_count.append(len(all_stock))

    print("共有", len(stock_count), "支股票")
    date_list = []
    j = 0
    count = 0
    cursor = 0
    next_cursor = 0
    #遍历每支股票
    while(count < len(stock_count) - 1):

        cursor = stock_count[count]
        # print("索引为", cursor)
        next_cursor = stock_count[count + 1]
        s = 0
        while s < check_day:
            if(cursor + day_num >= next_cursor):
                break
            # print(stock_count[count + 1] - stock_count[count])
            #数据库数据不足
            if(stock_count[count + 1] - stock_count[count] < day_num):
                print("数据库数据不足")
                break
            print("数据库数据充足")
            #股票停板
            print(all_stock[cursor])
            # if s == 0:
            #     if(all_stock[cursor][0] != last_date):
            #         print("股票停板")
            #         break
            #     print("股票未停板，进入模型")
            m = 0
            if(model.spindle_model(all_stock[cursor])):
                print("符合纺缍体模型")
                i = 0
                while i < day_num - 1:
                    # print(float(all_stock[cursor + i][5]) , all_stock[cursor + i + 1][5])
                    # print("前一天", float(all_stock[cursor + i + 1][5]) , float(all_stock[cursor + i + 1][2]))
                    # if(float(all_stock[cursor + i][5]) < ((float(all_stock[cursor + i + 1][5]) + float(all_stock[cursor + i + 1][2])) / 2) or
                    if (float(all_stock[cursor + i][5]) >= float(all_stock[cursor + i + 1][5]) or
                        float(all_stock[cursor + i + 1][5]) > float(all_stock[cursor + i + 1][2])):
                        # or float(all_stock[cursor + i][5]) >= float(all_stock[cursor + i + 1][5])):
                        m = 1
                        break
                    i = i + 1
                    print("第", i, "天符合")

                if(m == 0):
                    date_list.append([all_stock[cursor][0], all_stock[cursor][1]])
                    j = j + 1
#                print('找到一支股票符合条件:', all_stock[cursor])
#                else:
#                    break


            cursor = cursor + 1
            s = s + 1

        count = count + 1
        print('已处理', count, '支股票')

    print(date_list)
    print('共' + str(j) + "只股票符合纺锤体模型")

#破箱模型
# day_num = 10 #箱子天数
sliding_scales = 0.1 #浮动比例
def get_breakBox_2_stock(day_num, sliding_scales):

    # 打开数据库连接
    db = pymysql.connect("localhost", db_user, db_pwd, db_name)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # sql_all_stock = "select stock_code from all_stock_historydata group by stock_code"
    # sql = "select * from all_stock_historydata where stock_code like %s order by date desc limit 3"
    # sql = "select * from all_stock_historydata where stock_code like '%300025' order by date desc limit 15"
    sql = "select * from all_stock_historydata order by stock_code, date desc"
    cursor.execute(sql)
    all_stock = cursor.fetchall()
    # last_date = '2020-03-13'

    #查询所有数据，统计每支股票数据数
    i = 0
    stock_count = [0]
    while i < len(all_stock) - 1:
        print('----------')
        print(all_stock[i][1], all_stock[i + 1][1])
        if(all_stock[i][1] != all_stock[i + 1][1]):
            # if(results[s][1] == 'sh.600699'):
            #     print('come')
            stock_count.append(i + 1)
        i = i + 1
        print('已统计', i, '条数据')
    stock_count.append(len(all_stock))

    print("共有", len(stock_count), "支股票")
    up_list = []
    down_list = []
    j = 0
    k = 0
    count = 0
    cursor = 0
    next_cursor = 0
    #遍历每支股票
    while(count < len(stock_count) - 1):

        cursor = stock_count[count]
        print("索引为", cursor)
        next_cursor = stock_count[count + 1]
        s = 0

        print(stock_count[count + 1] - stock_count[count])
        #数据库数据不足
        if(stock_count[count + 1] - stock_count[count] < day_num + 1):
            print("数据库数据不足")
            count = count + 1
            continue
        print("数据库数据充足")
        #股票停板
        print(all_stock[cursor])
        # if s == 0:
        #     if(all_stock[cursor][0] != last_date):
        #         print("股票停板")
        #         break
        #     print("股票未停板，进入模型")
        key, high_price, low_price = model.breakBox_2_model(all_stock, cursor + 1, day_num, sliding_scales)
        if(key):
            print("符合箱体模型")
            if(float(all_stock[cursor][3])  > (1 + 1.2 * sliding_scales) * low_price):
                print("高破")
                up_list.append([all_stock[cursor][0], all_stock[cursor][1]])
                j = j + 1
            if(float(all_stock[cursor][4]) < (1 - 0.2 * sliding_scales) * low_price):
                print("低破")
                down_list.append([all_stock[cursor][0], all_stock[cursor][1]])
                k = k + 1


        count = count + 1
        print('已处理', count, '支股票')

    print(up_list)
    print('共' + str(j) + "只股票符合高破箱体模型")
    print(down_list)
    print('共' + str(k) + "只股票符合低破箱体模型")

#看涨吞没形态月白
def get_rise_embezzle_stock():

    # 打开数据库连接
    db = pymysql.connect("localhost", db_user, db_pwd, db_name)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # sql_all_stock = "select stock_code from all_stock_historydata group by stock_code"
    # sql = "select * from all_stock_historydata where stock_code like %s order by date desc limit 3"
    # sql = "select * from all_stock_historydata where stock_code like '%300025' order by date desc limit 15"
    sql = "select * from all_stock_historydata order by stock_code, date desc"
    cursor.execute(sql)
    all_stock = cursor.fetchall()
    # last_date = '2020-03-13'

    #查询所有数据，统计每支股票数据数
    i = 0
    stock_count = [0]
    while i < len(all_stock) - 1:
        print('----------')
        print(all_stock[i][1], all_stock[i + 1][1])
        if(all_stock[i][1] != all_stock[i + 1][1]):
            # if(results[s][1] == 'sh.600699'):
            #     print('come')
            stock_count.append(i + 1)
        i = i + 1
        print('已统计', i, '条数据')
    stock_count.append(len(all_stock))

    print("共有", len(stock_count), "支股票")
    date_list = []
    j = 0
    count = 0
    cursor = 0
    next_cursor = 0
    #遍历每支股票
    while(count < len(stock_count) - 1):

        cursor = stock_count[count]
        print("索引为", cursor)
        # next_cursor = stock_count[count + 1]
        if(model.embezzle_model(all_stock[cursor + 1], all_stock[cursor])):
            print("符合吞没形态")
            date_list.append([all_stock[cursor][0], all_stock[cursor][1]])
            j = j + 1
#
        count = count + 1
        print('已处理', count, '支股票')

    print(date_list)
    print('共' + str(j) + "只股票符合吞没形态")

#启明星形态-月线
def get_star_stock():

    # 打开数据库连接
    db = pymysql.connect("localhost", db_user, db_pwd, db_name)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # sql_all_stock = "select stock_code from all_stock_historydata group by stock_code"
    # sql = "select * from all_stock_historydata where stock_code like %s order by date desc limit 3"
    # sql = "select * from all_stock_historydata where stock_code like '%300025' order by date desc limit 15"
    sql = "select * from all_stock_historydata_interval where frequency = 'm' order by stock_code, date desc"
    cursor.execute(sql)
    all_stock = cursor.fetchall()
    # last_date = '2020-03-13'

    #查询所有数据，统计每支股票数据数
    i = 0
    stock_count = [0]
    while i < len(all_stock) - 1:
        print('----------')
        print(all_stock[i][1], all_stock[i + 1][1])
        if(all_stock[i][1] != all_stock[i + 1][1]):
            # if(results[s][1] == 'sh.600699'):
            #     print('come')
            stock_count.append(i + 1)
        i = i + 1
        print('已统计', i, '条数据')
    stock_count.append(len(all_stock))

    print("共有", len(stock_count), "支股票")
    date_list = []
    j = 0
    count = 0
    cursor = 0
    next_cursor = 0
    #遍历每支股票
    while(count < len(stock_count) - 1):

        cursor = stock_count[count]
        print("索引为", cursor)
        # next_cursor = stock_count[count + 1]
        if(model.star_model(all_stock[cursor + 1], all_stock[cursor])):
            print("符合启明星形态")
            date_list.append([all_stock[cursor][0], all_stock[cursor][1]])
            j = j + 1
#
        count = count + 1
        print('已处理', count, '支股票')

    print(date_list)
    print('共' + str(j) + "只股票符合吞没形态")


#股票监控
def stock_monitor():
    up_range = 1.05
    down_range = 0.93
    stock_list = [('600307', 2.437), ('601878', 10.75)]
    while True:
        try:
            results = ts.get_today_all()
            for i in range(0, len(results)):
                # print(results['code'][i], results['name'][i], results['open'][i], results['high'][i], results['low'][i],
                #       results['trade'][i], results['changepercent'][i])

                for row in stock_list:

                    if (results['code'][i] == row[0]):
                        print(row)
                        print(results['code'][i], results['name'][i], results['open'][i], results['high'][i],
                              results['low'][i],
                              results['trade'][i], results['changepercent'][i])

                        print('变化情况：', results['trade'][i]/ row[1])
                        if(results['trade'][i]/ row[1] > up_range):
                            message = '股票代码：' + str(results['code'][i]) + '股票名称：' + str(results['name'][i]) + '上浮达' + str((results['trade'][i]/ row[1] - 1) * 100) + '%'
                            print(message)
                            send_message.send_message_mail(message)
                        if (results['trade'][i] / row[1] < down_range):
                            message = '股票代码：' + str(results['code'][i]) + '股票名称：' + str(results['name'][i]) + '跌浮达' + str(
                                (results['trade'][i] / row[1] - 1) * 100) + '%'

                            send_message.send_message_mail(message)
        except IOError:
            print("网络连接失败")
        time.sleep(180)

# date_now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
date_now = '2019-04-04'
def get_too_monkey_stock():
    results = ts.get_stock_basics()
    date_list = []
    data_ago = -1
    num = 0
    for i in range(0, len(results)):

        for j in range(0, 3):
            data = text.get_next_day(date_now, data_ago)
            print(data, results.index[i])
            if(not text.check_block_transaction_when(results.index[i], data)):
                break
            data_ago = data_ago - 1
        if(data_ago == -4):
            date_list.append([results.index[i], results['name'][i]])
            num = num + 1
        data_ago = -1
        # print(results['code'][i], results['name'][i], results['open'][i], results['high'][i], results['low'][i],
        #       results['trade'][i], results['changepercent'][i])
        print([results.index[i], results['name'][i]])
        # if model.macd_model(results.index[i]):
        #     print("1+++++++++符合macd")
        #     if(text.check_block_transaction(results.index[i])):
        #         date_list.append([results.index[i], results['name'][i]])
        #         j = j + 1
        #         print("2入选================================")

        # if model.fan_macd_model(results.index[i]):
        #     print("1+++++++++符合macd")
        #     date_list.append([results.index[i], results['name'][i]])
        #     j = j + 1

        print('已处理完' + str(i + 1) + '只股票')
        print("================================")

    print(date_list)
    print('目前共' + str(num) + "只股票三天交易都大额")

# get_star_stock()
# get_zangling_stock()
get_bottom_spindle_stock()
# get_rise_embezzle_stock()
# get_not_recovered_stock()
# get_too_monkey_stock()
# get_breakBox_2_stock(10, 0.1)

# up_stock = ts.get_hist_data('600680', start='2019-03-14', end='2019-03-14')
# print(up_stock['ma5'][0], up_stock['ma10'][0], up_stock['ma20'][0],)
# print(up_stock)
#
#
# print(len(up_stock))
# if up_stock is None:
#     print('1111111')
# if(len(up_stock) == 0):
#     print('2222222')

# get_breakbox_model()
# while True:
#     try:
#         get_breakbox_model()
#         break
#     except:
#         print('111')

# stock_monitor()
# get_today_dingzi_stock()
# get_zangling_stock()
# get_dingzi_stock()

# check_dingzi_isstrong()
# get_strong_stock()
# get_this_year_strong_stock()


