from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, redirect, get_object_or_404, render, render_to_response, reverse, resolve_url
from django.views.generic import ListView, TemplateView, View, DetailView
from .models import Device, Family, Repair, DeviceRepair, LAP, PHONE, TAB, DEV_TYPES
from django.http import JsonResponse


class IndexView(ListView):
    template_name = "repair/index.html"
    context_object_name = "devices"

    def get_queryset(self):
        return Device.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        device_devices = Device.objects.filter(device_type=PHONE)
        context['devices'] = device_devices.filter(has_family=False)
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


class SearchDevices(RepairMixin, View):
    def get(self, request):
        query = request.GET.get('search_query')
        # Temporary need to write clean query function
        if query == "":
            response = JsonResponse({"error": "there was an error"})
            response.status_code = 403
            return response
        resp = {'device': [], 'family': []}
        for x in self.devices:
            opt = [x.name, x.device_type, x.brand, x.model_number]
            r = [i for i in opt if i is not None and query.lower() in i.lower()]
            if not any(r):
                if x.has_family:
                    family = x.devices.first()
                    if family.pk not in resp['family']:
                        resp['family'].append(family.pk)
                else:
                    if x.pk not in resp['device']:
                        resp['device'].append(x.pk)
        return JsonResponse(resp)
