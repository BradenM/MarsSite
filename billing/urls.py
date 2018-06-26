from . import views
from django.urls import path

app_name = "billing"
urlpatterns = [

    # Payment Methods
    path('add-card/', views.SaveCard.as_view(), name="add_card"),
    path('remove-card/<int:pk>/', views.RemoveCard.as_view(), name="remove_card"),
    path('set-card-default/<int:pk>/', views.SetDefaultCard.as_view(), name="set_default_card"),

    # Charge
    path('order/', views.ChargeCustomer.as_view(), name="complete_order"),
]
