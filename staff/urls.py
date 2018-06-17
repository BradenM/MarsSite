from django.contrib import admin
from django.conf import settings
from django.urls import path
from . import views

app_name = "staff"
urlpatterns = [

    # Control Panel
    path('', views.ControlPanel.as_view(), name="control-panel"),
    path('users/', views.ControlUsers.as_view(), name="control-users"),

    # Users
    path('users/<int:pk>', views.ViewUser.as_view(), name="view-user"),

    # Tracker
    path('users/tracker/<int:pk>', views.ViewTracker.as_view(), name="view-tracker"),
]
