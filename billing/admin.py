from django.contrib import admin
from .models import Invoice, Order

admin.site.register(Invoice)
admin.site.register(Order)
