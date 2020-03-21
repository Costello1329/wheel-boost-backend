from django.apps import AppConfig


class GetEventsServiceConfig(AppConfig):
    name = 'get_events_service'


class Driver:
    latitude: float
    longitude: float

    def __init__(self, driver_latitude, driver_longitude):
        self.latitude = driver_latitude
        self.longitude = driver_longitude
