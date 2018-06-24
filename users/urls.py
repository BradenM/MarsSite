from django.urls import path, include
from . import views

app_name = "users"
urlpatterns = [

    # Pages
    path('', views.AccountPage.as_view(), name="my_account"),
    path('settings/', views.SettingsPage.as_view(), name="my_settings"),
    path('invoices/', views.ListInvoices.as_view(), name="my_invoices"),
    path('orders/', views.ListOrders.as_view(), name="my_orders"),

    # Functions
    # Order Search
    path('orders/search/', views.SearchOrders.as_view(), name="search_orders"),
    # Change Phone
    path('change_phone/', views.ChangePhone.as_view(), name="change_phone"),
]
