import stripe
from .models import Invoice, Order, ORDER_TYPE
from tracker.models import Tracker, TrackerUpdate
from django.conf import settings
from django.shortcuts import HttpResponse, redirect, render
from django.views.generic import View
from pinax.stripe import mixins
from pinax.stripe.actions import charges, customers, sources
from pinax.stripe.models import Card
from store.mixins import CartMixin


class CustomerMixin(mixins.CustomerMixin):

    def create_card(self, request):
        token = request.POST.get('stripeToken')
        holder = request.POST.get('card_holder')
        card = sources.create_card(self.customer, token=token)
        sources.update_card(self.customer, card.stripe_id, name=holder)

    def delete_card(self, stripe_id):
        sources.delete_card(self.customer, stripe_id)

    def set_default_card(self, stripe_id):
        customers.set_default_source(self.customer, stripe_id)

    def edit_card(self, stripe_id, date=None, name=None):
        sources.update_card(self.customer, stripe_id,
                            exp_month=date.month, exp_year=date.year, name=name)

    def charge_customer(self, amount, source):
        charge = charges.create(
            amount=amount,
            customer=self.customer,
            source=source,
            send_receipt=False
        )
        return charge

    def create_order(self, cart, charge, tracker=True):
        # Create Invoice
        invoice = Invoice.objects.create(
            user=self.user,
            total=self.cart.total,
            charge=charge
        )
        # Create Orders
        for item in cart.entries.all():
            order = Order.objects.create(
                user=self.user,
                product=item.product,
                invoice=invoice,
                order_type=ORDER_TYPE[item.type]
            )
            # Create Tracker if needed
            if tracker:
                new_track = Tracker.objects.create(
                    user=self.user,
                    order=order
                )
                TrackerUpdate.objects.create(
                    tracker=new_track
                )

    @property
    def sources(self):
        return Card.objects.filter(customer=self.customer)

    @property
    def invoices(self):
        return Invoice.objects.filter(user=self.request.user)

    @property
    def orders(self):
        return Order.objects.filter(user=self.request.user)
