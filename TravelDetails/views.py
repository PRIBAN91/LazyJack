from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from TravelDetails.serializers import TravelRequestSerializer
from TravelDetails.services import determine_fastest_route


@api_view(['POST'])
def fastest_travel_time(request):
    request_body = TravelRequestSerializer(data=request.data)
    if request_body.is_valid():
        return Response(determine_fastest_route(request_body.data), status=status.HTTP_200_OK)
    else:
        return Response("Invalid request format: {}".format(request_body.errors), status=status.HTTP_400_BAD_REQUEST)
