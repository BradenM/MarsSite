from django.conf import settings
from django.urls import path
from allauth.account.decorators import verified_email_required
from . import views

urlpatterns = [
    path('cart/', verified_email_required(views.CartView.as_view()), name="cart")
]
