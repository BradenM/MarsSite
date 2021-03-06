from django.urls import path, include
from . import views

app_name = "users"
urlpatterns = [

    # Pages
    path('', views.AccountPage.as_view(), name="my_account"),
    path('settings/', views.SettingsPage.as_view(), name="my_settings"),
    path('payments/', views.PaymentsPage.as_view(), name="my_payments"),
    path('invoices/', views.ListInvoices.as_view(), name="my_invoices"),
    path('orders/', views.ListOrders.as_view(), name="my_orders"),

    # Order Search
    path('orders/search/', views.SearchOrders.as_view(), name="search_orders"),
    # Change Info
    path('change_phone/', views.ChangePhone.as_view(), name="change_phone"),
    path('change_email/', views.ChangeEmail.as_view(), name="change_email")
]
