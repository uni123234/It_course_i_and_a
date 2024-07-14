from django.urls import path
from . import views

app_name = "help"

urlpatterns = [
    path("", views.request_help, name="request_help"),
]
