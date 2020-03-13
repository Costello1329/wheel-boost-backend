from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Event


class UserView(APIView):
    def post(self, request):
        # TODO: Protocol validations.
        events = request.data["events"]

        for event in events:
            Event.objects.create(
                title=event.title,
                description=event.description,
                coordinates=event.coordinates,
                startTime=event.startTime,
                endTime=event.endTime,
                price=event.price,
                peopleCount=event.peopleCount
            )

        return Response(status=200, content_type="application/json")
