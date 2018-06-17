from django.urls import path
from . import views

app_name = "tracker"
urlpatterns = [
    path('<int:pk>', views.TrackerView.as_view(), name="tracker"),
]
