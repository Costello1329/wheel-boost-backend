from django.db import models

# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    price = models.IntegerField()
    peopleCount = models.IntegerField()
