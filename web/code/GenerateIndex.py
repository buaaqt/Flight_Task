import sqlite3
import csv

'''
根据数据里的出发时间和到达时间来计算飞行时间，并保存在数据库里
计算出的飞行时间只精确到分钟，并且单位也为分钟
'''
def calculate_time():
    month_day=[31,28,31,30,31,30,31,31,30,31,30,31]
    conn = sqlite3.connect("D:\web\web\APP.db")
    c = conn.cursor()
    c.execute('SELECT id FROM Model_airplane ORDER BY id DESC LIMIT 1')
    data = c.fetchone()
    plane_id = data[0]+1
    for i in range(1,plane_id):
        c.execute('SELECT * FROM Model_airplane WHERE id=?',(i,))
        data=c.fetchone()
        start_list=data[4].split(" ")
        start_date=start_list[0]
        start_time=start_list[1]
        end_list=data[5].split(" ")
        end_date=end_list[0]
        end_time=end_list[1]
        start_date_list=start_date.split("-")
        end_date_list=end_date.split("-")

        start_date_year=int(start_date_list[0])
        end_date_year=int(end_date_list[0])
        start_date_month=int(start_date_list[1])
        end_date_month=int(end_date_list[1])
        start_date_day=int(start_date_list[2])
        end_date_day=int(end_date_list[2])
        start_time_list = start_time.split(":")
        end_time_list = end_time.split(":")
        start_time_hour=int(start_time_list[0])
        end_time_hour=int(end_time_list[0])
        start_time_minute=int(start_time_list[1])
        end_time_minute=int(end_time_list[1])
        part1 = end_date_year - start_date_year
        part2 = end_date_month - start_date_month
        part3 = end_date_day - start_date_day
        part4 = end_time_hour - start_time_hour
        part5 = end_time_minute - start_time_minute
        if start_date_year%400==0:
            month_day[1]=29
        elif start_date_year%4==0&start_date_year%100!=0:
            month_day[1]=29
        else:
            month_day[1]=28
        time=part1*12*month_day[start_date_month-1]*24*60\
             +part2*month_day[start_date_month-1]*24*60+part3*24*60+part4*60+part5
        spend_time=str(time)
        c.execute('UPDATE Model_airplane SET spendtime=? WHERE id=?', (spend_time,i,))
    conn.commit()
    conn.close()


#建航班信息表
def create_airplane():
    conn=sqlite3.connect("D:\web\web\APP.db")
    c=conn.cursor()
    c.execute('''DROP TABLE IF EXISTS Model_airplane''')
    c.execute('''CREATE TABLE Model_airplane
                (id INTEGER PRIMARY KEY,
                number TEXT,
                departure TEXT,
                arrival TEXT,
                depart_time TEXT,
                arrive_time TEXT,
                spendtime TEXT,
                airline TEXT,
                price TEXT,
                delay TEXT,
                delay_rate TEXT)''')
    '''
    csv_file = csv.reader(open('Data.csv', 'r'))
    i = 0
    for data in csv_file:
        print(type(data))
        c.execute("INSERT INTO Model_airplane VALUES (?,?,?,?,?,?,?,?,?,?,?)",(i+1,data[i]['航班编号'],data[i]['出发地'],data[i]['目的地'],data[i]['出发时间'],data[i]['到达时间'],data[i]['飞行时间'],data[i]['航空公司'],data[i]['最低价格'],data[i]['禁运事项'],data[i]['AI预测延误概率']))
        i=i+1
    '''
    with open('flight.txt', "r") as f:
        f.seek(0, 0)
        data_str = f.read()
        data_str = data_str.replace('\n', '')
        #data_str = data_str.replace(' ', '')
        string="]\n["
        data_str=data_str.replace(string,",")
        data = list(eval(data_str))
        length = len(data)
    for i in range(length):
        list_time=data[i]['出发时间'].split(" ")
        data[i]['出发时间']=list_time[1]+" "+list_time[2]
        list_time = data[i]['到达时间'].split(" ")
        data[i]['到达时间'] = list_time[1] + " " + list_time[2]
        c.execute("INSERT INTO Model_airplane VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
        i+1, data[i]['航班编号'].replace(" ",""), data[i]['出发地'].replace(" ",""), data[i]['目的地'].replace(" ",""), data[i]['出发时间'], data[i]['到达时间'], data[i]['飞行时间'],
        data[i]['航空公司'].replace(" ",""), data[i]['最低价格'].replace(" ",""), "正常", data[i]['AI预测延误概率'].replace(" ","")))
    conn.commit()
    conn.close()


#建用户信息表
def create_user_table():
    conn = sqlite3.connect("D:\web\web\APP.db")
    c=conn.cursor()
    c.execute('''DROP TABLE IF EXISTS Model_user''')
    c.execute('''CREATE TABLE Model_user
                   (account TEXT PRIMARY KEY,
                   password TEXT,
                   plane_marked TEXT,
                   if_picked TEXT,
                   information TEXT,
                   if_manage TEXT)''')
    conn.commit()
    conn.close()

create_airplane()
calculate_time()
create_user_table()
