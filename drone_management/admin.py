from django.contrib import admin
from .models import DroneType,BatteryMaster,RCMaster,SensorMaster,CameraMaster, Drone, DroneComponent,DroneStatus,DronePurpose
# Register your models here.

admin.site.register(DroneType)
admin.site.register(DronePurpose)
admin.site.register(BatteryMaster)
admin.site.register(RCMaster)
admin.site.register(SensorMaster)
admin.site.register(CameraMaster)
admin.site.register(Drone)
admin.site.register(DroneComponent)
admin.site.register(DroneStatus)