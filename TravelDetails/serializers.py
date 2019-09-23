from rest_framework import serializers


class TravelRequestSerializer(serializers.Serializer):
    schedules = serializers.ListField(child=serializers.DictField(required=True), required=True)
    trip_plan = serializers.DictField(required=True)
    prefered_time = serializers.IntegerField(required=True)
