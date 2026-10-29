from rest_framework import serializers

class SensorEventSerializer(serializers.Serializer):
    event_id = serializers.CharField(max_length=50)
    junction_id = serializers.CharField(max_length=10)
    direction = serializers.CharField(max_length=10)
    event_type = serializers.CharField(max_length=20)
    vehicle_id = serializers.CharField(max_length=50)
    vehicle_type = serializers.CharField(max_length=20)
    sequence_no = serializers.IntegerField()
    timestamp = serializers.DateTimeField()