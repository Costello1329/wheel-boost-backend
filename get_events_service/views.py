import json

from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from math import sin, cos, acos, pi
from main.models import Event
from django.core import serializers


k_nearest_events_radius_in_kms = 5


def get_distance_in_kms (x1, y1, x2, y2):
    r = 6371
    x1 *= pi / 180
    x2 *= pi / 180
    y1 *= pi / 180
    y2 *= pi / 180
    return acos(sin(x1)*sin(x2) + cos(x1)*cos(x2)*cos(y1 - y2)) * r


def is_this_event_near(driver_x, driver_y, event_x, event_y):
    return get_distance_in_kms(driver_x, driver_y, event_x, event_y) < k_nearest_events_radius_in_kms


class UserView(APIView):
    def post(self, request):
        coordinates = request.data["coordinates"]  # 40.7143528;-74.0059731 такого вида
        driver_x, driver_y = coordinates.split(";")
        driver_x, driver_y = float(driver_x), float(driver_y)
        now = datetime.datetime.now()
        end_date = now + datetime.timedelta(days=1)
        events = Event.objects.filter(endTime__gte=now, endTime__lte=end_date)
        events_out = []
        for event in events:
            event_x, event_y = event.coordinates.split(";")
            event_x, event_y = float(event_x), float(event_y)
            if is_this_event_near(driver_x, driver_y, event_x, event_y):
                events_out.append(event)
        body = serializers.serialize("json", events_out)
        return Response(body, status=200, content_type="application/json")
