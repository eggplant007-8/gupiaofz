import baostock as bs
import pandas as pd
import pymysql


#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

#### 获取证券信息 ####
rs = bs.query_all_stock(day="2019-02-26")
print('query_all_stock respond error_code:'+rs.error_code)
print('query_all_stock respond  error_msg:'+rs.error_msg)

#### 打印结果集 ####
##data_list = {["股票代码"], ["股标名称"], ["半年增长金额"], ["半年增长幅度（%）"]}
data_list = [[]] * 4200
data_list[0] = ["股票代码", "股标名称", "半年增长金额", "半年增长幅度（%）"]

old_day = '2017-02-20'
now_day = '2019-02-26'
difference = 0
proportion = 0
i = 1




def get_all_id():
    while (rs.error_code == '0') & rs.next():
        #### 获取一条记录，将记录合并在一起

        gp = rs.get_row_data()
        dgp = bs.query_stock_basic(code = gp[0])
        print('query_stock_basic respond error_code:' + dgp.error_code)
        print('query_stock_basic respond  error_msg:' + dgp.error_msg)
        print(dgp.get_row_data())

        ##rs_old = bs.query_history_k_data(gp[0],
        ##                             "date,code,open,high,low,close，price_change",
        ##                             start_date = old_day, end_date = old_day,
        ##                             frequency = "d", adjustflag = "3")
        ##print(rs_old.error_code)
        ##print(rs_old.error_msg)

        ##old_data = rs_old.get_row_data()
        ##print(old_data)

        rs_now = bs.query_history_k_data(gp[0],
                                         "date,code,open,high,low,close",
                                         start_date=now_day, end_date=now_day,
                                         frequency="d", adjustflag="3")
        ##print(rs_now.error_code)
        ##print(rs_now.error_msg)

        # now_data = rs_now.get_row_data()
        # print(old_data)
        # print(now_data)

        # if len(old_data):
        #     difference = float(now_data[5]) - float(old_data[2])
        ##print(difference)
            # proportion = difference / float(old_data[2]) * 100
        ##print(float("%.2f" % proportion))
        ##print(proportion)

            # data_list[i] = ([gp[0], gp[2], float("%.2f" % difference), float("%.2f" % proportion)])
            # i = i + 1

    print(data_list)



        ##print(str(gp[0]))
        ##print(str(gp[0][3:9]))
        ##break
        ##data_list.append(gp)
        ##result = pd.DataFrame(data_list, columns=rs.fields)

    # 详细指标参数，参见“历史行情指标参数”章节


def find_gp():
    while (rs.error_code == '0') & rs.next():
        #### 获取一条记录，将记录合并在一起
        ##if(a == 1):
        ##    print(type(rs.get_row_data()[0][4:9]))
        ##    a = 0
        gp = rs.get_row_data()
        if (str(gp[0][3:9]) == '600105'):
            print(gp)
            print("---------------------------------------------------------")
            rs_old = bs.query_history_k_data("sh.600105",
                                             "date,code,open,high,low,close,pctChg",
                                             start_date='2019-02-25', end_date='2019-03-01',
                                             frequency="d", adjustflag="3")
            print(rs_old.error_code)
            print(rs_old.error_msg)




            #### 打印结果集 ####
            data_list = []
            while (rs_old.error_code == '0') & rs_old.next():
                # 获取一条记录，将记录合并在一起
                data_list.append(rs_old.get_row_data())
            result = pd.DataFrame(data_list, columns=rs_old.fields)

            #### 结果集输出到csv文件 ####
            print(data_list)
            break

def import_all_stock_to_mysql():

    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "root", "db_gpfz")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "insert into all_stock_list(stock_code, stock_name, ipodate) values(%s, %s, %s)"

    while (rs.error_code == '0') & rs.next():
        #### 获取一条记录，将记录参入数据库

        gp = rs.get_row_data()
        dgp = bs.query_stock_basic(code = gp[0]).get_row_data()
        # print('query_stock_basic respond error_code:' + dgp.error_code)
        # print('query_stock_basic respond  error_msg:' + dgp.error_msg)

        # print(dgp)
        data = (gp[0], gp[2], dgp[2])
        print(data)

        cursor.execute(sql, data)  # sql和data之间以","隔开
        db.commit()
    # 关闭数据库连接
    db.close()

find_gp()
# import_all_stock_to_mysql()
bs.logout()

