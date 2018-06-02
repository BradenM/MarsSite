from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render, render_to_response, reverse
from django.views import generic
from .models import Device, Family, LAP, PHONE, TAB


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


# Select Device from Family on Index View
def select_device(request):
    query = request.POST.get('selected_device')
    dev = get_object_or_404(Device, id=query)
    return HttpResponseRedirect(reverse('repair:device', args=[dev.slug]))