from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.core.serializers.json import json
from urllib.parse import unquote
import sys
import math
import time
import json


'''
import os
temp_path=os.getcwd()
f_path=os.path.abspath(os.path.dirname(temp_path)+os.path.sep+".")
'''
sys.path.append(r'/data/wwwroot/web/web/code')
from Model.models import airplane
from Model.models import user
import SearchPlane
import SearchUser
import eml


def hello(request):
    return HttpResponse("Hello world ! ")

def ChangeHP(request):
    return render(request,'index.html')

def ChangeHP2(request):
    return render(request,'index2.html')

def search_by_ID(request):
    #return render(request, 'search_FID_results.html')
    FlightId = request.GET['FlightId']
    FlightTime = request.GET['FlightTime']
    data=SearchPlane.search_number(FlightId,FlightTime,0,0,0)
    print(data)
    return render(request,'search_FID_results.html',{'FlightTime':FlightTime,'FlightId':FlightId,'data':data})

def search_by_FT(request):
    FlightFrom = request.GET['FlightFrom']
    FlightTo = request.GET['FlightTo']
    FlightTime = request.GET['FlightTime']
    data=SearchPlane.search_place(FlightFrom,FlightTo,FlightTime,0,0,0)
    return render(request,'search_FFT_results.html',{'FlightTime':FlightTime,'FlightFrom':FlightFrom,'FlightTo':FlightTo,'data':data})

def admin(request):
    return render(request,'admin_login.html')

def admin_login(request):
    username = request.GET['username']
    password = request.GET['password']

    plane_num=airplane.objects.count()
    user_num=user.objects.count()
    data=[]
    dic={}
    dic['plane_num']=plane_num
    dic['user_num']=user_num
    data.append(dic)

    tag=SearchUser.judge_user(username,password)
    print(tag)
    if tag==3 or tag==4:
        return render(request,'admin_index.html',{'data':data})
    
def search_by_UID(request):
    UserId = request.GET['UserId']
    username = request.GET['AdminId']
    data_user=user.objects.all()
    list_user=[]
    for u in data_user:
        dict_user={}
        dict_user['account']=u.account
        if u.if_manage=="1":
            dict_user['character']="管理员"
        elif u.if_manage=="2":
            dict_user['character']="群主"
        else:
            dict_user['character']="用户"
        data_plane=SearchUser.search_user_plane(u.account)
        dict_user['marked_num']=str(len(data_plane))
        dict_user['plane_im']=data_plane
        list_user.append(dict_user)
    return render(request,'admin_user.html',{'UserId':UserId,'username':username,'data':list_user})


def register_by_app(request):
    if(request.method=='GET'):
        user_acc=unquote(request.GET.get('account',""),encoding="utf-8")
        pwd=unquote(request.GET.get('password',""),encoding="utf-8")
        verifycode=unquote(request.GET.get('verifycode',""),encoding="utf-8")
        flag=request.GET.get('flag',"")

        #print(verifycode)
        
        state={}
        '''
        if flag=="0":
            code=eml.SendVerifyCode(user_acc)
            if code=="0":
                state['status']=0
                state['msg']="发送失败"
            else:
                tag=SearchUser.judge_user(user_acc,"x")
                if tag==1:
                    user.objects.create(account=user_acc,verify=code,if_manage="0")
                    state['status']=1
                    state['msg']="发送成功"
                else:
                    string="用户名已存在"
                    state['status']=0
                    state['msg']=string
        else:
            c_list=[]
            qs=user.objects.filter(account=user_acc).values('verify')
            for c in qs:
                c_list.append(c)
            code=c_list[0]['verify']
            #print(code)
            if verifycode!=code:
                string="验证码错误"
                user.objects.filter(account=user_acc).delete()
                state['status']=0
                state['msg']=string
            else:
        user.objects.filter(account=user_acc).update(password=pwd,if_manage="0",if_picked="0")
        '''
        tag=SearchUser.record_user(user_acc,pwd,"0")
        if tag==1:
            string="注册成功"
            state['status']=1
            state['msg']=string
        else:
            state['status']=0
            state['msg']="注册失败"
                
        response=json.dumps(state,ensure_ascii=False)
        return HttpResponse(response,content_type='application/json; charset=utf-8')
'''
def send_by_app(request):
    if(request.method=='GET'):
        user_acc=request.GET.get('account',"")

        code=eml.SendVerifyCode(user_acc)
        state={}
        if code=="0":
            state['status']=0
            state['msg']="验证码发送失败"

        else:
            tag=SearchUser.judge_user(user_acc,"x")
            if tag==1:
                user.objects.create(account=user_acc,verify=code)
                state['status']=1
                state['msg']="成功"
            else:
                string="用户名已存在"
                state['status']=0
                state['msg']=string
                
        response=json.dumps(state)
        return HttpResponse(response)
'''

def login_by_app(request):
    if(request.method=='GET'):
        account=unquote(request.GET.get('account',""),encoding="utf-8")
        password=unquote(request.GET.get('password',""),encoding="utf-8")

        state={}

        tag=SearchUser.judge_user(account,password)
        
        if tag>1:
            state['status']=1
            state['msg']="成功"
            data=SearchUser.search_user_plane(account)
            data1=[]
            for air in data:
                num=air['id']
                air['id']=str(num)
                data1.append(air)
            state['data']=data1
        else:
            state['status']=0
            state['msg']="用户未注册"

        response=json.dumps(state,ensure_ascii=False)
        return HttpResponse(response,content_type='application/json; charset=utf-8')
            
def search_mark_plane(request):
    if(request.method=='GET'):
        departure=unquote(request.GET.get('departure',""),encoding="utf-8")
        arrival=unquote(request.GET.get('arrival',""),encoding="utf-8")
        number=request.GET.get('number',"")
        date=request.GET.get('date',"")
        account=unquote(request.GET.get('account',""),encoding="utf-8")
        plane_id=unquote(request.GET.get('plane_id',""),encoding="utf-8")
        flag=request.GET.get('flag',"")

        

        state={}

        if flag=="0":
            data=SearchPlane.search_place(departure,arrival,date,0,0,0)
        elif flag=="1":
            data=SearchPlane.search_number(number,date,0,0,0)
        else:
            tag=SearchUser.record_user_plane(account,int(plane_id))
            if tag==0:
                state['status']=0
                state['msg']="用户已标记购买了该航班"
            else:
                data=SearchUser.search_user_plane(account)
                data1=[]
                for air in data:
                    num=air['id']
                    air['id']=str(num)
                    data1.append(air)
                state['status']=1
                state['msg']="标记成功"
                state['data']=data1
            response=json.dumps(state,ensure_ascii=False)
            return HttpResponse(response,content_type='application/json; charset=utf-8')

        if len(data)==0:
            state['status']=0
            state['msg']="没有符合要求的航班"
        else:
            data1=[]
            for air in data:
                num=air['id']
                air['id']=str(num)
                data1.append(air)
            state['status']=1
            state['msg']="查询成功"
            state['data']=data1
            
        response=json.dumps(state,ensure_ascii=False)
        return HttpResponse(response,content_type='application/json; charset=utf-8')

'''
def marked_by_app(request):
    if(request.method=='GET'):
        account=request.GET.get('account',"")
        plane_id=request.GET.get('plane_id',"")

        tag=SearchUser.record_user_plane(account,int(plane_id))

        state={}

        if tag==0:
            state['status']=0
            state['msg']="用户已标记购买了该航班"
        else:
            string="枪支，弹药，军械，警械，管制刀具，爆炸物品，易燃易爆物，剧毒物质，放射性物质，腐蚀性物质，危险溶液等"
            state['status']=1
            state['msg']="成功"
            state['data']=string
        response=json.dumps(state)
        return HttpResponse(response)
'''
 
def searchmarked_cancel(request):
    if(request.method=='GET'):
        account=unquote(request.GET.get('account',""),encoding="utf-8")
        plane_id=request.GET.get('plane_id')
        flag=request.GET.get('flag')

        state={}

        if flag=="1":
            state['status']=1
            state['msg']="查询成功"
        else:
            tag=SearchUser.cancel_marked(account,int(plane_id))
            if tag==1:
                state['status']=1
                state['msg']="取消成功"
            else:
                state['status']=0
                state['msg']="取消错误"
                state['data']=[]
                response=json.dumps(state,ensure_ascii=False)
                return HttpResponse(response,content_type='application/json; charset=utf-8')
        data=SearchUser.search_user_plane(account)
        data1=[]
        for air in data:
            num=air['id']
            air['id']=str(num)
            data1.append(air)
        state['data']=data1
        
        response=json.dumps(state,ensure_ascii=False)
        return HttpResponse(response,content_type='application/json; charset=utf-8')        
    
            
        

        
        
    

