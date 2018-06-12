from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, redirect, get_object_or_404, render, render_to_response, reverse, resolve_url
from django.views import generic
from .models import Device, Family, Repair, DeviceRepair, LAP, PHONE, TAB
from allauth.account.forms import SignupForm
from users.forms import ExtLoginForm

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
        context['login_form'] = ExtLoginForm()
        signup_data = self.request.session.get('invalid_signup', None)
        if signup_data is None:
            sign_up = SignupForm()
        else:
            sign_up = SignupForm(signup_data)
        context['signup_form'] = sign_up

        login_data = self.request.session.get('invalid_login', None)
        if login_data is None:
            log_in = ExtLoginForm()
        else:
            log_in = ExtLoginForm(login_data)
        context['login_form'] = log_in

        return context


def select_device(request):
    query = request.POST.get('devices')
    dev = get_object_or_404(Device, pk=query)
    return HttpResponseRedirect(reverse('repair:device', args=[dev.slug]))


class DeviceView(generic.DetailView):
    model = Device
    template_name = "repair/detail.html"


def get_repair(request, slug, pk):
    repair = get_object_or_404(DeviceRepair, pk=pk)
    print(repair.repair.name)
    return render(request, 'repair/repair_detail.html', {'active_repair': repair})