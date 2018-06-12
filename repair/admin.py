from django.contrib import admin
from .models import Repair, DeviceRepair, Family, Device

admin.site.register(Repair)
admin.site.register(DeviceRepair)
admin.site.register(Family)
admin.site.register(Device)