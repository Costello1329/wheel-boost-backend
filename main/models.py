from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=50)
    coordinates = models.CharField(max_length=40)
    description = models.TextField()
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    price = models.IntegerField()
    peopleCount = models.IntegerField()
