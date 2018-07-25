from django.urls import path
from . import views

app_name = "repair"
urlpatterns = [

    # Index View
    path('', views.IndexView.as_view(), name="index"),

    # Device Info
    path('select/', views.select_device, name="select_device"),
    path('devices/repair/<slug:slug>/',
         views.DeviceView.as_view(), name="device"),
    path('devices/get_repair/',
         views.GetRepair.as_view(), name="get_repair"),
    # View Devices
    path('view/',
         views.ViewDevices.as_view(), name="view_devices"),
    # Ajax / Info urls
    path('view/ajax/get_info/',
         views.GetDeviceInfo.as_view(), name="device_info"),
    path('view/ajax/search/',
         views.SearchDevices.as_view(), name="search_devices"),
]
