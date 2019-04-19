from django.http import HttpResponse

from Model.models import airplane
from Model.models import user

import json

def testdb(request):
   

    list=airplane.objects.all()

    list2=[]

    for var in list:
        data={}
        data['id']=var.id
        data['departure']=var.departure
        data['arrival']=var.arrival
        data['dpt_airport']=var.dpt_airport
        data['arv_airport']=var.arv_airport
        data['depart_time']=var.depart_time
        data['arrive_time']=var.arrive_time
        data['number']=var.number
        data['spendtime']=var.spendtime
        data['airline']=var.airline
        data['price']=var.price
        data['delay']=var.delay
        data['delay_rate']=var.delay_rate
        data['merge_from']=var.merge_from
        data['merge_to']=var.merge_to
        list2.append(data)

    c=json.dumps(list2)
    


    return HttpResponse(c)
