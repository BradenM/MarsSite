from django.db import models
from django.contrib.auth.models import User
from repair.models import DeviceRepair
from datetime import datetime
from store.models import REPAIR, COMPUTER
from pinax.stripe.models import Charge, Card
from pinax.stripe.actions import sources, customers
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import stripe

ORDER_TYPE = {
    REPAIR: 'REP',
    COMPUTER: 'COM'
}


class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_no = models.CharField(
        max_length=512, blank=True, null=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    charge = models.ForeignKey(
        Charge, on_delete=models.SET_NULL, related_name='server_invoice', blank=True, null=True)
    payment = models.ForeignKey(
        'UserPayment', on_delete=models.CASCADE, related_name='charges', null=True)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def get_invoice_no(self):
        prev = Invoice.objects.filter(user=self.user).order_by('id').last()
        user_id = self.user.id
        if not prev or prev.invoice_no is None:
            return str(user_id) + f"-0001"
        prev_no = int(prev.invoice_no.split('-')[-1])
        new_no = '%04d' % (prev_no + 1)
        new_invoice = str(user_id) + f"-{new_no}"
        return new_invoice

    def get_date(self):
        return self.date.strftime("%B %d, %Y")

    def save(self, *args, **kwargs):
        if self.invoice_no is None:
            self.invoice_no = self.get_invoice_no()

        super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email}'s invoice of ${self.total} on {self.date.date()} - No.{self.invoice_no}"


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    order_no = models.CharField(
        max_length=512, blank=True, null=True)
    order_type = models.CharField(max_length=16, blank=True, null=True)
    product = models.ForeignKey(
        DeviceRepair, related_name="product", on_delete=models.CASCADE)
    invoice = models.ForeignKey(
        Invoice, related_name='orders', on_delete=models.CASCADE)

    def get_order_no(self):
        prev = Order.objects.all().order_by('id').last()
        user_id = self.user.id
        if not prev:
            return f"{self.order_type}{self.product.id}-0001"
        prev_no = int(prev.order_no.split('-')[-1])
        new_no = '%04d' % (prev_no + 1)
        new_order = str(self.order_type) + str(self.product.id) + f"-{new_no}"
        return new_order

    def device_type(self):
        dev = self.product.device.device_type
        return f"{dev} Repair"

    def device(self):
        return self.product.device.name

    def repair(self):
        return self.product.repair.name

    def order_date(self):
        return self.invoice.date.strftime("%B %d, %Y")

    def save(self, *args, **kwargs):
        if self.order_no is None:
            self.order_no = self.get_order_no()
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email}'s order of {self.product} -- Order #: {self.order_no}"


# Payment Model to house all methods
PAYMENT_TYPES = (
    ('card', 'Card'),
    ('paypal', 'Paypal'),
    ('other', 'Other'),
)


class UserPayment(models.Model):
    type = models.CharField(max_length=32, choices=PAYMENT_TYPES)
    user = models.ForeignKey(
        User, related_name='payment_methods', on_delete=models.CASCADE)
    temporary = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    default = models.BooleanField(default=False)
    name = models.CharField(max_length=64, blank=True, null=True)
    last4 = models.CharField(max_length=64, blank=True, null=True)
    brand = models.CharField(max_length=64, blank=True, null=True)
    exp_month = models.CharField(max_length=64, blank=True, null=True)
    exp_year = models.CharField(max_length=64, blank=True, null=True)
    stripe_id = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return f"{self.user}: {self.type} - Active: {self.active} - Temp: {self.temporary}"


class PaymentCardManager(models.Manager):
    def create(self, stripe_token, *args, **kwargs):
        # Create Stripe Card
        customer = customers.get_customer_for_user(kwargs['user'])
        card = sources.create_card(customer, token=stripe_token)
        kwargs['name'] = card.name
        kwargs['last4'] = card.last4
        kwargs['brand'] = card.brand
        kwargs['exp_month'] = card.exp_month
        kwargs['exp_year'] = card.exp_year
        kwargs['stripe_id'] = card.stripe_id
        kwargs['type'] = 'card'
        return super(PaymentCardManager, self).create(*args, **kwargs)

    def get_queryset(self):
        return super(PaymentCardManager, self).get_queryset().filter(type='card')


class PaymentCard(UserPayment):
    objects = PaymentCardManager()

    def update_card(self, **kwargs):
        name = kwargs.get('name')
        exp_month = kwargs.get('exp_month')
        exp_year = kwargs.get('exp_year')
        if name is not None:
            self.name = name
        if exp_month is not None:
            self.exp_month = exp_month
        if exp_year is not None:
            self.exp_year = exp_year
        self.save()
        return sources.update_card(self.customer, self.stripe_id, **kwargs)

    def delete_card(self):
        self.active = False
        self.save()
        try:
            sources.delete_card(self.customer, self.stripe_id)
        except stripe.error.InvalidRequestError as e:
            print("Stripe Error")
            print(e)
            pass
        return self

    def set_default(self):
        cur_default = PaymentCard.objects.filter(default=True)
        if cur_default:
            cur_default.default = False
            cur_default.save()
        self.default = True
        self.save()
        return customers.set_default_source(self.customer, self.stripe_id)

    @property
    def customer(self):
        return customers.get_customer_for_user(self.user)

    class Meta:
        proxy = True
