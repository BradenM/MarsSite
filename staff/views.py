from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View, TemplateView
from django.shortcuts import HttpResponse
from store.models import Cart
from billing.models import Order
from billing.models import Invoice
from tracker.models import Tracker, TrackerUpdate
from django.contrib.auth.models import User


class ControlMixin:

    def user_orders(self, user):
        orders = Order.objects.filter(user=user)
        return orders

    def get_tracker(self, order):
        tracker = Tracker.objects.get(user=self.request.user, order=order)
        return tracker

    @property
    def carts(self):
        all_carts = Cart.objects.all()
        return all_carts

    @property
    def users(self):
        users = User.objects.all()
        return users

    @property
    def orders(self):
        orders = Order.objects.all()
        return orders


class ControlPanel(TemplateView, ControlMixin):
    template_name = "staff/control-panel.html"

    def get_context_data(self, **kwargs):
        context = super(ControlPanel, self).get_context_data(**kwargs)
        context['orders'] = self.carts
        context['users'] = self.users
        return context


class ControlUsers(TemplateView, ControlMixin):
    template_name = "staff/users.html"

    def get_context_data(self, **kwargs):
        context = super(ControlUsers, self).get_context_data(**kwargs)
        context['users'] = self.users
        context['orders'] = self.orders
        return context


class ViewUser(TemplateView, ControlMixin):
    template_name = 'staff/users/view.html'

    def get_context_data(self, **kwargs):
        context = super(ViewUser, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        user = User.objects.get(pk=pk)
        context['user'] = user
        context['orders'] = self.user_orders(user)
        return context


class ViewTracker(TemplateView, ControlMixin):
    template_name = 'staff/users/view_tracker.html'

    def get_context_data(self, **kwargs):
        context = super(ViewTracker, self).get_context_data(**kwargs)
        order = Order.objects.get(pk=self.kwargs.get('pk'))
        context['tracker'] = self.get_tracker(order)
        return context
