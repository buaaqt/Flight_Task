from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
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

def register_by_app(request):
    if(request.method=='GET'):
        user_acc=request.GET.get('account',"")
        pwd=request.GET.get('password',"")
        verifycode=request.GET.get('verifycode',"")

        print(verifycode)

        
        c_list=[]
        qs=user.objects.filter(account=user_acc).values('verify')
        for c in qs:
            c_list.append(c)


        code=c_list[0]['verify']
            
        print(code)

        state={}

        if verifycode!=code:
            string="验证码错误"
            user.objects.filter(account=user_acc).delete()
            state['status']=0
            state['msg']=string

        else:
            user.objects.filter(account=user_acc).update(password=pwd,if_manage="0")
            string="成功"
            state['status']=1
            state['msg']=string
                
        response=json.dumps(state)
        return HttpResponse(response)

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

def login_by_app(request):
    if(request.method=='GET'):
        account=request.GET.get('account',"")
        password=request.GET.get('password',"")

        state={}

        tag=SearchUser.judge_user(account,password)
        
        if tag>1:
            state['status']=1
            state['msg']="成功"
            data=SearchUser.search_user_plane(account)
            state['data']=data
        else:
            state['status']=0
            state['msg']="用户未注册"

        response=json.dumps(state)
        return HttpResponse(response)
            
def search_app(request):
    if(request.method=='GET'):
        departure=request.GET.get('departure',"")
        arrival=request.GET.get('arrival',"")
        number=request.GET.get('number',"")
        date=request.GET.get('date',"")
        flag=request.GET.get('flag',"")

        if flag=="0":
            data=SearchPlane.search_place(departure,arrival,date,0,0,0)
        else:
            data=SearchPlane.search_number(number,date,0,0,0)

        state={}
        
        if len(data)==0:
            state['status']=0
            state['msg']="没有符合要求的航班"
        else:
            state['status']=1
            state['msg']="成功"
            state['data']=data
            
        response=json.dumps(state)
        return HttpResponse(response)


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

def search_marked_app(request):
    if(request.method=='GET'):
        account=request.GET.get('account',"")

        data=SearchUser.search_user_plane(account)

        state={}
        state['status']=1
        state['msg']="成功"
        state['data']=data
        
        response=json.dumps(state)
        return HttpResponse(response)
        
        
    
            
        

        
        
    

