import stripe
from .mixins import CustomerMixin
from .models import Invoice, Order
from django.conf import settings
from django.shortcuts import HttpResponse, redirect, render
from django.views.generic import View
from pinax.stripe import mixins
from pinax.stripe.actions import charges, customers, sources
from pinax.stripe.models import Card
from store.mixins import CartMixin


class SaveCard(View, CustomerMixin):
    def post(self, request, *args, **kwargs):
        try:
            self.create_card(request.POST.get("stripeToken"))
            return redirect("store:checkout")
        except stripe.CardError as e:
            print(e)
            return redirect("store:checkout")


class RemoveCard(View, CustomerMixin):
    def get(self, request, pk):
        try:
            source = Card.objects.get(pk=pk)
            self.delete_card(source.stripe_id)
            return redirect("store:checkout")
        except stripe.CardError as e:
            print(e)
            return redirect("store:checkout")


class ChargeCustomer(View, CustomerMixin, CartMixin):
    def post(self, request):
        try:
            # Get Payment Method
            payment_selection = request.POST.get("selected_card")
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
