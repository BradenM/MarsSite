from django.shortcuts import render
from allauth.account.views import PasswordChangeView
from django.shortcuts import HttpResponseRedirect, reverse, redirect, HttpResponse, render
from django.urls import reverse_lazy
from django.contrib import messages
from allauth.account.forms import SignupForm
from django.views.generic import View, TemplateView, FormView
from billing.mixins import CustomerMixin
from billing.models import Order
from django.http import JsonResponse
from .user_forms import ExtChangePasswordForm, ExtAddEmailForm, ChangePhoneForm
from crispy_forms.utils import render_crispy_form
from django.template.context_processors import csrf
from allauth.account.views import _ajax_response, AjaxCapableProcessFormViewMixin


class AccountPage(TemplateView):
    template_name = 'users/account.html'


class SettingsPage(CustomerMixin, TemplateView):
    template_name = 'users/settings.html'

    def get_context_data(self, **kwargs):
        context = super(SettingsPage, self).get_context_data(**kwargs)
        context['form'] = ExtChangePasswordForm()
        context['email_form'] = ExtAddEmailForm()
        context['phone_form'] = ChangePhoneForm()
        return context


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
        context['empty_msg'] = "You haven't made any orders."
        return context


class SearchOrders(CustomerMixin, View):
    def get(self, request):
        query = request.GET.get('search_query')
        # Temporary, need to clean query
        if query == "":
            response = JsonResponse({"error": "there was an error"})
            response.status_code = 403
            return response
        results = []
        for x in self.orders:
            opt = [x.device(), x.repair(),
                   x.order_date()]
            r = [i for i in opt if query.lower() in i.lower()]
            if any(r):
                results.append(x)
        return render(
            request, 'users/order_tile.html', context={'orders': results, 'empty_msg': "No orders match your search query."})


class ChangePhone(AjaxCapableProcessFormViewMixin, FormView):
    template_name = "users/forms/form.html"
    form_class = ChangePhoneForm
    success_url = reverse_lazy('users:my_account')

    def get_form_kwargs(self):
        kwargs = super(ChangePhone, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        phone = form.save(self.request)
        return super(ChangePhone, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        res = super(ChangePhone, self).post(request, *args, **kwargs)
        return res
