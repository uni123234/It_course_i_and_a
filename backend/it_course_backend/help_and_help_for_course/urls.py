from django.urls import path
from . import views

app_name = "help"

urlpatterns = [
    path("request-help/", views.request_help, name="request_help"),
]
