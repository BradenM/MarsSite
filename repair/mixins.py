from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render, render_to_response,
                              resolve_url, reverse)
from django.views.generic import DetailView, ListView, TemplateView, View
from .models import (DEV_TYPES, LAP, PHONE, TAB, Device, DeviceRepair, Family,
                     Repair)


class RepairMixin(object):
    device_types = DEV_TYPES
    # devices, families = Device().get_devices()

    def get_device(self, type):
        devices = {}
        for d in Device.objects.filter(device_type=type):
            if not d.has_family:
                if not d.brand in devices.keys():
                    devices[d.brand] = []
                devices[d.brand].append(d)
        for d in Family.objects.filter(device_type=type):
            if not d.brand in devices.keys():
                devices[d.brand] = []
            devices[d.brand].append(d)
        return devices

    @property
    def types(self):
        return DEV_TYPES

    @property
    def brands(self):
        brands = []
        for d in Device.objects.all():
            if not d.brand in brands and d.brand is not None:
                brands.append(d.brand)
        return brands

    @property
    def devices(self):
        return Device.objects.all()

    @property
    def phones(self):
        return self.get_device(PHONE)

    @property
    def tablets(self):
        return self.get_device(TAB)

    @property
    def laptops(self):
        return self.get_device(LAP)
