from . import views
from django.urls import path

app_name = "billing"
urlpatterns = [
    path('add-card', views.SaveCard.as_view(), name="add_card"),
    path('remove-card/<int:pk>', views.RemoveCard.as_view(), name="remove_card"),
]
