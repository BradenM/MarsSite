from django.conf import settings
from django.urls import path
from allauth.account.decorators import verified_email_required
from . import views

app_name = "store"
urlpatterns = [
    path('cart/', verified_email_required(views.CartView.as_view()), name="cart"),
    path('cart/add/<int:pk>', verified_email_required(views.add_to_cart), name="add_cart"),
    path('cart/remove/<int:pk>', verified_email_required(views.remove_from_cart), name="remove_cart")
]
