from django.urls import path
from .views import UserView
app_name = "add_events_service"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('', UserView.as_view()),
    ]