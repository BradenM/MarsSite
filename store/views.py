from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse, redirect
from django.views import generic
from repair.models import DeviceRepair
from .models import UserCart, CartItem, REPAIR
from django.contrib import messages
from django.conf import settings
from .forms import CardForm
from djstripe.models import Customer, Card

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
class Checkout(generic.TemplateView):
    template_name = "store/checkout.html"

    def get_context_data(self, **kwargs):
        context = super(Checkout, self).get_context_data(**kwargs)
        customer, created = Customer.get_or_create(subscriber=self.request.user)
        context['user'] = self.request.user
        context['customer'] = customer
        context['form'] = CardForm()
        context['stripe_key'] = settings.STRIPE_TEST_PUBLIC_KEY
        return context
    

# Payment Details

def add_card(request):
    print(request.POST)
    user, cart = get_cart(request)
    customer, created = Customer.get_or_create(subscriber=user)
    num = request.POST['number']
    exp_month = request.POST['expiration_0']
    exp_year = request.POST['expiration_1']
    cvc = request.POST['ccv']
    token = Card.create_token(num, exp_month, exp_year, cvc)
    customer.add_card(token, set_default=True)
    return redirect('store:checkout')

