from django.urls import path
from . import views

app_name = "repair"
urlpatterns = [

    # Index View
    path('', views.IndexView.as_view(), name="index"),

    # Device View
    path('select/', views.select_device, name="select_device"),
    path('<slug:slug>/repair<int:pk>/', views.DeviceView.as_view(), name="device_repair"),
    path('devices/<slug:slug>/', views.DeviceView.as_view(), name="device"),
]

