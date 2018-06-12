from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from django.views import generic
from repair.models import DeviceRepair
from .models import UserCart, CartItem, REPAIR

class CartView(generic.TemplateView):
    template_name = "store/cart.html"

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        user = self.request.user
        cart = user.usercart
        context['cart'] = cart

        return context
    

def add_to_cart(request, pk):
    current_user = request.user
    cart = current_user.usercart
    print(cart.id)
    item = DeviceRepair.objects.get(pk=pk)
    cart_item = CartItem.objects.create(type=REPAIR, order=item)
    cart.products.add(cart_item)
    cart.save()
    return HttpResponseRedirect(reverse('store:cart'))


def remove_from_cart(request, pk):
    current_user = request.user
    cart = current_user.usercart
    cart_item = CartItem.objects.get(pk=pk)
    cart.products.remove(cart_item)
    return HttpResponseRedirect(reverse('store:cart'))
