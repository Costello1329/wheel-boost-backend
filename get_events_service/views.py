import json
from math import sqrt

from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from main.models import Event
from django.core import serializers

class UserView(APIView):
    def post(self, request):
        coordinates = request.data["coordinates"]  # 40.7143528;-74.0059731 такого вида
        x, y = coordinates.split(";")
        x, y = float(x), float(y)
        now = datetime.datetime.now()
        end_date = now + datetime.timedelta(days=1)
        events = Event.objects.filter(endTime__gte=now, endTime__lte=end_date)
        events_out = []
        for event in events:
            x1, y1 = event.coordinates.split(";")
            x1, y1 = float(x1), float(y1)
            range = sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
            if range < 99999999999:
                events_out.append(event)
            body = serializers.serialize("json", events_out)
        return Response(body, status=200, content_type="application/json")