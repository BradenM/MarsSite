import stripe
from .mixins import CustomerMixin
from .models import Invoice, Order
from django.conf import settings
from django.shortcuts import HttpResponse, redirect, render, Http404
from django.http import JsonResponse
from django.views.generic import View
from pinax.stripe import mixins
from pinax.stripe.actions import charges, customers, sources
from pinax.stripe.models import Card
from store.mixins import CartMixin
from .validators import validate_date
from .render import InvoiceFile


class SaveCard(View, CustomerMixin):
    def post(self, request, *args, **kwargs):
        next = request.GET.get('next')
        try:
            self.create_card(request)
            return redirect(next)
        except stripe.CardError as e:
            print(e)
            return redirect(next)


class RemoveCard(View, CustomerMixin):
    def get(self, request, pk):
        next = request.GET.get('next')
        try:
            source = Card.objects.get(pk=pk)
            self.delete_card(source.stripe_id)
            return redirect(next)
        except stripe.CardError as e:
            print(e)
            return redirect(next)


class SetDefaultCard(CustomerMixin, View):
    def get(self, request, pk):
        next = request.GET.get('next')
        try:
            source = Card.objects.get(pk=pk)
            self.set_default_card(source.stripe_id)
            return redirect(next)
        except stripe.CardError as e:
            print(e)
            return redirect(next)


class EditCard(CustomerMixin, View):
    def post(self, request):
        holder = request.POST.get('card_new_holder')
        new_exp = request.POST.get('card_new_exp')
        source = request.POST.get('source_id')
        resp = {'success': False, 'date_errors': ''}
        exp_status, exp = validate_date(new_exp)
        if exp_status is True:
            resp['success'] = True
            self.edit_card(source, date=exp, name=holder)
            return JsonResponse(resp)

        resp['date_errors'] = exp
        return JsonResponse(resp, status=406)


class ChargeCustomer(View, CustomerMixin, CartMixin):
    def post(self, request):
        try:
            # Get Payment Method
            payment_selection = request.POST.get("payment_method_card")
            source_obj = Card.objects.get(pk=payment_selection)
            source = source_obj.stripe_id
            # Get Cart Total
            charge_amnt = self.cart.total
            # Charge
            created_charge = self.charge_customer(charge_amnt, source)
            # Create Orders
            self.create_order(self.cart, created_charge)
            # Clear Cart
            self.clear_cart()
            return redirect('store:checkout_thanks')
        except stripe.CardError as e:
            print(e)
            return HttpResponse(f"Card Error: {e}")


class ViewInvoice(CustomerMixin, View):
    def get(self, request, invoice_no):
        try:
            path = self.get_invoice(invoice_no)
        except FileNotFoundError:
            raise Http404
        file = open(path, 'rb')
        response = HttpResponse(content=file)
        response['Content-Type'] = 'application/pdf'
        return response
