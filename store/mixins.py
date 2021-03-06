from .models import Cart, CartEntry, REPAIR
from django.contrib import messages

class CartMixin:
    status_removed = "removed from your cart"
    status_added = "added to your cart"

    def add_item(self, item):
        cart_item = CartEntry.objects.create(product=item, cart=self.cart)
        self.notify_cart_update(cart_item, self.status_added)

    def remove_item(self, item):
        self.notify_cart_update(item, self.status_removed)
        deduct = self.cart.total - item.product.price
        user_cart = Cart.objects.get(user=self.user)
        user_cart.total = deduct
        user_cart.save()
        item.delete()

    def clear_cart(self):
        self.cart.entries.all().delete()
        user_cart = Cart.objects.get(user=self.user)
        user_cart.total = 0.00
        user_cart.save()

    def notify_cart_update(self, item, status):
        messages.success(
            self.request, f'{item.product.device.name} {item.product.repair.name} {item.type} has been {status}.', extra_tags='user_alert_info')

    @property
    def user(self):
        user = self.request.user
        return user

    @property
    def cart(self):
        cart, created = Cart.objects.get_or_create(user=self.user)
        return cart
