from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=50)
    coordinates = models.CharField(max_length=40)
    description = models.TextField()
    isInfinite = models.BooleanField(default=False) # set true if event is infinite.
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    price = models.IntegerField()
    peopleCount = models.IntegerField()
