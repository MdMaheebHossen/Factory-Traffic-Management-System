from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .models import VehicleQueue, ProcessedEvent, Junction, SignalState
from .serializers import SensorEventSerializer
from .traffic_engine import safe_transition

@api_view(['POST'])
def sensor_event_receiver(request):
    serializer = SensorEventSerializer(data=request.data)
    if serializer.is_valid():
        event_id = serializer.validated_data['event_id']
        if ProcessedEvent.objects.filter(event_id=event_id).exists():
            return Response({"error": "Duplicate event ignored"}, status=400)
        ProcessedEvent.objects.create(event_id=event_id)
        
        if serializer.validated_data['event_type'] == 'VEHICLE_ARRIVED':
            VehicleQueue.objects.create(
                direction=serializer.validated_data['direction'],
                vehicle_type=serializer.validated_data['vehicle_type'],
                sequence_no=serializer.validated_data['sequence_no']
            )
        return Response({"message": "Event processed successfully"})
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def manual_command(request, junction_id):
    try:
        junction = Junction.objects.get(name=junction_id)
        command = request.data.get('command')
        direction = request.data.get('direction')
        
        if command == 'MANUAL_GREEN_REQUEST':
            junction.mode = 'MANUAL'
            junction.save()
            next_phase = 'NORTH_SOUTH' if direction in ['NORTH', 'SOUTH'] else 'EAST_WEST'
            safe_transition(junction, next_phase)
            return Response({"message": f"Manual GREEN requested for {direction}"})
        elif command == 'RETURN_TO_AUTOMATIC':
            junction.mode = 'AUTOMATIC'
            junction.save()
            return Response({"message": "Returned to automatic mode"})
        return Response({"error": "Invalid command"}, status=400)
    except Junction.DoesNotExist:
        return Response({"error": "Junction not found"}, status=404)

def dashboard_view(request):
    try:
        junction = Junction.objects.get(name='A')
        states = SignalState.objects.filter(junction=junction)
        queues = VehicleQueue.objects.filter(junction=junction, status='WAITING')
        context = {
            'north_state': states.get(direction='NORTH').desired_state if states.filter(direction='NORTH').exists() else 'RED',
            'south_state': states.get(direction='SOUTH').desired_state if states.filter(direction='SOUTH').exists() else 'RED',
            'east_state': states.get(direction='EAST').desired_state if states.filter(direction='EAST').exists() else 'RED',
            'west_state': states.get(direction='WEST').desired_state if states.filter(direction='WEST').exists() else 'RED',
            'north_queue': queues.filter(direction='NORTH').count(),
            'south_queue': queues.filter(direction='SOUTH').count(),
            'east_queue': queues.filter(direction='EAST').count(),
            'west_queue': queues.filter(direction='WEST').count(),
        }
        return render(request, 'dashboard.html', context)
    except Exception as e:
        return render(request, 'dashboard.html', {'error': str(e)})