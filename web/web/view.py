from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
import sys
import math
import time
import json
sys.path.append(r'/data/wwwroot/web/web/code')
from Model.models import airplane
import SearchPlane
import SearchUser



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
    return render(request,'search_FID_results.html',{'FlightTime':FlightTime,'FlightId':FlightId,'data':data})


