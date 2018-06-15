from django.db import models
from django.contrib.auth.models import User
from repair.models import DeviceRepair

REPAIR = "Repair"
COMPUTER = "Computer"
ITEM_TYPES = (
    (REPAIR, "Repair"),
    (COMPUTER, "Computer"),
)

class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user}'s cart - Total: {self.total}"

class CartEntry(models.Model):
    product = models.ForeignKey(DeviceRepair, null=True, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE, related_name="entries")
    type = models.CharField(max_length=32, choices=ITEM_TYPES, default=REPAIR)

    def save(self, *args, **kwargs):
        self.cart.total += self.product.price
        self.cart.save()
        super(CartEntry, self).save(*args, **kwargs)

    def __str__(self):
        return f"Entry of {self.product.repair.name} to ({self.cart})"

    
