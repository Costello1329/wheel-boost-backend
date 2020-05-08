from itertools import chain
from math import log
import datetime
import numpy as np
from django.shortcuts import render
from scipy.stats import norm

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Event, HeatMap

scale = 0.001

upper_left_border = (55.98, 37.29)
upper_right_border = (55.98, 38.05)
lower_left_border = (55.46, 37.29)
lower_right_border = (55.46, 38.05)

map_size_x = round((lower_right_border[1] - lower_left_border[1]) / scale)
map_size_y = round((upper_right_border[0] - lower_right_border[0]) / scale)

initial_time_deviation = 0.5  # (-) 0.5 hour
final_time_deviation = 3  # (+) 3 hour


def update_heat_map():
    heat_map = np.zeros((map_size_x, map_size_y))
    infinite_events = Event.objects.filter(isInfinite=True)
    start_date = datetime.datetime.now() - datetime.timedelta(hours=initial_time_deviation)
    end_date = datetime.datetime.now() + datetime.timedelta(hours=final_time_deviation)
    finite_events = Event.objects.filter(
        isInfinite=False, endTime__gte=start_date, endTime__lte=end_date)
    events = list(chain(infinite_events, finite_events))
    for event in events:
        markup_heat_map(event, heat_map)
    HeatMap.objects.all().delete()
    try:
        db = HeatMap.objects.create(data=heat_map.tobytes())
        db.save()
    except:
        print()
    a = np.frombuffer(HeatMap.objects.all()[0].data)
    print("1")


def check_heat_map_index(x, y):
    if x < 0 or map_size_x <= x or x < 0 or map_size_y <= y:
        return False
    return True


def get_weights(event, loop):
    distribution = norm.pdf(loop, 0)
    people_count_coff = event.peopleCount * 1.25
    price_coff = event.price * 0.10
    return distribution * people_count_coff * price_coff


def drawing_weights(event, heat_map, start_coordinates, loops):
    if loops == 0:
        heat_map[start_coordinates[0], start_coordinates[1]] += get_weights(event, loops)

    if get_weights(event, loops) == 0:
        return
    # adjoining squares to the left and top
    left_top_zone = (start_coordinates[0] + loops - 1, start_coordinates[1] + (loops + 1))
    for i in range(0, loops + 2):
        zone = (left_top_zone[0] + i, left_top_zone[0])
        draw_weights_to_zone(event, loops, zone, heat_map)
        zone = (left_top_zone[0], left_top_zone[0] - i)
        draw_weights_to_zone(event, loops, zone, heat_map)

    # adjoining squares to the right and bottom
    upper_right_zone = (start_coordinates[0] + loops + 1, start_coordinates[1] - (loops + 1))
    for i in range(0, loops + 1):
        zone = (upper_right_zone[0] - i, upper_right_zone[0])
        draw_weights_to_zone(event, loops, zone, heat_map)
        zone = (upper_right_zone[0], upper_right_zone[0] + i)
        draw_weights_to_zone(event, loops, zone, heat_map)

    drawing_weights(event, heat_map, start_coordinates, loops + 1)


def draw_weights_to_zone(event, loops, zone, heat_map):
    if not check_heat_map_index(zone[0], zone[1]):
        heat_map[zone[0], zone[1]] += get_weights(event, loops)


def markup_heat_map(event, heat_map):
    event_latitude, event_longitude = event.coordinates.split(";")
    event_latitude, event_longitude = float(event_latitude), float(event_longitude)
    x, y = get_cell_location(event_latitude, event_longitude)
    if not check_heat_map_index(x, y):
        return
    drawing_weights(event, heat_map, (x, y), 0)


def get_cell_location(latitude, longitude):
    round_scale = -round(log(0.001, 10))
    latitude_location = - int((lower_left_border[0] - round(latitude, round_scale)) / scale) - 1
    longitude_location = - int((lower_left_border[1] - round(longitude, round_scale)) / scale) - 1
    return latitude_location, longitude_location


class UserView(APIView):
    def post(self, request):
        update_heat_map()
        body = {}
        return Response(body, status=200, content_type="application/json")
