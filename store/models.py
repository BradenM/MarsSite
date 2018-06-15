from django.db import models
from django.contrib.auth.models import User
from repair.models import DeviceRepair

REPAIR = "Repair"
COMPUTER = "Computer"
ITEM_TYPES = (
    (REPAIR, "Repair"),
    (COMPUTER, "Computer"),
)

class UserCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('CartItem', related_name="products", blank=True)
    total = models.FloatField(default="0.00")

    def save(self, *args, **kwargs):
        for p in self.products:
            self.total += p.order.price
        super(Device, self).save(*args, **kwargs)

    def __str__(self):
        return f"{user}'s Cart'"


class CartItem(models.Model):
    type = models.CharField(max_length=32, choices=ITEM_TYPES)
    order = models.ForeignKey(DeviceRepair, related_name='order', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order.repair.name} - {self.order.price}"