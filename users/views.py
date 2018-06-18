from django.shortcuts import render
from allauth.account.views import SignupView, LoginView
from django.shortcuts import HttpResponseRedirect, reverse
from django.contrib import messages
from allauth.account.forms import SignupForm
from django.views.generic import View, TemplateView
from billing.mixins import CustomerMixin


class AccountPage(TemplateView):
    template_name = 'users/account.html'


class ListInvoices(TemplateView, CustomerMixin):
    template_name = 'users/invoices.html'

    def get_context_data(self, **kwargs):
        context = super(ListInvoices, self).get_context_data(**kwargs)
        context['invoices'] = self.invoices
        return context


class ListOrders(TemplateView, CustomerMixin):
    template_name = 'users/orders.html'

    def get_context_data(self, **kwargs):
        context = super(ListOrders, self).get_context_data(**kwargs)
        context['orders'] = self.orders
        return context
