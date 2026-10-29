from django.db import models

class Junction(models.Model):
    name = models.CharField(max_length=10, default='A')
    mode = models.CharField(max_length=20, default='AUTOMATIC')
    current_phase = models.CharField(max_length=20, default='NORTH_SOUTH')
    controller_status = models.CharField(max_length=20, default='ONLINE')

    def __str__(self):
        return f"Junction {self.name}"

class SignalState(models.Model):
    junction = models.ForeignKey(Junction, on_delete=models.CASCADE)
    direction = models.CharField(max_length=10)
    desired_state = models.CharField(max_length=10, default='RED')
    actual_state = models.CharField(max_length=10, default='RED')

class VehicleQueue(models.Model):
    junction = models.ForeignKey(Junction, on_delete=models.CASCADE)
    direction = models.CharField(max_length=10)
    vehicle_type = models.CharField(max_length=20)
    sequence_no = models.IntegerField()
    status = models.CharField(max_length=20, default='WAITING')

class ProcessedEvent(models.Model):
    event_id = models.CharField(max_length=50, unique=True)