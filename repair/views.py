from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, redirect, get_object_or_404, render, render_to_response, reverse, resolve_url
from django.views import generic
from django.views.generic.edit import ModelFormMixin, ProcessFormView
from .models import Device, Family, Repair, LAP, PHONE, TAB


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


def select_device(request):
    query = request.POST.get('devices')
    dev = get_object_or_404(Device, pk=query)
    return HttpResponseRedirect(reverse('repair:device', args=[dev.slug]))



class DeviceView(generic.DetailView):
    model = Device
    template_name = "repair/detail.html"

