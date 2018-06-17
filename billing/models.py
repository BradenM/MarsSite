from django.db import models
from django.contrib.auth.models import User
from repair.models import DeviceRepair


class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.email}'s invoice of ${self.total} on {self.date.date()}"


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        DeviceRepair, related_name="product", on_delete=models.CASCADE)
    invoice = models.ForeignKey(
        Invoice, related_name='orders', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email}'s order of {self.product}"
