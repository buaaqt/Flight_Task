
import sys
sys.path.append('../')
from Model.models import airplane


#按价格排序（函数内调用，不是提供给外部的接口）
def price_sort(data):
    for i in range(len(data)):
        min_price = int(data[i]['price'])
        index=i
        for j in range(i, len(data)):
            #print(j,int(data[j][8]))
            if int(data[j]['price']) < min_price:
                index = j
                min_price = int(data[i]['price'])
            mark = data[i]
            data[i] = data[index]
            data[index] = mark
    return data

#按飞行时间排序 （函数内调用，不是提供给外部的接口）
def time_sort(data):
    for i in range(len(data)):
        min_spend = int(data[i]['spendtime'])
        index=i
        for j in range(i, len(data)):
            #print(j,int(data[j][8]))
            if int(data[j]['spendtime']) < min_spend:
                index = j
                min_spend = int(data[i]['spendtime'])
            mark = data[i]
            data[i] = data[index]
            data[index] = mark
    return data

'''
比较两个时间大小
time1小的话返回1.否则返回0
两个参数都是字符串类型
'''
def compare(time1,time2):
    time1_list_1=time1.split(" ")
    time2_list_1=time2.split(" ")
    time1_list=time1_list_1[1].split(":")
    time2_list=time2_list_1[1].split(":")
    time1_hour=int(time1_list[0])
    time1_minute=int(time1_list[1])
    time1_second=int(time1_list[2])
    time2_hour=int(time2_list[0])
    time2_minute=int(time2_list[1])
    time2_second=int(time2_list[2])
    if time1_hour==time2_hour:
        if time1_minute==time2_minute:
            if time1_second<time2_second:
                return 1
            else:
                return 0
        elif time1_minute<time2_minute:
            return 1
        else:
            return 0
    elif time1_hour<time2_hour:
        return 1
    else:
        return 0

'''
按出发时间排序
'''
def dpt_time_sort(data):
    for i in range(len(data)):
        min_spend = data[i]['depart_time']
        index=i
        for j in range(i, len(data)):
            #print(j,int(data[j][8]))
            if compare(data[j]['depart_time'],min_spend)==1:
                index = j
                min_spend = data[i]['depart_time']
            mark = data[i]
            data[i] = data[index]
            data[index] = mark
    return data


'''
两地间查询，flag代表是否按价格排序,flag1代表是否按飞行时间排序,flag2代表是否按出发时间排序（三种排序方式只能选择一种）
因现在数据里飞行时间并没有完善，所以按飞行时间排序只适用于测试数据
depart表示出发地，arrive目的地，date为出发日期，格式例如 2019/3/21
前三个参数都是字符串形式，后三个参数是int
返回结果是列表里嵌套元组的结构，即列表每一个元素是字典，每一字典里是一个航班的信息
'''
def search_place(depart,arrive,date,flag,flag1,flag2):
    qs=airplane.objects.filter(departure=depart,arrival=arrive).values()
    data=[]
    for air in qs:
        data.append(air)
    if len(data)==0:
        return data
    data_new=[]
    for i in range(len(data)):
        #print(data[i])
        date_list=data[i]['depart_time'].split(" ")
        list1=data_list[0].split("-")
        list2=date.split("-")
        if int(list1[0])==int(list2[0]) and int(list1[1])==int(list2[1]) and int(list1[2])==int(list2[2]):
            data_new.append(data[i])
    if flag==1:
        data1=data_new
        data=price_sort(data1)
    elif flag1==1:
        data1 = data_new
        data = time_sort(data1)
    elif flag2==1:
        data1=data_new
        data=dpt_time_sort(data1)
    else:
        return data_new
    return data

'''
航班编号查询
plane_num是所要查询的航班编号，类型为字符串
返回结果是列表里嵌套字典的结构，即列表每一个元素是字典，每一字典里是一个航班的信息
'''
def search_number(plane_num,date,flag,flag1,flag2):
    qs=airplane.objects.filter(number=plane_num).values()
    data=[]
    for air in qs:
        data.append(air)
    if len(data)==0:
        return data
    data_new=[]
    for i in range(len(data)):
        #print(data[i])
        date_list=data[i]['depart_time'].split(" ")
        list1=date_list[0].split("-")
        list2=date.split("-")
        if int(list1[0])==int(list2[0]) and int(list1[1])==int(list2[1]) and int(list1[2])==int(list2[2]):
            data_new.append(data[i])
    if flag==1:
        data1=data_new
        data=price_sort(data1)
    elif flag1==1:
        data1 = data_new
        data = time_sort(data1)
    elif flag2==1:
        data1=data_new
        data=dpt_time_sort(data1)
    else:
        return data_new
    return data

'''
查询航班（后台管理人员）
plane_id为要查询的航班的序号
返回的数据是列表内字典类型，字典里是航班的信息
参数是int类型
'''
def search_plane_im(plane_id):
    qs=airplane.objects.filter(id=plane_id).values()
    data=[]
    for air in qs:
        data.append(air)
    if len(data)==0:
        return data
    return data

'''
查询航班信息后台管理人员
plane_id为要查询的航班的序号
flag为0时返回航班编号，为1时返回出发地，为2时返回目的地，为3时返回出发时间，为4时返回到达时间
为5时返回飞行时间，为6时返回航空公司，为7时返回最低价格，为8时返回状态，为9时返回航班延误概率
两个参数都是int类型
返回的数据是列表类型，列表里的元素为字典，字典为要查询的信息
返回0的话代表出错
'''
def search_plane_part(plane_id,flag):
    if flag == 0:
        qs=airplane.objects.filter(id=plane_id).values('number')
    elif flag == 1:
        qs=airplane.objects.filter(id=plane_id).values('departure')
    elif flag == 2:
        qs=airplane.objects.filter(id=plane_id).values('arrival')
    elif flag == 3:
        qs=airplane.objects.filter(id=plane_id).values('depart_time')
    elif flag == 4:
        qs=airplane.objects.filter(id=plane_id).values('arrive_time')
    elif flag == 5:
        qs=airplane.objects.filter(id=plane_id).values('spendtime')
    elif flag == 6:
        qs=airplane.objects.filter(id=plane_id).values('airplane')
    elif flag == 7:
        qs=airplane.objects.filter(id=plane_id).values('price')
    elif flag == 8:
        qs=airplane.objects.filter(id=plane_id).values('delay')
    elif flag == 9:
        qs=airplane.objects.filter(id=plane_id).values('delay_rate')
    else:
        print("没有这种查询方式")
    #print(qs)
    data=[]
    for air in qs:
        data.append(air)
    if len(data)!=1:
        print("id重复")
        return 0
   
    return data

'''
更新航班信息（后台管理人员）
plane_id是你所有更改的航班的序号
flag为0时要更新的是相应的航班编号的值，为1时要更新的是出发地，为2 时要更新的是目的地
为3的时候要更新的是相应的出发时间，为4的时候要更新的是相应的到达时间，为5时要更新的时飞行时间
为6时要更新的是相应的航空公司，为7的时候要更新的是最低价格，为8的时候要更新的是状态，
为9的时候要更新的是相应的航班延误概率
new为新值
前两个参数是int，最后一个是字符串类型
返回0代表出错，返回1代表成功
'''
def update_plane(plane_id,flag,new):
    if flag==0:
        airplane.objects.filter(id=plane_id).update(number=new)
    elif flag==1:
        airplane.objects.filter(id=plane_id).update(departure=new)
    elif flag==2:
        airplane.objects.filter(id=plane_id).update(arrival=new)
    elif flag==3:
        airplane.objects.filter(id=plane_id).update(depart_time=new)
    elif flag==4:
        airplane.objects.filter(id=plane_id).update(arrive_time=new)
    elif flag==5:
        airplane.objects.filter(id=plane_id).update(spendtime=new)
    elif flag==6:
        airplane.objects.filter(id=plane_id).update(airline=new)
    elif flag==7:
        airplane.objects.filter(id=plane_id).update(price=new)
    elif flag==8:
        airplane.objects.filter(id=plane_id).update(delay=new)
    elif flag==9:
        airplane.objects.filter(id=plane_id).update(delay_rate=new)
    else:
        print("没有这种更新方式")
        return 0
    return 1

'''
增加航班（后台管理人员）
11个参数分别是代表着出发地，目的地，出发时间，到达时间，飞行时间，航空公司，最低价格，禁运事项，延误概率
11个参数都是字符串类型
返回1代表操作成功
'''
def add_plane(dpt,arv,dpt_time,arv_time,spt,line,pie,dly,rate):
    airplane.objects.create(departure=dpt,arrival=arv,depart_time=dpt_time,arrive_time=arv_time,spendtime=spt,airline=line,price=pie,delay=dly,delay_rate=rate)
    return 1

'''
删除航班（后台管理人员）
plane_id为要删除的航班的序号
参数为int
返回1代表操作成功
'''
def delete_plane(plane_id):
    qs=airplane.objects.filter(id=plane_id).delete()
    return 1
'''
接受到航班延误信息对数据库进行更新
plane_id为延误的航班的序号,类型为int，time为延误的时间，单位是分钟，类型为int
返回0出错，返回1成功
'''
def delay_plane(plane_id,time):
    month_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    qs=airplane.objects.filter(id=plane_id)
    data=[]
    for air in qs:
        data.append(air)
    if len(data)!=1:
        print("id重复")
        return 0
    dpt_list=data[0].depart_time.split(" ")
    arv_list=data[0].arrive_time.split(" ")
    dpt_date=dpt_list[0]
    dpt_time=dpt_list[1]
    arv_date=arv_list[0]
    arv_time=arv_list[1]
    dpt_time_list=dpt_time.split(":")
    arv_time_list=arv_time.split(":")
    dpt_date_list=dpt_date.split("-")
    arv_date_list=arv_date.split("-")
    dpt_time_hour=int(dpt_time_list[0])
    dpt_time_minute = int(dpt_time_list[1])
    arv_time_hour = int(arv_time_list[0])
    arv_time_minute = int(arv_time_list[1])
    dpt_date_year = int(dpt_date_list[0])
    dpt_date_month = int(dpt_date_list[1])
    dpt_date_day = int(dpt_date_list[2])
    arv_date_year = int(arv_date_list[0])
    arv_date_month = int(arv_date_list[1])
    arv_date_day = int(arv_date_list[2])
    last_dpt_minute=dpt_time_minute
    last_dpt_hour = dpt_time_hour
    last_dpt_day = dpt_date_day
    last_dpt_month= dpt_date_month
    last_dpt_year = dpt_date_year
    last_arv_minute = arv_time_minute
    last_arv_hour = arv_time_hour
    last_arv_day = arv_date_day
    last_arv_month = arv_date_month
    last_arv_year = arv_date_year
    dpt_time_minute=(dpt_time_minute+time)%60
    part=int((last_dpt_minute+time)/60)
    dpt_time_hour=(dpt_time_hour+part)%24
    part=int((last_dpt_hour+part)/24)
    dpt_date_day=(dpt_date_day+part)%month_day[dpt_date_month]
    if dpt_date_year%400==0:
        month_day[1]=29
    if dpt_date_year%4==0&dpt_date_year%100!=0:
        month_day[1]=29
    part=int((last_dpt_day+part)/month_day[dpt_date_month])
    dpt_date_month=(dpt_date_month+part)%12
    part=int((last_dpt_month+part)/12)
    dpt_date_year=dpt_date_year+part
    arv_time_minute = (arv_time_minute + time) % 60
    part = int((last_arv_minute + time) / 60)
    arv_time_hour = (arv_time_hour + part) % 24
    part = int((last_arv_hour + part) / 24)
    arv_date_day = int((arv_date_day + part) % month_day[arv_date_month])
    if arv_date_year % 400 == 0:
        month_day[1] = 29
    if arv_date_year % 4 == 0 & arv_date_year % 100 != 0:
        month_day[1] = 29
    part = int((last_arv_day + part) / month_day[arv_date_month])
    arv_date_month = (arv_date_month + part) % 12
    part = int((last_arv_month + part) / 12)
    arv_date_year = arv_date_year + part
    dpt_new=str(dpt_date_year)+"-"+str(dpt_date_month)+"-"+str(dpt_date_day)+" "+str(dpt_time_hour)+":"\
            +str(dpt_time_minute)+":00"
    arv_new = str(arv_date_year) + "-" + str(arv_date_month) + "-" + str(arv_date_day) + " " + str(
        arv_time_hour) + ":" + str(arv_time_minute) + ":00"
    airplane.objects.filter(id=plane_id).update(depart_time=dpt_new)
    airplane.objects.filter(id=plane_id).update(arrive_time=arv_new)
    airplane.objects.filter(id=plane_id).update(delay="延误")
    return 1

#测试航班信息表
def test_airplane():
    print("广州到北京的航班按价格排序:")
    print(search_place("广州","北京","2019-04-23",1,0,0))
    print("广州到北京的航班按飞行时间排序:")
    print(search_place("广州", "北京","2019-04-23",0,1,0))
    print("广州到北京的航班按出发时间排序:")
    print(search_place("广州", "北京", "2019-04-23", 0, 0, 1))
    print("航班编号为SC7238的航班信息：")
    print(search_number("HU7238"))

    delay_plane(2,20)
