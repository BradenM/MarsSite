from django.db import models
from django.contrib.auth.models import User
from repair.models import DeviceRepair
from datetime import datetime
from store.models import REPAIR, COMPUTER

ORDER_TYPE = {
    REPAIR: 'REP',
    COMPUTER: 'COM'
}


class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_no = models.CharField(
        max_length=512, blank=True, null=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
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
