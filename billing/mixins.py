import stripe
from .models import Invoice, Order
from django.conf import settings
from django.shortcuts import HttpResponse, redirect, render
from django.views.generic import View
from pinax.stripe import mixins
from pinax.stripe.actions import charges, customers, sources
from pinax.stripe.models import Card
from store.mixins import CartMixin


class CustomerMixin(mixins.CustomerMixin):

    def create_card(self, stripe_token):
        sources.create_card(self.customer, token=stripe_token)

    def delete_card(self, stripe_id):
        sources.delete_card(self.customer, stripe_id)

    def charge_customer(self, amount, source):
        charges.create(
            amount=amount,
            customer=self.customer,
            source=source,
            send_receipt=False
        )

    def create_order(self, cart):
        # Create Invoice
        invoice = Invoice.objects.create(
            user=self.user,
            total=self.cart.total,
        )
        # Create Orders
        for item in cart.entries.all():
            Order.objects.create(
                user=self.user,
                product=item.product,
                invoice=invoice
            )

    @property
    def sources(self):
        return Card.objects.filter(customer=self.customer)