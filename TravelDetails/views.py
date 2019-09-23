from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from TravelDetails.services import determine_fastest_route


@api_view(['POST'])
def fastest_travel_time(request):
    determine_fastest_route(request.data)
    return Response('abcd', status=status.HTTP_200_OK)
