from django.db import models

# Create your models here.
    
class Graph(models.Model):
    case_id = models.CharField(max_length=150)
    activity = models.CharField(max_length=100)
    timestamp = models.CharField(max_length=100)

    def __str__(self):
        return self.case_id
class CaseData(models.Model):
    case_id = models.CharField(max_length=150)
    start_time = models.CharField(max_length=100)
    end_time = models.CharField(max_length=100)
    duration  = models.CharField(max_length=250)
    repairIn5d = models.IntegerField()
    deviceType  = models.CharField(max_length=50)
    servicePoint = models.CharField(max_length=50)
    deviceCat =  models.CharField(max_length=50)
    warranty = models.IntegerField()

    def __str__(self):
        return self.case_id
    
# class Process(models.Model):
#     case_id = models.CharField(max_length=150)
#     activity = models.CharField(max_length=100)
#     timestamp = models.CharField(max_length=100)

#     def __str__(self):
#         return self.case_id
