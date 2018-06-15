from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse, redirect
from django.views import generic
from repair.models import DeviceRepair
from .models import UserCart, CartItem, REPAIR
from django.contrib import messages
from django.conf import settings
from .forms import CardForm
from billing.views import CustomerMixin
from pinax.stripe.mixins import PaymentsContextMixin

class CartView(generic.TemplateView):
    template_name = "store/cart.html"

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        user = self.request.user
        cart = user.usercart
        context['cart'] = cart

        return context

# User Cart
def get_cart(request):
    current_user = request.user
    cart = current_user.usercart
    return current_user, cart    

def add_to_cart(request, pk):
    _, cart = get_cart(request)
    item = DeviceRepair.objects.get(pk=pk)
    cart_item = CartItem.objects.create(type=REPAIR, order=item)
    cart.products.add(cart_item)
    messages.success(
        request, f'{cart_item.order.device.name} {cart_item.order.repair.name} {cart_item.type} has been added to your cart.', extra_tags='user_alert_info')
    redirect = request.GET['next']
    return HttpResponseRedirect(redirect)


def remove_from_cart(request, pk):
    _, cart = get_cart(request)
    cart_item = CartItem.objects.get(pk=pk)
    cart.products.remove(cart_item)
    return HttpResponseRedirect(reverse('store:cart'))

def clear_cart(request):
    _, cart = get_cart(request)
    for item in cart.products.all():
        cart.products.remove(item)
    return HttpResponseRedirect(reverse('store:cart'))


# Checkout
class Checkout(generic.TemplateView, CustomerMixin):
    template_name = "store/checkout.html"

    def get_context_data(self, **kwargs):
        context = super(Checkout, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['customer'] = self.customer
        context['sources'] = self.sources
        context['stripe_id'] = settings.PINAX_STRIPE_PUBLIC_KEY
        context['form'] = CardForm()
        return context
    

