from django.urls import path
from .views import UserView


app_name = "get_events_service"

urlpatterns = [
    path('', UserView.as_view()),
]
