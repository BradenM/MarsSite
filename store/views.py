from .mixins import CartMixin
from .models import Cart, CartEntry, REPAIR
from billing.views import CustomerMixin
from django.conf import settings
from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect, \
    render, reverse
from django.views.generic import DetailView, ListView, TemplateView, View
from pinax.stripe.mixins import PaymentsContextMixin
from repair.models import DeviceRepair


class CartView(TemplateView, CartMixin):
    template_name = "store/cart.html"

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


# User Cart
class AddCartEntry(View, CartMixin):
    def get(self, request, pk):
        item = DeviceRepair.objects.get(pk=pk)
        self.add_item(item)
        return self.redirect()


class RemoveCartEntry(View, CartMixin):
    def get(self, request, pk):
        entry = CartEntry.objects.get(pk=pk)
        self.remove_item(entry)
        return self.redirect()


class ClearCart(View, CartMixin):
    def get(self, request):
        self.clear_cart()
        return self.redirect()


# Checkout
class Checkout(TemplateView, CustomerMixin, CartMixin):
    template_name = "store/checkout.html"

    def get_context_data(self, **kwargs):
        context = super(Checkout, self).get_context_data(**kwargs)
        context['stripe_id'] = settings.PINAX_STRIPE_PUBLIC_KEY
        return context


class CheckoutComplete(TemplateView, CartMixin):
    template_name = "store/thanks.html"

    def get_context_data(self, **kwargs):
        context = super(CheckoutComplete, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['cart'] = self.cart
        return context
