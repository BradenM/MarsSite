from django.shortcuts import render, reverse, HttpResponseRedirect, get_object_or_404
from django.views import generic
from .models import Device
from django import forms

class IndexView(generic.ListView):
    template_name = "repair/index.html"
    context_object_name = "devices"

    def get_queryset(self):
        return Device.objects.all()
        
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context

# def sort_devices(request):
#     brand = get_object_or_404(Brand, pk=request.POST['brand'])
#     return reverse('repair:index', args=())