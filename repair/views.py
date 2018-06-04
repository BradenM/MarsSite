from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render, render_to_response, reverse
from django.views import generic
from .models import Device, Family, Repair, LAP, PHONE, TAB


class IndexView(generic.TemplateView):
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

        active_fam = kwargs.get('pk', None)
        if active_fam:
            fam = Family.objects.get(pk=active_fam) 
            context['active_fam'] = fam
        return context


class DeviceView(generic.DetailView):
    model = Device
    template_name = "repair/detail.html"

# def repair_info(request, pk):
#     rep = get_object_or_404(Repair, pk=pk)
#     print(rep)
#     return reverse('repair:device', kwargs={'repair':rep})

# Select Device from Family on Index View
def select_device(request):
    query = request.POST.get('selected_device')
    dev = get_object_or_404(Device, id=query)
    return HttpResponseRedirect(reverse('repair:device', args=[dev.slug]))