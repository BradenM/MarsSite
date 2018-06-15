from . import views
from django.urls import path

app_name = "billing"
urlpatterns = [
    path('add-card', views.AddCard.as_view(), name="add_card"),
]
