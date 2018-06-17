from django.shortcuts import render, get_object_or_404
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from billing.models import Order
from .models import Tracker


class TrackerView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.get(pk=pk)
        tracker = get_object_or_404(Tracker, user=request.user, order=order)
        context = {'tracker': tracker}
        return render(request, 'tracker/tracker.html', context=context)
