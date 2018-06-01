from django.shortcuts import render, reverse, HttpResponseRedirect, get_object_or_404
from django.views import generic
from .models import Device, Family, PHONE, TAB, LAP
from django import forms

class IndexView(generic.ListView):
    template_name = "repair/index.html"
    context_object_name = "devices"

    def get_queryset(self):
        return Device.objects.all()
        
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        device_phones = Device.objects.filter(device_type = PHONE)
        context['phones'] = device_phones.filter(has_family=False)
        context['phone_families'] = Family.objects.filter(device_type = PHONE)
        context['tablets'] = Device.objects.filter(device_type = TAB)
        context['laptops'] = Device.objects.filter(device_type = LAP)
        return context


class DeviceView(generic.DetailView):
    model = Device
    template_name = "repair/detail.html"

