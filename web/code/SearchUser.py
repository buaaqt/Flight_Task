import sys
sys.path.append('../')
from Model.models import airplane
from Model.models import user



'''
更新用户信息
user_acc代表要更新的用户的账号
flag为0代表要更新的标记购买的航班，为1时代表要更新是否有接机人，为2时代表更新接机人信息，为3时代表更新是否由管理员权限
new为新值
第一个和最后一个参数为字符串类型，第二个参数为int类型
返回0出错，返回1成功
'''
def update_user(user_acc,flag,new):
    if flag==0:
        user.objects.filter(account=user_acc).update(plane_marked=new)
    elif flag==1:
        user.objects.filter(account=user_acc).update(if_picked=new)
    elif flag==2:
        user.objects.filter(account=user_acc).update(information=new)
    elif flag == 3:
        user.objects.filter(account=user_acc).update(if_manage=new)
    else:
        print("没有这种更新方式")
        return 0
    return 1

'''
查询用户信息（后台管理人员）
user_acc是要查询的用户的账号
返回的是列表内字典类型
返回0代表出错
'''
def search_user(user_acc):
    qs=user.objects.filter(account=user_acc).values()
    data=[]
    for air in qs:
        data.append(air)
    if len(data)!=1:
        print("用户名重复或不存在用户")
        return 0
    return data

'''
查询用户信息（后台管理人员）
user_acc代表要查询的用户的账号
flag为0时代表查询用户标记购买的航班，为1时代表查询用户是否有接机人，为2时代表查询用户接机人信息，为3时代表查询用户是否有管理员权限
返回的时列表类型，列表里是字典，字典是里时要查询的信息
第一个参数时字符串类型，第二个参数时int类型
'''
def search_user_part(user_acc,flag):
    if flag==0:
        qs=user.objects.filter(account=user_acc).values('plane_arked')
    elif flag==1:
        qs=user.objects.filter(account=user_acc).values('if_picked')
    elif flag==2:
        qs=user.objects.filter(account=user_acc).values('information')
    elif flag == 3:
        qs=user.objects.filter(account=user_acc).values('if_manage')
    else:
        print("没有这种查询方式")
        return 0
    data=[]
    for u in qs:
        data.append(u) 
    return data

'''增加用户（后台管理员）
参数为要添加的用户的信息，分别为账号，密码，标记购买的航班，是否有接机人，接机人信息，是否有管理员权限
参数都为字符串类型
返回1成功
'''
def add_user(acc,pwd,marked,picked,ifm,manage,code):
    user.objects.create(account=user_acc,password=pwd,plane_marked=marked,if_picked=picked,information=ifm,if_manage=manage,verify=code)
    return 1

'''
删除用户（后台管理员）
user_acc代表要删除的用户的账号
参数为字符串类型
返回1代表成功
'''
def delete_user(user_acc):
    user.objects.filter(account=user_acc).delete()
    return 1

'''
user_cc为账号名，pwd是密码，两种都是字符串类型
当户名user_acc还没有被注册返回1，当应被注册且密码与数据库一样并且是普通用户
返回2，当应被注册且密码与数据库一样并且拥有管理权限返回3，,当应被注册且密码与数据库一样并且是群主返回4
与数据库不一样返回5
'''
def judge_user(user_acc,pwd):
    qs=user.objects.filter(account=user_acc).values()
    data=[]
    for u in qs:
        data.append(u)
    #print(len(data))
    if len(data)>1:
        return 0
    elif len(data)==0:
        return 1
    else:
        user_password=data[0]['password']
        if user_password==pwd:
            manage=data[0]['if_manage']
            if manage == "0":
                return 2
            elif manage=="1":
                return 3
            else:
                return 4
        else:
            return 5

'''
用户注册时录入用户的账号密码
acc为账号名，pwd为密码，manage为1代表用户注册的是拥有管理权限的账号，manage为0代表是
用户注册的是不拥有管理权限的普通账号
三个参数都是字符串类型\
返回1注册成功,返回0失败（已被注册）
'''
def record_user(acc,pwd,manage):
    tag=judge_user(acc,pwd)
    #如果账户名acc没有被注册过
    #print(acc)
    print(tag)
    if tag==1:
        user.objects.create(account=acc,password=pwd,if_manage=manage,plane_marked=" ",if_picked="0",information=" ")
        return 1
    else:
        return 0

'''
此函数用与用户标记购买某个航班时判断该航班是否已经被用户标记购买
返回0即表示此航班序号的航班已经被标记过，返回1表示没有别标记过
第一个参数为字符串类型，第二个参数为int
'''
def judge_same(plane_str,plane_id):
    plane_str_list=plane_str.split("-")
    for i in range(len(plane_str_list)):
        if plane_str_list[i]==str(plane_id):
            return 0
    return 1

'''
用户每次选中购买某个航班，录入该航班信息
user_acc代表用户的账号名，即代表是哪一个用户选中了航班
plane_id代表被该用户选中购买的航班的序号
plane_num代表该用户选中购买的航班的编号
说明：因为一个航班编号可以对应多个航班，所以在录入的时候增加了序号这一特征，航班序号在数据库建表已经保存
存在用户信息表里的确认购买的航班的信息以“航班1序号-航班2序号....”的结构存储
两个参数的类型都是字符串类型
返回0出错，返回1成功
'''
def record_user_plane(user_acc,plane_id):
    qs=user.objects.filter(account=user_acc).values('plane_marked')
    plane_tur=[]
    for u in qs:
        plane_tur.append(u)
    if len(plane_tur)!=1:
        return 0
    #print(plane_tur)
    #print(user_acc)
    plane_str=plane_tur[0]['plane_marked']
    tag=judge_same(plane_str,plane_id)
    if tag==0:
        return 0
    if plane_str!=" " and plane_str!="":
        plane_str=plane_str+"-"+str(plane_id)
    else:
        plane_str=str(plane_id)
    #print(plane_str)
    user.objects.filter(account=user_acc).update(plane_marked=plane_str)
    return 1

'''
取消购买某个航班
user_acc为当前用户的账号，plane_id为要取消购买的航班的编号
第一个参数时字符串类型，第二个参数时int类型
返回0出错，返回1成功
'''
def cancel_marked(user_acc,plane_id):
    qs=user.objects.filter(account=user_acc).values('plane_marked')
    data=[]
    for u in qs:
        data.append(u)
    if len(data)!=1:
        return 0
    plane_str=data[0].plane_marked
    string=plane_str.split("-")
    tag=0
    for i in range(len(string)):
        if string[i]==plane_id:
            tag=i
            break
    string1=""
    tag1=0
    for i in range(len(string)):
        if i!=tag:
            if tag1==0:
                string1=string1+string[i]
                tag1=1
            else:
                string1=string1+"-"+string[i]
        else:
            string1=string1
    user.objects.filter(account=user_acc).update(plane_marked=string1)
    return 1

'''
录入用户有关是否被接机和接机人信息
user_acc代表当前用户名
flag代表该用户是否有接机人(1为有，0为没有）
im代表当flag为1时用户填写的接机人信息
第一个和最后一个参数都是字符串类型，第二个参数是int
'''
def record_user_picked(user_acc,flag,im):
    user.objects.filter(account=user_acc).update(if_picked=flag)
    if flag==1:
        user.objects.filter(account=user_acc).update(information=im)
    return 1

'''
查询用户已确认购买的航班
user_acc为用户账号名，类型为字符串
返回结果是列表里嵌套字典的结构，即列表每一个元素是字典，每一字典里是一个航班的信息
'''
def search_user_plane(user_acc):
    qs=user.objects.filter(account=user_acc).values('plane_marked')
    plane_tur=[]
    #print(qs)
    for u in qs:
        plane_tur.append(u)
    if len(plane_tur)==1 and plane_tur[0]['plane_marked']=="":
        return plane_tur
    plane_str=plane_tur[0]['plane_marked']
    #print(plane_str)
    plane_num_list=plane_str.split("-")
    plane_list=[]
    for i in range(len(plane_num_list)):
        #print(plane_num_list[i])
        plane_id=int(plane_num_list[i])
        data=[]
        qs_air=airplane.objects.filter(id=plane_id).values()
        for air in qs_air:
            data.append(air)
        plane_list.append(data[0])
    return plane_list

#测试用户信息表
def test_user():
    record_user("小H","16061083","0")
    record_user("小K","16061064","1")
    record_user("小L","16061077","0")
    record_user("小X","16061102","0")
    record_user("小Q","16061045","0")
    record_user("小M","16061068","0")
    record_user("小Z","16061087","0")
    record_user("小Y","16061064","0")


    record_user_plane("小K",21)
    record_user_picked("小K", 1, "小Y")
    record_user_plane("小H",19)
    record_user_picked("小H",1,"小L")

    record_user_plane("小K",20)

    print("用户小K确认购买的航班的航班信息:")
    data=search_user_plane("小K")
    print(type(data))
    print(data[0])
    print(data[0]['number'])
    
    print("用户小H确认购买的航班的航班信息:")
    print(search_user_plane("小H"))

    print("当账户名user_acc还没有被注册返回1，当应被注册且密码与数据库一样并且是普通用户返回2")
    print("当应被注册且密码与数据库一样并且拥有管理权限返回3，与数据库不一样返回4")
    print("账号小W密码16061121用户类型标号：")
    print(judge_user("小W", "16061121"))
    print("账号小K密码16061064用户类型标号：")
    print(judge_user("小K", "16061064"))
    print("账号小K密码16061121用户类型标号：")
    print(judge_user("小K", "16061121"))
    print("账号小H密码1606083用户类型标号：")
    print(judge_user("小H", "16061083"))

