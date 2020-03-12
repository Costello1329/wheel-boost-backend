from math import sqrt

from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from main.models import Event


class UserView(APIView):
    def post(self, request):
        coordinates = request.data["coordinates"]  # 40.7143528;-74.0059731 такого вида
        x, y = coordinates.split(";")
        x, y = float(x), float(y)
        now = datetime.datetime.now()
        end_date = now + datetime.timedelta(days=1)
        events = Event.objects.filter(startTime__gte=now, startTime__lte=end_date)
        events_out = []
        for event in events:
            x1, y1 = event.split(";")
            range = sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
            if range < 99999999999:
                events_out.append(event)
        body = {
            "events": events_out
        }
        return Response(body, status=200, content_type="application/json")