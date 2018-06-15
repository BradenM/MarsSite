from django.contrib import admin
from django.conf import settings
from django.urls import path
from . import views

app_name="staff"
urlpatterns = [
    path('', views.ControlPanel.as_view(), name="control-panel"),
]
