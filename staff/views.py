from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View, TemplateView
from django.shortcuts import HttpResponse
from store.models import Cart

class ControlMixin:
    
    @property
    def orders(self):
        all_carts = Cart.objects.all()
        return all_carts


class ControlPanel(TemplateView, ControlMixin):
    template_name = "staff/control-panel.html"

    def get_context_data(self, **kwargs):
        context = super(ControlPanel, self).get_context_data(**kwargs)
        context['orders'] = self.orders
        return context
    