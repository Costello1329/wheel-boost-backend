from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from math import sin, cos, acos, pi

from get_events_service.apps import Driver
from main.models import Event

k_nearest_events_radius_in_kms = 5
k_expansion_step_in_kms = 1
k_max_radius = 15

initial_time_deviation = 0.5  # (-) 0.5 hour
final_time_deviation = 3  # (+) 3 hour


# TODO: Use more time-driven metrics:
def get_distance_in_kms(first_latitude, first_longitude, second_latitude, second_longitude):
    r = 6371  # Earth's radius.
    first_latitude *= pi / 180
    second_latitude *= pi / 180
    first_longitude *= pi / 180
    second_longitude *= pi / 180

    return r * acos(
        sin(first_latitude) * sin(second_latitude) +
        cos(first_latitude) * cos(second_latitude) * cos(first_longitude - second_longitude)
    )


def is_this_event_near(driver_latitude, driver_longitude, event_latitude, event_longitude, radius):
    return get_distance_in_kms(
        driver_latitude,
        driver_longitude,
        event_latitude,
        event_longitude
    ) < radius


def get_nearest_event(events, driver):
    events_out = []
    for current_radius in range(k_nearest_events_radius_in_kms, k_max_radius, k_expansion_step_in_kms):
        for event in events:
            event_latitude, event_longitude = event.coordinates.split(";")
            event_latitude, event_longitude = float(event_latitude), float(event_longitude)

            if is_this_event_near(driver.latitude, driver.longitude, event_latitude, event_longitude, current_radius):
                event_dict = {
                    "title": event.title,
                    "coordinates": event.coordinates,
                    "description": event.description,
                    "startTime": event.startTime,
                    "endTime": event.endTime,
                    "price": event.price,
                    "peopleCount": event.peopleCount
                }
                events_out.append(event_dict)
        if len(events_out) != 0:
            return events_out
    return events_out


class UserView(APIView):
    def post(self, request):
        coordinates = request.data["coordinates"]
        driver_latitude, driver_longitude = coordinates.split(";")
        driver_latitude, driver_longitude = float(driver_latitude), float(driver_longitude)
        start_date = datetime.datetime.now() - datetime.timedelta(hours=initial_time_deviation)
        end_date = datetime.datetime.now() + datetime.timedelta(hours=final_time_deviation)
        events = Event.objects.filter(endTime__gte=start_date, endTime__lte=end_date)
        driver = Driver(driver_latitude, driver_longitude)
        events_out = get_nearest_event(events, driver)
        body = {
            "events": events_out
        }
        return Response(body, status=200, content_type="application/json")
