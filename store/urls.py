from django.conf import settings
from django.urls import path
from allauth.account.decorators import verified_email_required
from . import views

app_name = "store"
urlpatterns = [

    # User Cart
    path('cart/', verified_email_required(views.CartView.as_view()), name="cart"),
    path('cart/add/<int:pk>',
         verified_email_required(views.AddCartEntry.as_view()), name="add_cart"),
    path('cart/remove/<int:pk>',
         verified_email_required(views.RemoveCartEntry.as_view()), name="remove_cart"),
    path('cart/clear/', verified_email_required(views.ClearCart.as_view()),
         name="clear_cart"),

    # Checkout
    path('checkout/', verified_email_required(views.Checkout.as_view()), name="checkout"),
    path('checkout/thanks/',
         verified_email_required(views.CheckoutComplete.as_view()), name="checkout_thanks")
]
