from django.contrib import admin
from .models import Invoice, Order, UserPayment

admin.site.register(Invoice)
admin.site.register(Order)
admin.site.register(UserPayment)
