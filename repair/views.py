from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, redirect, get_object_or_404, render, render_to_response, reverse, resolve_url
from django.views.generic import ListView, TemplateView, View, DetailView
from .models import Device, Family, Repair, DeviceRepair, LAP, PHONE, TAB, DEV_TYPES


class IndexView(ListView):
    template_name = "repair/index.html"
    context_object_name = "devices"

    def get_queryset(self):
        return Device.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        device_phones = Device.objects.filter(device_type=PHONE)
        context['phones'] = device_phones.filter(has_family=False)
        context['phone_families'] = Family.objects.filter(device_type=PHONE)
        context['tablets'] = Device.objects.filter(device_type=TAB)
        context['laptops'] = Device.objects.filter(device_type=LAP)

        return context


def select_device(request):
    query = request.POST.get('devices')
    dev = get_object_or_404(Device, pk=query)
    return HttpResponseRedirect(reverse('repair:device', args=[dev.slug]))


class DeviceView(DetailView):
    model = Device
    template_name = "repair/detail.html"


def get_repair(request, slug, pk):
    repair = get_object_or_404(DeviceRepair, pk=pk)
    print(repair.repair.name)
    return render(request, 'repair/repair_detail.html', {'active_repair': repair})


class RepairMixin(object):
    device_types = DEV_TYPES
    #devices, families = Device().get_devices()

    def phone_brands(self):
        brands = []
        for d in Device.objects.filter(device_type=PHONE):
            if not d.brand in brands and d.brand is not None:
                brands.append(d.brand)
        print(brands)
        return brands

    def get_phones(self):
        phones = {}
        for d in Device.objects.filter(device_type=PHONE):
            if not d.has_family:
                if not d.brand in phones.keys():
                    phones[d.brand] = []
                phones[d.brand].append(d)
        for d in Family.objects.filter(device_type=PHONE):
            if not d.brand in phones.keys():
                phones[d.brand] = []
            phones[d.brand].append(d)
        return phones


class ViewDevices(RepairMixin, TemplateView):
    template_name = "repair/view_devices.html"


class GetDeviceInfo(RepairMixin, View):
    template = "repair/device_info.html"

    def get(self, request):
        query = request.GET.get('device')
        fam_query = request.GET.get('family', False)
        if fam_query:
            dev_or_fam = Family.objects.get(pk=query)
        else:
            dev_or_fam = Device.objects.get(pk=query)
        return render(request, self.template, context={'device': dev_or_fam})
