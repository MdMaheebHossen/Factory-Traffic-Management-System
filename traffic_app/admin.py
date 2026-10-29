from django.contrib import admin
from .models import Junction, SignalState, VehicleQueue, ProcessedEvent

admin.site.register(Junction)
admin.site.register(SignalState)
admin.site.register(VehicleQueue)
admin.site.register(ProcessedEvent)