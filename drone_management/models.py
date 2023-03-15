from django.db import models
from django.contrib.auth.models import User
# from masters.models import Product
# Create your models here.

class DronePurpose(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, default='', null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "dms_drone_purpose"
    def __str__(self):
        return "{}".format(self.name)

class DroneType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    additional_features = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    purpose = models.ForeignKey(DronePurpose, default='', null=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, default='', null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "dms_drone_type"
    def __str__(self):
        return "{}".format(self.name)


class BatteryMaster(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    capacity = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    warranty = models.CharField(max_length=100)
    discharge_rate = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    weight = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    
    created_by = models.ForeignKey(User, default='', null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "dms_battery_master"
    def __str__(self):
        return "{}".format(self.name)

class RCMaster(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    range = models.CharField(max_length=100)
    gc_status  = models.BooleanField(default=False)
    video_transmission = models.BooleanField(default=False)
    uid = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    
    created_by = models.ForeignKey(User, default='', null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "dms_rc_master"
    def __str__(self):
        return "{}".format(self.name)

class SensorMaster(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    
    created_by = models.ForeignKey(User, default='', null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "dms_sensor_master"
    def __str__(self):
        return "{}".format(self.name)

class CameraMaster(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    
    created_by = models.ForeignKey(User, default='', null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "dms_camera_master"
    def __str__(self):
        return "{}".format(self.name)
class DroneStatus(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    type = models.CharField(max_length=100,blank=True, null=True)

    # created_by = models.ForeignKey(User, default='', null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        # unique_together = ('status', 'type',)
        db_table = "dms_drone_status"
    def __str__(self):
        return "{}".format(self.status)


class Drone(models.Model):
    id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=100)
    model_no = models.CharField(max_length=100)
    serial_no = models.CharField(max_length=100)
    uin = models.CharField(max_length=100)
    drone_type = models.ForeignKey(
        DroneType, default='', null=True, on_delete=models.CASCADE)
    drone_purpose = models.ForeignKey(
        DronePurpose, default='', null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='drone_images')
    video_link = models.TextField(blank=True, null=True)
    features =  models.TextField(blank=True, null=True)
    additional_features =  models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    image1 = models.FileField(upload_to='drone_type_images/',null = True, blank = True)
    image2 = models.FileField(upload_to='drone_type_images/',null = True, blank = True)
    schema = models.TextField(blank=True,null=True)

    allocated = models.BooleanField(default=False)
    drone_status = models.ForeignKey(
        DroneStatus, default='', null=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, default='', null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "dms_drones"
    def __str__(self):
        return "{}".format(self.model)




class DroneComponent(models.Model):
    id = models.AutoField(primary_key=True)
    drone = models.ForeignKey(
        Drone, default='', null=True, on_delete=models.CASCADE)
    battery = models.TextField(blank=True,null=True)
    sensors = models.TextField(blank=True,null=True)
    camera = models.TextField(blank=True,null=True)
    rc = models.TextField(blank=True,null=True)
    fc = models.TextField(blank=True,null=True)
    qgc = models.TextField(blank=True,null=True)
    frame = models.TextField(blank=True,null=True)
    created_by = models.ForeignKey(User, default='', null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "dms_drone_components"
    def __str__(self):
        return "{}".format(self.id)


