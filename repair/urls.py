from django.urls import path
from . import views

app_name = "repair"
urlpatterns = [

    # Index View
    path('', views.IndexView.as_view(), name="index"),

    # Device View
    path('select/', views.select_device, name="select_device"),
    path('devices/<slug:slug>/', views.DeviceView.as_view(), name="device"),
    path('devices/<slug:slug>/repair/<int:pk>',
         views.get_repair, name="get_repair"),
    path('devices/view/<str:device_type>',
         views.ViewDevices.as_view(), name="view_devices"),
    # Ajax / Info urls
    path('devices/ajax/get_info/',
         views.GetDeviceInfo.as_view(), name="device_info"),
    path('devices/ajax/search_devices/',
         views.SearchDevices.as_view(), name="search_devices"),
]
