from django.urls import path, include
from . import views

app_name = "users"
urlpatterns = [
    path('', views.AccountPage.as_view(), name="my_account"),
    path('invoices/', views.ListInvoices.as_view(), name="my_invoices"),
    path('orders/', views.ListOrders.as_view(), name="my_orders"),
]
