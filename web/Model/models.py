from django.db import models

# Create your models here.

class airplane(models.Model):
    id= models.IntegerField(primary_key=True)
    number=models.TextField()
    departure=models.TextField()
    arrival=models.TextField()
    depart_time=models.TextField()
    arrive_time=models.TextField()
    spendtime=models.TextField()
    airline=models.TextField()
    price=models.TextField()
    delay=models.TextField()
    delay_rate=models.TextField()
    dpt_airport=models.TextField(default="xx")
    arv_airport=models.TextField(default="yy")
    merge_from=models.TextField(default="xx")
    merge_to=models.TextField(default="yy")    

class user(models.Model):
    account=models.TextField(primary_key=True)
    password=models.TextField()
    plane_marked=models.TextField()
    if_picked=models.TextField()
    information=models.TextField()
    if_manage=models.TextField()
    verify=models.TextField(default="xxxx")


#class History(models.Model):
    #query = models.CharField(max_length=64)
    #date = models.CharField(max_length=64)

    
    
