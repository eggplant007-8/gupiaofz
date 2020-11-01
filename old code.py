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

#获得藏铃模型
def get_zangling_stock():

    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    date = "'2020-02-10'"
    # print(date)

    # 打开数据库连接
    db = pymysql.connect("localhost", db_user, db_pwd, db_name)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "select * from all_stock_historydata where date = " + date
    sql1 = "select * from all_stock_historydata where date = %s and stock_code = %s"
    cursor.execute(sql)
    results = cursor.fetchall()

    if(results ==None):
        return
    print(sql)
    date_list = []
    j = 0
    count = 0

    for row in results:
        if (float(row[2]) > 200):
            continue

        i = 0
        get_two_mess = 0
        yesterday_row = None
        before_yesterday_row = None

        print(row)
        if text.check_stock_complete(row) == False:
            continue
        while get_two_mess < 2:
            while get_two_mess < 1:
                yesterday = text.get_next_day(row[0], -1 + i)
                cursor.execute(sql1, (yesterday, row[1]))
                yesterday_row = cursor.fetchone()
                print(yesterday_row)
                if yesterday_row and text.check_stock_complete(yesterday_row):
                    get_two_mess = 1
                    break
                i = i - 1

            before_yesterday = text.get_next_day(row[0], -2 + i)
            cursor.execute(sql1, (before_yesterday, row[1]))
            before_yesterday_row = cursor.fetchone()
            print(before_yesterday_row)
            if before_yesterday_row and text.check_stock_complete(before_yesterday_row):
                get_two_mess = 2
                break
            i = i - 1

        if model.zangling_model(before_yesterday_row, yesterday_row, row):
            date_list.append(row[1])
            j = j + 1
            print('找到一支股票符合条件！！！！！')
            # break
        count = count + 1
        print('已处理', count, '支股票')


    print(date_list)
    print('共' + str(j) + "只股票符合藏铃模型")
