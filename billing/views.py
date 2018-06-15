from django.shortcuts import render
from pinax.stripe.actions import customers
from pinax.stripe import mixins
from pinax.stripe.actions import sources
from pinax.stripe.models import Card
from django.conf import settings
from django.shortcuts import HttpResponse, redirect
from django.views.generic import View
import stripe

#stripe_token = settings.PINAX_STRPI

class CustomerMixin(mixins.CustomerMixin):

    def create_card(self, stripe_token):
        sources.create_card(self.customer, token=stripe_token)

    def delete_card(self, stripe_id):
        sources.delete_card(self.customer, stripe_id)

    @property
    def sources(self):
        return Card.objects.filter(customer=self.customer)

    



class SaveCard(View, CustomerMixin):
    def post(self, request, *args, **kwargs):
        try:
            self.create_card(request.POST.get("stripeToken"))
            return redirect("store:checkout")
        except stripe.CardError as e:
            print(e)
            return redirect("store:checkout")


class RemoveCard(View, CustomerMixin):
    def get(self, request, pk):
        try:
            source = Card.objects.get(pk=pk)
            self.delete_card(source.stripe_id)
            return redirect("store:checkout")
        except stripe.CardError as e:
            print(e)
            return redirect("store:checkout")

class Order(View, CustomerMixin):
    def post(self, request):
        try:
            # Get Payment Method
            payment_selection = request.POST.get("selected_card")
            source_obj = Card.objects.get(pk=payment_selection)
            source = source_obj.stripe_id
            # Get Cart Total
        except:
            pass