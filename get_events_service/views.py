from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from math import sin, cos, acos, pi
from main.models import Event

k_nearest_events_radius_in_kms = 5


# TODO: Use more time-driven metrics:
def get_distance_in_kms(first_latitude, first_longitude, second_latitude, second_longitude):
    r = 6371 # earth's radius.
    first_latitude *= pi / 180
    second_latitude *= pi / 180
    first_longitude *= pi / 180
    second_longitude *= pi / 180

    return r * acos(
        sin(first_latitude) * sin(second_latitude) +
        cos(first_latitude) * cos(second_latitude) * cos(first_longitude - second_longitude)
    )


def is_this_event_near(driver_latitude, driver_longitude, event_latitude, event_longitude):
    return get_distance_in_kms(
        driver_latitude,
        driver_longitude,
        event_latitude,
        event_longitude
    ) < k_nearest_events_radius_in_kms


class UserView(APIView):
    def post(self, request):
        coordinates = request.data["coordinates"]
        driver_latitude, driver_longitude = coordinates.split(";")
        driver_latitude, driver_longitude = float(driver_latitude), float(driver_longitude)
        now = datetime.datetime.now()
        end_date = now + datetime.timedelta(days=1)
        events = Event.objects.filter(endTime__gte=now, endTime__lte=end_date)
        events_out = []

        for event in events:
            event_latitude, event_longitude = event.coordinates.split(";")
            event_latitude, event_longitude = float(event_latitude), float(event_longitude)

            if is_this_event_near(driver_latitude, driver_longitude, event_latitude, event_longitude):
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

        body = {
            "events": events_out
        }

        return Response(body, status=200, content_type="application/json")
