from django.urls import path
from . import views

app_name = "repair"
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('<slug:slug>/', views.DeviceView.as_view(), name="device")
]
