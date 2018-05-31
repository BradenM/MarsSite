from django.contrib import admin
from .models import Repair, RepairCost, Family, Device

admin.site.register(Repair)
admin.site.register(RepairCost)
admin.site.register(Family)
admin.site.register(Device)