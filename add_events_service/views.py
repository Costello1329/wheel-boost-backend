from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import Event


class UserView(APIView):
    def post(self, request):
        # TODO: Protocol validations.
        events = request.data["events"]

        for event in events:
            # datetime.fromisoformat('2011-11-04 00:05:23.283+00:00')
            Event.objects.create(
                title=event["title"],
                description=event["description"],
                coordinates=event["coordinates"],
                startTime=datetime.fromisoformat(event["startTime"][:-1]),
                endTime=datetime.fromisoformat(event["endTime"][:-1]),
                price=event["price"],
                peopleCount=event["peopleCount"]
            )

        return Response(status=200, content_type="application/json")
