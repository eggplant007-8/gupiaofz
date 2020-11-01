import baostock as bs
import pandas as pd
import numpy as np
import time
import datetime
from dateutil import parser
import pymysql

db_user = 'root'
db_pwd = 'root'
db_name = 'db_gpfz'

def get_stock_history_data():
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)


    #### 获取证券信息 ####
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    # today = '2020-03-09'
    print(today)
    rs = bs.query_all_stock(day = '2020-10-22') #这个日期一定要开盘日期，不能是周末
    print('query_all_stock respond error_code:'+rs.error_code)
    print('query_all_stock respond  error_msg:'+rs.error_msg)

    start_day = '2020-10-21'

    # 打开数据库连接
    db = pymysql.connect("localhost", db_user, db_pwd, db_name)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    #获取股票每天的数据 111
    sql = "insert into all_stock_historydata values(%s, %s, %s, %s, %s, %s, %s, %s)"
    #获取股票周期数据-月线 or 年线
    # sql = "insert into all_stock_historydata_interval values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    i = 1
    while (rs.error_code == '0') & rs.next():

        gp = rs.get_row_data()
        #frequency：数据类型，默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟k线数据
        rs_inf = bs.query_history_k_data(gp[0],
                                         "date,code,open,high,low,close,pctChg,turn",
                                         start_date=start_day, end_date=today,
                                         frequency="d", adjustflag="3")
        data_list = []

        while (rs_inf.error_code == '0') & rs_inf.next():
            # 获取一条记录，将记录合并在一起
            rs_inf_insert = rs_inf.get_row_data()
            #月线或年线多一个标识数据 月线：m 周线：w
            # rs_inf_insert = rs_inf.get_row_data()
            # rs_inf_insert.append('m')
            # print(rs_inf_insert)
            cursor.execute(sql, rs_inf_insert)  # sql和data之间以","隔开
            db.commit()

        print("已插入" + str(i) + "只股票信息")
        i = i + 1

    # print(data_list)
    db.close()
    bs.logout()

def Calculate_days(ipoday):
    time_string = ipoday # 这里可以是任意的时间格式
    end = parser.parse(time_string)
    # print (type(end))# <type 'datetime.datetime'>
    # print (end.strftime('%Y-%m-%d %H:%M:%S')) # 2016-12-22 13:58:59
    start = datetime.datetime.now()
    # print(start)

    print ((start-end).days) # 0 天数
    return ((start-end).days)



get_stock_history_data()
# print(compare_time('2019-01-01', '2019-03-01'))

#增加一列主键自己序号
#ALTER TABLE all_stock_historydata_interval ADD id INT AUTO_INCREMENT,add PRIMARY KEY (id);
#DELETE from all_stock_historydata_interval where id > 435836;
