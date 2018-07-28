import stripe
from .models import Invoice, ORDER_TYPE, Order
from .render import InvoiceFile
from billing.models import Invoice, PaymentCard
from django.conf import settings
from django.shortcuts import HttpResponse, redirect, render
from django.views.generic import View
from pinax.stripe import mixins
from pinax.stripe.actions import charges, customers, sources
from pinax.stripe.models import Card
from store.mixins import CartMixin
from tracker.models import Tracker, TrackerUpdate


class CustomerMixin(mixins.CustomerMixin):

    def get_card(self, stripe_id):
        return PaymentCard.objects.get(stripe_id=stripe_id)

    def create_card(self, token, holder, temp=False):
        card = PaymentCard.objects.create(token, user=self.request.user, temporary=temp)
        card.update_card(name=holder)

    def delete_card(self, stripe_id):
        card = self.get_card(stripe_id)
        card.delete_card()

    def set_default_card(self, stripe_id):
        card = self.get_card(stripe_id)
        card.set_default()

    def edit_card(self, stripe_id, date=None, name=None):
        card = self.get_card(stripe_id)
        card.update_card(exp_month=date.month, exp_year=date.year, name=name)

    def charge_customer(self, amount, stripe_id):
        charge = charges.create(
            amount=amount,
            customer=self.customer,
            source=stripe_id,
            send_receipt=False
        )
        return charge

    def create_order(self, cart, charge, tracker=True):
        # Create Invoice
        invoice = Invoice.objects.create(
            user=self.user,
            total=self.cart.total,
            charge=charge,
            payment=self.get_card(charge.card.stripe_id)
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
        # Generate and send invoice
        self.send_receipt(invoice)

    def send_receipt(self, invoice):
        # Generate PDF
        InvoiceFile().generate(invoice)
        receipt = {
            'subject': f'Receipt from BradenMars.me for Invoice #{invoice.invoice_no}',
            'body': f'Thank you for your order. Your Invoice (Number {invoice.invoice_no}) has been attached for your reference.',
            'receiver': self.request.user.email,
            'invoice': invoice.invoice_no
        }
        print(receipt)
        InvoiceFile().send_receipt(receipt)

    def get_invoice(self, number):
        invoice = Invoice.objects.get(invoice_no=number)
        return InvoiceFile().get_pdf(invoice.invoice_no)

    @property
    def sources(self):
        return PaymentCard.objects.filter(user=self.request.user, active=True, temporary=False)

    @property
    def invoices(self):
        return Invoice.objects.filter(user=self.request.user)

    @property
    def orders(self):
        return Order.objects.filter(user=self.request.user)
