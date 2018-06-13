from django.conf import settings
from django.urls import path
from allauth.account.decorators import verified_email_required
from . import views

app_name = "store"
urlpatterns = [

    # User Cart
    path('cart/', verified_email_required(views.CartView.as_view()), name="cart"),
    path('cart/add/<int:pk>', verified_email_required(views.add_to_cart), name="add_cart"),
    path('cart/remove/<int:pk>', verified_email_required(views.remove_from_cart), name="remove_cart"),
    path('cart/clear/', verified_email_required(views.clear_cart), name="clear_cart"),

    # User Checkout
    path('checkout/', verified_email_required(views.Checkout.as_view()), name="checkout"),

    # User Payments
    path('user/add-card/', verified_email_required(views.add_card), name="add-card"),
]
