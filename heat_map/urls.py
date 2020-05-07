from django.urls import path
from .views import UserView


app_name = "heat_map"

urlpatterns = [
    path('', UserView.as_view()),
]
