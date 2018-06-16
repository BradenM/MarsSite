from django.shortcuts import render
from django.views.generic import View, TemplateView
from billing.models import Order
from .models import Tracker


class TrackerView(View):
    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.get(pk=pk)
        tracker = Tracker.objects.get(order=order)
        context = {'tracker': tracker}
        return render(request, 'tracker/tracker.html', context=context)
