from django.db import models
from django.contrib.auth.models import User
from repair.models import RepairCost

REPAIR = "Repair"
COMPUTER = "Computer"
ITEM_TYPES = (
    (REPAIR, "Repair"),
    (COMPUTER, "Computer"),
)

class UserCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('CartItem', related_name="products", blank=True)


class CartItem(models.Model):
    type = models.CharField(max_length=32, choices=ITEM_TYPES)
    order = models.ForeignKey(RepairCost, related_name='order', on_delete=models.CASCADE)

    def __str__(self):
        return self.type