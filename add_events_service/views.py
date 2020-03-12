from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Event


class UserView(APIView):
    def post(self, request):
        events = request.data["events"]
        for event in events:
            Event.objects.create(title=event.title, description=event.description, startTime=event.startTime,
                                 endTime=event.endTime, price=event.price, peopleCount=event.peopleCount)
        body = {
            "ok": "ok"
        }
        return Response(body, status=200, content_type="application/json")